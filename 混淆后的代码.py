from selenium import webdriver #line:1
from lxml import etree #line:2
from time import sleep #line:3
import os #line:4
import six #line:5
from six .moves .urllib .parse import urljoin #line:7
import pandas as pd #line:8
from hashlib import md5 #line:9
fingerprint =lambda O0OO0OOO000000000 :md5 (O0OO0OOO000000000 .encode ()).hexdigest ()#line:12
DIR =os .path .abspath (os .path .dirname (__file__ ))#line:14
SELENIUM_PATH =os .path .join (DIR ,"chromedriver.exe")#line:16
CLASS_URL_LIST =["https://www.icourse163.org/learn/ZJU-21002?tid=21007#/learn/announce","https://www.icourse163.org/learn/ZJU-21002?tid=249002#/learn/announce","https://www.icourse163.org/learn/ZJU-21002?tid=397002#/learn/announce","https://www.icourse163.org/learn/ZJU-21002?tid=1001599002#/learn/announce","https://www.icourse163.org/learn/ZJU-21002?tid=1001771009#/learn/announce","https://www.icourse163.org/learn/ZJU-21002?tid=1002009005#/learn/announce","https://www.icourse163.org/learn/ZJU-21002?tid=1002385004#/learn/announce","https://www.icourse163.org/learn/ZJU-21002?tid=1002783042#/learn/announce","https://www.icourse163.org/learn/ZJU-21002?tid=1002999001#/learn/announce","https://www.icourse163.org/learn/ZJU-21002?tid=1206099251#/learn/announce","https://www.icourse163.org/learn/ZJU-21002?tid=1206952286#/learn/announce",]#line:30
brower =webdriver .Chrome (executable_path =SELENIUM_PATH )#line:32
lxls_name =["主题名称","主题内容","主题回复"]#line:33
reviewData =[]#line:34
def get_forum_url (O0OO0OOOO00OOO0O0 ,O0000O0OOO0OOO000 ):#line:36
    ""#line:37
    O0OO0OOOO00OOO0O0 =etree .HTML (O0OO0OOOO00OOO0O0 )#line:38
    return [urljoin (O0000O0OOO0OOO000 ,O00OO000000O0OOOO )for O00OO000000O0OOOO in O0OO0OOOO00OOO0O0 .xpath ('//li[@class="u-greentab j-tabitem f-f0 last"]/a/@href')][-1 ]#line:39
def get_bar_url_list (O0OOOO0000O000OOO ,OO0OOO0OO00OOO00O ):#line:42
    ""#line:43
    O0OOOO0000O000OOO =etree .HTML (O0OOOO0000O000OOO )#line:44
    return [urljoin (OO0OOO0OO00OOO00O ,O00OO00O0O0O00OOO )for O00OO00O0O0O00OOO in O0OOOO0000O000OOO .xpath ('//div[@class="f-fl con"]/a/@href')]#line:45
def get_bar_all_url (OO0O0OO00000O00OO ,OOO00O0O0000OO0O0 ):#line:48
    ""#line:49
    OO0O0OO00000O00OO =etree .HTML (OO0O0OO00000O00OO )#line:50
    O00000000O0000000 =OO0O0OO00000O00OO .xpath ('//a[@class="zbtn znxt"]/..//text()')#line:51
    O00000000O0000000 =O00000000O0000000 [-2 ]if O00000000O0000000 else 1 #line:52
    O00OOO00O0O00O0O0 =[OOO00O0O0000OO0O0 +f"&t=0&p={OO0O00OO0OOOO0000}"for OO0O00OO0OOOO0000 in range (1 ,int (O00000000O0000000 )+1 )]#line:53
    return O00OOO00O0O00O0O0 #line:54
def get_all_theme (OOO00OO00O0000O00 ,O0O00OO000OOOO00O ):#line:57
    ""#line:58
    OOO00OO00O0000O00 =etree .HTML (OOO00OO00O0000O00 )#line:59
    O0OOOOOO000OOOO0O =OOO00OO00O0000O00 .xpath ('//li[@class="u-forumli"]/div//a/@href')#line:60
    if not O0OOOOOO000OOOO0O :#line:61
        return None #line:62
    O0OOOOOO000OOOO0O =[urljoin (O0O00OO000OOOO00O ,OO000O00OOOO0OO00 )for OO000O00OOOO0OO00 in O0OOOOOO000OOOO0O ]#line:63
    return O0OOOOOO000OOOO0O #line:64
def clean_data (OOO000OOOOO0O0O0O ):#line:66
    ""#line:67
    OOO000OOOOO0O0O0O =etree .HTML (OOO000OOOOO0O0O0O )#line:68
    OO0O0000000OO0000 =OOO000OOOOO0O0O0O .xpath ('//div[@class="f-cb"]/h3/text()')[0 ]#line:69
    O0OOO0OO000O0OOO0 ='\n'.join (OOO000OOOOO0O0O0O .xpath ('//div[@class="f-cb"]/..//div[2]//text()')).split ("赞同",1 )[1 ].rsplit ("来自课件““",1 )[0 ].rsplit ("\n2",1 )[0 ]#line:70
    OO00OO000000OOOOO =OOO000OOOOO0O0O0O .xpath ('//div[@class="j-list"]//div[@class="bar f-cb"]/..//div[2]//text()')#line:71
    OO0O000OO0OO0O0O0 ="\n".join (OO00OO000000OOOOO ).split ("赞同")#line:72
    OO0O000OO0OO0O0O0 =[OOOOO0000O000OOO0 .rsplit ("\n2",1 )[0 ]for OOOOO0000O000OOO0 in OO0O000OO0OO0O0O0 ]#line:73
    if OO0O000OO0OO0O0O0 :#line:74
        for O000000OOOO0OO000 in OO0O000OO0OO0O0O0 :#line:76
            reviewData .append ([OO0O0000000OO0000 ,O0OOO0OO000O0OOO0 ,O000000OOOO0OO000 ])#line:77
    else :#line:78
        reviewData .append ([OO0O0000000OO0000 ,O0OOO0OO000O0OOO0 ,"无主题回复数据"])#line:79
def main (O0OO00O00O00OOO0O ,OOOOO00O0O00000O0 ):#line:82
    ""#line:87
    O0OO00O00O00OOO0O =O0OO00O00O00OOO0O -1 if O0OO00O00O00OOO0O >1 else 0 #line:88
    for O000O0O0OOO0000O0 in CLASS_URL_LIST [O0OO00O00O00OOO0O :OOOOO00O0O00000O0 ]:#line:90
        brower .get (O000O0O0OOO0000O0 )#line:92
        sleep (1 )#line:93
        OOO0OOO0OO00000O0 =brower .page_source #line:95
        OO0OO00OO0000O00O =get_forum_url (OOO0OOO0OO00000O0 ,O000O0O0OOO0000O0 )#line:96
        brower .get (OO0OO00OO0000O00O )#line:97
        sleep (1 )#line:98
        OO00O0OOOOO0000O0 =brower .page_source #line:99
        sleep (1 )#line:101
        OO00OOOOOOO000O00 =get_bar_url_list (OO00O0OOOOO0000O0 ,O000O0O0OOO0000O0 )#line:102
        for O00OO00OO0O0O0O00 in OO00OOOOOOO000O00 :#line:103
            brower .get (O00OO00OO0O0O0O00 )#line:104
            sleep (1 )#line:105
            OO00O0OOOOO0000O0 =brower .page_source #line:106
            OO0O000O000O0O0O0 =get_bar_all_url (OO00O0OOOOO0000O0 ,O00OO00OO0O0O0O00 )#line:107
            for O000O00OOOO0OOOOO in OO0O000O000O0O0O0 :#line:109
                brower .get (O000O00OOOO0OOOOO )#line:110
                sleep (1 )#line:111
                OO00O0OOOOO0000O0 =brower .page_source #line:112
                O000O0000OOOOO000 =get_all_theme (OO00O0OOOOO0000O0 ,O000O00OOOO0OOOOO )#line:113
                if not O000O0000OOOOO000 :#line:115
                    break #line:116
                for O0OO0OO000OO0O00O in O000O0000OOOOO000 :#line:118
                    brower .get (O0OO0OO000OO0O00O )#line:119
                    sleep (1 )#line:120
                    try :#line:121
                        while True :#line:123
                            O0O00O00OO00OO00O =brower .page_source #line:124
                            sleep (1 )#line:125
                            clean_data (O0O00O00OO00OO00O )#line:126
                            O00O0OO00OO0O000O =etree .HTML (O0O00O00OO00OO00O ).xpath ('//a[@class="zbtn znxt"]')#line:127
                            OOOOO0O00OO0OO0O0 =brower .find_element_by_xpath ('//a[@class="zbtn znxt"]')#line:128
                            OOOOO0O00OO0OO0O0 .click ()#line:129
                    except :#line:130
                        continue #line:131
if __name__ =="__main__":#line:135
    main (1 ,11 )#line:137
    pd_data =pd .DataFrame (columns =lxls_name ,data =reviewData )#line:138
    pd_data .to_excel (os .path .join (DIR ,"课时数据.xlsx"),index =False ,header =True )#line:139
