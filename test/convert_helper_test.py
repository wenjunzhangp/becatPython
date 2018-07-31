#!/usr/bin/evn python
# coding=utf-8

import datetime
import unittest
from common import convert_helper


class ConvertHelperTest(unittest.TestCase):
    """转换操作包测试类"""

    def setUp(self):
        """初始化测试环境"""
        print('------ini------')

    def tearDown(self):
        """清理测试环境"""
        print('------clear------')

    def test_to_int(self):
        self.assertEqual(convert_helper.to_int('1'), 1)
        self.assertEqual(convert_helper.to_int('1.0'), 0)
        self.assertEqual(convert_helper.to_int('1a'), 0)
        self.assertEqual(convert_helper.to_int('aaa'), 0)
        self.assertEqual(convert_helper.to_int(''), 0)
        self.assertEqual(convert_helper.to_int(None), 0)
        self.assertEqual(convert_helper.to_int('-1'), -1)
        self.assertEqual(convert_helper.to_int(10), 10)
        self.assertEqual(convert_helper.to_int(-10), -10)

        self.assertEqual(convert_helper.to_int0('1'), 1)
        self.assertEqual(convert_helper.to_int0('1.0'), 0)
        self.assertEqual(convert_helper.to_int0('1a'), 0)
        self.assertEqual(convert_helper.to_int0('aaa'), 0)
        self.assertEqual(convert_helper.to_int0(''), 0)
        self.assertEqual(convert_helper.to_int0(None), 0)
        self.assertEqual(convert_helper.to_int0('-1'), 0)
        self.assertEqual(convert_helper.to_int0(10), 10)
        self.assertEqual(convert_helper.to_int0(-10), 0)

        self.assertEqual(convert_helper.to_int1('1'), 1)
        self.assertEqual(convert_helper.to_int1('1.0'), 1)
        self.assertEqual(convert_helper.to_int1('1a'), 1)
        self.assertEqual(convert_helper.to_int1('aaa'), 1)
        self.assertEqual(convert_helper.to_int1(''), 1)
        self.assertEqual(convert_helper.to_int1(None), 1)
        self.assertEqual(convert_helper.to_int1('-1'), 1)
        self.assertEqual(convert_helper.to_int1(10), 10)
        self.assertEqual(convert_helper.to_int1(-10), 1)

    def test_to_float(self):
        self.assertEqual(convert_helper.to_float('1'), 1.0)
        self.assertEqual(convert_helper.to_float('1.0'), 1.0)
        self.assertEqual(convert_helper.to_float('1a'), 0.0)
        self.assertEqual(convert_helper.to_float('aaa'), 0.0)
        self.assertEqual(convert_helper.to_float(''), 0.0)
        self.assertEqual(convert_helper.to_float(None), 0.0)
        self.assertEqual(convert_helper.to_float('-1'), -1.0)
        self.assertEqual(convert_helper.to_float(10), 10.0)
        self.assertEqual(convert_helper.to_float(-10), -10.0)

    def test_to_decimal(self):
        self.assertEqual(convert_helper.to_decimal('1'), 1.0)
        self.assertEqual(convert_helper.to_decimal('1.0'), 1.0)
        self.assertEqual(convert_helper.to_decimal('1a'), 0.0)
        self.assertEqual(convert_helper.to_decimal('aaa'), 0.0)
        self.assertEqual(convert_helper.to_decimal(''), 0.0)
        self.assertEqual(convert_helper.to_decimal(None), 0.0)
        self.assertEqual(convert_helper.to_decimal('-1'), -1.0)
        self.assertEqual(convert_helper.to_decimal(10), 10.0)
        self.assertEqual(convert_helper.to_decimal(-10), -10.0)

    def test_to_datetime(self):
        print('---test_to_datetime---')
        print(convert_helper.to_datetime(None))
        print(convert_helper.to_datetime(''))
        print(convert_helper.to_datetime('xxx'))
        print(convert_helper.to_datetime('2017-09-01'))
        print(convert_helper.to_datetime('2017-09-01 11:11'))
        print(convert_helper.to_datetime('2017-09-0111:11'))
        print(convert_helper.to_datetime('2017-09-01 11:11:11'))
        print(convert_helper.to_datetime('2017-09-01 11:11:11.111'))

        self.assertEqual(convert_helper.to_datetime(None), None)
        self.assertEqual(convert_helper.to_datetime(''), None)
        self.assertEqual(convert_helper.to_datetime('xxx'), None)
        result = datetime.datetime(2017, 9, 1)
        self.assertEqual(convert_helper.to_datetime('2017-09-01'), result)
        result = datetime.datetime(2017, 9, 1, 11, 11)
        self.assertEqual(convert_helper.to_datetime('2017-09-01 11:11'), result)
        self.assertEqual(convert_helper.to_datetime('2017-09-0111:11'), None)
        result = datetime.datetime(2017, 9, 1, 11, 11, 11)
        self.assertEqual(convert_helper.to_datetime('2017-09-01 11:11:11'), result)
        result = datetime.datetime(2017, 9, 1, 11, 11, 11, 111000)
        self.assertEqual(convert_helper.to_datetime('2017-09-01 11:11:11.111'), result)

    def test_to_date(self):
        print('---test_to_date---')
        self.assertEqual(convert_helper.to_date(None), None)
        self.assertEqual(convert_helper.to_date(''), None)
        self.assertEqual(convert_helper.to_date('xxx'), None)
        result = datetime.datetime(2017, 9, 1).date()
        print(result)
        self.assertEqual(convert_helper.to_date('2017-09-01'), result)
        self.assertEqual(convert_helper.to_date('2017-09-01 11:11'), result)
        self.assertEqual(convert_helper.to_date('2017-09-01 11:11:11'), result)
        self.assertEqual(convert_helper.to_date('2017-09-01 11:11:11.111'), result)

    def test_to_timestamp10(self):
        print('---test_to_timestamp10---')
        self.assertEqual(convert_helper.to_timestamp10(None), 0)
        self.assertEqual(convert_helper.to_timestamp10(''), 0)
        self.assertEqual(convert_helper.to_timestamp10('xxx'), 0)
        result = int(datetime.datetime(2017, 9, 1).timestamp())
        print(result)
        self.assertEqual(convert_helper.to_timestamp10('2017-09-01'), result)
        result = int(datetime.datetime(2017, 9, 1, 11, 11).timestamp())
        print(result)
        self.assertEqual(convert_helper.to_timestamp10('2017-09-01 11:11'), result)
        result = int(datetime.datetime(2017, 9, 1, 11, 11, 11).timestamp())
        print(result)
        self.assertEqual(convert_helper.to_timestamp10('2017-09-01 11:11:11'), result)
        result = int(datetime.datetime(2017, 9, 1, 11, 11, 11, 111000).timestamp())
        print(result)
        self.assertEqual(convert_helper.to_timestamp10('2017-09-01 11:11:11.111'), result)

    def test_to_timestamp13(self):
        print('---test_to_timestamp13---')
        self.assertEqual(convert_helper.to_timestamp13(None), 0)
        self.assertEqual(convert_helper.to_timestamp13(''), 0)
        self.assertEqual(convert_helper.to_timestamp13('xxx'), 0)
        result = int(datetime.datetime(2017, 9, 1).timestamp() * 1000)
        print(result)
        self.assertEqual(convert_helper.to_timestamp13('2017-09-01'), result)
        result = int(datetime.datetime(2017, 9, 1, 11, 11).timestamp() * 1000)
        print(result)
        self.assertEqual(convert_helper.to_timestamp13('2017-09-01 11:11'), result)
        result = int(datetime.datetime(2017, 9, 1, 11, 11, 11).timestamp() * 1000)
        print(result)
        self.assertEqual(convert_helper.to_timestamp13('2017-09-01 11:11:11'), result)
        result = int(datetime.datetime(2017, 9, 1, 11, 11, 11, 111000).timestamp() * 1000)
        print(result)
        self.assertEqual(convert_helper.to_timestamp13('2017-09-01 11:11:11.111'), result)


if __name__ == '__main__':
    unittest.main()
