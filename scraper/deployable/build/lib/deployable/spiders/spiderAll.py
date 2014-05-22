#python imports
import string
from datetime import datetime
import sys
import re
sys.path.append('/home/ec2-user/bblio/')
sys.path.append('/home/ec2-user/bblio/build/')

#django imports
from search.models import Site, Document

#scrapy imports
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy import log, signals
from scrapy.xlib.pydispatch import dispatcher

#config import
import config_file

#ec2 import
import aws.ec2

class SpiderAll(CrawlSpider):
    name = "SpiderAll"
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
        self.id = kw['id']
        #self.id = 25
        site = Site.objects.get(pk=self.id)
        
        self.allowed_domains = site.source_allowed_domains.split(';')
        self.start_urls = site.source_start_urls.split(';')
        self.follow = []
        self.parsing = []
        self.deny = []
        if site.parse_parameters:  self.parsing = site.parse_parameters.strip().encode('utf-8').split(";")
        if site.follow_parameters:  self.follow = site.follow_parameters.strip().encode('utf-8').split(";")   
        if site.deny_parameters: self.deny = site.deny_parameters.strip().encode('utf-8').split(";")    
        
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
        log.msg('Parsing Start: ' + response.url,level=log.INFO)
         
        try:
            item = {
                    'urlAddress' : response.url,
                    'domain' :  self.allowed_domains,
                    'site' : Site.objects.get(pk=self.id),
                    'response_code' : response.status, 
                    'isUsed' : 0
                    }

            if '.pdf' in str(response.url[-4:]):
                pdf_name = str(self.id) + '_' + str(datetime.now().isoformat()) + '.pdf'
                path = '/home/ec2-user/bblio/scraper/pdf/'
                item.update({
                        'document_html' : path + pdf_name,
                        'encoding' : 'PDF'
                        })
                log.msg('PDF path: ' + path + pdf_name,level=log.INFO)        
                
                with open(path + pdf_name, "wb") as f: 
                    f.write(response.body)
                f.close()
                aws.ec2.copy_file_to_web_server(path+pdf_name ,path + pdf_name)
            else:
                item.update({
                    'encoding' : response.headers['content-type'].split('charset=')[-1],
                    'document_html': (response.body).decode('utf-8','ignore').encode('utf-8')
                    })
            d = Document(**item)
            d.save()
            
            log.msg('Parsing Success: ' + response.url,level=log.INFO)

            return
        except AttributeError:
            log.msg('* Cannot parse: ' + response.url,level=log.INFO)
            log.msg(sys.exc_info()[0], level=log.INFO)
            return

        except:
            log.msg('* Unexpected error:' + str(sys.exc_info()[0]) + '\n' + str(sys.exc_info()[1]), level=log.INFO)
            return

