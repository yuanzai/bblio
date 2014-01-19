from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^create/$',views.create, name='create'),
    url(r'^testscrape/$',views.testscrape),
    url(r'^(?P<key_id>\d+)/$', views.result, name='result'),
)
