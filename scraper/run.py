#!/usr/bin/env python
import sys
sys.path.append('/home/ec2-user/bblio/build/')
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Build.settings'
from django.forms.models import model_to_dict
from search.models import Site
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.log import ScrapyFileLogObserver
from scrapy import log, signals
from scrapy1.spiders.spiderAll import SpiderAll
from scrapy.settings import CrawlerSettings
from scrapy.xlib.pydispatch import dispatcher
from scrapy.resolver import CachingThreadedResolver
import importlib
from Queue import * 

def start_crawler():
    global q
    r = q.get()
    log.msg("Pipeline.spider_closed called", level=log.DEBUG)
    spider = SpiderAll(**r)
    settings_module = importlib.import_module('scrapy1.settings')
    settings = CrawlerSettings(settings_module)
    crawler = Crawler(settings)
    crawler.configure()
    crawler.crawl(spider)   
    crawler.start()

def spider_closed():
    global k, q
    k = k - 1
    print(k)
    if q.empty():
        if k == 0:
            reactor.stop()
    else:
        reactor.callLater(0, start_crawler)

def run_grouping(grouping):
    global k, q
    # log.start(logstdout=True,logfile='scrapelog.txt',loglevel='INFO')
    q = Queue()
    dispatcher.connect(spider_closed, signal=signals.spider_closed)
    if grouping:    
	result = Site.objects.filter(grouping=grouping)
    else:
        result = Site.objects.all()
      
    if len(result) == 0:
        return
 
    for r in result:
	r = model_to_dict(r)
	q.put(r)
    k = len(result)
    logfile = open('/home/ec2-user/bblio/scraper/crawl.log', 'w')
    log_observer = ScrapyFileLogObserver(logfile, level=log.INFO)
    log_observer.start()
    log.start(loglevel='INFO')
    log.msg("Grouping [" + grouping + "] count: " + str(k), level=log.INFO)
    for i in range(min(len(result),4)):
        reactor.callLater(0, start_crawler)    
    #reactor.installResolver(CachingThreadedResolver(reactor))
    #reactor.run(installSignalHandlers=False)
    reactor.run()


if __name__ == '__main__':
    arg = sys.argv
    if len(sys.argv) > 1:
	run_grouping(arg[1])
    else:
        run_grouping('')

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
