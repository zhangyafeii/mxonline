# -*- coding: utf-8 -*-

"""
@Datetime: 2019/2/27
@Author: Zhang Yafei
"""
from random import Random

from django.core.mail import send_mail
from django.conf import settings

from users.models import EmailVerifyRecord


def send_register_email(email, send_type='register'):
    print(email)
    email_record = EmailVerifyRecord()
    # 随机生成验证码
    code = random_str(4) if send_type == 'update_email' else random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    if send_type == 'register':
        email_title = '幕学在线网注册激活链接'
        email_body = '请点击下面的连接激活你的账号：http://127.0.0.1:8000/active/{0}'.format(code)

        send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
        return send_status
    elif send_type == 'forget':
        email_title = '幕学在线网注册密码重置链接'
        email_body = '请点击下面的连接激活你的账号：http://127.0.0.1:8000/reset/{0}'.format(code)

        send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
        return send_status
    elif send_type == "update_email":
        email_title = "NBA邮箱修改验证码"
        email_body = "你的邮箱验证码为{0}".format(code)
        # 使用Django内置函数完成邮件发送。四个参数：主题，邮件内容，从哪里发，接受者list
        send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
        print('发送成功')
        # 如果发送成功
        return send_status


def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str
