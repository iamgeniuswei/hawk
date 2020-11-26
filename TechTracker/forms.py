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


class FTopAnalysisParams(forms.ModelForm):
    f_object = forms.TypedChoiceField(label='分析对象',
        choices=ANALYSIS_OBJECT, widget=forms.RadioSelect, coerce=int
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # 初始化父类方法
        for field in self.fields.values():
            if field.label != '分析对象':
                field.widget.attrs = {'class': 'form-control'}

    class Meta:
        model = TTopAnalysisParams
        fields = ['f_purpose', 'f_start', 'f_end', 'f_domain', 'f_source' , 'f_top']


class FCoAnalysisParams(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # 初始化父类方法
        for field in self.fields.values():
            field.widget.attrs = {'class': 'form-control'}

    class Meta:
        model = TCoAnalysisParams
        fields = '__all__'