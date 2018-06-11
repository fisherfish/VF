from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name='昵称', default='')
    birday = models.DateField(verbose_name='生日', null=True, blank=True)
    address = models.CharField(max_length=50, verbose_name='地址', default='')
    gender = models.CharField(max_length=6, choices=(('male', '男'), ('female', '女')), default='female')
    image = models.ImageField(max_length=100, upload_to='image/%Y/%m', default='image/default.png')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
    def get_unread_nums(self):
        from operation.models import UserMessage
        return UserMessage.objects.filter(user=self.id,has_read=False).count()
# 邮箱验证码
class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name='验证码')
    email = models.EmailField(max_length=50, verbose_name='邮箱')
    send_type = models.CharField(verbose_name='验证码类型',max_length=20, choices=(('register', '注册'), ('forgetpwd', '找回密码')))
    send_time = models.DateField(default=datetime.now,verbose_name='发送时间')

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

# 轮播图
class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name='标题')
    image = models.ImageField(max_length=100, upload_to='banner/%Y/%m', verbose_name='轮播图')
    url = models.CharField(max_length=200, verbose_name='访问地址')
    index = models.IntegerField(default=100, verbose_name='顺序')
    add_time = models.DateField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

# Create your models here.
