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
    time.sleep(3+random.random())
    url_douban_movie = "http://www.hlxns.com/index.php?r=l&u=427272&page="+str(start)
    html = get_html(url_douban_movie)
    html = etree.HTML(html)
    # 获取优惠券商品信息
    goods = html.xpath('//*[@id="dtk_mian"]/div[4]/ul/li/a/@href')
    for info in range(0, 101):
        try :
            time.sleep(3+random.random())
            url_douban_movie = "http://www.hlxns.com"+goods[info]
            #print(url_douban_movie)
            html = get_html(url_douban_movie)
            html = etree.HTML(html)
            # 商品名称
            goodsname = html.xpath('//*[@id="dtk_mian"]/div[2]/div[2]/div[1]/a[1]/span/text()')
            #print(goodsname[0])
            # 商品卖点
            goodsremark = html.xpath('//*[@id="dtk_mian"]/div[2]/div[2]/div[1]/div/span/text()')
            #print(goodsremark[0])
            # 在售价格
            onlineprice = html.xpath('//*[@id="dtk_mian"]/div[2]/div[2]/div[1]/div[2]/span[2]/i/text()')
            #print(onlineprice[0])
            # 卷后价格
            couponprice = html.xpath('//*[@id="dtk_mian"]/div[2]/div[2]/div[1]/div[2]/span[1]/b/i/text()')
            #print(couponprice[0])
            # 优惠券数量
            #totalcount = html.xpath('//*[@id="dtk_mian"]/div[2]/div[2]/div[1]/div[3]/span[1]/i/text()')
            #print(totalcount[0])
            # 购买人数
            buynum = html.xpath('//*[@id="dtk_mian"]/div[2]/div[2]/div[1]/div[3]/span[2]/i/text()')
            #print(buynum[0])
            # 获取优惠券地址
            url = html.xpath('//*[@id="dtk_mian"]/div[2]/div[2]/div[1]/div/a/@href')
            #print(goodsname[0],url[0])
            goodsinfo = {
                'goodsname' : goodsname[0],
                'goodsremark' : goodsremark[0],
                'onlineprice' : onlineprice[0],
                'couponprice': couponprice[0],
                'totalcount' : 1000000,
                'buynum' : buynum[0],
                'url' : url[0]
            }
            curd.InsertDate(goodsinfo);
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
    for i in range(14,641):
        my_queue.put_nowait(i)
    for a in range(0, 5):
        threadD = threadDownload(my_queue)
        threadD.start()
    while my_queue.empty():
        break