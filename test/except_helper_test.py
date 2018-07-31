#!/usr/bin/evn python
# coding=utf-8

import unittest
from common import except_helper


class ExceptHelperTest(unittest.TestCase):
    """堆栈信息获取操作包测试类"""

    def setUp(self):
        """初始化测试环境"""
        print('------ini------')

    def tearDown(self):
        """清理测试环境"""
        print('------clear------')

    def test(self):
        print(except_helper.detailtrace())

if __name__ == '__main__':
    unittest.main()
