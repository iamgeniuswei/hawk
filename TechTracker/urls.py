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
    path('topn', views.html_topn, name='topn'),
    path('co', views.html_co, name='co'),
    path('coauthor', views.html_author_co, name='coauthor'),
    path('cokeyword', views.html_keyword_co, name='cokeyword'),
    path('table', views.html_author_info, name='table'),
    path('config_topn', views.html_topn_config, name='ConfigTopN'),
    path('config_co', views.html_co_config, name='ConfigCo'),
    path('config_parser', views.html_config_parser, name='ConfigParser'),
    path('persist_domain', views.json_persist_domain, name='PersistDomain'),
    path('topn_embed', views.html_topn_embed, name='TopNEmbed'),
    path('author_detail', views.html_node_detail, name='AuthorDetail'),
    path('clean', views.json_data_clean, name='CleanData')
]
