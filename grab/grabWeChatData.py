import requests
import time
import random
import queue
from lxml import etree
from threading import Thread
from grab import curd

# 获取html文档
def get_html(url):
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5383.400 QQBrowser/10.0.1313.400'}
    # proxies = {
    #     "http": "218.95.82.27:9000"
    # }
    response = requests.get(url, headers=headers,timeout=60)
    response.encoding = 'utf-8'
    return response.text

def grabData(start):
    time.sleep(2+random.random())
    url_douban_movie = "http://ktccy.gamedog.cn/gonglue/list_42219_"+str(start)+".html"
    html = get_html(url_douban_movie)
    html = etree.HTML(html)
    # 获取优惠券商品信息
    goods = html.xpath('//*[@id="daquan_list"]/li/a/@href')
    for info in range(0, 18):
        try :
            time.sleep(2+random.random())
            url_douban_movie = goods[info]
            html = get_html(url_douban_movie)
            html = etree.HTML(html)
            # 成语图片
            imageurl = html.xpath('//*[@class="news_neirong"]/p[2]/img/@src')
            print(imageurl[0])
            # 成语答案
            answer = html.xpath('//*[@class="news_neirong"]/p[3]/text()')
            print(answer[0])
            # 解析释义
            content = html.xpath('//*[@class="news_neirong"]/p[last()]/text()')
            print(content[0])
            data = {
                'imageurl' : imageurl[0],
                'answer' : answer[0],
                'content' : content[0]
            }
            curd.InsertDate(data);
            print("正在爬取【"+str(start)+"】页【"+str(info)+"】条数据!!!")
        except Exception as e:
            continue


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
    for i in range(1,396):
        my_queue.put_nowait(i)
    for a in range(0, 1):
        threadD = threadDownload(my_queue)
        threadD.start()
    while my_queue.empty():
        break