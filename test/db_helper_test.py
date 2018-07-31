#!/usr/bin/evn python
# coding=utf-8

import unittest
from common import db_helper


class DbHelperTest(unittest.TestCase):
    """数据库操作包测试类"""

    def setUp(self):
        """初始化测试环境"""
        print('------ini------')

    def tearDown(self):
        """清理测试环境"""
        print('------clear------')

    def test(self):
        # 新增记录
        sql = """
            INSERT INTO product_class(
              name, is_enable)
            VALUES (%s, %s)
        """
        data = ('糖果', 1)
        result = db_helper.write(sql, data)
        print(result)

        # 新增记录
        sql = """
            INSERT INTO product_class(
              name, is_enable)
            VALUES (%s, %s)
            RETURNING id;
        """
        data = ('饼干', 1)
        result = db_helper.write(sql, data)
        print(result)

        # 修改不存在的记录
        sql = """
            UPDATE product_class
               SET name=%s, is_enable=%s
            WHERE id=10000
            RETURNING id;
        """
        data = ('糖果', 1)
        result = db_helper.write(sql, data)
        print(result)

        # 查询记录
        sql = """
            SELECT * FROM product_class
        """
        result = db_helper.read(sql)
        print(result)

if __name__ == '__main__':
    unittest.main()
