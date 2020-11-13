#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/11 15:38
# @Author  : Geniuswei
# @Email   : iamgeniuswei@sina.com
# @File    : utils.py
# @Desc    :

import os


# 遍历文件夹下的文件
from typing import List, Union


class Utility(object):
    @staticmethod
    def get_files_in_dir(path):
        files: Union[List[str], List[bytes]] = os.listdir(path)
        path_list = []
        for file in files:
            file_path = os.path.join(path,file)
            path_list.append(file_path)
        return path_list