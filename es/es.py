#!/usr/bin/env python
from elasticsearch import Elasticsearch
import getdoc as docdata
import re
import pprint
import sys
sys.path.append('/home/ec2-user/bblio/build/')
sys.path.append('/home/ec2-user/bblio/aws/')
import ec2
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Build.settings'
from django.forms.models import model_to_dict
import time
import subprocess
from django.db import connection
from search.models import Document

#host = 'http://ec2-54-201-141-21.us-west-2.compute.amazonaws.com:9200'
host = str(ec2.getESip()) + ':9200'
print(host)
def restart():
    p = subprocess.Popen(["sudo", "service", "mysqld","restart"], stdout=subprocess.PIPE)
    output, err = p.communicate()
    print output
    #p = subprocess.Popen(["sudo", "service", "elasticsearch","restart"], stdout=subprocess.PIPE)
    #output, err = p.communicate()
    #print output

def clearcache():
    print('Clear Cache')
    es = Elasticsearch(host)
    es.indices.clear_cache()    

def delete():
    print('Delete Index')
    es = Elasticsearch(host)
    es.indices.delete(index='_all')    

def show():
    es = Elasticsearch(host)
    pp = pprint.PrettyPrinter(indent=4)
    data = es.indices.stats(index='legal-index')['_all']['primaries']['docs']

    pp.pprint(data)
    return data

def delete(id): 
    es = Elasticsearch(host)
    es.delete(index='legal-index',doc_type='legaltext',id=id)

def index_one(id):
    es = Elasticsearch(host)
    d = Document.object.get(pk=id)
    doc = {
            "title" : d.title,
            "urlAddress" : d.urlAddress,
            "text" : re.sub('</br>','  ',d.document_text),
            }
    es.index(index='legal-index',doc_type='legaltext',body=doc,id=id)
 
def index(n=0,end=0,k=100):
    print('INDEX')
    es = Elasticsearch(host)
    if es.indices.exists(index='legal-index'):
        print('index found!')
    
    if end == 0:
        doc_count = Document.objects.count()
    else:
        doc_count = end
    while True:
        if n > doc_count:
            dList = Document.objects.all()[n:doc_count]
        else:
            dList = Document.objects.all()[n:int(n)+k]
        print(n) 
        docs = []
        for d in dList:
            header = { "index" : { "_index" : "legal-index", "_type" : "legaltext", "_id" : d.id } }

            doc = {
                   "title" : d.title,
                   "urlAddress" : d.urlAddress,
                   "text" : re.sub('</br>','  ',d.document_text),
                   }
            docs.append(header)
            docs.append(doc)
        es.bulk(body=docs,index='legal-index', doc_type='legaltext')

        time.sleep(1)
        n =n + k
        if n % 2000 == 0:
            dList = None
            es.indices.clear_cache(index='legal-index')
        if n >= doc_count:
            break

def search(search_term,result,start_result=0):
    es = Elasticsearch(host)
    q = {   
            "fields" : ["title","urlAddress","text"],
            "from" : start_result,
            "size" : result,
            "query": {
                "query_string": {
                    "query": search_term,
                                }               
                      },
            "highlight": {
                 "fields": {
                    "text": {"fragment_size" : 100, "number_of_fragments": 5}
                        }
                    } 
             }
    res = es.search(index="legal-index", body=q)    
    r =  res['hits']['hits']
    l = []
    for re in r:
        d = {"urlAddress" : re['fields']['urlAddress'],
             "title" : str(re['fields']['title'][3:-2].decode('utf-8')),
             "id" : re['_id'],
             "score" : re['_score'],}
        if d['title'] == '':
            d['title'] = d['urlAddress']
        try:
            d.update({"highlight" : re['highlight']['text']})
        except:
            pass

        l.append(d)
    return {'result_list': l,
            'result_count': res['hits']['total']}


if __name__ == '__main__':
    arg = sys.argv
    if len(sys.argv) > 1:
        if arg[1] == 'index':
            index(int(arg[2]),int(arg[3]),int(arg[4]))
        elif arg[1] == 'search':
            search(arg[2],10)
        elif arg[1] == 'delete':
            delete()
        elif arg[1] == 'clear':
            clearcache()
        elif arg[1] == 'show':
            show()
        elif arg[1] == 'restart':
            restart()
        else:
            print('Wrong arguments enter')
    else:
        print(search('hello',2))
