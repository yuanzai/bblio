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

    ignored_extensions = [
    # images
    'mng', 'pct', 'bmp', 'gif', 'jpg', 'jpeg', 'png', 'pst', 'psp', 'tif',
    'tiff', 'ai', 'drw', 'dxf', 'eps', 'ps', 'svg',

    # audio
    'mp3', 'wma', 'ogg', 'wav', 'ra', 'aac', 'mid', 'au', 'aiff',

    # video
    '3gp', 'asf', 'asx', 'avi', 'mov', 'mp4', 'mpg', 'qt', 'rm', 'swf', 'wmv',
    'm4a',

    # office suites
    'xls', 'xlsx', 'ppt', 'pptx', 'doc', 'docx', 'odt', 'ods', 'odg', 'odp',

    # other
    'css', 'exe', 'bin', 'rss', 'zip', 'rar',
    ]


    def __init__(self, *a, **kw):
        self.allowed_domains = kw['source_allowed_domains'].split(';')
        self.start_urls = kw['source_start_urls'].split(';')
        self.follow = []
        self.parsing = []
        self.deny = []
        print self.allowed_domains
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
                    deny_extensions=self.ignored_extensions,
                    ), 
                    callback='parse_item', follow='true'),
                Rule(SgmlLinkExtractor(
                    allow=self.follow,
                    deny=self.deny,
                    unique=True,
                    restrict_xpaths=self._restrict_xpath,
                    ), 
                    callback='follow_item', follow='true'),
                )
        super(SpiderAll, self).__init__(*a, **kw) 
    
    def follow_item(self, response):
        log.msg('Following: ' + response.url,level=log.INFO)
        return None

    def parse_item(self, response):
        log.msg('Parsing: ' + response.url,level=log.INFO)
         
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
                path = '/home/ec2-user/bblio/scraper/pdf/'
                item['document_html'] = path + pdf_name
                item['encoding'] = 'PDF'
                log.msg('PDF path: ' + path + pdf_name,level=log.INFO)        
                
                with open(path + pdf_name, "wb") as f: 
                    f.write(response.body)
                f.close()
                aws.ec2.copy_file_to_web_server(path+pdf_name ,path + pdf_name)
            else:
                item['encoding'] = response.headers['content-type'].split('charset=')[-1]
                item['document_html'] = (response.body).decode('utf-8','ignore').encode('utf-8')
            items.append(item)
            return items
        except AttributeError:
            log.msg('* Cannot parse: ' + response.url,level=log.INFO)
            log.msg(sys.exc_info()[0], level=log.INFO)
            return
    

