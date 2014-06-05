#base class import
from BaseESController import BaseESController

#pdf import
from PDFController import PDFController

#python imports
import re
from lxml import etree
from io import StringIO, BytesIO

#djang imports
from search.models import Site

class YTHESController(BaseESController):
    _es_index = "yth-index"
    _doc_type = "yth-doc"
    _xpath =  "body/descendant-or-self::*[not(self::script|self::link)]"

    def search_raw_result(self, search_term, jurisdiction = [],
            results_per_page=10,
            current_page=1):
        query = {}
        
        
        #searching component
        
        q = {
                #fields to return in the ES request
                "fields" : ["title","text","urlAddress"], 

                #start result - from 0
                "from" : (int(current_page) - 1) * results_per_page,
                "size" : results_per_page,
                "min_score": 0.1,
                "query": {
                    "query_string": {
                        "default_field" : "text",
                        "query": search_term,
                                    }
                          }
                }
        query.update(q)

        #highlights - ie the summarised data in the search result
        h = {
                "pre_tags" : ["<b>"],
                "post_tags" : ["</b>"],
                "fields": {
                    "text": {
                        "fragment_size" : 150,
                        "number_of_fragments": 4,
                        "no_match_size": 150,
                        "highlight_query": {
                            "query_string":{
                                "default_field" : "text",
                                "query":search_term.replace('"','')
                            }
                        }
                    }
                }
            }
        query.update({"highlight" : h})
        
        #suggestion - ie did you mean
        s = {
                "text" : search_term,
                "simple_phrase" : {
                    "phrase" : {
                        "field" : "text",
                        "size" : 1,
                        "real_word_error_likelihood" : 0.95,
                        "max_errors" : 0.5,
                        "gram_size" : 2,
                        "direct_generator" : [ {
                            "field" : "text",
                            "suggest_mode" : "popular",
                            "min_word_len" : 1,
                            "min_doc_freq" : 0.01,
                            "max_term_freq" : 0.01
                        } ]
                    }
                }
            }

        query.update({"suggest" : s})

        #filters - currently for jurisdiction as of now
        f = {
                "term": {
                    "jurisdiction": jurisdiction
                }
            }
        if jurisdiction: query.update({"filter" : f })
        return self._es.search(index=self._es_index, body=query)
    
    def search(self, search_term, jurisdiction = [],
            results_per_page=10,
            current_page=1):

        res = self.search_raw_result(search_term,jurisdiction , results_per_page, current_page)
        print res
        result = {}
        """
        takes the raw return from elastic search and handles the suggestions
        """
        try:
            suggested =res['suggest']['simple_phrase'][0] \
                    ['options'][0]['text'].encode('utf-8')
            
            #suggestion
            result.update({'suggestion': suggested})

            #suggestion URL
            result.update({'suggestion_urlencode': urllib.quote(suggested)})
        except:
            pass

        """
        takes the raw return from ES and handles the hit results and highlights
        """
        l = []
        for re in res['hits']['hits']:
            d = {"urlAddress" : re['fields']['urlAddress'],
                 "id" : re['_id'],
                 "score" : re['_score'],}
           
            try:
                d.update({"title": re['fields']['title']})
            except:
                d.update({"title": d['urlAddress']})

            try:
                h_list = []
                for h in re['highlight']['text']:
                    h_list.append(h)

                d.update({"highlight" : h_list})
            except:
                pass
            l.append(d)

        """
        total count
        """

        result_count = res['hits']['total']
        if not result_count:
            result_count = 0

        result.update({'result_list' : l})
        result.update({'result_count' : result_count})

        return result

    def index_one_doc(self, Document):
        if not self._es.indices.exists(index=self._es_index):
            self._es.indices.create(index=self._es_index,body=self.get_mapping())
        
        doc = self.get_doc(Document)
        return self._es.index(
                index=self._es_index,
                doc_type=self._doc_type,
                body=doc,
                id=Document.id)

    def get_doc(self, Document):
        site = Site.objects.get(pk=Document.site_id)
        doc = {
                "urlAddress" : Document.urlAddress,
                "jurisdiction" : site.jurisdiction,
                "site_id" : site.id
        }
 
        if Document.encoding == 'PDF':
            pdf = PDFController()
            doc.update({
                "title" : Document.urlAddress,
                "text" : pdf.get_string(Document.document_html),
                })
        else:
            doc.update({
                "title" : self.title_parse(Document.document_html),
                "text" : ' '.join(self.text_parse(Document.document_html)),
                })
        return doc
    
    def get_tree(self, text):
        text = re.sub('<strong>','',text)
        text = re.sub('</strong>','',text)
        text = re.sub('\n','',text)
        text = re.sub('\t','',text)
        text = re.sub(r'\s+',' ',text)
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(text.encode('utf-8').decode('utf-8')), parser)
        return tree

    def get_body_html(self, text):
        tree = self.get_tree(text)
        result = tree.xpath(self._xpath)
        body = []
        for s in result:
            body.append(etree.tostring(s))
        return '\n'.join(body)

    def title_parse(self, text):
        tree = self.get_tree(text)
        try:
            return tree.xpath("title/text()")[0]
        except:
            return

    def text_parse(self, text):
        tree = self.get_tree(text)
        result = tree.xpath(self._xpath + "/text()")
        return result

    def get_mapping(self):
        m = {
                "mappings":{
                    self._doc_type:{
                        "properties":{
                            "text":{
                                "type":"string",
                                "analyzer":"my_analyzer"
                                },
                            "jurisdiction":{
                                "type" : "string",
                                "index" : "not_analyzed"
                                },
                            "site_id":{
                                "type" : "long",
                                "index" : "not_analyzed"
                                }
                            }
                        }
                    },
                "settings":{
                    "index":{
                        "analysis" : {
                            "analyzer":{
                                "my_analyzer":{
                                    "tokenizer": "standard",
                                    "filter":["standard","lowercase","porter_stem","filter1"],
                                    },
                                },
                            "filter" : {
                                "filter1": {
                                    "type":"shingle",
                                    "min_shingle_size":2,
                                    "max_shingle_size":4,
                                    "output_unigrams":"true",
                                    },
                                },
                            }
                        }
                    }
                }

        return m

