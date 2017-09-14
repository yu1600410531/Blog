# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from django.db import models
from django import forms
from .models import Comment,Article,Column,NewUser, Author


class CommentAdmin(admin.ModelAdmin):
    '''
    admin.ModelAdmin是django内置的处理自定义界面的模块
    list_display 是数据库模型的字段，可以自定义后台
    要实现哪些字段。所有的模块定义好以后，使用admin.site.register注册
    '''
    list_display = ('user_id', 'article_id', 'pub_date', 'content', 'poll_num')




class ArticleAdmin(admin.ModelAdmin):
    # formfield_overrides 可以更改字段默认的后台显示细节
    # formfield_overrides = {
    #     models.TextField:{
    #         # 有两个字段，一个max_length, 一个widget
    #         'widget':forms.Textarea(
    #             attrs={
    #                 'rows':41,
    #                 'cols':100
    #             })},
    # }
    class Media:
        js = (
            'kindeditor/kindeditor-all.js',
            'kindeditor/lang/zh-CN.js',
            'kindeditor/config.js',
        )

    list_display = ('title','pub_date', 'poll_num')

class NewUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'date_joined', 'profile')

class ColumnAdmin(admin.ModelAdmin):
    list_display = ('name', 'intro')

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'profile')

admin.site.register(Comment, CommentAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Column, ColumnAdmin)
# admin.site.register(NewUser)
admin.site.register(NewUser, NewUserAdmin)
admin.site.register(Author, AuthorAdmin)





