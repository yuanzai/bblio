from django.conf.urls import patterns, include, url
from django.contrib import admin
import search.views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Build0001.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$',search.views.index),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^scraped/', include('search.urls', namespace="search")),
    url(r'^testscrape/$',search.views.testscrape),    
)
