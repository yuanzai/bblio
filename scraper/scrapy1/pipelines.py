# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlite3 import dbapi2 
from scrapy import log, signals
import string

class AllPipeline(object):
    def __init__(self):
        self.connection = dbapi2.connect('//mnt/my-data/db.sqlite3',check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS doc (id INTEGER PRIMARY KEY, urlAddress TEXT, document_text TEXT, title TEXT, domain TEXT)')

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        log.msg("Pipeline.spider_opened called", level=log.DEBUG)

    def spider_closed(self, spider):
        log.msg("Pipeline.spider_closed called", level=log.DEBUG)
    
    def process_item(self, item, spider):
        self.cursor.execute("SELECT * FROM doc WHERE urlAddress=?", (item['urlAddress'],))
        result = self.cursor.fetchone()
        if result:
            log.msg("Item already in database: %s" % item, level=log.DEBUG)
        else:

            self.cursor.execute("INSERT INTO doc \
                (urlAddress, document_text, title, domain) \
                VALUES (?, ?, ?, ?)",\
                string.join(item['urlAddress'],''),\
                string.join(item['document_text'],''),\
                string.join(item['title'],''),\
                string.join(item['domain'],''))

            self.connection.commit()
            log.msg("Item stored : " % item, level=log.DEBUG)
        return item
