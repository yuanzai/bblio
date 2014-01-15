import os,sys

path='/home/ec2-user/bblio/build'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'Build.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

