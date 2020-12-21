#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/23 15:52
# @Author  : Geniuswei
# @Email   : iamgeniuswei@sina.com
# @File    : analyzer.py
# @Desc    :

from ..models import *
from django.db.models import Q
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

class Analyzer(object):
    def __init__(self):
        self.errors = []


class CoAnalyzer(Analyzer):
    def __init__(self):
        Analyzer.__init__(self)
        self.analyzer = {
            1: self.co_author,
            2: self.co_institute,
            3: self.co_keyword
        }


    def coourrance(self, new_to_co:list, nodes: dict, links: dict):
        other_items = new_to_co
        for item in new_to_co:
            if item not in nodes:
                nodes[item] = 1
            else:
                nodes[item] += 1
            other_items = other_items[1:]
            for other in other_items:
                A, B = item, other
                if A > B:
                    A, B = B, A
                key = A + ',' + B
                if key not in links:
                    links[key] = 1
                else:
                    links[key] += 1


    def get_articles(self, params):
        articles = None
        try:
            filter_source = params['f_source']
            filter_domain = params['f_domain']
            filter_start = params['f_start']
            filter_end = params['f_end']
            if filter_domain.count() == 0:
                articles = TWoSArticle.objects.filter(f_py__range=(filter_start, filter_end),
                                                      f_source_id=filter_source.id)
            else:
                articles = TWoSArticle.objects.filter(f_py__range=(filter_start, filter_end),
                                                      f_source_id=filter_source.id, f_domain__in=filter_domain)
        except Exception as e:
            error = "获取成果数据出现错误，错误原因：{0}".format(str(e))
            self.errors.append(error)
        return articles

    def co_author(self, articles, params):
        nodes = {}
        links = {}
        for article in articles:
            try:
                list_authors = article.f_af.split(';')
                list_authors = [author.strip() for author in list_authors]
                self.coourrance(list_authors, nodes, links)
            except Exception as e:
                error = "成果 {0} 作者共现分析出现错误，错误原因：{0}".format(article.f_ti, str(e))
                self.errors.append(error)
        return nodes, links



    def co_institute(self, articles, params):
        nodes = {}
        links = {}
        for article in articles:
            try:
                list_institutes = article.f_c1.split(';')
                list_institutes = [(institute.split(',')[0]).strip() for institute in list_institutes]
                self.coourrance(list_institutes, nodes, links)
            except Exception as e:
                error = "成果 {0} 机构共现分析出现错误，错误原因：{0}".format(article.f_ti, str(e))
                self.errors.append(error)
        return nodes, links

    def co_keyword(self, articles, params):
        nodes = {}
        links = {}
        for article in articles:
            try:
                list_keywords = article.f_de.title().split(';')
                list_keywords = [keyword.strip() for keyword in list_keywords]
                self.coourrance(list_keywords, nodes, links)
            except Exception as e:
                error = "成果 {0} 热点共现分析出现错误，错误原因：{0}".format(article.f_ti, str(e))
                self.errors.append(error)
        return nodes, links


    def co_analysis(self, params:dict):
        nodes = {}
        links = {}
        try:
            articles = self.get_articles(params)
            if articles is None:
                return nodes, links, self.errors
            nodes, links = self.analyzer.get(params['f_object'])(articles, params)
            return nodes, links
        except Exception as e:
            error = "共现分析出现错误，错误原因：{0}".format(str(e))
            self.errors.append(error)





def analyze_topn(params: dict):
    if params['f_object'] == 1:
        analyzer = TopAnalyzerForResearcher()
        return analyzer.topn(params)
    elif params['f_object'] == 2:
        analyzer = TopAnalyzerForInstitute()
        return analyzer.topn(params)
    elif params['f_object'] == 3:
        analyzer = TopAnalyzerForKeyword()
        return analyzer.topn(params)



class TopAnalyzer(Analyzer):
    def __init__(self):
        Analyzer.__init__(self)
        self.authors_anlyzer = {
            'FIRST': self.topn_author_first,
            'ALL': self.topn_author_all
        }
        self.institutes_anlyzer = {
            'FIRST': self.topn_institutes_first,
            'ALL': self.topn_institutes_all
        }
        self.object_anlyzer = {
            '研究人员': self.topn_authors,
            '研究机构': self.topn_institutes,
            '研究热点': self.topn_keywords
        }

    def dict_to_list_in_order(self, unorder_dict):
        order_list = sorted(unorder_dict.items(), key=lambda x:x[1], reverse=True)
        key_list = []
        value_list = []
        [(key_list.append(item[0]),value_list.append(item[1])) for item in order_list]
        return key_list, value_list

    def default_anlyzer(self):
        ret = {}
        return ret

    def topn_in_cnki(self, articles):
        first_authors_dict = {}
        all_authors_dict = {}
        for article in articles:
            try:
                list_authors= article.f_authors_str.split(',')
                first_author = list_authors[0]
                if first_author not in first_authors_dict:
                    first_authors_dict[first_author] = 1
                else:
                    first_authors_dict[first_author] += 1

                for author in list_authors:
                    if author not in all_authors_dict:
                        all_authors_dict[author] = 1
                    else:
                        all_authors_dict[author] += 1
            except Exception as e:
                error = "{0} 分析错误，错误原因：{1}".format(article.f_name, str(e))
                print(error)
        return first_authors_dict, all_authors_dict

    def topn_author_first(self, articles):
        authors_dict = {}
        for article in articles:
            try:
                obj_author = TAuthorOrder.objects.get(f_article=article, f_order=1).f_author
                first_author = obj_author.f_name
                if first_author not in authors_dict:
                    authors_dict[first_author] = 1
                else:
                    authors_dict[first_author] += 1
            except Exception as e:
                error = "文献{0} 分析错误，错误原因：{1}".format(article.f_ti, str(e))
                print(error)
        return authors_dict

    def topn_author_all(self, articles):
        authors_dict = {}
        for article in articles:
            try:
                qs_author = article.f_authors.all()
                for author in qs_author:
                    str_author = author.f_name
                    if str_author not in authors_dict:
                        authors_dict[str_author] = 1
                    else:
                        authors_dict[str_author] += 1
            except Exception as e:
                error = "文献{0} 分析错误，错误原因：{1}".format(article.f_ti, str(e))
                print(error)
        return authors_dict

    def topn_institutes_first(self, articles):
        institutes_dict = {}
        for article in articles:
            try:
                list_institutes = article.f_c1.split(';')
                first_institutes = list_institutes[0].strip()
                institute = (first_institutes.split(',')[0]).strip()
                if institute not in institutes_dict:
                    institutes_dict[institute] = 1
                else:
                    institutes_dict[institute] += 1
            except Exception as e:
                error = "文献{0} 分析错误，错误原因：{1}".format(article.f_ti, str(e))
                print(error)
        return institutes_dict

    def topn_institutes_all(self, articles):
        institutes_dict = {}
        for article in articles:
            try:
                list_institutes = article.f_institutes.all()
                for institute in list_institutes:
                    str_institute = institute.f_name
                    if str_institute not in institutes_dict:
                        institutes_dict[str_institute] = 1
                    else:
                        institutes_dict[str_institute] += 1
            except Exception as e:
                error = "文献{0} 分析错误，错误原因：{1}".format(article.f_ti, str(e))
                print(error)
        return institutes_dict

    def topn_institutes(self, articles, index):
        institutes_dict = self.institutes_anlyzer.get(index)(articles)
        return institutes_dict

    def topn_authors(self, articles, index):
        authors_dict = self.authors_anlyzer.get(index)(articles)
        return authors_dict

    def topn_keywords(self, articles, index):
        keywords_dict = {}
        for article in articles:
            try:
                list_keywords = article.f_de.title().split(';')
                for keyword in list_keywords:
                    keyword = keyword.strip()
                    if keyword not in keywords_dict:
                        keywords_dict[keyword] = 1
                    else:
                        keywords_dict[keyword] += 1
            except Exception as e:
                error = "文献{0} 分析错误，错误原因：{1}".format(article.f_ti, str(e))
                print(error)
        return keywords_dict


    def topn(self, param:dict):
        topn = param['f_top']
        object = (param['f_object']).f_object
        if object == 1:
            object = 'AUTHOR'
        elif object == 2:
            object = 'INSTITUTE'
        elif object == 3:
            object = 'KEYWORD'
        index = param['f_index'].f_abbrv
        filter_source = param['f_source']
        filter_domain = param['f_domain']
        if filter_domain.count() == 0:
            articles = TWoSArticle.objects.filter(f_py__range=(param['f_start'], param['f_end']), f_source__in=filter_source)
        else:
            articles = TWoSArticle.objects.filter(f_py__range=(param['f_start'], param['f_end']), f_source__in=filter_source, f_domain__in=filter_domain)

        ret_dict = self.object_anlyzer.get(object)(articles, index)

        name, amount = self.dict_to_list_in_order(ret_dict)
        return name[:topn], amount[:topn], articles.count()


class TopAnalyzerForResearcher(TopAnalyzer):
    def __init__(self):
        TopAnalyzer.__init__(self)
        self.authors_anlyzer = {
            'FIRST':self.topn_author_first,
            'ALL': self.topn_author_all
        }
        self.institutes_anlyzer = {
            'FIRST': self.topn_institutes_first,
            'ALL':self.topn_institutes_all
        }
        self.object_anlyzer = {
            'AUTHOR': self.topn_authors,
            'INSTITUTE': self.topn_institutes,
        }

    def default_anlyzer(self):
        ret = {}
        return ret

    def topn_in_cnki(self, articles):
        first_authors_dict = {}
        all_authors_dict = {}
        for article in articles:
            try:
                list_authors= article.f_authors_str.split(',')
                first_author = list_authors[0]
                if first_author not in first_authors_dict:
                    first_authors_dict[first_author] = 1
                else:
                    first_authors_dict[first_author] += 1

                for author in list_authors:
                    if author not in all_authors_dict:
                        all_authors_dict[author] = 1
                    else:
                        all_authors_dict[author] += 1
            except Exception as e:
                error = "{0} 分析错误，错误原因：{1}".format(article.f_name, str(e))
                print(error)
        return first_authors_dict, all_authors_dict

    def topn_author_first(self, articles):
        authors_dict = {}
        for article in articles:
            try:
                list_authors= article.f_af.split(';')
                first_author = list_authors[0].strip()
                if first_author not in authors_dict:
                    authors_dict[first_author] = 1
                else:
                    authors_dict[first_author] += 1
            except Exception as e:
                error = "文献{0} 分析错误，错误原因：{1}".format(article.f_ti, str(e))
                print(error)
        return authors_dict

    def topn_author_all(self, articles):
        authors_dict = {}
        for article in articles:
            try:
                list_authors = article.f_af.split(';')
                for author in list_authors:
                    author = author.strip()
                    if author not in authors_dict:
                        authors_dict[author] = 1
                    else:
                        authors_dict[author] += 1
            except Exception as e:
                error = "文献{0} 分析错误，错误原因：{1}".format(article.f_ti, str(e))
                print(error)
        return authors_dict

    def topn_institutes_first(self, articles):
        institutes_dict = {}
        for article in articles:
            try:
                list_institutes = article.f_c1.split(';')
                first_institutes = list_institutes[0].strip()
                institute = (first_institutes.split(',')[0]).strip()
                if institute not in institutes_dict:
                    institutes_dict[institute] = 1
                else:
                    institutes_dict[institute] += 1
            except Exception as e:
                error = "文献{0} 分析错误，错误原因：{1}".format(article.f_ti, str(e))
                print(error)
        return institutes_dict

    def topn_institutes_all(self, articles):
        institutes_dict = {}
        for article in articles:
            try:
                list_institutes = article.f_c1.split(';')
                for institute in list_institutes:
                    institute = (institute.split(',')[0]).strip()
                    if institute not in institutes_dict:
                        institutes_dict[institute] = 1
                    else:
                        institutes_dict[institute] += 1
            except Exception as e:
                error = "文献{0} 分析错误，错误原因：{1}".format(article.f_ti, str(e))
                print(error)
        return institutes_dict

    def topn_institutes(self, articles):
        pass

    def topn_authors(self, articles, index):
        authors_dict = self.authors_anlyzer.get(index)(articles)
        return authors_dict

    def topn(self, param:dict):
        topn = param['f_top']
        object = param['f_object']
        if object == 1:
            object = 'AUTHOR'
        elif object == 2:
            object = 'INSTITUTE'
        index = param['f_index'].f_abbrv
        filter_source = param['f_source']
        filter_domain = param['f_domain']
        if filter_domain.count() == 0:
            articles = TWoSArticle.objects.filter(f_py__range=(param['f_start'], param['f_end']), f_source_id=filter_source.id)
        else:
            articles = TWoSArticle.objects.filter(f_py__range=(param['f_start'], param['f_end']), f_source_id=filter_source.id, f_domain__in=filter_domain)

        ret_dict = self.object_anlyzer.get(object, default=self.default_anlyzer)(articles, index)

        name, amount = self.dict_to_list_in_order(ret_dict)
        return name[:topn], amount[:topn], articles.count()



class TopAnalyzerForInstitute(TopAnalyzer):
    def __init__(self):
        TopAnalyzer.__init__(self)

    def topn_in_cnki(self, articles):
        all_institutes_dict = {}
        for article in articles:
            try:
                list_institutes = article.f_institutes_str.split(',')
                for institute in list_institutes:
                    if institute not in all_institutes_dict:
                        all_institutes_dict[institute] = 1
                    else:
                        all_institutes_dict[institute] += 1
            except Exception as e:
                error = "{0} 分析错误，错误原因：{1}".format(article.f_name, str(e))
                print(error)
        return all_institutes_dict

    def topn(self, param:dict):
        articles = TArticle.objects.all()
        topn = param['f_top']
        if param['f_source'].f_name == 'CNKI':
            all_institutes_dict = self.topn_in_cnki(articles)
            all_institutes_name, all_institutes_amount = self.dict_to_list_in_order(all_institutes_dict)
            return all_institutes_name[:topn], all_institutes_amount[:topn]
        return None

class TopAnalyzerForKeyword(TopAnalyzer):
    def __init__(self):
        TopAnalyzer.__init__(self)

    def topn_analysis(self, articles):
        all_keywords_dict = {}
        for article in articles:
            try:
                list_keywords = article.f_keywords_str.split(',')
                for keyword in list_keywords:
                    if keyword not in all_keywords_dict:
                        all_keywords_dict[keyword] = 1
                    else:
                        all_keywords_dict[keyword] += 1
            except Exception as e:
                error = "{0} 分析错误，错误原因：{1}".format(article.f_name, str(e))
                print(error)
        return all_keywords_dict

    def topn(self, param:dict):
        articles = TArticle.objects.all()
        topn = param['f_top']
        all_keywords_dict = self.topn_analysis(articles)
        all_keywords_name, all_keywords_amount = self.dict_to_list_in_order(all_keywords_dict)
        return all_keywords_name[:topn], all_keywords_amount[:topn]
