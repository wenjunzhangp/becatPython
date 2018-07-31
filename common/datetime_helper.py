#!/usr/bin/evn python
# coding=utf-8

import time
import datetime


def to_date(dt):
    """将时间格式化为日期字符串"""
    if isinstance(dt, datetime.datetime):
        return dt.strftime('%Y-%m-%d')
    elif isinstance(dt, datetime.date):
        return dt.strftime('%Y-%m-%d')
    else:
        raise Exception("日期类型错误")


def to_datetime(dt):
    """将时间格式化为日期时间字符串"""
    if isinstance(dt, datetime.datetime):
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(dt, datetime.date):
        return dt.strftime('%Y-%m-%d')
    else:
        raise Exception("日期类型错误")


def to_number(format=''):
    """当前时间转换为年月日时分秒毫秒共10位数的字符串"""
    if format:
        return datetime.datetime.now().strftime(format)
    else:
        return datetime.datetime.now().strftime('%Y%m%d%H%M%S')


def to_timestamp10():
    """获取当前时间长度为10位长度的时间戳"""
    return int(time.time())


def to_timestamp13():
    """获取当前时间长度为13位长度的时间戳"""
    return int(time.time() * 1000)


def timedelta(sign, dt, value):
    """
    对指定时间进行加减运算，几秒、几分、几小时、几日、几周、几月、几年
    sign: y = 年, m = 月, w = 周, d = 日, h = 时, n = 分钟, s = 秒
    dt: 日期，只能是datetime或datetime.date类型
    value: 加减的数值
    return: 返回运算后的datetime类型值
    """
    if not isinstance(dt, datetime.datetime) and not isinstance(dt, datetime.date):
        raise Exception("日期类型错误")

    if sign == 'y':
        year = dt.year + value
        if isinstance(dt, datetime.date):
            return datetime.datetime(year, dt.month, dt.day)
        elif isinstance(dt, datetime.datetime):
            return datetime.datetime(year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond)
        else:
            return None
    elif sign == 'm':
        year = dt.year
        month = dt.month + value
        ### 如果月份加减后超出范围，则需要计算一下，对年份进行处理 ###
        # 如果月份加减后等于0时，需要特殊处理一下
        if month == 0:
            year = year - 1
            month = 12
        else:
            # 对年月进行处理
            year = year + month // 12
            month = month % 12
        if isinstance(dt, datetime.date):
            return datetime.datetime(year, month, dt.day)
        elif isinstance(dt, datetime.datetime):
            return datetime.datetime(year, month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond)
        else:
            return None
    elif sign == 'w':
        delta = datetime.timedelta(weeks=value)
    elif sign == 'd':
        delta = datetime.timedelta(days=value)
    elif sign == 'h':
        delta = datetime.timedelta(hours=value)
    elif sign == 'n':
        delta = datetime.timedelta(minutes=value)
    elif sign == 's':
        delta = datetime.timedelta(seconds=value)
    else:
        return None

    return dt + delta
