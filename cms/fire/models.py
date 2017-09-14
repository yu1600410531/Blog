# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
# 内置兼容python2和python3 __unicode__的装饰器，只是针对__str__方法
from django.conf import settings
from django.utils import timezone

# 用于扩展django自带的user库
from django.contrib.auth.models import AbstractBaseUser,AbstractUser


from django.contrib.auth import get_user_model
# def get_sentinel_user():
#     return get_user_model().objects.get_or_create(username='deleted')[0]

#  用户信息扩展
@python_2_unicode_compatible
class NewUser(AbstractUser):
    profile = models.CharField(verbose_name='profile',default='', max_length=256)
    avatar = models.ImageField(verbose_name='用户头像', upload_to='user/', default='default.jpg')
    email = models.EmailField(verbose_name='邮箱', max_length=50)


    def __str__(self):
        return self.username

# 文章所属的分类

@python_2_unicode_compatible
class Column(models.Model):
    name = models.CharField(verbose_name='column_name', max_length=256)
    intro = models.TextField(verbose_name='introduction', default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = "Column"
        ordering = ['name']

# 文章管理器
class ArticleMananger(models.Manager):

    # 查询文章所属分类
    def query_by_column(self,column_id):
        query = self.get_queryset().filter(column_id=column_id)

    # 根据用户id查询文章列表
    def query_by_user(self, user_id):
        user = User.objects.get(id=user_id)
        article_list = user.article_set.all()
        return article_list

    # 根据文章点赞数排序后的文章对象
    def query_by_polls(self):
        query = self.get_queryset().order_by('poll_num')
        return query

    # 文章更新顺序获取对象，由近到远
    def query_by_time(self):
        query = self.get_queryset().order_by('-pub_date')
        return query

    # 很据文章标题模糊查询文章对象
    def query_by_keyword(self,keyword):
        query = self.get_queryset().filter(title__contains=keyword)
        return query

# self.get_queryset()   这个方法得到的是相关的查询集








#  文章数据模型
@python_2_unicode_compatible
class Article(models.Model):
    # 文章所属分类
    column = models.ForeignKey('Column',blank=True, null=True, verbose_name='belong to')
    # 标题
    title = models.CharField(max_length=256)
    # 作者
    author = models.ForeignKey('Author')
    # 收藏用户,普通用户
    user = models.ManyToManyField(NewUser, blank=True)
    # 内容
    content = models.TextField(verbose_name='content')
    # 发表时间
    pub_date = models.DateTimeField(auto_now_add=True, editable=True)
    # 更新时间
    update_time = models.DateTimeField(auto_now_add=True, null=True)
    # 是否发表
    published = models.BooleanField(verbose_name='notDraft', default=True)
    # 点赞数量
    poll_num = models.IntegerField(default=0)
    # 评论数量
    comment_num = models.IntegerField(default=0)
    # 收藏数量
    keep_num = models.IntegerField(default=0)
    # 将查询类与查询方法关联起来，可以扩展其方法。objects.....
    objects = ArticleMananger()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = verbose_name = 'article'


#  评论的数据模型
@python_2_unicode_compatible
class Comment(models.Model):
    user = models.ForeignKey(NewUser, null=True)
    article = models.ForeignKey(Article, null=True)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True, editable=True)
    poll_num = models.IntegerField(default=0)

    def __str__(self):
        return self.content

#   增加点赞的数据模型
class Poll(models.Model):
    user = models.ForeignKey(NewUser, null=True)
    article = models.ForeignKey(Article, null=True)
    comment = models.ForeignKey(Comment, null=True)


@python_2_unicode_compatible
class Author(models.Model):
    name = models.CharField(max_length=256)
    profile = models.CharField('profile',default='', max_length=256)
    password = models.CharField('password', max_length=256)
    # editable = True  强制显示
    register_date = models.DateTimeField(auto_now_add=True, editable=True)

    def __str__(self):
        return self.name



