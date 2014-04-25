from django.conf.urls import patterns, url
from django.http import HttpResponse

def index(request):
    return HttpResponse("""
            <a href="follow">follow</a><br>
            <a href="parse">parse</a><br>
            <a href="deny">deny</a><br>
            <a href="slow">slow</a><br>
            <a href="date/2000/10/10/">date</a><br>
            <a href="t1_L1">[L1] Type 1</a><br>
            """)


# test for Type 1 sites
def t1_L1(request):
    return HttpResponse("""
        <a href="t1_2014-02-01">[L2] Previous Article</a><br>
        <a href="t1_2014-02-03">[L2] Newer Article</a><br>
        <a href="t1_L2FB">[L2] Lame FB Link</a><br>
        """)

def t1_L2(request):
    return HttpResponse("""
        <a href="t1_2014-03-01">[L3] Previous Article</a><br>
        <a href="t1_2014-03-03">[L3] Newer Article</a><br>
        <a href="t1_L3FB">[L2] Lame FB Link</a><br>
        """)

def t1_L3(request):
    return HttpResponse("""
        <a href="t1_2014-04-01">[L4] Previous Article</a><br>
        <a href="t1_2014-04-03">[L4] Newer Article</a><br>
        <a href="t1_L4FB">[L2] Lame FB Link</a><br>
        """)


# test for Type 2 sites
def t2_L3(request):
    return HttpResponse("""
        <a href="t2_L31">[L3] Should have stopped on the prev page</a><br>
        <a href="t2_L32">[L3] DepthLimit set?</a><br>
        <a href="t2_L33">[L3] These links should NOT be parsed.</a><br>
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
    url(r'^t1_L1/$', t1_L1),
    url(r'^t1_L2/$', t1_L2),
    url(r'^t1_L3/$', t1_L2),
)