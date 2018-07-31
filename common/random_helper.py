#!/usr/bin/evn python
# coding=utf-8

import random
import uuid
from common import encrypt_helper

### 定义常量 ###
# 小写字母
lowercase_letters = "abcdefghijklmnopqrstuvwxyz"
# 大写字母
majuscule = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
# 数字
numbers = "0123456789"
################

def ___get_randoms(length, text):
    """
    内部函数，获取指定长度的随机字符
    :param length: 将要生成的字符长度
    :param text: 生成随机字符的字符池
    :return: 生成好的随机字符串
    """
    return random.sample(text, length)

def get_number(length):
    """
    获取指定长度的数字，类型是字符串
    :param length: 将要生成的字符长度
    :return: 生成好的随机字符串
    """
    return  ''.join(___get_randoms(length, numbers))

def get_number_for_range(small, max):
    """
    获取指定大小的整形数值
    :param small: 最小数值
    :param max: 最大数值
    :return: 生成好的随机数值
    """
    return random.randint(small, max)

def get_string(length):
    """
    获取指定长度的字符串（大小写英文字母+数字）
    :param length: 将要生成的字符长度
    :return: 生成好的随机字符串
    """
    return  ''.join(___get_randoms(length, lowercase_letters + majuscule + numbers))

def get_letters(length):
    """
    生成随机英文字母字符串（大小写英文字母）
    :param length: 将要生成的字符长度
    :return: 生成好的随机字符串
    """
    return  ''.join(___get_randoms(length, lowercase_letters + majuscule))

def get_uuid():
    """
    随机生成uuid
    :return: 生成好的uuid
    """
    return str(uuid.uuid4()).replace('-', '')
