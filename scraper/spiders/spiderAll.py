#python imports
import string
from datetime import datetime
import sys
sys.path.append('/home/ec2-user/bblio/')

#django imports
from build.search.models import Site

#scrapy imports
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scraper.items import URLItem
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy import log, signals
from scrapy.xlib.pydispatch import dispatcher



class SpiderAll(CrawlSpider):
    name = None
    rules = None
    groupName = None
    count = 0
    _restrict_xpath= ('//*[not(self::meta)]')
    id = None
    def __init__(self, *a, **kw):
        self.allowed_domains = kw['source_allowed_domains'].split(';')
        self.start_urls = kw['source_start_urls'].split(';')
        self.follow = None
        self.parsing = None
        if kw['parse_parameters']:  self.parsing = kw['parse_parameters'].split(";")
        if kw['follow_parameters']:  self.follow = kw['follow_parameters'].split(";")   
        
        self.deny = None 
        if kw['deny_parameters']: self.deny = kw['deny_parameters'].split(";")    
        
        self.rules = (
                Rule(SgmlLinkExtractor(
                    allow=self.parsing,
                    deny=self.deny,
                    unique=True,
                    restrict_xpaths=self._restrict_xpath), 
                    callback='parse_item', follow='true'),
                Rule(SgmlLinkExtractor(
                    allow=self.follow,
                    deny=self.deny,
                    unique=True,
                    restrict_xpaths=self._restrict_xpath) , 
                    follow='true'),
                )    
        super(SpiderAll, self).__init__(*a, **kw) 
 

    def parse_link_extractor(self):
        return SgmlLinkExtractor(
                allow=self.parsing,
                deny=self.deny,
                unique=True,
                restrict_xpaths=self._restrict_xpath)

    def follow_link_extractor(self):
        return SgmlLinkExtractor(
                allow=self.follow,
                deny=self.deny,
                unique=True,
                restrict_xpaths=self._restrict_xpath)

    def parse_item(self, response):
        try:            
            sel = Selector(response)
            items = []
            item = URLItem()
            item['urlAddress'] = response.url
            item['domain'] = self.allowed_domains
            item['site'] = Site.objects.get(pk=self.id)
            item['response_code'] = response.status
            item['encoding'] = response.headers['content-type'].split('charset=')[-1]
            item['document_html'] = (response.body).encode('utf-8')
            item['isUsed'] = 0
            items.append(item)
            return items
        except AttributeError:
            log.msg('* Cannot parse: ' + response.url,level=log.INFO)
            log.msg(sys.exc_info()[0], level=log.INFO)
            return

