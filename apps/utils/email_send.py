from random import Random
from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from VF.settings import EMAIL_FROM

def random_str(length):
    str = ''
    chars = 'qwertyuioplkjhgfdsazxcvbnmMNBVCXZASDFGHJKLPOIUYTREWQ1234567890'
    random = Random()
    for i in range(length):
        str+=chars[random.randint(1,len(chars))]
    return str

def send_register_email(email,send_type ='register'):
    email_record = EmailVerifyRecord()
    code = random_str(6)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    if send_type == 'register':
        email_title = 'VF视界注册激活连接'
        email_body = '点击连接激活你的账号：\nhttp://127.0.0.1:8000/active/{0}'.format(code)
        send_status = send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            pass
    elif send_type == 'forgetpwd':
        email_title = 'VF视界网修改密码连接'
        email_body = '点击重置你的密码：\nhttp://127.0.0.1:8000/reset/{0}'.format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
    elif send_type == 'update_email':
        email_title = 'VF视界重置邮箱验证码'
        email_body = '请保护好您的邮箱重置验证码：\n{0}'.format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass