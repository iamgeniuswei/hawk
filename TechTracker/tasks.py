#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/26 10:16
# @Author  : Geniuswei
# @Email   : iamgeniuswei@sina.com
# @File    : tasks.py
# @Desc    :
from __future__ import absolute_import, unicode_literals
from celery import shared_task
import time
from .core.file_to_article_parser import *
import json

@shared_task
def test_task(x, y):
    time.sleep(5)
    return x+y


@shared_task
def parse_files_db(params:str):
    try:
        params = json.loads(s=params)
        parser = None
        if params['f_source'] == 'WoS':
            parser = WoSParser('WoS', params['f_path'])
        elif params['f_source'] == 'CNKI':
            parser = CNKIParser('CNKI', params['f_path'])
        parser.parse_files_to_articles()
        return True
    except Exception as e:
        print(str(e))
        return False