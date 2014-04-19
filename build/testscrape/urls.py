from django.conf.urls import patterns, url
from django.http import HttpResponse

def index(request):
    return HttpResponse("""
            <a href="follow">follow</a><br>
            <a href="parse">parse</a><br> 
            <a href="deny">deny</a><br> 
            <a href="slow">slow</a><br> 
            <a href="date/2000/10/10/">date</a>
            """)

def uk(request):
    return HttpResponse('<a href="2">UK2</a>')

def uk2(request):
    return HttpResponse('UK2')

def follow(request):
    return HttpResponse('Followed Link')

def parse(request):
    return HttpResponse('Parsed Link')

def deny(request):
    return HttpResponse('Denied Link')

def slow(request):
    import time
    time.sleep(30)
    return HttpResponse('Slow link')

def date(request):
    return HttpResponse('Date link')


urlpatterns = patterns('',
    url(r'^$', index),
    url(r'^follow/$', follow),
    url(r'^parse/$', parse),
    url(r'^deny/$', deny),
    url(r'^slow/$', slow),
    url(r'^uk/$',uk),
    url(r'^uk/2/$',uk2),
    url(r'^date/\d{4}/\d{2}/\d{2}/$', date),
)
