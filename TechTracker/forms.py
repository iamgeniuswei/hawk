#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/11 11:27
# @Author  : Geniuswei
# @Email   : iamgeniuswei@sina.com
# @File    : forms.py
# @Desc    :
from django import forms
from .models import *
class FProject(forms.ModelForm):
    class Meta:
        model = TProject
        fields = ['f_name', 'f_topic', 'f_time']