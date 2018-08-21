import urllib.request
from selenium import webdriver
from PIL import Image
import time
from grab import grabDouBanCommentData

url = 'http://accounts.douban.com/login'
# email = input('E-mail:')
# password = input('Password:')
email = 'zhangwenjunp@126.com'
password = 'z971886506'

browser = webdriver.PhantomJS(executable_path=r'D:\codetools\phantomjs-2.1.1-windows\bin\phantomjs.exe')
browser.get(url)

#send account key
print('writing username and password...')
browser.find_element_by_name('form_email').send_keys(email)
browser.find_element_by_name('form_password').send_keys(password)

#get captcha link and save to local
print('saving captcha image...')
captcha_link = browser.find_element_by_id('captcha_image').get_attribute('src')
urllib.request.urlretrieve(captcha_link,'captcha.jpg')
Image.open('captcha.jpg').show()
captcha_code = input('Pls input captcha code:')
browser.find_element_by_id('captcha_field').send_keys(captcha_code)

print('begin login...')
browser.find_element_by_name('login').click()
time.sleep(3)

if browser.current_url == 'https://www.douban.com/':
    print('login success!')
    cookies_list = browser.get_cookies()
    key_dict = {i["name"]:i["value"] for i in cookies_list}
    cookies_str = ''
    for key in key_dict:
        #print('key is %s,value is %s'%(key,key_dict[key]))
        cookies_str += key +'='+ key_dict[key] + ";"
    grabDouBanCommentData.begin(cookies_str)
else:
    print('login error!')
    quit()

browser.quit()