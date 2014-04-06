from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy1.items import URLItem
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy import log, signals
from scrapy.xlib.pydispatch import dispatcher
import string
from datetime import datetime
import sys
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
        allowFollow = kw['source_allowFollow'].split(";")   
        denyFollow = None
        if kw['source_denyFollow']: 
            denyFollow = kw['source_denyFollow'].split(";")    
        
        denyParse = None
        allowParse = kw['source_allowParse'].split(";")
        if kw['source_denyParse']:
            denyParse = kw['source_denyParse'].split(";")
        
        self.rules = (
	Rule(SgmlLinkExtractor(allow=allowParse,deny=denyParse, unique=True,restrict_xpaths=('//*[not(self::meta)]')), 
        callback='parse_start_url', follow='true'),
        
        Rule(SgmlLinkExtractor(allow=allowFollow,deny=denyFollow,unique=True), follow='true'),
 
        )    
        super(SpiderAll, self).__init__(*a, **kw) 
        
    def parse_start_url(self, response):
        try:            
            sel = Selector(response)
            sites = sel.xpath("//p|//li|//td|//div")
            #sites = sel.xpath("//")
            items = []
            item = URLItem()
            item['title'] = sel.xpath("//title/text()").extract()
            item['document_text'] = str(sites.xpath('text()').extract()).encode('utf8')
            item['urlAddress'] = response.url
            item['domain'] = self.allowed_domains
            item['site'] = Site.objects.get(pk=self.id)
            item['response_code'] = response.status
            item['encoding'] = response.headers['content-type'].split('charset=')[-1]
            item['document_html'] = (response.body).encode('utf-8')
            items.append(item)
            return items
        except AttributeError:
	    log.msg('* Cannot parse: ' + response.url,level=log.INFO)
            log.msg(sys.exc_info()[0], level=log.INFO)
            return

