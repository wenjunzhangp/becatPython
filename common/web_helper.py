#!/usr/bin/evn python
# coding=utf-8

import json
import re
import urllib.parse
from bottle import response, HTTPResponse, request
from common import json_helper


def get_ip():
    """获取当前客户端ip"""
    try:
        ip = request.remote_addr
    except:
        ip = ''
    if not ip:
        try:
            ip = request.environ.get('REMOTE_ADDR')
        except:
            pass
    return ip


def get_session():
    """获取当前用户session"""
    return request.environ.get('beaker.session')


def return_msg(state, msg, data={}):
    """
    接口输出数据到客户端
    :param state:   状态码（公共参数，-1=出错，0=正常）
    :param msg:     说明信息（公共参数）
    :param data:    数据字典
    :return:        返回组合后的json字符串
    """
    msg = {
        "state": state,
        "msg": msg,
        "data": data
    }
    # 将字典转为字符串输出
    message = json.dumps(msg, cls=json_helper.CJsonEncoder).encode('utf-8').decode('unicode_escape')
    return message

def return_msg(state, msg, data):
    """
    接口输出数据到客户端
    :param state:   状态码（公共参数，-1=出错，0=正常）
    :param msg:     说明信息（公共参数）
    :param data:    数据字典
    :return:        返回组合后的json字符串
    """
    #msg = msg.encode('utf-8').decode('unicode_escape')
    msg = {
        "state": state,
        "msg": msg,
        "data": data
    }
    # 将字典转为字符串输出
    message = json.dumps(msg, cls=json_helper.CJsonEncoder).encode('utf-8').decode('unicode_escape')
    return message

def return_raise(msg=''):
    """
    直接终止程序，返回结果给客户端
    修改bottle的异常状态码和异常返回body内容
    :param msg:     输出内容
    :return:        输出字符串
    """
    res = response.copy(cls=HTTPResponse)
    res.status = 200
    res.body = str(msg)
    raise res


def get_form(args_name, msg, is_strip=True, lenght=0, is_check_null=True, notify_msg='', is_check_special_char=True):
    """
    获取客户端Form方式提交的参数值
    :param args_name: 参数名
    :param msg: 参数中文名称
    :param is_strip: 字符串两端是否自动去除空格
    :param lenght: 参数长度最大限制，0为不限制
    :param is_check_null: 是否要求进行非空检测，True：当参数值为空时，返回错误提示客户端不能为空
    :param notify_msg: 非必填项，当参数值为空时，默认返回“xxx 不允许为空”这个提示，如果这个变量有值，则直接返回这个变量值，即定制好的错误提示
    :param is_check_special_char: 判断参数值是否含有特殊字符，True=默认会对特殊字符进行判断，False=不做判断处理，需要手动对接收参数值进行过滤处理，去除危险字符
    :return: 返回处理后的参数
    """
    args_value = ''
    if request.method.upper() in ('POST', 'PUT', 'DELETE'):
        try:
            if request.json:
                args_value = str(request.json.get(args_name, '')).strip()
            else:
                args_value = str(request.forms.get(args_name, '')).strip()
        except:
            args_value = str(request.forms.get(args_name, '')).strip()
        if not args_value:
            args_value = str(request.POST.get(args_name, '')).strip()

    return __request_handle(args_value, msg, is_strip, lenght, is_check_null, notify_msg, is_check_special_char)


def get_query(args_name, msg, is_strip=True, lenght=0, is_check_null=True, notify_msg='', is_check_special_char=True):
    """
    获取客户端Get方式提交的参数值
    :param args_name: 参数名
    :param msg: 参数中文名称
    :param is_strip: 字符串两端是否自动去除空格
    :param lenght: 参数长度最大限制，0为不限制
    :param is_check_null: 是否要求进行非空检测，True：当参数值为空时，返回错误提示客户端不能为空
    :param notify_msg: 非必填项，当参数值为空时，默认返回“xxx 不允许为空”这个提示，如果这个变量有值，则直接返回这个变量值，即定制好的错误提示
    :param is_check_special_char: 判断参数值是否含有特殊字符，True=默认会对特殊字符进行判断，False=不做判断处理，需要手动对接收参数值进行过滤处理，去除危险字符
    :return: 返回处理后的参数
    """
    return __request_handle(__get(args_name), msg, is_strip, lenght, is_check_null, notify_msg, is_check_special_char)


def __get(args_name):
    """
    从get请求中提取请求值（直接使用python的GET获取参数时，有时转换编码时会出现乱码，所以还是直接采用截取后直接转码比较好）
    例如：http://127.0.0.1:81/manage/manager/?page=0&rows=20&sidx=id&sord=desc&name=%E5%BC%A0%E4%B8%89
    :param args_name: 要取值的参数名：name
    :return: 截取的编码值：%E5%BC%A0%E4%B8%89
    """
    get = '?' + request.query_string
    start_index = get.find('&' + args_name + '=')
    if start_index == -1:
        start_index = get.find('?' + args_name + '=')
        if start_index == -1:
            return ''
    end_index = get.find('&', start_index + 1)
    if end_index == -1:
        return get[start_index + len(args_name + '=') + 1:]
    else:
        return get[start_index + len(args_name + '=') + 1:end_index]


def __request_handle(args_value, msg, is_strip, lenght, is_check_null, notify_msg, is_check_special_char):
    """
    对客户端提交的参数进行各种判断与处理
    :param args_value: 参数值
    :param msg: 参数中文名称
    :param is_strip: 字符串两端是否自动去除空格
    :param lenght: 参数长度最大限制，0为不限制
    :param is_check_null: 是否要求进行非空检测，True：当参数值为空时，返回错误提示客户端不能为空
    :param notify_msg: 非必填项，当参数值为空时，默认返回“xxx 不允许为空”这个提示，如果这个变量有值，则直接返回这个变量值，即定制好的错误提示
    :param is_check_special_char: 判断参数值是否含有特殊字符，True=默认会对特殊字符进行判断，False=不做判断处理，需要手动对接收参数值进行过滤处理，去除危险字符
    :return: 返回处理后的参数
    """
    # 如果参数为空，则返回该参数不允许为空的json串给前端
    if is_check_null and not args_value:
        if notify_msg:
            return_raise(return_msg(-1, notify_msg))
        else:
            return_raise(return_msg(-1, "%s 不允许为空" % msg))
    elif not args_value:
        return args_value

    # 把utf-8的url编码解码成中文字符
    try:
        if '%25' in args_value:
            args_value = urllib.parse.unquote(args_value.replace('%25', '%'))
        else:
            args_value = urllib.parse.unquote(args_value)
    except:
        pass

    # 替换特殊的空字符
    args_value = args_value.replace(u'\xa0', u'')
    # 是否字符串两端去空格
    if is_strip:
        args_value = args_value.strip()
    # 判断是否超出指定长度
    if lenght > 0 and len(args_value) > lenght:
        return_raise(return_msg(-1, "%s 超出 %s 个字符" % (msg, lenght)))

    # 如果参数含有特殊字符，则返回该参数不允许有特殊字符的json串给前端
    if is_check_special_char:
        re_result = re.search('\||`|<|>|&|%|~|\^|;|\'', args_value)
        if re_result:
            return_raise(return_msg(-1, "%s 含有特殊字符，请重新输入" % msg))
    return args_value
