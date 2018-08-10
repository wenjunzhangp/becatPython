import requests
import re
import time
import random
import queue
from bs4 import BeautifulSoup
from grab import curd
from threading import Thread

# 获取html文档
def get_html(url):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4295.400'
    headers = {'User-Agent': user_agent}
    proxies = {
        "http": "http://username:passwd@101.101.101.101:9000",
        "http": "http://username:passwd@101.101.101.101:9000"
    }
    response = requests.get(url, headers=headers,timeout=5, proxies=proxies)
    response.encoding = 'utf-8'
    return response.text

# 获取标题、描述、正文
def get_news_title(html):
    soup = BeautifulSoup(html,'lxml')
    joke_content = soup.select('div.title-box h1.title')[0].get_text().strip()
    return joke_content

def get_news_remark(html):
    soup = BeautifulSoup(html,'lxml')
    joke_content = soup.select('p.description')[0].get_text().strip()
    return joke_content

def get_news_content(html):
    soup = BeautifulSoup(html,'lxml')
    joke_content = soup.select('div.info-box')[0].get_text().strip()
    return joke_content

def grabData(page):
    time.sleep(random.random())
    url_joke = "http://www.yc.cn/news/news-"+str(page)+".html"
    html = get_html(url_joke)
    print(html)
    news_title = get_news_title(html)
    print(news_title)
    news_content = get_news_content(html)
    print(news_content)
    print(str(page)+"页数据已经爬取完!!")
    curd.InsertDate(news_title,news_content)

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
    for i in range(2500,40925):
        my_queue.put_nowait(i)
    for a in range(0, 1):
        threadD = threadDownload(my_queue)
        threadD.start()
    while my_queue.empty():
        break