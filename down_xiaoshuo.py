import requests
from lxml.etree import HTML
import os
from threading import Thread
from queue import Queue
from six.moves.urllib.parse import urljoin
import tkinter
import time


ABS_DIR = os.path.abspath(__file__ + "\..")

def handling_garbled(response):
    """处理response乱码"""
    if response.encoding == 'ISO-8859-1':
        encodings = requests.utils.get_encodings_from_content(response.text)
        if encodings:
            encoding = encodings[0]
        else:
            encoding = response.apparent_encoding
    else:
        encoding = response.encoding
    response.encoding = encoding
    return response


class Biquwx_Spider:
    def __init__(self, list_url) -> None:
        self.q = Queue()
        self.list_url = list_url
        self.data = {}
        self.file_path = None
        self.step = 1
        self.title = None
    
    def request_list(self, list_url):
        title = "欢迎来到实力至上主义的教室"#html.xpath("//title/text()")[0].split('最新章节列表', 1)[0]
        self.title = title
        self.file_path = os.path.join(ABS_DIR, title + ".txt")
        for i in range(1, 16):
            list_url = f"http://www.tstdoors.com/ldks/39021/index_{i}.html"
            response = handling_garbled(requests.get(list_url))
            html = HTML(response.text)
            list_urls = html.xpath('//ul[@class="section-list fix"]')[1].xpath('.//a/@href')
            print(list_urls)
            list_urls = [urljoin(list_url, i) for i in list_urls]
            l = len(list_urls)
            self.step += l
            for i in range(l):
                self.q.put((i, list_urls[i]))
    
    def parse_detail(self, detail_url, number):
        response = handling_garbled(requests.get(detail_url))
        html = response.text
        title = HTML(html).xpath('//h1[@class="title"]//text()')[0]
        context = '\n'.join(HTML(html).xpath('//div[@id="content"]//text()'))
        while True:
            next_url = HTML(html).xpath('//div[@class="section-opt m-bottom-opt"]//a[3]//text()')[0]
            print(next_url)
            if next_url == "下一章":
                break
            detail_url = urljoin(detail_url, HTML(html).xpath('//div[@class="section-opt m-bottom-opt"]//a[3]//@href')[0])
            response = handling_garbled(requests.get(detail_url))
            html = response.text
            context = context + '\n'.join(HTML(html).xpath('//div[@id="content"]//text()'))
        
        self.data[number] = {
            "title":title,
            "content": context
        }
        print("内容页: ", detail_url + "    下载完成", "  编号", number, " 标题：" + title )

    def run(self):
        t1 = time.time()
        self.request_list(self.list_url)
        while not self.q.empty():
            ts = []
            for i in range(5):
                if not self.q.empty():
                    d = self.q.get()
                    ts.append(Thread(target=self.parse_detail, args=(d[1], d[0])))
            [t.start() for t in ts]
            [t.join() for t in ts]
        ss = []
        s = len(self.data)
        for i in range(s):
            ss.append(self.data[i]["title"])
            ss.append(self.data[i]["content"])
        ss = "\n".join(ss)
        with open(self.file_path, 'w', encoding="utf-8") as f:
            f.write(ss)
        print(self.title, "   下载完毕, 共计"+ str(self.step)+ "个页面  " + "耗时:", str(time.time()-t1) + 's')

def start_down():
    url = url_entry.get()
    Biquwx_Spider(url).run()
    url_entry.delete(0, 'end')

if __name__ == "__main__":
    window = tkinter.Tk()
    window.title("笔趣阁xiaoshuo下载器")
    window.geometry("300x150+1200+100")

    url_label = tkinter.Label(window, text="小说列表页网址", fg="#d2961e", bg="Bisque")
    url_label.pack()
    url_entry = tkinter.Entry(window)
    url_entry.pack()

    button = tkinter.Button(window, text="点击下载", command=start_down, bg="OldLace", fg="Tan", bd="6", font="黑体")
    button.pack()
    window.mainloop()
