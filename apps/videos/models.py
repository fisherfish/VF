from django.db import models
from datetime import datetime

class Video(models.Model):
    name = models.CharField(max_length=50, verbose_name='视频名称')
    desc = models.CharField(max_length=300, verbose_name='视频描述')
    detail = models.TextField(verbose_name='视频简介')
    video_times = models.IntegerField(default=0, verbose_name='时长(分钟数)')
    tags = models.CharField(default='电影',verbose_name='视频分类',max_length=20)
    fav_nums = models.IntegerField(default=0, verbose_name='收藏人数')
    image = models.ImageField(max_length=100, upload_to='video/%Y/%m', verbose_name='封面')
    click_nums = models.IntegerField(default=0, verbose_name='评分')
    add_time = models.DateField(default=datetime.now, verbose_name='添加时间')
    url = models.CharField(max_length=200, default='', verbose_name='视频链接')

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

class Season(models.Model):
    video = models.ForeignKey(Video, verbose_name='视频')
    name = models.CharField(max_length=100, verbose_name='季名')
    add_time = models.DateField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '分季'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

class Episode(models.Model):
    season = models.ForeignKey(Season, verbose_name='季名')
    name = models.CharField(max_length=100, verbose_name='集名')
    url = models.CharField(max_length=200,default='',verbose_name='视频链接')
    add_time = models.DateField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '分集'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name


# Create your models here.
