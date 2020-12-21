#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/11 15:33
# @Author  : Geniuswei
# @Email   : iamgeniuswei@sina.com
# @File    : file_to_article_parser.py
# @Desc    :
import json

import pandas as pd
from .utils import Utility
from ..models import *
from .nlp import *
import networkx as nx
import re
from django.db import transaction

class FileParser(object):
    def __init__(self, params):
        self._params = params
        self._format = params['f_source']
        self._path = params['f_path']
        self._errors = list()

    def get_domains(self):
        domain_objects = []
        list_domains = self._params['f_domain']
        if len(list_domains) == 0:
            return domain_objects
        for domain in list_domains:
            domain_object = TTechDomain.objects.get_or_create(f_name=domain)[0]
            domain_objects.append(domain_object)
        return domain_objects

    def parse_articles_to_db(self):
        new_articles = []
        try:
            files = Utility.get_files_in_dir(self._path)
            for file in files:
                try:
                    df = pd.read_excel(file, sheet_name=0).fillna(value='佚名')
                    articles = self.parse_single_file(df)
                    new_articles += articles
                except Exception as e:
                    error = "导入文献文件 {0} 失败，失败原因：{1}".format(file, str(e))
                    self._errors.append(error)
                    print(error)
            return new_articles, self._errors
        except Exception as e:
            error = "导入文献失败，失败原因：{0}".format(str(e))
            self._errors.append(error)
            print(error)
            return new_articles, self._errors

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

    def parse_single_file(self, df):
        new_articles = []
        domain_objects = []
        for domain in self._params['f_domain']:
            domain_object = TTechDomain.objects.get_or_create(f_name=domain)[0]
            domain_objects.append(domain_object)
        obj_source = TDataSource.objects.get_or_create(f_name=self._params['f_source'])[0]
        for row in df.index:
            try:
                with transaction.atomic():
                    obj_article = self.persist_article(df, row, obj_source)
                    if obj_article is not None:
                        list_obj_authors, list_obj_institutes = self.persist_authors_institutes(obj_article)
                        list_obj_keywords = self.persist_keywords(obj_article)
                        self.persist_article_domain(obj_article, domain_objects)
                        self.persist_article_keyword(obj_article, list_obj_keywords)
                        self.persist_article_authors(obj_article, list_obj_authors)
                        self.persist_article_institutes(obj_article, list_obj_institutes)
                    new_articles.append(obj_article)
            except Exception as e:
                error = "文献 {0} 解析失败，失败原因：{1}".format(obj_article.f_ti, str(e))
                self._errors.append(error)
                print(error)
        return new_articles

    def persist_article_domain(self, obj_article, list_obj_domain):
        for domain in list_obj_domain:
            obj_article.f_domain.add(domain)

    def persist_article_keyword(self, obj_article, list_obj_keywords):
        for keyword in list_obj_keywords:
            obj_article.f_keywords.add(keyword)

    def persist_article_authors(self, obj_article, list_obj_authors):
        index = 0
        for author in list_obj_authors:
            index += 1
            TAuthorOrder.objects.update_or_create(f_author=author, f_article=obj_article, f_order=index)

    def persist_article_institutes(self, obj_article, list_obj_institutes):
        index = 0
        for institute in list_obj_institutes:
            index += 1
            TInstituteOrder.objects.update_or_create(f_institute=institute, f_article=obj_article, f_order=index)

    def persist_article(self, df, row, tdatasource_object):
        pass

    def persist_authors_institutes(self, obj_article):
        list_obj_authors = []
        list_obj_institutes = []
        return list_obj_authors, list_obj_institutes

    def persist_keywords(self, obj_article):
        list_obj_keywords = []
        return list_obj_keywords



class CNKIParser(FileParser):
    def parse_articles_to_db(self):
        new_articles = []
        try:
            files = Utility.get_files_in_dir(self._path)
            for file in files:
                articles = self.parse_single_file(file)
                new_articles.append(articles)
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

from collections import defaultdict
class WoSArticleParser(FileParser):
    def str_to_int(self, nr, u1, u2, py):
        if type(nr) == type(int):
            int_nr = int(nr)
        else:
            int_nr = 0
        if u1.isdigit():
            int_u1 = int(u1)
        else:
            int_u1 = 0
        if u2.isdigit():
            int_u2 = int(u2)
        else:
            int_u2 = 0
        if py.isdigit():
            int_py = int(py)
        else:
            int_py = 0
        return int_nr, int_u1, int_u2, int_py

    def get_institute(self, str_intitutes, str_authors):
        author_institutes = defaultdict(list)
        list_authors = str_authors.split(';')
        if '[' in str_intitutes and ']' in str_intitutes:
            str_intitutes += ';'
            list_institutes = re.findall(r'\[.*?\].*?;', str_intitutes)
            for author in list_authors:
                author = author.strip()
                for institute in list_institutes:
                    if author in institute:
                        institute = (re.search(r'\].*?;', institute).group()).strip('] ').strip(';')
                        author_institutes[author].append(institute)
        else:
            for author in list_authors:
                author = author.strip()
                author_institutes[author].append(str_intitutes)
        return author_institutes

    def persist_article(self, df, row, tdatasource_object):
        new_article = None
        try:
            str_pt = df.loc[row].values[0]
            str_dt = df.loc[row].values[13]
            str_fu = df.loc[row].values[27]
            str_fx = df.loc[row].values[28]
            str_af = df.loc[row].values[5]
            str_ti = df.loc[row].values[8]
            str_de = df.loc[row].values[19]
            str_id = df.loc[row].values[20]
            str_ab = df.loc[row].values[21]
            str_c1 = df.loc[row].values[22]
            str_cr = df.loc[row].values[29]
            int_nr = df.loc[row].values[30]
            int_u1 = df.loc[row].values[33]
            int_u2 = df.loc[row].values[34]
            int_py = df.loc[row].values[44]
            str_wc = df.loc[row].values[58]
            str_sc = df.loc[row].values[59]
            new_article = TWoSArticle.objects.get_or_create(f_ti=str_ti,
                                                            f_pt=str_pt,
                                                            f_dt=str_dt,
                                                            f_fu=str_fu,
                                                            f_fx=str_fx,
                                                            f_af=str_af,
                                                            f_de=str_de,
                                                            f_id=str_id,
                                                            f_ab=str_ab,
                                                            f_c1=str_c1,
                                                            f_cr=str_cr,
                                                            f_nr=int_nr,
                                                            f_u1=int_u1,
                                                            f_u2=int_u2,
                                                            f_py=int_py,
                                                            f_wc=str_wc,
                                                            f_sc=str_sc,
                                                            f_source_id=tdatasource_object.id)[0]
        except Exception as e:
            error = "文献 {0} 解析失败，失败原因：{1}".format(str_ti, str(e))
            self._errors.append(error)
            print(error)
        return new_article


    # def parse_single_file(self, file):
    #     try:
    #         df = pd.read_excel(file, sheet_name=0).fillna(value='佚名')
    #         domain_objects = []
    #         for domain in self._params['f_domain']:
    #             domain_object = TTechDomain.objects.get_or_create(f_name=domain)[0]
    #             domain_objects.append(domain_object)
    #         source_object = TDataSource.objects.get_or_create(f_name=self._params['f_source'])[0]
    #         for row in df.index:
    #             str_pt = df.loc[row].values[0]
    #             str_dt = df.loc[row].values[13]
    #             str_fu = df.loc[row].values[27]
    #             str_fx = df.loc[row].values[28]
    #             str_af = df.loc[row].values[5]
    #             str_ti = df.loc[row].values[8]
    #             str_de = df.loc[row].values[19]
    #             str_id = df.loc[row].values[20]
    #             str_ab = df.loc[row].values[21]
    #             str_c1 = df.loc[row].values[22]
    #             str_cr = df.loc[row].values[29]
    #             int_nr = df.loc[row].values[30]
    #             int_u1 = df.loc[row].values[33]
    #             int_u2 = df.loc[row].values[34]
    #             int_py = df.loc[row].values[44]
    #             str_wc = df.loc[row].values[58]
    #             str_sc = df.loc[row].values[59]
    #
    #             authors_institutes = self.get_institute(str_c1, str_af)
    #             list_institutes = []
    #             for item in authors_institutes.values():
    #                 if item not in list_institutes:
    #                     list_institutes.append(item)
    #             str_c1 = ';'.join(list_institutes)
    #             try:
    #                 with transaction.atomic():
    #                     new_article = TWoSArticle.objects.get_or_create(f_ti=str_ti,
    #                                                                     f_pt=str_pt,
    #                                                                     f_dt=str_dt,
    #                                                                     f_fu=str_fu,
    #                                                                     f_fx=str_fx,
    #                                                                     f_af=str_af,
    #                                                                     f_de=str_de,
    #                                                                     f_id=str_id,
    #                                                                     f_ab=str_ab,
    #                                                                     f_c1=str_c1,
    #                                                                     f_cr=str_cr,
    #                                                                     f_nr=int_nr,
    #                                                                     f_u1=int_u1,
    #                                                                     f_u2=int_u2,
    #                                                                     f_py=int_py,
    #                                                                     f_wc=str_wc,
    #                                                                     f_sc=str_sc,
    #                                                                     f_source_id=source_object.id)[0]
    #                     for domain in domain_objects:
    #                         new_article.f_domain.add(domain)
    #                     new_keywords = self.persist_keywords(str_de, int_py)
    #                     for keyword in new_keywords:
    #                         new_article.f_keywords.add(keyword)
    #                     new_authors, new_institutes = self.persist_authors_and_institutes(authors_institutes)
    #                     index = 0
    #                     for author in new_authors:
    #                         index += 1
    #                         TAuthorOrder.objects.update_or_create(f_author=author, f_article=new_article, f_order=index)
    #                     for institute in new_institutes:
    #                         institute.f_articles.add(new_article)
    #
    #             except Exception as e:
    #                 error = "文献 {0} 解析错误，错误原因：{1}".format(str_ti, str(e))
    #                 self._errors.append(error)
    #                 print(error)
    #
    #     except Exception as e:
    #         error = "文件 {0} 解析错误，错误原因：{1}".format(file, str(e))
    #         self._errors.append(error)
    #         print(error)

    def persist_authors_institutes(self, article):
        map_author_institute = self.get_institute(article.f_c1, article.f_af)
        list_obj_authors = []

        list_obj_institutes = []
        for key, value in map_author_institute.items():
            object_author = TWoSAuthor.objects.get_or_create(f_name=key)[0]
            list_obj_authors.append(object_author)
            for item in value:
                list_inst = item.split(',')
                object_inst = TWoSInstitute.objects.get_or_create(f_name=list_inst[0].strip())[0]
                object_inst.f_fullname = value
                object_inst.f_country = list_inst[-1]
                object_inst.save()
                object_author.f_institutes.add(object_inst)
                if object_inst not in list_obj_institutes:
                    list_obj_institutes.append(object_inst)
        return list_obj_authors, list_obj_institutes

    # def persist_authors_and_institutes(self, authors_institutes):
    #     object_authors = []
    #     object_institutes = []
    #     for key, value in authors_institutes.items():
    #         list_inst = value.split(',')
    #         object_inst = TWoSInstitute.objects.get_or_create(f_name=list_inst[0].strip())[0]
    #         object_inst.f_fullname = value
    #         object_inst.f_country = list_inst[-1]
    #         object_inst.save()
    #         object_author = TWoSAuthor.objects.get_or_create(f_name=key)[0]
    #         object_author.f_institutes.add(object_inst)
    #         object_authors.append(object_author)
    #         if object_inst not in object_institutes:
    #             object_institutes.append(object_inst)
    #
    #     return object_authors, object_institutes

    def persist_keywords(self, obj_article):
        list_keyword = obj_article.f_de.split(';')
        year = obj_article.f_py
        object_keywords = []
        for keyword in list_keyword:
            keyword = keyword.strip()
            object_keyword, created = TKeyword.objects.get_or_create(f_name=keyword)
            if created is True:
                object_keyword.f_freq = 1
                object_keyword.f_promote = year
                object_keyword.save()
            else:
                object_keyword.f_freq += 1
                object_keyword.f_promote = year if object_keyword.f_promote > year else object_keyword.f_promote
                object_keyword.save()
            object_keywords.append(object_keyword)
        return object_keywords







class CNKIPatentParser(FileParser):
    def map_author_institute(self, str_authors, str_institutes):
        dict_author_institute = {}
        list_authors = str_authors.split(";")
        list_institutes = str_institutes.split(";")
        for author in list_authors:
            if author not in dict_author_institute:
                dict_author_institute[author] = list_institutes[0]
        return dict_author_institute, list_institutes

    def persist_authors_institutes(self, obj_article):
        dict_author_institute, list_institutes = self.map_author_institute(obj_article.f_af, obj_article.f_c1)
        object_authors = []
        object_institutes = []
        for key, value in dict_author_institute.items():
            object_inst = TWoSInstitute.objects.get_or_create(f_name=value)[0]
            object_author = TWoSAuthor.objects.get_or_create(f_name=key)[0]
            object_author.f_institutes.add(object_inst)
            object_authors.append(object_author)
            if object_inst not in object_institutes:
                object_institutes.append(object_inst)
        for institute in list_institutes[1:]:
            object_inst = TWoSInstitute.objects.get_or_create(f_name=institute)[0]
            if object_inst not in object_institutes:
                object_institutes.append(object_inst)
        return object_authors, object_institutes

    def persist_keywords(self, obj_article):
        object_keywords = []
        return object_keywords


    def get_py(self, str_py):
        if str_py == '佚名':
            return 2000
        return int(str_py.split('-')[0])


    def persist_article(self, df, row, tdatasource_object):
        new_article = None
        try:
            str_af = df.loc[row].values[1]
            str_ti = df.loc[row].values[3]
            str_ab = df.loc[row].values[6]
            str_c1 = df.loc[row].values[2]
            int_py = self.get_py(df.loc[row].values[5])
            str_memo = df.loc[row].values[4] + df.loc[row].values[7]
            new_article = TWoSArticle.objects.get_or_create(f_ti=str_ti,
                                                            f_af=str_af,
                                                            f_ab=str_ab,
                                                            f_c1=str_c1,
                                                            f_py=int_py,
                                                            f_memo=str_memo,
                                                            f_source_id=tdatasource_object.id)[0]
        except Exception as e:
            error = "文献 {0} 解析失败，失败原因：{1}".format(str_ti, str(e))
            self._errors.append(error)
            print(error)
        return new_article

    # def parse_single_file(self, df):
    #     articles = []
    #     try:
    #         domain_objects = []
    #         for domain in self._params['f_domain']:
    #             domain_object = TTechDomain.objects.get_or_create(f_name=domain)[0]
    #             domain_objects.append(domain_object)
    #         source_object = TDataSource.objects.get_or_create(f_name=self._params['f_source'])[0]
    #         for row in df.index:
    #             str_af = df.loc[row].values[1]
    #             str_ti = df.loc[row].values[3]
    #             str_ab = df.loc[row].values[6]
    #             str_c1 = df.loc[row].values[2]
    #             int_py = self.get_py(df.loc[row].values[5])
    #             str_memo = df.loc[row].values[4] + df.loc[row].values[7]
    #             try:
    #                 with transaction.atomic():
    #                     new_article = TWoSArticle.objects.get_or_create(f_ti=str_ti,
    #                                                                     f_af=str_af,
    #                                                                     f_ab=str_ab,
    #                                                                     f_c1=str_c1,
    #                                                                     f_py=int_py,
    #                                                                     f_memo=str_memo,
    #                                                                     f_source_id=source_object.id)[0]
    #                     for domain in domain_objects:
    #                         new_article.f_domain.add(domain)
    #                     keywords = NLPHelper.get_keyword(str_ab)
    #                     new_keywords = self.persist_keywords(keywords, int_py)
    #                     for keyword in new_keywords:
    #                         new_article.f_keywords.add(keyword)
    #                     new_authors, new_institutes = self.persist_authors_institutes(str_af, str_c1)
    #                     index = 0
    #                     for author in new_authors:
    #                         index += 1
    #                         TAuthorOrder.objects.update_or_create(f_author=author, f_article=new_article, f_order=index)
    #                     index = 0
    #                     for institute in new_institutes:
    #                         index += 1
    #                         TInstituteOrder.objects.update_or_create(f_institute=institute, f_article=new_article, f_order=index)
    #                     articles.append(new_article)
    #             except Exception as e:
    #                 error = "文献 {0} 解析错误，错误原因：{1}".format(str_ti, str(e))
    #                 self._errors.append(error)
    #                 print(error)
    #     except Exception as e:
    #         error = "文件 {0} 解析错误，错误原因：{1}".format(df, str(e))
    #         self._errors.append(error)
    #         print(error)
    #     return articles


class ParserHelper(object):
    @staticmethod
    def parse_article_to_db(params):
        params = json.loads(s=params)
        parser = None
        if params['f_source'] == 'WoS论文':
            parser = WoSArticleParser(params)
        elif params['f_source'] == 'CNKI论文':
            parser = CNKIParser(params)
        elif params['f_source'] == 'CNKI专利':
            parser = CNKIPatentParser(params)
        new_articles = (parser.parse_articles_to_db())[0]
        with transaction.atomic():
            new_project = TProject(f_name=params['f_batchname'],
                                   f_topic=params['f_batchname'])
            new_project.save()
            for article in new_articles:
                new_project.f_aritcles.add(article)



