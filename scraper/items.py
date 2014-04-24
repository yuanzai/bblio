import sys
import os
sys.path.append(os.environ['HOME'] + '/bblio/')
from scrapy.contrib.djangoitem import DjangoItem
from build.search.models import Document, Site


class URLItem(DjangoItem):
    django_model = Document
