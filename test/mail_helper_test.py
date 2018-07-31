#!/usr/bin/evn python
# coding=utf-8

import unittest
from common import mail_helper, except_helper


class MailHelperTest(unittest.TestCase):
    """邮件操作包测试类"""

    def setUp(self):
        """初始化测试环境"""
        print('------ini------')

    def tearDown(self):
        """清理测试环境"""
        print('------clear------')

    def test(self):
        mail_helper.send_mail('test', 'test', '1654937@qq.com')
        except_info = except_helper.detailtrace()
        mail_helper.send_error_mail('出现异常，堆栈信息：' + except_info)


if __name__ == '__main__':
    unittest.main()
