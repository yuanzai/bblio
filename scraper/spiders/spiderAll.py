#python imports
import string
from datetime import datetime
import sys
import re
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

#config import
import config_file

#ec2 import
import aws.ec2

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
        self.follow = []
        self.parsing = []
        self.deny = []
        if kw['parse_parameters']:  self.parsing = kw['parse_parameters'].strip().encode('utf-8').split(";")
        if kw['follow_parameters']:  self.follow = kw['follow_parameters'].strip().encode('utf-8').split(";")   
        if kw['deny_parameters']: self.deny = kw['deny_parameters'].strip().encode('utf-8').split(";")    
        config = config_file.get_config()
        universal_deny = config.get('bblio','universal_deny').strip().split(";")
        self.deny.extend(universal_deny)
        if len(self.follow) > 0:
            for i,d in enumerate(self.follow):
                if "r'" in str(d[0:2]) and "'" in str(d[-1]):
                    self.follow[i] = d[2:-1]
        
        if len(self.parsing) > 0:
            for i,d in enumerate(self.parsing):
                if "r'" in str(d[0:2]) and "'" in str(d[-1]):
                    self.parsing[i] = d[2:-1]
        
        if len(self.deny) > 0:
            for i,d in enumerate(self.deny):
                if "r'" in str(d[0:2]) and "'" in str(d[-1]):
                    self.deny[i] = d[2:-1]

        self.rules = (
                Rule(SgmlLinkExtractor(
                    allow=self.parsing,
                    deny=self.deny,
                    unique=True,
                    restrict_xpaths=self._restrict_xpath,
                    ), 
                    callback='parse_item', follow='true'),
                Rule(SgmlLinkExtractor(
                    allow=self.follow,
                    deny=self.deny,
                    unique=True,
                    restrict_xpaths=self._restrict_xpath,
                    ), 
                    follow='true'),
                )    
        super(SpiderAll, self).__init__(*a, **kw) 
    
    def parse_item(self, response):
        log.msg('Currently parsing: ' + response.url,level=log.INFO)
         
        try:
            items = []
            item = URLItem()
            item['urlAddress'] = response.url
            item['domain'] = self.allowed_domains
            item['site'] = Site.objects.get(pk=self.id)
            item['response_code'] = response.status
            item['isUsed'] = 0
            
            if '.pdf' in str(response.url[-4:]):
                pdf_name = str(self.id) + '_' + str(datetime.now().isoformat()) + '.pdf'
                item['encoding'] = 'PDF'
                path = '/home/ec2-user/bblio/scraper/pdf/'
                log.msg('PDF Check: ' + path + pdf_name,level=log.INFO)        
                
                with open(path + pdf_name, "wb") as f: 
                    f.write(response.body)
                f.close()
                import threading
                
                t = threading.Thread(target=aws.ec2.copy_file_to_web_server,
                        args=(path + pdf_name, path + pdf_name))
                t.setDaemon(True)
                t.start()

            else:
                item['encoding'] = response.headers['content-type'].split('charset=')[-1]
                item['document_html'] = (response.body).decode('utf-8','ignore').encode('utf-8')
            items.append(item)
            return items
        except AttributeError:
            log.msg('* Cannot parse: ' + response.url,level=log.INFO)
            log.msg(sys.exc_info()[0], level=log.INFO)
            return
    

