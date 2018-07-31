#!/usr/bin/evn python
# coding=utf-8

import os

def read_file(file_path):
    """读取文本文件内容"""
    all_line = None
    try:
        if exists(file_path):
            fsock = open(file_path, "r")
            all_line = fsock.readlines()
            fsock.close()
    except:
        pass
    return all_line

def read_file_line(file_path, encoding='utf-8'):
    if not exists(file_path):
        return
    with open(file_path, 'r', encoding=encoding) as f:
        while True:
            block = f.readline()
            if block:
                yield block
            else:
                return

def save_file(file_path, content, encoding='utf-8'):
    """保存内容到文件里"""
    try:
        file_object = open(file_path, 'a', encoding=encoding)
        file_object.write(content)
        file_object.close()
        return True
    except Exception as e:
        return False

def remove_file(file_path):
    """删除文件"""
    try:
        if os.path.isfile(file_path):
            os.remove(file_path)
            return True
    except:
        pass
    return False

def remove_all_file(file_list):
    """批量删除文件"""
    try:
        for file_path in file_list:
            remove_file(file_path)
    except:
        pass

def exists(file_path):
    """检查文件是否存在"""
    return os.path.exists(file_path)
