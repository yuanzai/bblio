#!/usr/bin/env python
import sys
sys.path.append('/home/ec2-user/bblio/build/')
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Build.settings'
from search.models import Document


def clean_site_id(site_id):
    Document.objects.filter(site_id=int(site_id)).delete()
    #Document.objects.all().delete()
    print('Done!')
    #print(str(len(Document.objects.all())))

if __name__ == '__main__':
    arg = sys.argv
    if len(sys.argv) > 1:
        clean_site_id(arg[1])
    else:
        print('Site ID required')

