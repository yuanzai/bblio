from django.shortcuts import render, get_object_or_404
from models import Document, Site
import es
import re
import sqlite
from lib2to3.fixer_util import Newline
from django.http import HttpResponseRedirect, HttpResponse, Http404

def index(request):
    try:
        context = es.search(str(request.POST['search_term']))
    except:
        context = {}
    context.update({'count' : Document.objects.count()})
    return render(request, 'search/index.html',context)

def delete(request, site_id):
    if not request.user.is_staff:
        raise Http404
    else:
        Document.objects.filter(site_id=int(site_id)).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

"""
def scrape(request):
    output = 
    s = Site.objects.all()
"""

def scraped(request, site_id):
    d = Document.objects.filter(site_id=site_id)
    output = '<br>'.join([doc.urlAddress for doc in d])
    return HttpResponse(output)

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

def testscrape(request):
    return render(request, 'search/testscrape.html')    
