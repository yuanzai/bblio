#scrapy imports
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from bblioCrawler.items import URLItem
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy import log, signals
from scrapy.xlib.pydispatch import dispatcher

#python imports
import string
from datetime import datetime
import sys

#django imports
sys.path.append('/home/ec2-user/bblio/build/')
from search.models import Site


class SpiderAll(CrawlSpider):
    name = None
    allowed_domains = None
    rules = None
    groupName = None
    count = 0
    id = None
    def __init__(self, *a, **kw):
        self.allowed_domains = kw['source_allowed_domains'].split(';')
        self.start_urls = kw['source_start_urls'].split(';')
        
        follow = kw['follow_parameters'].split(";")   
        deny = None
        if kw['deny_parameters']: 
            denyFollow = kw['deny_parameters'].split(";")    
        
        parse = kw['parse_parameter'].split(";")
        
        self.rules = (
                Rule(SgmlLinkExtractor(
                    allow=parse,
                    deny=deny, 
                    unique=True,
                    restrict_xpaths=('//*[not(self::meta)]')), 
                    callback='parse_item', follow='true'),

                Rule(SgmlLinkExtractor(
                    allow=follow,
                    deny=deny,
                    unique=True), follow='true'),
 
        )    
        super(SpiderAll, self).__init__(*a, **kw) 
        
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

