# -*- coding: utf-8 -*-
import views

from django.conf.urls import url


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    # url(r'checkusername', views.check_username, name='check_username'),
    url(r'^login/$', views.log_in, name='login'),
    url(r'^logout/$', views.log_out, name='logout'),

    # 用户详细信息界面
    url(r'user_detail/$', views.user_detail, name='user_detail'),
    url(r'^modify_user/$', views.modify_user, name='modify_user'),

    url(r'^(?P<article_id>[0-9]+)/comment/$', views.comment, name='commnet'),
    url(r'^(?P<article_id>[0-9]+)/keep/$', views.get_keep, name='keep'),
    url(r'^(?P<article_id>[0-9]+)/poll/$', views.get_poll_article, name='poll'),
    url(r'^(?P<article_id>[0-9]+)/$', views.article, name='article'),

    url(r'^column/(?P<column_id>[0-9]+)/$', views.get_column, name='column'),
    url(r'^search/$', views.search, name='search'),

    url(r'^create_article/$', views.create_article, name='create_article'),
    url(r'^poll_article/$',views.user_poll, name='user_poll'),
    url(r'^keep_article/$',views.user_keep, name='user_keep'),
    url(r'^comment_article/$',views.user_comment, name='user_comment'),
]

