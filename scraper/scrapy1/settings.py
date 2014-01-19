# Scrapy settings for tutorial project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'scrapeAll'

SPIDER_MODULES = ['scrapy1.spiders']
NEWSPIDER_MODULE = 'scrapy1.spiders'
ITEM_PIPELINES = {'scrapy1.pipelines.AllPipeline':1000}
DOWNLOAD_DELAY = 1
DEPTH_LIMIT = 0

import sys
sys.path.append('/home/ec2-user/bblio/build/')

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Build.settings'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'tutorial (+http://www.yourdomain.com)'
