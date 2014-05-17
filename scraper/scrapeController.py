#!/usr/bin/env python

#python imports

import sys
sys.path.append('/home/ec2-user/bblio/build/')

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Build.settings'
import importlib
import shutil
import telnetlib
import getpass
import httplib, urllib
import json

#django imports
from django.forms.models import model_to_dict
from search.models import Site

#scrapy imports
from twisted.internet import reactor
from twisted.internet.base import ReactorBase
from twisted.internet.interfaces import IReactorCore
from scrapy.crawler import Crawler, CrawlerProcess
from scrapy.log import ScrapyFileLogObserver
from scrapy import log, signals
from scrapy.settings import CrawlerSettings
from scrapy.xlib.pydispatch import dispatcher
from scrapy.resolver import CachingThreadedResolver
from scraper.deployable.deployable.spiders.spiderAll import SpiderAll
from scrapy import telnet


#import aws 

import aws.ec2 as ec2

def get_settings():
    settings_module = importlib.import_module('settings')
    return CrawlerSettings(settings_module)

def check_reactor():
    try:
        tn = telnetlib.Telnet('0.0.0.0', '6023')
        ret = tn.read_until('>>>')
        tn.write("spider.id\n")
        ret = tn.read_until('>>>').splitlines()
 
        tn.close()
        print ret
        return ret
    except:
        print 'no crawler active'
        return

def clear_schedule(id):
    if not id:
        raise BlankIDError('Please enter a site id')
    settings = get_settings()
    try:
        shutil.rmtree(settings['JOBDIR'] + str(id))
    except:
        print('No directory found')
 

def run_site_id(id):
    if not id:
        raise BlankIDError('Please enter a site id')
 
    settings = get_settings()
    dispatcher.connect(reactor.stop, signal=signals.spider_closed)
    #logfile = open('/home/ec2-user/bblio/scraper/log/' + id + '.log', 'w')
    #log_observer = ScrapyFileLogObserver(logfile, level=log.INFO)
    #log_observer.start()
    log.start(loglevel='INFO')
    site = Site.objects.get(pk=id)
    
    s = model_to_dict(site)
    
    process = CrawlerProcess(settings)
    process.settings.overrides['DEPTH_LIMIT'] = site.depthlimit
    process.settings.overrides['JOBDIR'] = settings['JOBDIR'] + str(id) + '/'
    
    crawler = process.create_crawler()
    spider = SpiderAll(**s)
    crawler.crawl(spider)
    process.start()    

def post_curl(url, method, params=None):
    params = urllib.urlencode(
            {
                'project': 'deployable',
                'spider': 'SpiderAll',
                })
    headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "Accept": "text/plain"}

    conn = httplib.HTTPConnection(url, port=6800)
    conn.request("POST", "/schedule.json", params, headers)
    response = conn.getresponse()
    print response.status, response.reason
    data = response.read()
    json_data = json.load(data)
    print data
    conn.close()
    return json_data

def curl_schedule_crawl(site_id, crawler_instance='i-260aa82e'):
    url = ec2.getInstanceFromInstanceName(crawler_instance).ip_address
    params = urllib.urlencode({'project': 'deployable', 'spider': 'SpiderAll', 'id' : site_id})
    return post_curl(url, "/schedule.json",params)

def curl_test():
    curl_schedule_crawl(25, 'i-260aa82e')



if __name__ == '__main__':
    arg = sys.argv
    if len(sys.argv) > 1:
        if arg[1] == 'clear':
            clear_schedule(arg[2])
        elif arg[1] == 'check':
            check_reactor()
        elif arg[1] == 'curl':
            curl_test()
        else:
            run_site_id(arg[1])
    else:
        print('Site ID required')
