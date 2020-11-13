#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/11 8:40
# @Author  : Geniuswei
# @Email   : iamgeniuswei@sina.com
# @File    : urls.py
# @Desc    :

from django.urls import path


from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cnki', views.cnki, name='cnki'),
    path('project', views.project, name='project'),
    path('analyze', views.analyze, name='analyze'),
    path('topn', views.get_top_n, name='topn'),
    path('co', views.html_author_keywords, name='co'),
    path('coauthor',views.html_author_co, name='coauthor'),
    path('table', views.html_author_info, name='table'),
]