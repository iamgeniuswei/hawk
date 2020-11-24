#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/11 15:33
# @Author  : Geniuswei
# @Email   : iamgeniuswei@sina.com
# @File    : file_to_article_parser.py
# @Desc    :

import pandas as pd
from .utils import Utility
from ..models import *
import networkx as nx

class FileParser(object):
    def __init__(self, format, path):
        self._format = format
        self._path = path

    def parse_files_to_articles(self):
        pass

    def str_to_list(self, src_str):
        '''
        四种情况：
        1）','分隔
        2）';'分隔
        3）' '分隔
        4）无分隔
        '''
        list_str = []
        src_str = src_str.replace(' ', '')
        src_str = src_str.replace(',', ';')
        if ';' in src_str:
            list_str = src_str.rstrip(';').split(';')
        else:
            list_str.append(src_str)
        return list(filter(None, list_str))

class CNKIParser(FileParser):
    def parse_files_to_articles(self):
        try:
            files = Utility.get_files_in_dir(self._path)
            for file in files:
                self.parse_single_file(file)

        except Exception as e:
            print(str(e))


    def parse_single_file(self, file):
        try:
            df = pd.read_excel(file, sheet_name=0).fillna(value='佚名')

            for row in df.index:
                str_title = df.loc[row].values[1]
                str_publication = df.loc[row].values[4]
                str_pulish_time = df.loc[row].values[7]
                str_abstract = df.loc[row].values[6]
                list_authors = self.str_to_list(df.loc[row].values[2])
                list_institute = self.str_to_list(df.loc[row].values[3])
                list_keywords = self.str_to_list(df.loc[row].values[5])

                objects_authors = self.parse_authors(list_authors, list_institute)
                objects_institutes = self.parse_institutes(list_institute)
                objects_keywords = self.parse_keywords(list_keywords)
                object_publication = self.parse_publication(str_publication)

                try:
                    new_article = TArticle.objects.get_or_create(f_name=str_title,
                                                                 f_abstract=str_abstract,
                                                                 f_authors_str= ','.join(list_authors),
                                                                 f_institutes_str= ','.join(list_institute),
                                                                 f_keywords_str= ','.join(list_keywords),
                                                                 f_year=self.parse_publication_time(str_pulish_time),
                                                                 f_publication=object_publication,
                                                                 f_source_id=1)[0]
                    for author in objects_authors:
                        new_article.f_other_authors.add(author)
                    for institute in objects_institutes:
                        new_article.f_institutes.add(institute)
                    for keyword in objects_keywords:
                        new_article.f_keywords.add(keyword)
                except Exception as e:
                    print(str(e))

        except Exception as e:
            print(str(e))

    def parse_authors(self, list_authors, list_institute):
        objects_authors = []
        if len(list_authors) >= 1:
            if len(list_institute) >= 1:
                institute = TInstitute.objects.get_or_create(f_name=list_institute[0])[0]
                first_author = TAuthor.objects.get_or_create(f_name=list_authors[0], f_institute=institute)[0]
            else:
                first_author = TAuthor.objects.get_or_create(f_name=list_authors[0])[0]
            objects_authors.append(first_author)
            for author in list_authors[1:]:
                if len(list_institute) == 1:
                    institute = TInstitute.objects.get_or_create(f_name=list_institute[0])[0]
                    other_author = TAuthor.objects.get_or_create(f_name=author, f_institute=institute)[0]
                else:
                    other_author = TAuthor.objects.get_or_create(f_name=author, f_institute=institute)[0]
                objects_authors.append(other_author)
        else:
            first_author = TAuthor.objects.get_or_create(f_name='佚名')[0]
            objects_authors.append(first_author)
        return objects_authors

    def parse_publication(self, publictaion):
        new_publication = None
        new_publication = TPublication.objects.get_or_create(f_name=publictaion)[0]
        return new_publication


    def parse_keywords(self, list_keywords):
        objects_keywords = []
        for keyword in list_keywords:
            new_keyword = TKeyword.objects.get_or_create(f_name=keyword)[0]
            objects_keywords.append(new_keyword)
        return objects_keywords

    def parse_institutes(self, list_institutes):
        objects_institutes = []
        for institute in list_institutes:
            new_institute = TInstitute.objects.get_or_create(f_name=institute)[0]
            objects_institutes.append(new_institute)
        return objects_institutes

    def parse_publication_time(self, time_str):
        if len(time_str)<4:
            return 2020
        else:
            try:
                return int(time_str[:4])
            except Exception as e:
                print(str(e))
                return 2020





