# Scrapy settings for tutorial project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'scrapeAll'

SPIDER_MODULES = ['scrapy1.spiders']
NEWSPIDER_MODULE = 'scrape1.spiders'
ITEM_PIPELINES = {'scrape1.pipelines.AllPipeline':1000}
DOWNLOAD_DELAY = 1
DEPTH_LIMIT = 0
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'tutorial (+http://www.yourdomain.com)'
