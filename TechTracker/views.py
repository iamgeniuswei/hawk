import json

from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError, JsonResponse
# Create your views here.
from .forms import *

from .core.file_to_article_parser import *
from django.db.models import Count, Max
import pandas as pd
from .core.analyzer import *
import math
from .tasks import *
def index(request):
    res = test_task.delay(1, 3)
    print(res.task_id)
    return render(request, 'TechTracker/index.html')

def cnki(request):
    return render(request, 'TechTracker/cnki.html')

def project(request):
    form_project = FProject()
    return render(request, 'TechTracker/project.html', locals())

def analyze(request):
    try:
        project = FProject(request.POST)
        if project.is_valid():
            new_project = project.save(commit=True)
            new_project.save()

        file = "F:/Project/hawk/data"
        parser = CNKIParser('CNKI', file)
        parser.parse_articles_to_db()
        print('All is Done')
    except Exception as e:
        print(str(e))

def get_top_n(request):
    try:
        authors = []
        amounts = []
        qs_author = TAuthor.objects.annotate(tarticle__count=Count('article_fist_author')).order_by('-tarticle__count')[:100]
        # qs_author = TInstitute.objects.annotate(tarticle__count=Count('article_institutes')).order_by('-tarticle__count')[:100]
        for item in qs_author:
            authors.append(item.f_name)
            amounts.append(item.tarticle__count)


        return render(request, 'TechTracker/page_topn.html', locals())
    except Exception as e:
        print(str(e))


def html_author_keywords(request):
    try:
        categories = ['作者', '关键词']
        nodes_dict = {}
        links = []
        co = dict()
        author = TAuthor.objects.get(f_name='武传坤')
        author_dict = {}
        author_dict['name'] = author.f_name
        author_dict['category'] = 0
        nodes_dict[author.f_name] = author_dict
        articles = author.article_fist_author.all()
        for article in articles:
            keywords = article.f_keywords.all()
            for keyword in keywords:
                if keyword.f_name not in nodes_dict.keys():
                    node_dict = {}
                    node_dict['name'] = keyword.f_name
                    node_dict['category'] = 1
                    nodes_dict[keyword.f_name] = node_dict
                key = author.f_name + '-' + keyword.f_name
                if key not in co.keys():
                    temp = dict()
                    temp['source'] = author.f_name
                    temp['target'] = keyword.f_name
                    co[key] = temp

        nodes = list(nodes_dict.values())
        links = list(co.values())



        return render(request, 'TechTracker/cooccurance.html', locals())
    except Exception as e:
        print(str(e))

def html_author_co(request):
    try:
        articles = TArticle.objects.all()
        co = CoOccuranceAnalyzer()
        au_dict, au_group, test = co.author_cooccurance(articles)
        nodes = []
        links = []
        for au,value in au_dict.items():
            tmp = {'name': au,
                   'value': value}

            nodes.append(tmp)
        for au_co in au_group.keys():
            co = au_co.split(',')
            tmp = {'source': co[0],
                   'target': co[1],}
            links.append(tmp)

        return render(request, 'TechTracker/coauthor.html', locals())
    except Exception as e:
        print(str(e))

import networkx as nx
def bet(au_group):
    g = nx.Graph()
    for key, value in au_group.items():
        src_dst = key.split(',')
        g.add_edge(src_dst[0], src_dst[1])
    score = nx.betweenness_centrality(g)
    score = sorted(score.items(), key=lambda item: item[1], reverse=True)
    print(score)



def html_keyword_co(request):
    try:
        articles = TArticle.objects.all()
        co = CoOccuranceAnalyzer()
        key_dict, key_co = co.keyword_cooccurance(articles)
        nodes = []
        links = []
        for au, value in key_dict.items():
            if value < 3:
                continue
            if value > 5:
                category = 1
            else:
                category = 0
            tmp = {'name': au,
                   'value': value,
                   'category': category}

            nodes.append(tmp)
        for au_co, value in key_co.items():
            co = au_co.split(',')
            if key_dict[co[1]] < 3 or key_dict[co[0]] < 3:
                continue
            tmp = {'source': co[0],
                   'target': co[1],
                   'value': value}
            links.append(tmp)

        return render(request, 'TechTracker/html_co.html', locals())
    except Exception as e:
        print(str(e))


def html_author_info(request):
    try:
        articles = TArticle.objects.all()
        co = CoOccuranceAnalyzer()
        au_dict, au_group, first_dict = co.author_cooccurance(articles)
        data = [{'name': 'afaf', 'value': 1}, {'name': 'afafasfasf', 'value': 2}]
        bet(au_group)
        return render(request, 'TechTracker/table.html', locals())
    except Exception as e:
        print(str(e))




def html_topn_config(request):
    try:
        form_topn_params = FTopAnalysisParams()
        return render(request, 'TechTracker/html_topn_config.html', locals())
    except Exception as e:
        print(str(e))

def remove_node(request):
    try:
        pass
    except Exception as e:
        print(str(e))

topn_object_dict = {
    1 : '研究人员',
    2 : '研究机构',
    3 : '研究热点'
}

def html_topn(request):
    try:
        form_topn_params = FTopAnalysisParams(request.POST)
        if form_topn_params.is_valid():
            topn = form_topn_params.cleaned_data['f_top']
            topn_object = form_topn_params.cleaned_data['f_object']
            topn_index = form_topn_params.cleaned_data['f_index'].f_index
            anlyzer = TopAnalyzer()
            names, amounts, article_count = anlyzer.topn(form_topn_params.cleaned_data)
            nodes = []
            for name, amount in zip(names, amounts):
                tmp = {
                    'name': name,
                    'value': amount
                }
                nodes.append(tmp)
            return render(request, 'TechTracker/page_topn.html', locals())
        else:
            return HttpResponseServerError()
    except Exception as e:
        print(str(e))


def html_topn_embed(request):
    try:
        form_topn_params = FTopAnalysisParams(request.POST)
        if form_topn_params.is_valid():
            topn = form_topn_params.cleaned_data['f_top']
            topn_title = form_topn_params.cleaned_data['f_index'].f_index
            names, amounts, article_count = analyze_topn(form_topn_params.cleaned_data)
            return render(request, 'TechTracker/html_topn_embed.html', locals())
        else:
            return HttpResponseServerError()
    except Exception as e:
        print(str(e))


def html_node_detail(request):
    try:
        name = request.POST['name']
        object = request.POST['object']
        count = int(request.POST['count'])
        if object == '研究人员':
            authors = TWoSAuthor.objects.filter(f_name=name)
            form_author = FWosAuthor(instance=authors[0])
            author = authors[0]
            articles = author.f_articles.all()
            institutes = author.f_institutes.all()
            return render(request, 'TechTracker/html_author_detail.html', locals())
        elif object == '研究机构':
            institutes = TWoSInstitute.objects.filter(f_name=name)
            form_institute = FWosInstitute(instance=institutes[0])
            institute = institutes[0]
            articles = institute.f_articles.all()
            year_articles = articles.values('f_py').annotate(num_py=Count('f_py'))
            return render(request, 'TechTracker/html_institute_detail.html', locals())
        elif object == '研究热点':
            keywords = TKeyword.objects.filter(f_name=name)
            keyword = keywords[0]
            form_keyword = FKeyword(instance=keyword)
            articles = keyword.wosarticle_keywords.all().order_by('-f_py')
            return render(request, 'TechTracker/html_keyword_detail.html', locals())


    except Exception as e:
         print(str(e))



def html_co_config(request):
    try:
        form_co_params = FCoAnalysisParams()
        return render(request, 'TechTracker/html_co_config.html', locals())
    except Exception as e:
        print(str(e))


def html_co(request):
    try:
        form_co_params = FCoAnalysisParams(request.POST)
        if form_co_params.is_valid():
            co = CoAnalyzer()
            nodes_dict, links_dict = co.co_analysis(form_co_params.cleaned_data)
            nodes = []
            links = []
            categories = []
            index = 0
            category = 0
            length = len(nodes_dict.items())
            nodes_sorted = sorted(nodes_dict.items(), key=lambda x:x[1], reverse=True)
            for item in nodes_sorted:
                category = math.ceil(index/length*10)
                tmp = {'name': item[0],
                       'value': item[1],
                       'category': category}
                nodes.append(tmp)
                index += 1
            for key, value in links_dict.items():
                co = key.split(',')
                tmp = {'source': co[0],
                       'target': co[1],
                       'value': value}
                links.append(tmp)
            for i in range(category):
                if i == 0:
                    categories.append({'name': 'MAX'})
                else:
                    categories.append({'name': "TOP %" + str(i/category)})

            return render(request, 'TechTracker/html_co.html', locals())
    except Exception as e:
        print(str(e))


def html_config_parser(request):
    try:
        if request.method == 'GET':
            form_params = FParserParams()
            form_domains = FTechDomain()
            form_source = FDataSource()
            return render(request, 'TechTracker/html_parser_config.html', locals())
        elif request.method == 'POST':
            form_params = FParserParams(request.POST)

            # 为了将任务提交至celery后台执行，必须将参数转换成json格式
            if form_params.is_valid():
                params = {}
                params['f_path'] = form_params.cleaned_data['f_path'].strip('"')
                params['f_source'] = form_params.cleaned_data['f_source'].f_name
                params['f_batchname'] = form_params.cleaned_data['f_batchname']
                domains = list()
                for domain in form_params.cleaned_data['f_domain']:
                    domains.append(domain.f_name)
                if len(domains) > 0:
                    params['f_domain'] = domains
                params = json.dumps(params)
                try:
                    ParserHelper.parse_article_to_db(params)
                    return render(request, 'TechTracker/html_parser_status.html', locals())
                except Exception as e:
                    print(str(e))
                return render(request, 'TechTracker/html_parser_status.html', locals())
            else:
                pass

    except Exception as e:
        print(str(e))


def json_persist_domain(request):
    form_domains = FTechDomain(request.POST)
    if form_domains.is_valid():
        new_entry = form_domains.save(commit=False)
        new_entry.save()
        return JsonResponse({'flag': True, 'id':new_entry.id}, safe=False)


def json_data_clean(request):
    try:
        type = request.POST['type']
        to_clean = request.POST.getlist('to_clean')
        if type == 'discard':
            for item in to_clean:
                keyword = TKeyword.objects.get(f_name=item)
                articles = keyword.wosarticle_keywords.all().order_by('-f_py')
                articles.f_keywords.remove(keyword)
                keyword.delete()
        elif type == 'merge':
            pass
    except Exception as e:
        print(str(e))