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
    response = requests.get(url)
    response.encoding = 'utf-8'
    return response.text

# 获取笑话
def get_certain_joke(html,count):
    soup = BeautifulSoup(html, 'lxml')
    joke_content = soup.select('div.content')[count].get_text().strip()
    return filter_emoji(joke_content)

# 糗事百科一页13条数据，判断是13的倍数就返回true page+1
def isPowerOfTwo(count):
    if count == 0:
        return False
    if int(count) % int(10) == 0:
        return True
    else :
        return False

# 过滤段子中特殊表情
def filter_emoji(restr):
    try:
        co = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return co.sub(u'', restr)

def grabData(page):
    count = 0
    time.sleep(random.random())
    while count<10:
        url_joke = "https://www.qiushibaike.com/textnew/page/"+ str(page) +"/"
        html = get_html(url_joke)
        joke_content = get_certain_joke(html,count)
        #print(joke_content)
        count = count + 1
        print("正在爬取"+str(page)+"页数据，第"+str(count)+"条数据!!")
        curd.InsertDate(joke_content,count)

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
    for i in range(1,35):
        my_queue.put_nowait(i)
    for a in range(0, 10):
        threadD = threadDownload(my_queue)
        threadD.start()
    while my_queue.empty():
        break