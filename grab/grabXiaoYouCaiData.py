import requests
import time
import random
import queue
from lxml import etree
from threading import Thread

# 获取html文档
def get_html(url):
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
    headers = {'User-Agent': user_agent}
    proxies = {
        "http": "219.141.153.41:80"
    }
    response = requests.get(url, headers=headers,timeout=10)
    response.encoding = 'utf-8'
    return response.text

def grabData(start):
    time.sleep(random.random())
    url_douban_movie = "http://www.xycjinfu.com/loan/list_4_"+str(start)+".html"
    html = get_html(url_douban_movie)
    html = etree.HTML(html)
    # 标的名称
    loan_title = html.xpath('//*[@id="transDiv"]/div/div/div[1]/a/text()')
    print(loan_title)
    # 标的利率
    loan_rate_q = html.xpath('//*[@id="transDiv"]/div/div/div[2]/h3/strong/text()')
    loan_rate_h = html.xpath('//*[@id="transDiv"]/div/div/div[2]/h3/text()')
    loan_rate = []
    for a in range(0, 10):
        loan_rate.append(loan_rate_q[a]+loan_rate_h[a])
    print(loan_rate)
    # 标的天数
    loan_day = html.xpath('//*[@id="transDiv"]/div/div/div[3]/h3/strong/text()')
    print(loan_day)
    # 可投金额
    loan_money = html.xpath('//*[@id="transDiv"]/div/div/div[4]/h3/strong/text()')
    print(loan_money)
    with open("xiaoyoucai.txt",'a',encoding='utf-8') as f:
        for j in range(0, 10):
            f.write("标的名称\t"+loan_title[j].strip()+"\n")
            f.write("标的利率\t"+loan_rate[j]+"\n")
            f.write("标的天数\t"+loan_day[j]+"\n")
            f.write("剩余可投金额\t"+loan_money[j]+"\n")
            f.write('*' * 50 + '\n')
    f.close()
    print("正在爬取【"+str(start)+"】数据!!")

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
    for i in range(1,1871):#1871
        my_queue.put_nowait(i)
    for a in range(0, 10):
        threadD = threadDownload(my_queue)
        threadD.start()
    while my_queue.empty():
        break