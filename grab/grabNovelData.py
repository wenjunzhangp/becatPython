import requests
import re
import time
import random
import queue
from lxml import etree
from threading import Thread

# 获取html文档
def get_html(url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
    proxies = {
        "http": "219.141.153.41:80"
    }
    response = requests.get(url, headers=headers,timeout=10,proxies = proxies)
    response.encoding = 'gbk'
    return response.text

def grabData(start):
    time.sleep(random.random())
    page = start - 336143

    url_book_title = "http://www.quanshuwang.com/book/1/1018"
    html_title = get_html(url_book_title)
    html_title = etree.HTML(html_title)
    # 小说章节名称
    novel_title = html_title.xpath('//*[@id="chapter"]/div[3]/div[3]/ul/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/li/a/@title')

    url_book_content = "http://www.quanshuwang.com/book/1/1018/"+str(start)+".html"
    html_content = get_html(url_book_content)
    html_content = etree.HTML(html_content)
    # 小说内容
    novel_content = html_content.xpath('//*[@id="content"]/text()')

    with open("D:\\novel\\异世邪君\\第六卷"+novel_title[page]+".txt",'w',encoding='utf-8') as f:
        for index, item in enumerate(novel_content):
            f.write(re.sub( '\s+', '\r\n\t', item))
    f.close()
    print("章节"+novel_title[page]+"下载完成!!!")

class threadDownload(Thread):
    def __init__(self, que):
        Thread.__init__(self)
        self.que = que
    def run(self):
        while True:
            if not self.que.empty():
                grabData(self.que.get())
            else:
                break

if __name__ == '__main__':
    my_queue = queue.Queue()
    for i in range(336143,3394452):
        my_queue.put_nowait(i)
    for a in range(0, 10):
        threadD = threadDownload(my_queue)
        threadD.start()
    while my_queue.empty():
        break