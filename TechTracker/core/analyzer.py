#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/23 15:52
# @Author  : Geniuswei
# @Email   : iamgeniuswei@sina.com
# @File    : analyzer.py
# @Desc    :

class CoOccuranceAnalyzer(object):
    def __init__(self):
        pass
    def analyze_cooccurance(self):
        pass

    def keyword_cooccurance(self, articles):
        co = {}
        key_dict = {}
        for article in articles:
            keywords = article.f_keywords.all()
            keywords_co = keywords
            for keyword in keywords:
                str_keyword = keyword.f_name
                if str_keyword not in key_dict:
                    key_dict[str_keyword] = 1
                else:
                    key_dict[str_keyword] += 1
                keywords_co = keywords_co[1:]
                for other in keywords_co:
                    str_other = other.f_name
                    A, B = str_keyword, str_other
                    if A > B:
                        A, B = B, A
                    co_key = A + ',' + B
                    if co_key not in co:
                        co[co_key] = 1
                    else:
                        co[co_key] += 1
        return key_dict, co





    def author_cooccurance(self, articles):
        au_dict = {}
        authors_first_dict = {}
        authors_all_dict = {}
        au_group = {}  # 两两作者合作
        for article in articles:
            try:
                list_authors = article.f_authors_str.split(',')
                first_author = list_authors[0]
                if first_author not in authors_first_dict:
                    authors_first_dict[first_author] = 1
                else:
                    authors_first_dict[first_author] += 1

                for author in list_authors:
                    pass



            except Exception as e:
                print(str(e))



            authors = article.f_other_authors.all()
            authors_str_list = []
            for author in authors:
                author_str = str(author.id)+'-'+author.f_name
                authors_str_list.append(author_str)
            for author in authors_str_list:
                if author not in au_dict:
                    au_dict[author] = 1
                else:
                    au_dict[author] += 1
                for author_co in authors_str_list[1:2]:
                    A, B = author, author_co  # 不能用本来的名字，否则会改变au自身
                    if A > B:
                        A, B = B, A  # 保持两个作者名字顺序一致
                    co_au = A + ',' + B  # 将两个作者合并起来，依然以逗号隔开
                    if co_au not in au_group:
                        au_group[co_au] = 1
                    else:
                        au_group[co_au] += 1
        return au_dict, au_group, authors_first_dict