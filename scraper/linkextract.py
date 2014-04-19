from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
import urllib2

class response:
    def __init__(self, body, url, encoding):
        self.body = body
        self.url = url
        self.encoding = encoding

def link_extractor(url, allowP=[], denyP=[], allowF=[], denyF=[]):
    res = urllib2.urlopen(url)
    html = res.read()
    encoding=res.headers['content-type'].split('charset=')[-1]    
    
    r = response(html,url, encoding)
    links = SgmlLinkExtractor(unique=True).extract_links(r)
    tree_list = []
    for i,link in enumerate(links):
        status = 'denied'
        if allowP:
            for a in allowP:
                if a in link.url:
                    status = 'parsed'
        else:
            status = 'parsed'
        if denyP:
            for a in denyP:
                if a in link.url:
                    status = 'denied'
        if status == 'denied':
            if allowF:
                for a in allowF:
                    if a in link.url:
                        status = 'followed'
            else:
                status = 'followed'
            if denyF:
                for a in denyF:
                    if a in link.url:
                        status = 'denied'
        tree_list.append({'url':link.url,'allow':status,'linkno':i})
    return tree_list
