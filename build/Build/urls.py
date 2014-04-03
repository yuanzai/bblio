from django.conf.urls import patterns, include, url
from django.contrib import admin
import search.views
import operations.urls
import testscrape.urls

admin.autodiscover()

urlpatterns = patterns('',

    #home page
    url(r'^$',search.views.index),
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^testing_input/$',search.views.testing_input,name='testing_input'),
    url(r'^testing/$',search.views.testing,name='testing'),
    
    url(r'^autocomplete/', search.views.autocomplete,name='autocomplete'),
    url(r'^search/',search.views.index,name='index'),

    #Operations App
    url(r'^operations/',include(operations.urls),name='operations'),
    
    #TestScrape App - crawling tester site
    url(r'^testscrape/',include(testscrape.urls),name='testscrape'),
    )
