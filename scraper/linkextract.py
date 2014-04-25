#python imports
import sys
import os
sys.path.append('/home/ec2-user/bblio/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'build.Build.settings'
import urllib2

from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http.response.html import HtmlResponse
from spiders.spiderAll import SpiderAll


def link_extractor(url, parse_parameters='', follow_parameters='', deny_parameters='', source_allowed_domains = ''):
    print 'tree ' + url
    res = urllib2.urlopen(url)
    print(res)
    html = res.read()
    print html
    encoding=res.headers['content-type'].split('charset=')[-1]    
    r = HtmlResponse(url=url,body=html,encoding=encoding)
    print r.body 
    spider = SpiderAll(
            parse_parameters=parse_parameters, 
            follow_parameters=follow_parameters,
            deny_parameters=deny_parameters,
            source_allowed_domains=source_allowed_domains,
            source_start_urls='',
            name='tree')
    a_links = SgmlLinkExtractor(unique=True).extract_links(r)
    a_list = [link.url for link in a_links]

    print a_list
    f_links = spider.follow_link_extractor().extract_links(r)
    f_list = [link.url for link in f_links]
    p_links = spider.parse_link_extractor().extract_links(r)
    p_list = [link.url for link in p_links]
    tree_list = []
    for i,link in enumerate(a_list):
        if link in p_list:
            status='parsed'
        elif link in f_list:
            status='followed'
        else:
            status='denied'

        tree_list.append({'url':link,'allow':status,'linkno':i})
    print tree_list
    return tree_list    

