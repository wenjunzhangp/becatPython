#!/usr/bin/evn python
# coding=utf-8

import datetime
import json
import unittest
from common import json_helper


class JsonHelperTest(unittest.TestCase):
    """json操作包测试类"""

    def setUp(self):
        """初始化测试环境"""
        print('------ini------')

    def tearDown(self):
        """清理测试环境"""
        print('------clear------')

    def test(self):
        js = {
            'test5': datetime.datetime.now(),
        }
        print(js)
        result = json.dumps(js, cls=json_helper.CJsonEncoder)
        print(result)


if __name__ == '__main__':
    unittest.main()
