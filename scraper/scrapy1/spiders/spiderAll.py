from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy1.items import URLItem
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy import log, signals
from scrapy.xlib.pydispatch import dispatcher
import string

class SpiderAll(CrawlSpider):
    name = None
    allowed_domains = None
    rules = None

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
        Rule(SgmlLinkExtractor(allow=allowParse,deny=denyParse, unique=True), 
        callback='parse_item', follow='true'),
        
        Rule(SgmlLinkExtractor(allow=allowFollow,deny=denyFollow,unique=True), follow='true'),
 
        )    
        super(SpiderAll, self).__init__(*a, **kw) 
        
    def parse_item(self, response):
        sel = Selector(response)
        sites = sel.xpath("//p|//li|//td")        
        items = []
        item = URLItem()
        item['title'] = sel.xpath("//title/text()").extract()
        item['document_text'] = string.join(sites.xpath('text()').extract(),"")
        item['urlAddress'] = response.url
	item['domain'] = self.allowed_domains
        items.append(item)
        return items

