#!/usr/bin/evn python
# coding=utf-8

import os
from bottle import post, request
from common import datetime_helper, random_helper, log_helper

@post('/api/files/')
def callback():
    """
    修改记录
    """
    # 初始化输出值
    result = {
        "state": "FAIL",
        "url": "",
        "title": "上传失败",
        "original": ""
    }
    # 获取上传文件
    try:
        # upfile为前端HTML上传控件名称
        upload = request.files.get('upfile')
        # 如果没有读取到上传文件或上传文件的方式不正确，则返回上传失败状态
        if not upload:
            return result

        # 取出文件的名字和后缀
        name, ext = os.path.splitext(upload.filename)
        # 给上传的文件重命名，默认上传的是图片
        if ext and ext != '':
            file_name = datetime_helper.to_number() + random_helper.get_string(5) + ext
        else:
            file_name = datetime_helper.to_number() + random_helper.get_string(5) + '.jpg'
        upload.filename = file_name

        # 设置文件存储的相对路径
        filepath = '/upload/' + datetime_helper.to_number('%Y%m%d') + '/'
        # 组合成服务器端存储绝对路径
        upload_path = os.getcwd() + filepath
        # 如果目录不存在，则创建目录
        if not os.path.exists(upload_path):
            os.mkdir(upload_path)
        # 保存文件
        upload.save(upload_path + upload.filename, overwrite=True)

        # 设置输出参数（返回相对路径给客户端）
        result['title'] = result['original'] = upload.filename
        result['url'] = filepath + upload.filename
        result['state'] = 'SUCCESS'
    except Exception as e:
        log_helper.error('上传失败：' + str(e.args))

    # 直接输出json
    return result
