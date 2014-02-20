from django.conf.urls import patterns, include, url
from django.contrib import admin
import search.views
import operations.urls


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',search.views.index),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^testscrape/$',search.views.testscrape),
    url(r'^testing_input/$',search.views.testing_input,name='testing_input'),
    url(r'^testing/$',search.views.testing,name='testing'),
    url(r'^scraped/(?P<site_id>\d+)/scraped/$',search.views.scraped,name='scraped'),
    url(r'^scraped/(?P<site_id>\d+)/delete/$',search.views.delete,name='delete'),
    url(r'^testsearch/(?P<query>\S+)/(?P<page>\d+)/$',search.views.testsearch,name='testsearch'),

    url(r'^search/',search.views.index2,name='index'),
    url(r'^operations',include(operations.urls),name='operations'),
)
