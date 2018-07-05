# -*- coding:utf-8 -*-
# Author:DaoYang

from django.contrib import admin
from django.urls import path, include, re_path
from app import views

urlpatterns = [
    # 首页
    re_path('index/$', views.Index.as_view()),
    re_path('index/news$', views.showNews),

    re_path('login/$', views.login),
    re_path('register/$', views.register),
    re_path('logout/$', views.logout),

    # 管理图书
    re_path('insert-book/$', views.InsertBook.as_view()),
    re_path('manage-book/$', views.ManageBook.as_view()),
    re_path('delete-book/$', views.deleteBook),
    re_path('modify-book/$', views.ModifyBook.as_view()),
    re_path('Checkbid/$', views.checkbid),
    # 管理用户
    re_path('manage-user/$', views.ManageUser.as_view()),
    re_path('insert-user/$', views.InsertUser.as_view()),
    re_path('delete-user/$', views.deleteUser),
    re_path('modify-user/$', views.ModifyUser.as_view()),
    re_path('Checkuid/$', views.checkuid),
    # 新闻管理
    re_path('manage-new/$', views.ManageNew.as_view()),
    re_path('insert-new/$', views.InsertNew.as_view()),
    re_path('delete-new/$', views.deleteNew),

    #查询
    re_path('query/$', views.query),
    re_path('recommend/$', views.recommend),

    re_path('borrowbook/$', views.borrowbook),

    re_path('zan/$', views.zan),
    re_path('cai/$', views.cai),
    re_path('manage-bb/$', views.bb),
    re_path('delete-bb/$', views.delbb),
]