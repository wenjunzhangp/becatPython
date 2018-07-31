#!/usr/bin/evn python
# coding=utf-8

import datetime
import unittest
from common import datetime_helper


class DatetimeHelperTest(unittest.TestCase):
    """日期函数操作包测试类"""

    def setUp(self):
        """初始化测试环境"""
        print('------ini------')

    def tearDown(self):
        """清理测试环境"""
        print('------clear------')

    def test(self):
        dt = datetime.datetime.now()
        print(datetime_helper.to_datetime(dt))
        print(datetime_helper.to_date(dt))
        print(datetime_helper.to_number())
        print(datetime_helper.to_timestamp10())
        print(datetime_helper.to_timestamp13())

    def test_timedelta(self):
        print('---test_timedelta---')
        result = datetime.datetime(2018, 9, 1)
        print(result)
        self.assertEqual(datetime_helper.timedelta('y', datetime.datetime(2017, 9, 1), 1), result)
        result = datetime.datetime(2016, 9, 1)
        print(result)
        self.assertEqual(datetime_helper.timedelta('y', datetime.datetime(2017, 9, 1), -1), result)
        result = datetime.datetime(2018, 3, 1)
        print(result)
        self.assertEqual(datetime_helper.timedelta('m', datetime.datetime(2017, 9, 1), 6), result)
        result = datetime.datetime(2017, 3, 1)
        print(result)
        self.assertEqual(datetime_helper.timedelta('m', datetime.datetime(2017, 9, 1), -6), result)
        result = datetime.datetime(2017, 3, 1)
        print(result)
        self.assertEqual(datetime_helper.timedelta('m', datetime.datetime(2017, 9, 1), -6), result)
        result = datetime.datetime(2017, 9, 8)
        print(result)
        self.assertEqual(datetime_helper.timedelta('w', datetime.datetime(2017, 9, 1), 1), result)
        result = datetime.datetime(2017, 8, 25)
        print(result)
        self.assertEqual(datetime_helper.timedelta('w', datetime.datetime(2017, 9, 1), -1), result)
        result = datetime.datetime(2017, 9, 2)
        print(result)
        self.assertEqual(datetime_helper.timedelta('d', datetime.datetime(2017, 9, 1), 1), result)
        result = datetime.datetime(2017, 8, 31)
        print(result)
        self.assertEqual(datetime_helper.timedelta('d', datetime.datetime(2017, 9, 1), -1), result)
        result = datetime.datetime(2017, 9, 1, 1)
        print(result)
        self.assertEqual(datetime_helper.timedelta('h', datetime.datetime(2017, 9, 1), 1), result)
        result = datetime.datetime(2017, 8, 31, 23)
        print(result)
        self.assertEqual(datetime_helper.timedelta('h', datetime.datetime(2017, 9, 1), -1), result)
        result = datetime.datetime(2017, 9, 1, 0, 1)
        print(result)
        self.assertEqual(datetime_helper.timedelta('n', datetime.datetime(2017, 9, 1), 1), result)
        result = datetime.datetime(2017, 8, 31, 23, 59)
        print(result)
        self.assertEqual(datetime_helper.timedelta('n', datetime.datetime(2017, 9, 1), -1), result)
        result = datetime.datetime(2017, 9, 1, 0, 0, 1)
        print(result)
        self.assertEqual(datetime_helper.timedelta('s', datetime.datetime(2017, 9, 1), 1), result)
        result = datetime.datetime(2017, 8, 31, 23, 59, 59)
        print(result)
        self.assertEqual(datetime_helper.timedelta('s', datetime.datetime(2017, 9, 1), -1), result)


if __name__ == '__main__':
    unittest.main()
