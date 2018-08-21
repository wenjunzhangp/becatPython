import requests
from bs4 import BeautifulSoup
from grab import grabDouBanCommentData

def _get_captcha(content):
    """
    验证码获取函数，返回两个参数
    :param content: 登录页面的html代码
    :return: 验证码id, 验证码图片的url
    """
    soup = BeautifulSoup(content)
    captcha_id_tag = soup.find('input', attrs={'type':'hidden', 'name': 'captcha-id'})
    captcha_image_tag = soup.find('img', attrs={'id': 'captcha_image', 'alt': 'captcha', 'class': 'captcha_image'})
    return captcha_id_tag['value'], captcha_image_tag['src']

class DoubanClient(object):
    def __init__(self):
        object.__init__(self)
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
            'origin': 'https://accounts.douban.com'
        }
        # create requests session
        self.session = requests.Session()
        self.session.headers.update(headers)

    def login(self, username, password,
              source='index_nav',
              redir='https://movie.douban.com',
              remember='on',
              login='登录'):

        """
        :param username: 用户名
        :param password: 密码
        :param source: 以下参数都是定死的字符串，抓包的时候查看
        :param redir:
        :param remember:
        :param login:
        """
        url = 'https://www.douban.com/accounts/login'
        # 获取登录页面的内容，解析出验证码
        r = requests.get(url)
        (captcha_id, captha_url) = _get_captcha(r.content)
        # 如果验证码解析正确，手动输入验证码
        if captcha_id:
            captcha_solution = input('please input the captcha for [%s]: ' % captha_url)
        # 模拟data
        data = {
            'form_email': username,
            'form_password': password,
            'source': source,
            'redir': redir,
            'remember': remember,
            'login': login
        }
        if captcha_id:
            data['captcha-id'] = captcha_id
            data['captcha-solution'] = captcha_solution
        # 模拟headers
        headers = {
            'referer': 'https://accounts.douban.com/login?uid=&alias=&redir=https%3A%2F%2Fwww.douban.com%2F&source=index_nav&error=1001',
            'host': 'accounts.douban.com'
        }
        proxies = {
            "http": "60.2.148.253:80"
        }
        # 向豆瓣服务器post，模拟豆瓣登录
        r = self.session.post(url, data=data, headers=headers, proxies=proxies)
        print(r)
        print(self.session.cookies.items())

    def edit_signature(self, username, signature):
        pass

if __name__ == '__main__':
    c = DoubanClient()
    c.login('zhangwenjunp@126.com', 'z971886506')
    grabDouBanCommentData.begin()