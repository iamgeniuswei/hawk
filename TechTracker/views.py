import json

from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from .forms import *
from .core.file_to_article_parser import *
from django.db.models import Count
import pandas as pd
def index(request):
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
        parser.parse_files_to_articles()
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


        return render(request, 'TechTracker/topn.html', locals())
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

        return render(request, 'TechTracker/cokeyword.html', locals())
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