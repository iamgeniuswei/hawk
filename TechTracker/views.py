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
        # qs_author = TAuthor.objects.annotate(tarticle__count=Count('article_fist_author')).order_by('-tarticle__count')[:100]
        qs_author = TInstitute.objects.annotate(tarticle__count=Count('article_institutes')).order_by('-tarticle__count')[:100]
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