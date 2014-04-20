from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
import urllib2

class response:
    def __init__(self, body, url, encoding):
        self.body = body
        self.url = url
        self.encoding = encoding

def link_extractor(url, parse_parameters=[], follow_parameters=[], deny_parameters=[]):
    res = urllib2.urlopen(url)
    html = res.read()
    encoding=res.headers['content-type'].split('charset=')[-1]    
    
    r = response(html,url, encoding)
    links = SgmlLinkExtractor(unique=True).extract_links(r)
    tree_list = []
    for i,link in enumerate(links):
        status = 'parsed'
        if parse_parameters:
            status = 'followed'
            for p in parse_parameters:
                if p in link.url:
                    status = 'parsed'
        if follow_parameters:
            for f in follow_parameters:
                if f in link.url:
                    status = 'followed'
        if deny_parameters:
            for d in deny_parameters:
                if d in link.url:
                    status = 'denied'
        tree_list.append({'url':link.url,'allow':status,'linkno':i})
    return tree_list
