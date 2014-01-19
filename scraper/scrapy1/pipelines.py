# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys
sys.path.append('/home/ec2-user/bblio/build/')
from sqlite3 import dbapi2 
from scrapy import log, signals
from search.models import Document
import string
import MySQLdb

class AllPipeline(object):
    def __init__(self):
	pass

    @classmethod
    def from_crawler(cls, crawler):
    	pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        log.msg("Pipeline.spider_opened called", level=log.DEBUG)

    def spider_closed(self, spider):
	stats = spider.crawler.stats
	"""
	self.cursor.execute("INSERT INTO crawlLOG \
	    (name, startTime, endTime, scrapeCount)\
	    VALUES (?, ?, ?, ?)",\
	    (spider.name,\
 	    str(stats.get_value('start_time')),\
	    str(stats.get_value('finish_time')),\
	    stats.get_value('item_scraped_count'))) 
	"""
        log.msg("Pipeline.spider_closed called", level=log.DEBUG)
   
 
    def process_item(self, item, spider):
        item.save()
	return item
