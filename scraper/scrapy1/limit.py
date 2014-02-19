from scrapy.http import Request
from scrapy import log
from scrapy.exceptions import NotConfigured
import time

class LimitRequestMiddleware(object):
    def __init__(self):
       log.msg('LimitRequestMiddleware Init',level=log.INFO)
 
    def process_spider_output(self, response, result, spider):
        self.max_queue_size = spider.crawler.settings.getint("REQUESTS_QUEUE_SIZE")
        if not self.max_queue_size:
            raise NotConfigured
        requests = []
        items = []
        for r in result:
            if isinstance(r, Request):
                requests.append(r)
            else:
                items.append(r)
        """
        log.msg('LimitRequestMiddleware Process',level=log.INFO)
        p = len(spider.crawler.engine.slot.inprogress)
	log.msg('InProgressCount ' + str(p),level=log.INFO,spider=spider)
        log.msg('ScheduleCount ' + str(len(spider.crawler.engine.slot.scheduler)),level=log.INFO,spider=spider)
        
        while len(spider.crawler.engine.slot.scheduler) > 50:
            time.sleep(1)
            log.msg('Waiting', level=log.INFO)        
        
        max_pending = getattr(spider, 'requests_queue_size', self.max_queue_size)
        if max_pending:
            pending_count = len(scrapyengine.scheduler.pending_requests.get(spider.domain_name, []))
            free_slots = max_pending - pending_count
            dropped_count = len(requests) - free_slots
            if dropped_count > 0:
                requests = requests[:free_slots]
                log.msg("Dropping %d request(s) because the maximum schedule size (%d) has been exceeded" % \
                        (dropped_count, max_pending), level=log.DEBUG, domain=spider.domain_name)
        """   
        return requests + items
