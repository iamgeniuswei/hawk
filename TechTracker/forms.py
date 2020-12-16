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
        fields = ['f_name', 'f_topic']


class FTopAnalysisParams(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # 初始化父类方法
        for field in self.fields.values():
            field.widget.attrs = {'class': 'form-control'}

    class Meta:
        model = TTopAnalysisParams
        fields = ['f_start', 'f_end', 'f_object', 'f_domain', 'f_source' ,'f_index', 'f_top']


class FCoAnalysisParams(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # 初始化父类方法
        for field in self.fields.values():
            field.widget.attrs = {'class': 'form-control'}

    class Meta:
        model = TCoAnalysisParams
        fields = '__all__'


class FParserParams(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # 初始化父类方法
        for field in self.fields.values():
            field.widget.attrs = {'class': 'form-control'}

    class Meta:
        model = TParserParams
        fields = '__all__'

class FTechDomain(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # 初始化父类方法
        for field in self.fields.values():
            field.widget.attrs = {'class': 'form-control'}

    class Meta:
        model = TTechDomain
        fields = '__all__'


class FDataSource(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # 初始化父类方法
        for field in self.fields.values():
            field.widget.attrs = {'class': 'form-control'}

    class Meta:
        model = TDataSource
        fields = '__all__'

class FWosAuthor(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # 初始化父类方法
        for field in self.fields.values():
            field.widget.attrs = {'class': 'form-control'}

    class Meta:
        model = TWoSAuthor
        fields = ['f_name', 'f_chinese', 'f_memo']

class FWosInstitute(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # 初始化父类方法
        for field in self.fields.values():
            field.widget.attrs = {'class': 'form-control'}

    class Meta:
        model = TWoSInstitute
        fields = ['f_name', 'f_chinese', 'f_fullname', 'f_memo']

class FKeyword(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # 初始化父类方法
        for field in self.fields.values():
            field.widget.attrs = {'class': 'form-control'}

    class Meta:
        model = TKeyword
        fields = '__all__'