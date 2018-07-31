#!/usr/bin/evn python
# coding=utf-8

from bottle import get, put
from common import web_helper, string_helper, db_helper


@get('/api/contact_us/')
def callback():
    """
    获取指定记录
    """
    sql = """select * from infomation where id = 2"""
    # 读取记录
    result = db_helper.read(sql)
    if result:
        # 直接输出json
        return web_helper.return_msg(0, '成功', result[0])
    else:
        return web_helper.return_msg(-1, "查询失败")


@put('/api/contact_us/')
def callback():
    """
    修改记录
    """
    content = web_helper.get_form('content', '内容', is_check_special_char=False)
    # 防sql注入攻击处理
    content = string_helper.filter_str(content, "'")
    # 防xss攻击处理
    content = string_helper.clear_xss(content)

    # 更新记录
    sql = """update infomation set content=%s where id=2 returning id"""
    vars = (content,)
    # 写入数据库
    result = db_helper.write(sql, vars)

    if result and result[0].get('id'):
        return web_helper.return_msg(0, '成功')
    else:
        return web_helper.return_msg(-1, "提交失败")
