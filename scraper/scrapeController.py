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
from subprocess import Popen, PIPE
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


#import aws 
import aws.ec2 as ec2

def get_settings():
    settings_module = importlib.import_module('settings')
    return CrawlerSettings(settings_module)

def deploy():
    for i in ec2.getCrawlerInstances():
        with open("/home/ec2-user/bblio/scraper/deployable/scrapy.cfg", "w") as f:
            f.write(
"""
[settings]
default = deployable.settings    
[deploy]
project = deployable\n
"""
            )
            f.write("url = http://")
            f.write(i.ip_address)
            f.write(":6800")
            print i.ip_address
        #p = Popen(["cd","/home/ec2-user/bblio/scraper/deployable/","&&","python","/usr/bin/scrapyd-deploy"],stdout=PIPE,shell=True)
        #p = Popen(["cd","/home/ec2-user/bblio/scraper/deployable"],stdout=PIPE,shell=True)
        p = Popen(['scrapyd-deploy'],stdout=PIPE,shell=True,cwd='/home/ec2-user/bblio/scraper/deployable')
        #p = Popen(["cd","/home/ec2-user/bblio/scraper/deployable","&&","/usr/bin/scrapyd-deploy"],stdout=PIPE,shell=True)
        print p.stdout.read() 
        while True:
            out = p.stdout.read(1)
            if out == '' and p.poll() != None:
                break
            if out != '':
                sys.stdout.write(out)
                sys.stdout.flush()

def curl(url, method, request_type, params=None):
    """
    params = urllib.urlencode(
            {
                'project': 'deployable',
                'spider': 'SpiderAll',

                })
    """
    headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "Accept": "text/plain"}
    conn = httplib.HTTPConnection(url, port=6800)
    conn.request(request_type, method, params, headers)
    response = conn.getresponse()
    data = response.read()
    json_data = json.loads(data)
    conn.close()
    return json_data

def curl_schedule_crawl(site_id, crawler_instance='i-260aa82e'):
    url = ec2.getInstanceFromInstanceName(crawler_instance).ip_address
    params = urllib.urlencode({'project': 'deployable', 'spider': 'SpiderAll', 'id' : site_id})
    ret = curl(url, "/schedule.json", "POST", params)
    return ret

def curl_test():
    curl_schedule_crawl(25, 'i-260aa82e')

def get_jobs_for_all_instances():
    instance_list = ec2.getCrawlerInstances()
    job_dict = {}
    for i in instance_list:
        try:    
            job_dict.update(get_jobs_for_instance(i.id))
        except:
            pass
    return job_dict

def get_jobs_for_instance(crawler_instance='i-260aa82e'):
    url = ec2.getInstanceFromInstanceName(crawler_instance).ip_address
    ret = curl(url, "/listjobs.json?project=deployable","GET")
    inv_map = {}
    try:
        for k,v in ret.items():
            if k != 'status':
                for j in v:
                    site_id = Job.objects.get(scrapyd_job_id=j['id']).site_id
                    inv_map.update({
                        j['id'] : {
                            'status':k,
                            'start_time': j['start_time'],
                            'end_time' : j['end_time'],
                            'instance' : crawler_instance,
                            'site' : site_id
                            }
                        })
    except:
        inv_map = None
    return inv_map

def get_jobs_for_site(site_id):
    j = Site.objects.get(pk=site_id).jobid
    i = Site.objects.get(pk=site_id).instance
    
    if j:
        instance_jobs = get_jobs_for_instance(i)
        if instance_jobs:
            if j in instance_jobs:
                try:
                    return instance_jobs[j]['status']
                except:
                    pass
    
    return None


def curl_cancel_crawl(site_id):
    s = Site.objects.get(pk=site_id)
    if not s:
        url = ec2.getInstanceFromInstanceName(s.instance).ip_address
        params = urllib.urlencode({'project': 'deployable', 'job' : s.jobid})
        ret = curl(url, "/cancel.json", "POST", params)
        return ret
    pass


if __name__ == '__main__':
    arg = sys.argv
    if len(sys.argv) > 1:
        if arg[1] == 'clear':
            clear_schedule(arg[2])
        elif arg[1] == 'check':
            check_reactor()
        elif arg[1] == 'curl':
            curl_test()
        elif arg[1] == 'jobs':
            get_jobs_for_all_instances()
        elif arg[1] == 'deploy':
            deploy()
        else:
            run_site_id(arg[1])

    else:
        print('Site ID required')
