#!/usr/bin/evn python
# coding=utf-8

import unittest
from common import encrypt_helper


class EncryptHelperTest(unittest.TestCase):
    """加密操作包测试类"""

    def setUp(self):
        """初始化测试环境"""
        print('------ini------')

    def tearDown(self):
        """清理测试环境"""
        print('------clear------')

    def test(self):
        result = encrypt_helper.md5(1)
        print(result)
        self.assertEqual(result, 'c4ca4238a0b923820dcc509a6f75849b')

        result = encrypt_helper.md5('1')
        print(result)
        self.assertEqual(result, 'c4ca4238a0b923820dcc509a6f75849b')

        result = encrypt_helper.md5(b'1')
        print(result)
        self.assertEqual(result, 'c4ca4238a0b923820dcc509a6f75849b')

if __name__ == '__main__':
    unittest.main()
