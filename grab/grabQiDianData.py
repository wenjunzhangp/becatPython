import requests,os
import re
from lxml import etree
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5383.400 QQBrowser/10.0.1313.400'}

def getbookname(url):
    html=requests.get(url,headers=headers)
    objects=etree.HTML(html.text)
    objs=objects.xpath("//ul[@class='all-img-list cf']/li")
    urlbox=[]
    for obj in objs:
        title=obj.xpath('div[2]/h4/a/text()')[0]
        bigurls=obj.xpath('div[2]/h4/a/@href')[0]
        bigurl='https:'+bigurls+'#Catalog'
        #指定大类目录和目录名字
        parentfilename='D:/起点爬虫/'+title
        info = {
            'title': title,
            'parentfilename':parentfilename,
            'bigurl': bigurl
        }
        urlbox.append(info)
        #如果目录不存在就创建
        if not os.path.exists(parentfilename):
            os.makedirs(parentfilename)
    # print(urlbox)
    return urlbox

def getbookurls(url):
    charpters = requests.get(url, headers=headers)
    objects = etree.HTML(charpters.text)
    objs=objects.xpath("//ul[@class='cf']/li")
    tinybox=[]
    for obj in objs:
        try:
            charpnames=obj.xpath('a/text()')[0]
            charpurls=obj.xpath('a/@href')[0]
            info={
                'charpnames':charpnames,
                'charpurls':'https:'+charpurls
            }
            tinybox.append(info)
            # print(charpnames,charpurls)
        except:
            pass
    return tinybox

def getcontent(url):
    content = requests.get(url, headers=headers)
    objects = etree.HTML(content.text)
    objs=objects.xpath("//div[@class='read-content j_readContent']/p/text()")
    neirong=[]
    for obj in objs:
        #obj=obj.replace('\u3000\u3000','')
        obj = re.sub( '\s+', '\r\n\t', obj)
        #print(obj,end='')
        neirong.append(obj)
    return neirong


def main(url):
    bookurls=getbookname(url)
    for bookurl in bookurls:
        #print(bookurl)
        subfilename=bookurl['parentfilename']
        #print(subfilename)
        get=getbookurls(bookurl['bigurl'])
        #print(get)
        #如果目录不存在就创建
        for g in get:
            charptername=subfilename+'/'+g['charpnames']
            if not os.path.exists(charptername):
                os.makedirs(charptername)
            bs=getcontent(g['charpurls'])
            with open('%s/%s.txt' % (charptername, g['charpnames']), 'a',encoding='utf-8') as f:
                for b in bs:
                    f.write(b)
    print("下载完成!!!")

if __name__ == '__main__':
    url = 'https://www.qidian.com/free/all'
    main(url)
