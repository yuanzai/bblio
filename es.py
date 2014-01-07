from elasticsearch import Elasticsearch
import getDocSQLite as docdata
import re
import pprint

def index():
    print('INDEX')
    es = Elasticsearch("0.0.0.0:9200")
    es.indices.delete(index='_all')
    
    dList = docdata.getData()
    for d in dList:
        doc = {
               "filename" : d['file_name'],
               "title" : d['title'],
               "urlAddress" : d['urlAddress'],
               "text" : re.sub('</br>','  ',d['document_text']),
               }
        es.index(index="legal-index", doc_type='legaltext', id=d['id'], body=doc)
 
def search(search_term):
    es = Elasticsearch("0.0.0.0:9200")
    q = {   
            "fields" : ["title","urlAddress"],
            "size" : 20,
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
    pp = pprint.PrettyPrinter(indent=4)
    print res['hits']['total']
    pp.pprint(r)
    print len(r)
    l = []
    for re in r:
        d = {"urlAddress" : re['fields']['urlAddress'],
             "title" : re['fields']['title'],
             "id" : re['_id'],
             "score" : re['_score'],}
        try:
            d.update({"highlight" : re['highlight']['text']})
        except:
            pass
            
            
        l.append(d)
        pp.pprint(d)

    return {'result_list': l,
            'result_count': res['hits']['total']}

    """
    try:
        print "Searching"
        q = {   
            "query": {
                "query_string": {
                    "query": search_term,
                                }               
                      },
            "highlight": {
                 "fields": {
                    "text": {"fragment_size" : 150, "number_of_fragments": 5}
                        }
                    } 
             }
        res = es.search(index="legal-index", body=q)    
        print res
        r =  res['hits']['hits']
        print 'count: ' + res['hits']['total']
        l = []
        for re in r:
            d = {
                 "shorttext" : re['_source']['text'][0:300] + '...',
                 "filename" : re['_source']['filename'],
                 "urlAddress" : re['_source']['urlAddress'],
                 "title" : re['_source']['title'],
                 "highlight" : re['highlight']['text'],
                 "id" : re['_id'],
                 "score" : re['_score'],
                 }
            l.append(d)
        return {'result_list': l,
                'result_count': res['hits']['total']}
    except:
        return {'result_list':'Nothing found',
                'result_count': 0}
    pass
    """
