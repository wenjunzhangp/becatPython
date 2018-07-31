#!/usr/bin/env python
# coding=utf-8

import pymysql
from common import log_helper
from config import const

# 初始化数据库参数
db_name = const.DB_NAME
db_host = const.DB_HOST
db_port = const.DB_PORT
db_user = const.DB_USER
db_pass = const.DB_PASS


def read(sql):
    """
    连接pg数据库并进行数据查询
    如果连接失败，会把错误写入日志中，并返回false，如果sql执行失败，也会把错误写入日志中，并返回false
    如果所有执行正常，则返回查询到的数据，这个数据是经过转换的，转成字典格式，方便模板调用，其中字典的key是数据表里的字段名
    """
    try:
        # 连接数据库
        conn = pymysql.connect(db_host, db_user, db_pass, db_name, charset='utf8')
        # 获取游标
        cursor = conn.cursor()
    except Exception as e:
        print(e.args)
        log_helper.error('连接数据库失败：' + str(e.args))
        return False
    try:
        # 执行查询操作
        cursor.execute(sql)
        results = cursor.fetchall()
        jsonData = []
        for row in results:
            result = {}
            result['id'] = row[0]
            result['userId'] = row[1]
            result['logType'] = row[2]
            result['userName'] = row[3]
            result['operModule'] = row[4]
            result['operType'] = row[5]
            result['operTime'] = row[6]
            result['remark'] = row[7]
            result['host'] = row[8]
            jsonData.append(result)
    except Exception as e:
        print(e.args)
        log_helper.error('sql执行失败:' + str(e.args) + ' sql:' + str(sql))
        return False
    finally:
        # 关闭游标和数据库链接
        cursor.close()
        conn.close()
    # 返回结果（字典格式）
    return jsonData


def write(sql, vars):
    """
    连接pg数据库并进行写的操作
    如果连接失败，会把错误写入日志中，并返回false，如果sql执行失败，也会把错误写入日志中，并返回false，如果所有执行正常，则返回true
    """
    try:
        # 连接数据库
        conn = pymysql.connect(db_host, db_user, db_pass, db_name, charset='utf8')
        # 获取游标
        cursor = conn.cursor()
    except Exception as e:
        print(e.args)
        log_helper.error('连接数据库失败：' + str(e.args))
        return False
    try:
        # 执行sql语句
        cursor.execute(sql, vars)
        # 提交事务
        conn.commit()
    except Exception as e:
        print(e.args)
        # 如果出错，则事务回滚
        conn.rollback()
        log_helper.error('sql执行失败:' + str(e.args) + ' sql:' + str(sql))
        return False
    else:
        # 获取数据
        try:
            data = [dict((cursor.description[i][0], value) for i, value in enumerate(row))
                         for row in cursor.fetchall()]
        except Exception as e:
            # 没有设置returning或执行修改或删除语句时，记录不存在
            data = None
    finally:
        # 关闭游标和数据库链接
        cursor.close()
        conn.close()

    # 如果写入数据后，将数据库返回的数据返回给调用者
    return data

