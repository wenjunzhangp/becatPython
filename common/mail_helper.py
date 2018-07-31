#!/usr/bin/evn python
# coding=utf-8

import smtplib
from email.mime.text import MIMEText
from traceback import format_exc
from config import const

# 初始化邮件参数
smtp = const.SMTP
port = const.PORT
user = const.EMAIL_USER
passwd = const.EMAIL_PWD
email_list = const.EMAIL_LIST
err_title = const.EMAIL_ERR_TITLE


def send_mail(subject, context, to_list):
    '''
    发送邮件
    接收参数：
    subject 邮件主题
    context 邮件内容
    to_list 接收者邮件列表，每个邮件地址用","分隔
    '''
    if not subject or not context or not to_list:
        return '邮件发送失败，邮件主题、内容与收件人邮件都是必填项'

    # 初始始化邮件相关参数
    email = MIMEText(context, 'html', 'utf-8')
    email['To'] = to_list
    email['Subject'] = subject
    email['From'] = user

    # QQ邮箱改为ssl方式发送了
    # s = smtplib.SMTP(smtp)
    s = smtplib.SMTP_SSL(smtp)
    try:
        s.login(user, passwd)
        s.sendmail(user, email_list, email.as_string())
        s.close()
        return None
    except Exception as e:
        s.close()
        stacktrace = format_exc()
        return '邮件发送失败，出现异常：' + str(e.args) + stacktrace + '\n'


def send_error_mail(context):
    '''
    发送邮件
    接收参数：
    context 邮件内容
    '''
    if not context:
        return '邮件内容是必填项'

    send_mail(err_title, context, email_list)
