from datetime import datetime
from django.db import models
from users.models import UserProfile
from videos.models import Video
from tinymce.models import HTMLField

class VideoComments(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    video = models.ForeignKey(Video, verbose_name='视频')
    comments_title = models.CharField(max_length=300,blank=True,verbose_name='评论标题')
    comments = HTMLField(verbose_name='评论')
    praise_num = models.IntegerField(default=0,verbose_name='点赞数')
    add_time = models.DateField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户评论'
        verbose_name_plural = verbose_name

class CommentsPraise(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    comment = models.ForeignKey(VideoComments,verbose_name='点赞评论')

    class Meta:
        verbose_name = '点赞评论'
        verbose_name_plural = verbose_name

class UserFavorite(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    fav_id = models.IntegerField(default=0, verbose_name='数据id')
    add_time = models.DateField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    user = models.IntegerField(default=0, verbose_name='接收用户')
    Message = models.CharField(max_length=500, verbose_name='消息内容')
    has_read = models.BooleanField(default=False, verbose_name='是否已读')
    add_time = models.DateField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户消息'
        verbose_name_plural = verbose_name
# Create your models here.
