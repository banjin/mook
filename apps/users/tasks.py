# coding:utf-8

from Mook.celery import app
from utils.email_send import random_str, send_mail
from .models import EmailVerifyRecord
from django.conf import settings


@app.task
def send_register(email, send_type="register"):
    email_record = EmailVerifyRecord()
    if send_type == "update_email":
        code = random_str(4)
    else:
        code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()
    email_title = ""
    email_body = ""
    if send_type == "register":
        email_title = u"慕学在线网注册激活链接"
        email_body = u"请点击下面的链接激活你的账号: http://www.imooc.com/active/{0}".format(code)
        send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
        if send_status:
            print "success"
    elif send_type == "forget":
        email_title = u"慕学在线网注册密码重置链接"
        email_body = u"请点击下面的链接重置密码: http://www.imooc.com/reset/{0}".format(code)
        send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
        if send_status:
            print "success"
    elif send_type == "update_email":
        email_title = u"慕学在线邮箱修改验证码"
        email_body = u"你的邮箱验证码为: {0}".format(code)
        send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
        if send_status:
            print "success"
