#!/usr/bin/env python
import sys
sys.path.append('/home/ec2-user/bblio/build/')
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Build.settings'
from django.forms.models import model_to_dict
from search.models import Site
from twisted.internet import reactor
from scrapy.crawler import Crawler, CrawlerProcess
from scrapy.log import ScrapyFileLogObserver
from scrapy import log, signals
from scrapy1.spiders.spiderAll import SpiderAll
from scrapy.settings import CrawlerSettings
from scrapy.xlib.pydispatch import dispatcher
from scrapy.resolver import CachingThreadedResolver
import importlib
from Queue import * 

def run_site_id(id):
    if not id:
        raise BlankIDError('Please enter a site id')
 
    dispatcher.connect(reactor.stop, signal=signals.spider_closed)
    # logfile = open('/home/ec2-user/bblio/scraper/log/%s.log'% (str(id)), 'w')
    logfile = open('/home/ec2-user/bblio/scraper/log/' + id + '.log', 'w')
    log_observer = ScrapyFileLogObserver(logfile, level=log.INFO)
    log_observer.start()
    log.start(loglevel='INFO')
    site = Site.objects.get(pk=id)
    settings_module = importlib.import_module('scrapy1.settings')
    settings = CrawlerSettings(settings_module)
#    crawler = Crawler(settings)
#    crawler.configure()
    
    s = model_to_dict(site)
    
    process = CrawlerProcess(settings)
    process.settings.overrides['DEPTH_LIMIT'] = site.depthlimit
    process.settings.overrides['JOBDIR'] = settings['JOBDIR'] + str(id) + '/'
    
    crawler = process.create_crawler()
    #spider = crawler.spiders.create('spiderAll', **s)
    spider = SpiderAll(**s)
    crawler.crawl(spider)
    process.start()    

"""
    crawler.crawl(spider)
    crawler.start()
 
    #reactor.installResolver(CachingThreadedResolver(reactor))
    #reactor.run(installSignalHandlers=False)
    reactor.run()
"""   

if __name__ == '__main__':
    arg = sys.argv
    if len(sys.argv) > 1:
	run_site_id(arg[1])
    else:
        print('Site ID required')

"""
arg = sys.argv
filePath =arg[1]

with open(filePath, 'rU') as csvfile:
    csvreader = csv.DictReader(csvfile, delimiter=',')
    for id,row in enumerate(csvreader):
        print row
        spider = SpiderAll(**row)
        setup_crawler(spider)
log.start(loglevel='INFO')
reactor.run()

"""
