#python imports
import sys
import os
#sys.path.append('/home/ec2-user/bblio/')
#os.environ['DJANGO_SETTINGS_MODULE'] = 'build.Build.settings'
import urllib2
import chardet

from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http.response.html import HtmlResponse
from scraper.deployable.deployable.spiders.spiderAll import SpiderAll

import re     
from urlparse import urlparse


def link_extractor(url, parse_parameters='', follow_parameters='', deny_parameters='', source_allowed_domains = ''):
    print source_allowed_domains
    res = urllib2.urlopen(url)
    html = res.read()

    if 'charset' in res.headers['content-type']:
        encoding = res.headers['content-type'].split('charset=')[-1]
    else:
        encoding = 'utf-8'

    print encoding
    r = HtmlResponse(url=url,body=html,encoding=encoding)
    spider = SpiderAll(
            parse_parameters=parse_parameters, 
            follow_parameters=follow_parameters,
            deny_parameters=deny_parameters,
            source_allowed_domains=source_allowed_domains,
            source_start_urls='',
            name='tree')
    a_links = SgmlLinkExtractor(unique=True).extract_links(r)
    a_list = [link.url for link in a_links]

    f_links = spider.rules[1].link_extractor.extract_links(r)
    #f_links = spider.follow_link_extractor().extract_links(r)
    f_list = [link.url for link in f_links]
    #p_links = spider.parse_link_extractor().extract_links(r)
    p_links = spider.rules[0].link_extractor.extract_links(r)
    p_list = [link.url for link in p_links]

    

    tree_list = []

    if not source_allowed_domains:
        host_regex = re.compile('')
    else:
        regex = r'^(.*\.)?(%s)$' % '|'.join(re.escape(d) for d in source_allowed_domains.split(";"))
        host_regex = re.compile(regex)


    for i,link in enumerate(a_list):
        if link in p_list:
            status='parsed'
        elif link in f_list:
            status='followed'
        else:
            status='denied'

        if not bool(host_regex.search(urlparse(link).hostname)):
            status='denied'

        tree_list.append({'url':link,'allow':status,'linkno':i})
    return tree_list    
