from django.conf.urls import patterns, url
from django.http import HttpResponse;


def index(request):
    return HttpResponse('<a href="follow">follow</a><br> \
            <a href="parse">parse</a><br> \
            <a href="deny">deny</a>')

def follow(request):
    return HttpResponse('Followed Link')

def parse(request):
    return HttpResponse('Parsed Link')

def deny(request):
    return HttpResponse('Denied Link')

urlpatterns = patterns('',
    url(r'^$', index),
    url(r'^follow/$', follow),
    url(r'^parse/$', parse),
    url(r'^deny/$', deny),
    
)
