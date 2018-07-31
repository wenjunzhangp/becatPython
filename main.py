#!/usr/bin/evn python
# coding=utf-8

import bottle
import sys
import os
import logging
import urllib.parse
from bottle import default_app, get, run, request, hook, response, static_file
from beaker.middleware import SessionMiddleware

# 导入工具函数包
from common import web_helper, log_helper
# 导入api代码模块（初始化api文件夹里的各个访问路由，这一句不能删除，删除后将无法访问api文件夹里的各个接口）
import api

#############################################
# 初始化bottle框架相关参数
#############################################
# 获取当前main.py文件所在服务器的绝对路径
program_path = os.path.split(os.path.realpath(__file__))[0]
# 将路径添加到python环境变量中
sys.path.append(program_path)
# 让提交数据最大改为2M（如果想上传更多的文件，可以在这里进行修改）
bottle.BaseRequest.MEMFILE_MAX = 1024 * 1024 * 2
# 定义upload为上传文件存储路径
upload_path = os.path.join(program_path, 'upload')

#############################################
# 初始化日志相关参数
#############################################
# 如果日志目录log文件夹不存在，则创建日志目录
if not os.path.exists('log'):
    os.mkdir('log')
# 初始化日志目录路径
log_path = os.path.join(program_path, 'log')
# 定义日志输出格式与路径
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    filename="%s/info.log" % log_path,
                    filemode='a')

# 设置session参数
session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 36000,
    'session.data_dir': '/tmp/sessions/simple',
    'session.auto': True
}


@hook('before_request')
def validate():
    """使用勾子处理接口访问事件"""
    r = request
    # 获取当前访问的Url路径
    path_info = request.environ.get("PATH_INFO")
    # 过滤不用做任何操作的路由（即过滤不用进行判断是否登录和记录日志的url）
    if path_info in ['/favicon.ico', '/', '/api/verify/'] or path_info.find('/upload/') > -1:
        return
    ### 记录客户端提交的参数 ###
    # 获取当前访问url路径与ip
    request_log = 'url:' + path_info + ' ip:' + web_helper.get_ip()
    try:
        # 添加json方式提交的参数
        if request.json:
            request_log = request_log + ' params(json):' + urllib.parse.unquote(str(request.json))
    except:
        pass
    try:
        # 添加GET方式提交的参数
        if request.query_string:
            request_log = request_log + ' params(get):' + urllib.parse.unquote(str(request.query_string))
        # 添加POST方式提交的参数
        if request.method == 'POST':
            request_log = request_log + ' params(post):' + urllib.parse.unquote(str(request.params.__dict__))
        # 存储到日志文件中
        log_helper.info(request_log)
    except:
        pass

    # 处理ajax提交的put、delete等请求转换为对应的请求路由（由于AJAX不支持RESTful风格提交，所以需要在这里处理一下，对提交方式进行转换）
    if request.method == 'POST' and request.POST.get('_method'):
        request.environ['REQUEST_METHOD'] = request.POST.get('_method', '')

    # 过滤不用进行登录权限判断的路由（登录与退出登录不用检查是否已经登录）
    url_list = ["/api/login/", "/api/logout/", "/api/about/", "/api/contact_us/", "/api/product_class/", "/api/product/"]
    if path_info in url_list or (request.method == 'GET' and path_info.find('/api/product/') > -1):
        pass
    else:
        # 已经登录成功的用户session肯定有值，没有值的就是未登录
        session = web_helper.get_session()
        # 获取用户id
        manager_id = session.get('id', 0)
        login_name = session.get('login_name', 0)
        # 判断用户是否登录
        if not manager_id or not login_name:
            web_helper.return_raise(web_helper.return_msg(-404, "您的登录已失效，请重新登录"))

@get('/upload/<filepath:path>')
def upload_static(filepath):
    """设置静态内容路由"""
    response.add_header('Content-Type', 'application/octet-stream')
    return static_file(filepath, root=upload_path)


# 函数主入口
if __name__ == '__main__':
    app_argv = SessionMiddleware(default_app(), session_opts)
    run(app=app_argv, host='0.0.0.0', port=80, debug=True, reloader=True)
else:
    # 使用uwsgi方式处理python访问时，必须要添加这一句代码，不然无法访问
    application = SessionMiddleware(default_app(), session_opts)
