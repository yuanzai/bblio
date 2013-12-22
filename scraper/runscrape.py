fom twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log
from scrapy1.spiders.spiderAll import SpiderAll
from scrapy.settings import CrawlerSettings
from scrapy.xlib.pydispatch import dispatcher
import importlib
import csv
import sys

dispatcher.connect(stop_reactor, signal=signals.spider_closed)
arg = sys.argv
filePath =arg[1]  

def stop_reactor():
    reactor.stop()

def setup_crawler(spider):
    settings_module = importlib.import_module('scrapy1.settings')
    settings = CrawlerSettings(settings_module)
    crawler = Crawler(settings)
    crawler.configure()
    crawler.crawl(spider)   
    crawler.start()

with open(filePath, 'rU') as csvfile:
    csvreader = csv.DictReader(csvfile, delimiter=',')
    for id,row in enumerate(csvreader):
        print row
        spider = SpiderAll(**row)
        setup_crawler(spider)
        
log.start(loglevel='INFO')
reactor.run()
