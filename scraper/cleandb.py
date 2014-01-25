#!/usr/bin/env python
import sys
sys.path.append('/home/ec2-user/bblio/build/')
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Build.settings'
from search.models import Document

Document.objects.all().delete()
print(str(len(Document.objects.all())))
