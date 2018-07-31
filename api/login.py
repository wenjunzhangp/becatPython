#!/usr/bin/evn python
# coding=utf-8

from bottle import put
from common import web_helper, encrypt_helper, db_helper


@put('/api/login/')
def post_login():
    """用户登陆验证"""
    ##############################################################
    # 获取并验证客户端提交的参数
    ##############################################################
    username = web_helper.get_form('username', '帐号')
    password = web_helper.get_form('password', '密码')
    verify = web_helper.get_form('verify', '验证码')
    ip = web_helper.get_ip()

    ##############################################################
    # 从session中读取验证码信息
    ##############################################################
    s = web_helper.get_session()
    verify_code = s.get('verify_code')
    # 删除session中的验证码（验证码每提交一次就失效）
    if 'verify_code' in s:
        del s['verify_code']
        s.save()
    # 判断用户提交的验证码和存储在session中的验证码是否相同
    if verify.upper() != verify_code:
        return web_helper.return_msg(-1, '验证码错误')

    ##############################################################
    ### 获取登录用户记录，并进行登录验证 ###
    ##############################################################
    sql = """select * from manager where login_name='%s'""" % (username,)
    # 从数据库中读取用户信息
    manager_result = db_helper.read(sql)
    # 判断用户记录是否存在
    if not manager_result:
        return web_helper.return_msg(-1, '账户不存在')

    ##############################################################
    ### 验证用户登录密码与状态 ###
    ##############################################################
    # 对客户端提交上来的验证进行md5加密将转为大写（为了密码的保密性，这里进行双重md5加密，加密时从第一次加密后的密串中提取一段字符串出来进行再次加密，提取的串大家可以自由设定）
    # pwd = encrypt_helper.md5(encrypt_helper.md5(password)[1:30]).upper()
    # 对客户端提交上来的验证进行md5加密将转为大写（只加密一次）
    pwd = encrypt_helper.md5(password).upper()
    # 检查登录密码输入是否正确
    if pwd != manager_result[0].get('login_password', ''):
        return web_helper.return_msg(-1, '密码错误')
    # 检查该账号虽否禁用了
    if manager_result[0].get('is_enable', 0) == 0:
        return web_helper.return_msg(-1, '账号已被禁用')

    ##############################################################
    ### 把用户信息保存到session中 ###
    ##############################################################
    manager_id = manager_result[0].get('id', 0)
    s['id'] = manager_id
    s['login_name'] = username
    s.save()

    ##############################################################
    ### 更新用户信息到数据库 ###
    ##############################################################
    # 更新当前管理员最后登录时间、Ip与登录次数（字段说明，请看数据字典）
    sql = """update manager set last_login_time=%s, last_login_ip=%s, login_count=login_count+1 where id=%s"""
    # 组合更新值
    vars = ('now()', ip, manager_id,)
    # 写入数据库
    db_helper.write(sql, vars)

    return web_helper.return_msg(0, '登录成功')
