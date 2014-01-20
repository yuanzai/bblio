#!/usr/bin/env python
import sys
sys.path.append('/home/ec2-user/bblio/build/')
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Build.settings'
from django.forms.models import model_to_dict
from search.models import Site
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy1.spiders.spiderAll import SpiderAll
from scrapy.settings import CrawlerSettings
from scrapy.xlib.pydispatch import dispatcher
from scrapy.resolver import CachingThreadedResolver
import importlib
import csv
import sys
from pprint import pprint
from Queue import * 

q = Queue()

def stop_reactor():
    reactor.stop()

def start_crawler():
    r = q.get()
    print(r['name'] + ' Started >>>')
    spider = SpiderAll(**r)
    settings_module = importlib.import_module('scrapy1.settings')
    settings = CrawlerSettings(settings_module)
    crawler = Crawler(settings)
    crawler.configure()
    crawler.crawl(spider)   
    crawler.start()

def spider_closed():
    global k 
    k = k - 1
    print(k)
    if q.empty():
        if k == 0:
            reactor.stop()
    else:
        reactor.callLater(0, start_crawler)

def run_grouping(grouping):
    global k
    dispatcher.connect(spider_closed, signal=signals.spider_closed)
    if grouping:    
	result = Site.objects.filter(grouping=grouping)
    else:
        result = Site.objects.all()

    for r in result:
	r = model_to_dict(r)
	q.put(r)
    print('Grouping ['+ grouping +'] queue size: ' + str(len(result)))
    k = min(len(result),10)
    for i in range(1):
        reactor.callLater(0, start_crawler)    
    reactor.installResolver(CachingThreadedResolver(reactor))
    reactor.run(installSignalHandlers=False)

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
