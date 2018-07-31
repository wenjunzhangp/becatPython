#!/usr/bin/evn python
# coding=utf-8

import re
import bleach


def check_string(text, pattern):
    """
    检查字符串是否符合指定规则
    :param text: 需要检查的字符串
    :param pattern: 正式表达式，如：'^[a-zA-Z]+$'
    :return: 含有指定字符时返回真，否则为假
    """
    match = re.search(pattern, text)
    if match:
        return True
    else:
        return False


def is_email(text):
    """
    验证字符串是否是email
    :param text: 需要检查的字符串
    :return: 符合返回True，不符合返回False
    """
    return check_string(text, '[^\._-][\w\.-]+@(?:[A-Za-z0-9]+\.)+[A-Za-z]+$')


def is_phone(text):
    """
    验证字符串是否是固定电话
    :param text: 需要检查的字符串
    :return: 符合返回True，不符合返回False
    """
    return check_string(text, '\(?0\d{2,3}[) -]?\d{7,8}$')


def is_mobile(text):
    """
    验证字符串是否是手机号码
    :param text: 需要检查的字符串
    :return: 符合返回True，不符合返回False
    """
    return check_string(text, '^1[3578]\d{9}$|^147\d{8}$')


def is_letters(text):
    """
    验证字符串是否全是字母
    :param text: 需要检查的字符串
    :return: 符合返回True，不符合返回False
    """
    return check_string(text, '^[a-zA-Z]+$')


def is_idcard(text):
    """
    验证字符串是否是身份证号码
    :param text: 需要检查的字符串
    :return: 格式正确返回True，错误返回False
    """
    ic = IdentityCard()
    return ic.check(text.upper())


def filter_str(text, filter='\||<|>|&|%|~|\^|;|\''):
    """
    过滤字符串
    :param text: 需要过滤的字符串
    :param filter: 过滤内容（正则表达式）
    :return: 去除特殊字符后的字符串
    """
    if text:
        return re.subn(filter, '', text)[0]
    else:
        return ''

def clear_xss(html):
    """
    清除xss攻击标签
    :param html: 要处理的html
    :return:
    """
    tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol', 'strong', 'ul']
    tags.extend(
        ['div', 'p', 'hr', 'br', 'pre', 'code', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'del', 'dl', 'img', 'sub', 'sup', 'u',
         'table', 'thead', 'tr', 'th', 'td', 'tbody', 'dd', 'caption', 'blockquote', 'section'])
    attributes = {'*': ['class', 'id'], 'a': ['href', 'title', 'target'], 'img': ['src', 'style', 'width', 'height']}
    return bleach.linkify(bleach.clean(html, tags=tags, attributes=attributes))

def filter_tags(htmlstr):
    """
    过滤HTML中的标签
    :param htmlstr: 要过滤的内容
    :return:
    """
    re_cdata=re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I) #匹配CDATA
    re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)#Script
    re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)#style
    re_br=re.compile('<br\s*?/?>')#处理换行
    re_h=re.compile('</?\w+[^>]*>')#HTML标签
    re_comment=re.compile('<!--[^>]*-->')#HTML注释
    s=re_cdata.sub('',htmlstr)#去掉CDATA
    s=re_script.sub('',s) #去掉SCRIPT
    s=re_style.sub('',s)#去掉style
    s=re_br.sub('\n',s)#将br转换为换行
    s=re_h.sub('',s) #去掉HTML 标签
    s=re_comment.sub('',s)#去掉HTML注释
    #去掉多余的空行
    blank_line=re.compile('\n+')
    s=blank_line.sub('\n',s)
    s=replaceCharEntity(s)#替换实体
    return s

def replaceCharEntity(htmlstr):
    """
    替换常用HTML字符
    :param htmlstr: 要替换的字符
    :return:
    """
    CHAR_ENTITIES={'nbsp':' ','160':' ',
                'lt':'<','60':'<',
                'gt':'>','62':'>',
                'amp':'&','38':'&',
                'quot':'"','34':'"',}
    re_charEntity=re.compile(r'&#?(?P<name>\w+);')
    sz=re_charEntity.search(htmlstr)
    while sz:
        entity=sz.group()#entity全称，如&gt;
        key=sz.group('name')#去除&;后entity,如&gt;为gt
        try:
            htmlstr=re_charEntity.sub(CHAR_ENTITIES[key],htmlstr,1)
            sz=re_charEntity.search(htmlstr)
        except KeyError:
            #以空串代替
            htmlstr=re_charEntity.sub('',htmlstr,1)
            sz=re_charEntity.search(htmlstr)
    return htmlstr


def string(text, is_return_null=False):
    """
    sql字符串拼接专用函数
    会在字符串两边添加'单撇号，用于生成数据库sql语句
    :param text: 需要添加'的字符串
    :param is_return_null: 是否返回null，是的话在字符串为空时返回null，否则返回''
    :return:
    """
    if not text is None and text != '':
        return "'" + str(text) + "'"
    elif not is_return_null:
        return "''"
    else:
        return "null"


def cut_str(text, length):
    """
    字符串按指定长度截取
    :param text: 需要进行截取的字符串
    :param length: 字符串保留的长度
    :return:
    """
    if not text or not isinstance(text, str):
        return text
    tem = ''
    try:
        tem = text.decode('utf8')
    except:
        pass
    if not tem or tem == '':
        try:
            tem = text[0:length]
        except:
            tem = text
    return tem[0:length]


class IdentityCard:
    """身份证号码验证类"""

    def __init__(self):
        self.__Wi = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        self.__Ti = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']

    def calculate(self, code):
        """计算校验位"""
        sum = 0
        for i in range(17):
            sum += int(code[i]) * self.__Wi[i]
        return self.__Ti[sum % 11]

    def check(self, code):
        """检查输入的号码是否正确"""

        if (len(code) != 18):
            return False
        if self.calculate(code) != code[17]:
            return False

        return True
