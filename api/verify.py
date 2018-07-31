#!/usr/bin/python
#coding: utf-8

from io import BytesIO
from bottle import get, response
from common import verify_helper, log_helper, web_helper


@get('/api/verify/')
def get_verify():
    """生成验证码图片"""
    try:
        # 获取生成验证码图片与验证码
        code_img, verify_code = verify_helper.create_verify_code()

        # 将字符串转化成大写保存到session中
        s = web_helper.get_session()
        s['verify_code'] = verify_code.upper()
        s.save()

        # 输出图片流
        buffer = BytesIO()
        code_img.save(buffer, "jpeg")
        code_img.close()
        response.set_header('Content-Type', 'image/jpg')
        return buffer.getvalue()
    except Exception as e:
        log_helper.error(str(e.args))
