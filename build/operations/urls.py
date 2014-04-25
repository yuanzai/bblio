from django.conf.urls import patterns, url
import operations.views

urlpatterns = patterns('',
    url(r'^$', operations.views.index),
    
    # admin

    url(r'^admin/$', operations.views.admin),

    # phrases
    url(r'^phrases/$', operations.views.phrases),
    

    # site
    url(r'^site/$',
        operations.views.sites),
    url(r'^site/(?P<site_id>\d+)/$',
        operations.views.site),

    # 3 - crawling
     url(r'^site/(?P<site_id>\d+)/crawl/$',
        operations.views.crawl),
    
    url(r'^site/(?P<site_id>\d+)/clear_crawl_schedule/$',    
        operations.views.clear_crawl_schedule),
    
    # 4 - document
    url(r'^site/(?P<site_id>\d+)/idocument_duplicate_filter/$',
        operations.views.document_duplicate_filter),
    url(r'^site/(?P<site_id>\d+)/document_reset_to_zero/$',
        operations.views.document_reset_to_zero), 
    url(r'^site/(?P<site_id>\d+)/document_delete/$',
        operations.views.document_delete),
   
    # 5 - indexing
    url(r'^site/(?P<site_id>\d+)/es_index_site/$',
        operations.views.es_index_site),

    url(r'^site/(?P<site_id>\d+)/es_remove_site_from_index/$',
        operations.views.es_remove_site_from_index),
    
    # tester
    url(r'^tester/$',operations.views.tester),
    url(r'^tester/(?P<query>[\w\ ]+)/(?P<testinggroup>\d+)/(?P<page>\d+)/$',operations.views.tester),
    url(r'^tester/(?P<query>\[\w ]+)/(?P<testinggroup>\d+)/$',operations.views.tester),
    url(r'^tester/(?P<query>\[\w\ ]+)/$',operations.views.tester),

    
    url(r'^document/(?P<doc_id>\d+)/$',operations.views.document),
    
    
    url(r'^tree/$', operations.views.tree),   
    #url(r'^(?P<site_id>\d+)/delete/$',views.delete,name='delete'),
    #url(r'^(?P<site_id>\d+)/delete/$',views.delete,name='delete'),
    #url(r'^(?P<site_id>\d+)/delete/$',views.delete,name='delete'),
    #url(r'^testing_input$',views.testing_input,name='testing_input'),
    #url(r'^testing$',views.testing,name='testing'),
)
