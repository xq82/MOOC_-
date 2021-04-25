from selenium import webdriver
from lxml import etree
from  time import sleep
import os
import six
#url拼接函数
from six.moves.urllib.parse import urljoin
import pandas as pd


#当前文件夹路径
DIR = os.path.abspath(os.path.dirname(__file__))
#selenium路径  当前文件夹下
# SELENIUM_PATH = os.path.join(DIR, "chromedriver.exe")
SELENIUM_PATH = 'D:\Google_selenium\chromedriver.exe'
#课时讨论区列表  由于需要登陆  所以我登陆后直接写死   如果要抓底12课时 ,直接将第12课时的链接放入即可
CLASS_URL_LIST = [
    "https://www.icourse163.org/learn/ZJU-21002?tid=21007#/learn/announce",
    "https://www.icourse163.org/learn/ZJU-21002?tid=249002#/learn/announce",
    "https://www.icourse163.org/learn/ZJU-21002?tid=397002#/learn/announce",
    "https://www.icourse163.org/learn/ZJU-21002?tid=1001599002#/learn/announce",
    "https://www.icourse163.org/learn/ZJU-21002?tid=1001771009#/learn/announce",
    "https://www.icourse163.org/learn/ZJU-21002?tid=1002009005#/learn/announce",
    "https://www.icourse163.org/learn/ZJU-21002?tid=1002385004#/learn/announce",
    "https://www.icourse163.org/learn/ZJU-21002?tid=1002783042#/learn/announce",
    "https://www.icourse163.org/learn/ZJU-21002?tid=1002999001#/learn/announce",
    "https://www.icourse163.org/learn/ZJU-21002?tid=1206099251#/learn/announce",
    "https://www.icourse163.org/learn/ZJU-21002?tid=1206952286#/learn/announce",
]
#selenium对象
brower = webdriver.Chrome(executable_path=SELENIUM_PATH)
lxls_name = ["主题名称", "主题内容", "主题回复"]
reviewData = []


def get_forum_url(html, url):
    """提取讨论区主url"""
    html = etree.HTML(html)
    return [urljoin(url, i) for i in html.xpath('//li[@class="u-greentab j-tabitem f-f0 last"]/a/@href')][-1]


def get_bar_url_list(html, url):
    """获取三个板块url"""
    html = etree.HTML(html)
    return [urljoin(url, i)  for i in html.xpath('//div[@class="f-fl con"]/a/@href')]


def get_bar_all_url(html, url):
    """获取每个板块所有页码url """
    html = etree.HTML(html)
    page_num = html.xpath('//a[@class="zbtn znxt"]/..//text()')
    page_num = page_num[-2] if page_num else 1
    get_bar_all_url_list = [url + f"&t=0&p={i}" for i in range(1, int(page_num) + 1)]
    return get_bar_all_url_list


def get_all_theme(html, url):
    "获取所有主题url"
    html = etree.HTML(html)
    all_theme_list = html.xpath('//li[@class="u-forumli"]/div//a/@href')
    if not all_theme_list:
        return None
    all_theme_list =[urljoin(url, i)  for i in all_theme_list]
    return all_theme_list


def clean_data(html):
    """处理评论数据"""
    html = etree.HTML(html)
    theme_title = html.xpath('//div[@class="f-cb"]/h3/text()')[0]
    theme_content = '\n'.join(html.xpath('//div[@class="f-cb"]/..//div[2]//text()')).split("赞同", 1)[1].rsplit("来自课件““", 1)[0].rsplit("\n2", 1)[0]
    reply = html.xpath('//div[@class="j-list"]//div[@class="bar f-cb"]/..//div[2]//text()')
    reply_data = "\n".join(reply).split("赞同")
    reply_data = [reply.rsplit("\n2", 1)[0] for reply in reply_data]
    if reply_data:
        #将评论数据加入reviewData列表中
        for i in  reply_data:
            reviewData.append([theme_title, theme_content, i])
    else:
        reviewData.append([theme_title, theme_content, "无主题回复数据"])


def main(start, end):
    """
    start: 开始课时  
    end: 结束课时
    防止程序中断以后没有记录
    """
    start = start-1 if start>1 else 0
    #循环访问每一个课时   由于页面要刷新,所以需要暂停
    for classUrl in CLASS_URL_LIST[start: end]:
        #用于存放抓取数据的列表
        brower.get(classUrl)
        sleep(1)
        #获得讨论区url并访问
        forum_html = brower.page_source                                                         #获取源码
        forum_url = get_forum_url(forum_html, classUrl)                                         #进入讨论区的url
        brower.get(forum_url)                                                                   #进入讨论区
        sleep(1)            
        bar_html = brower.page_source                                                           #获取讨论区源码
        #获取子版块url
        sleep(1)
        bar_url_type_list = get_bar_url_list(bar_html, classUrl)                                #获取所有板块类别url  老师答疑区   课堂交流区  综合讨论区  第一次循环...
        for bar_type_url in bar_url_type_list:
            brower.get(bar_type_url)                                                            #进入各个板块 挨个遍历
            sleep(1)
            bar_html = brower.page_source                                                       #获取各个板块源码  用以获取最大页码数量
            bar_all_url = get_bar_all_url(bar_html, bar_type_url)                               #获取所有该板块下所有列表页

            for bar_url in bar_all_url:
                brower.get(bar_url)                                                             #访问每一个主题列表页面
                sleep(1)
                bar_html = brower.page_source                                                   #获取源码
                theme_url_list = get_all_theme(bar_html, bar_url)                               #获取详情页url

                if not theme_url_list:                                                          #如果没有主题数据  跳出这个板块
                    break
                #访问每个主题数据  判断有无翻页  如果有 则翻页 没有 则下一个主题
                for theme_url in theme_url_list:
                    brower.get(theme_url)
                    sleep(1)
                    try:
                        #检测主题 下一页按钮  并根据页面的数据进行MD5  放入文章列表中 如果文章md5存在  如果报错了,则是最后一页
                        while True:
                            theme_html = brower.page_source   
                            sleep(1)
                            clean_data(theme_html)
                            zbtn_znxt = etree.HTML(theme_html).xpath('//a[@class="zbtn znxt"]')
                            theme_next_page = brower.find_element_by_xpath('//a[@class="zbtn znxt"]')
                            theme_next_page.click()
                    except:
                        continue
        

if __name__ == "__main__":
    #从第一课时到第二课时
    main(1, 2)
    #保存数据
    pd_data = pd.DataFrame(columns=lxls_name, data=reviewData)    
    pd_data.to_excel(os.path.join(DIR, "课时数据.xlsx"), index=False, header=True)

