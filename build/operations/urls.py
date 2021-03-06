from django.conf.urls import patterns, url
import operations.views
import operations.views.admin
import operations.views.site

urlpatterns = patterns('',
    url(r'^$', operations.views.index),
    
    # admin

    url(r'^admin/$', operations.views.admin.index),
    url(r'^admin/push_scrape/$', operations.views.admin.push_scrape),

    # phrases
    url(r'^phrases/$', operations.views.phrases),
    

    # site
    url(r'^site/$',
        operations.views.site.sites, name='sites'),
    url(r'^site/(?P<site_id>\d+)/$',
        operations.views.site.site,name='site'),
    
    # 1 - tree
    url(r'^tree/$', operations.views.site.tree,name='tree'),

    # 2 - input
    url(r'^site/(?P<site_id>\d+)/delete/$',
        operations.views.site.delete),
    
    # 3 - crawling
    url(r'^site/(?P<site_id>\d+)/crawl/$',
        operations.views.site.crawl),
    
    url(r'^site/(?P<site_id>\d+)/crawl_cancel/$',
        operations.views.site.crawl_cancel),
    
    url(r'^site/(?P<site_id>\d+)/crawl_not_running/$',    
        operations.views.site.crawl_not_running),
    
    # 4 - document
    url(r'^document/(?P<doc_id>\d+)/$',
        operations.views.site.document, name='get_document'),

    url(r'^site/(?P<site_id>\d+)/document_duplicate_filter/$',
        operations.views.site.document_duplicate_filter),
    url(r'^site/(?P<site_id>\d+)/document_reset_to_zero/$',
        operations.views.site.document_reset_to_zero), 
    url(r'^site/(?P<site_id>\d+)/document_delete/$',
        operations.views.site.document_delete),
   
    # 5 - indexing
    url(r'^site/(?P<site_id>\d+)/es_index_site/$',
        operations.views.site.es_index_site),

    url(r'^site/(?P<site_id>\d+)/es_remove_site_from_index/$',
        operations.views.site.es_remove_site_from_index),
    
    # tester
    url(r'^tester/$',operations.views.tester),
    url(r'^tester/(?P<query>[\w\ ]+)/(?P<testinggroup>\d+)/(?P<page>\d+)/$',operations.views.tester),
    url(r'^tester/(?P<query>\[\w ]+)/(?P<testinggroup>\d+)/$',operations.views.tester),
    url(r'^tester/(?P<query>\[\w\ ]+)/$',operations.views.tester),

    
    
    
    #url(r'^testing_input$',views.testing_input,name='testing_input'),
    #url(r'^testing$',views.testing,name='testing'),
)
