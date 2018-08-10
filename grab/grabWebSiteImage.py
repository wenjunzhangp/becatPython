from urllib import request
import re   #使用正则表达式

def getResponse(url):
    #url请求对象 Request是一个类
    url_request = request.Request(url)
    #print("Request对象的方法是：",url_request.get_method())

    #上下文使用的对象，包含一系列方法
    #url_response = request.urlopen(url) #打开一个url或者一个Request对象
    url_response = request.urlopen(url_request)
    '''
       geturl()：返回 full_url地址
         info(): 返回页面的元(Html的meta标签)信息
         <meta>：可提供有关页面的元信息（meta-information），比如针对搜索引擎和更新频度的描述和关键词。
      getcode(): 返回响应的HTTP状态代码 
      100-199 用于指定客户端应相应的某些动作。
      200-299 用于表示请求成功。      ------>  200
      300-399 用于已经移动的文件并且常被包含在定位头信息中指定新的地址信息。
      400-499 用于指出客户端的错误。  ------>  404
      500-599 用于支持服务器错误。 
         read(): 读取网页内容，注意解码方式(避免中文和utf-8之间转化出现乱码)
    '''

    return url_response   #返回这个对象

def getJpg(data):
    jpglist = re.findall(r'src="http.+?.jpg"',data)
    return  jpglist
def downLoad(jpgUrl,n):
    try:
        request.urlretrieve(jpgUrl,'%s.jpg'  %n)
    except Exception as e:
        print(e)
    finally:
        print('图片%s下载操作完成' % n)


http_response = getResponse("http://dzh.mop.com/") #拿到http请求后的上下文对象(HTTPResponse object)
data = http_response.read().decode('utf-8')
global n
n = 1
L = getJpg(data)
for jpginfo in L:
    print(jpginfo)
    s = re.findall(r'http.+?.jpg',jpginfo)
    downLoad(s[0],n)
    n= n +1

