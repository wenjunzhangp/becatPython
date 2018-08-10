import  requests
from bs4 import BeautifulSoup
import re

class Tools:
    removeImg = re.compile('<img.*?>')
    removBr = re.compile('<br>')
    removeHef = re.compile('<a href.*?>')
    removeA = re.compile('</a>')
    removeClass = re.compile('<a class.*?>|<aclass.*?>')
    removeNull = re.compile(' ')

    def remove(self,te):
        te = re.sub(self.removeImg,'',te)
        te = re. sub(self.removBr,'\n',te)
        te = re.sub(self.removeHef,'',te)
        te = re.sub(self.removeA,'',te)
        te = re.sub(self.removeClass,'',te)
        te = re.sub(self.removeNull, '', te)
        return  te

textTools = Tools()

def getHTMLText(url):
    try:
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = {'User-Agent': user_agent}
        r = requests.get(url,headers = headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

def printTitle(html):
    try:
        soup = BeautifulSoup(html, "html.parser")
        titleTag = soup.find_all('title')
        patten = re.compile(r'<title>(.*?)</title>', re.S)
        title = re.findall(patten, str(titleTag))
        return title
    except:
        return ""

def fillUnivlist(lis,li,html):
    try:
        patten = re.compile(r'<div id="post_content_\d*" class="d_post_content j_d_post_content ">(.*?)</div>', re.S)
        nbaInfo = re.findall(patten, str(html))
        pattenFloor = re.compile(r'<span class="tail-info">(\d*楼)</span><span class="tail-info">', re.S)
        floorText = re.findall(pattenFloor, str(html))
        number = len(nbaInfo)
        for i in range(number):
            Info = textTools.remove(nbaInfo[i])
            Info1 = textTools.remove(floorText[i])
            lis.append(Info1)
            li.append(Info)
    except:
        return ""

def writeText(titleText,fpath):
    try:
        with open(fpath, 'a', encoding='utf-8') as f:
            f.write(str(titleText) + '\n')
            f.write('\n')
            f.close()
    except:
        return ""

def writeUnivlist(lis,li,fpath,num):
    with open(fpath, 'a', encoding='utf-8') as f:
        for i in range(num):
            f.write(str(lis[i])+'\n')
            f.write('*'*50 + '\n')
            f.write(str(li[i]) + '\n')
            f.write('*' * 50 + '\n')
        f.close()

def main():
    count = 0
    url = 'https://tieba.baidu.com/p/3138733512?see_lz=1&pn=1'
    output_file = 'info.txt'
    html = getHTMLText(url)
    titleText = printTitle(html)
    writeText(titleText, output_file)
    for i in range(5):
        i = i + 1
        lis = []
        li = []
        url = 'https://tieba.baidu.com/p/3138733512?see_lz=1&pn=' + str(i)
        html = getHTMLText(url)
        fillUnivlist(lis, li, html)
        writeUnivlist(lis, li, output_file, len(lis))
        count = count + 1
        print("\r当前进度: {:.2f}%".format(count * 100 / 5), end="")

main()