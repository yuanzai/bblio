from django.shortcuts import render, get_object_or_404
from models import Document
import es
import re
import sqlite
from django.http.response import HttpResponse
from lib2to3.fixer_util import Newline

def index(request):
    #sqlite.populateSites('/Users/yuanzai/Google Drive/bblio/Development Code/Scrapy/tutorial/CrawledText/')
    #es.index()
    try:
        context = es.search(str(request.POST['search_term']))
    except:
        context = {}
    context.update({'count' : Document.objects.count()})
    return render(request, 'search/index.html',context)

def create(request):
    print 'create'
    
    sqlite.populateSites('/Users/yuanzai/Google Drive/bblio/Development Code/Scrapy/tutorial/CrawledText/')
    es.index()

    context = {}
    context.update({'count' : Document.objects.count()})
    return render(request, 'search/index.html',context)
    

def result(request, key_id):
    d = get_object_or_404(Document, pk=key_id)
    return HttpResponse(d.document_text)
    