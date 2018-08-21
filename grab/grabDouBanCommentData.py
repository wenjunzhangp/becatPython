import requests
import time
import random
import queue
from lxml import etree
from threading import Thread

#当前登录的cookies
cookies_str = ''

# 获取html文档
def get_html(url):
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
    headers = {
        'User-Agent': user_agent,
        'Connection': 'keep-alive',
        'host': 'movie.douban.com',
        'Cookie': cookies_str
    }
    proxies = {
        "http": "60.2.148.253:80"
    }
    response = requests.get(url, headers=headers,timeout=5, proxies=proxies)
    response.encoding = 'utf-8'
    return response.text

def grabData(start):
    time.sleep(random.random())
    url_douban_movie = "https://movie.douban.com/subject/26752088/comments?start="+str(start)+"&limit=20&sort=new_score&status=P"
    html = get_html(url_douban_movie)
    html = etree.HTML(html)
    # 获取评论昵称
    nickname = html.xpath('//div[@class="avatar"]/a/@title')
    #print(nickname)
    # 获取看客的评分
    satisfaction = html.xpath('//*[@id="comments"]/div/div/h3/span/span[2]/@title')
    #print(satisfaction)
    # 获取评论时间
    looktime = html.xpath('//*[@id="comments"]/div/div/h3/span/span[last()]/@title')
    #print(looktime)
    # 获取评论内容
    content = html.xpath('//*[@id="comments"]/div/div/p/span/text()')
    #print(content)
    with open("douban.txt",'a',encoding='utf-8') as f:
        for j in range(0, 20):
            f.write("昵称\t"+nickname[j]+"\n")
            f.write("评分\t"+satisfaction[j]+"\n")
            f.write("评论时间\t"+looktime[j]+"\n")
            f.write("内容\t"+content[j].strip()+"\n")
            f.write('*' * 50 + '\n')
    f.close()
    print("正在爬取【"+str(start)+"】数据!!")

def begin(cookies):
    global cookies_str
    cookies_str = cookies
    print("当前登录的cookies---------------->>>>>>>>>"+cookies_str)
    my_queue = queue.Queue()
    page = 0
    for i in range(0,26):
        my_queue.put_nowait(page)
        page = page + 20
    for a in range(0, 1):
        threadD = threadDownload(my_queue)
        threadD.start()
    while my_queue.empty():
        break

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
    page = 0
    for i in range(0,27):
        my_queue.put_nowait(page)
        page = page + 20
    for a in range(0, 1):
        threadD = threadDownload(my_queue)
        threadD.start()
    while my_queue.empty():
        break