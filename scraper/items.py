import sys
sys.path.append('/home/ec2-user/bblio/')
from scrapy.contrib.djangoitem import DjangoItem
from build.search.models import Document, Site


class URLItem(DjangoItem):
    django_model = Document
