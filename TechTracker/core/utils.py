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
        """
        获取文件夹的所有合法文件列表
        @param path:
        @return:
        """
        filenames: Union[List[str], List[bytes]] = os.listdir(path)
        files = []
        for file in filenames:
            file_path = os.path.join(path, file)
            if os.path.isfile(file_path):
                files.append(file_path)
        return files