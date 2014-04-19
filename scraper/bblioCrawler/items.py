import sys
sys.path.append('/home/ec2-user/bblio/build/')
from scrapy.contrib.djangoitem import DjangoItem
from search.models import Document, Site


class URLItem(DjangoItem):
    django_model = Document
