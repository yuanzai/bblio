from django.conf.urls import patterns, url
import operations.views

urlpatterns = patterns('',
    url(r'^$', operations.views.index),
    url(r'^phrases/$', operations.views.phrases),
    url(r'^site/$',operations.views.sites),
    url(r'^site/(?P<site_id>\d+)/$',operations.views.site),
    url(r'^site/(?P<site_id>\d+)/es_delete/$',operations.views.es_delete),
    url(r'^site/(?P<site_id>\d+)/duplicate_filter/$',operations.views.duplicate_filter),
    url(r'^site/(?P<site_id>\d+)/reset_to_zero/$',operations.views.reset_to_zero),
    url(r'^tester/$',operations.views.tester),
    url(r'^tester/(?P<query>[\w\ ]+)/(?P<testinggroup>\d+)/(?P<page>\d+)/$',operations.views.tester),
    url(r'^tester/(?P<query>\[\w ]+)/(?P<testinggroup>\d+)/$',operations.views.tester),
    url(r'^tester/(?P<query>\[\w\ ]+)/$',operations.views.tester),
    #url(r'^document/(?P<doc_id>\d+)/$',operations.views.document),
    url(r'^tree/$', operations.views.tree),   
    #url(r'^(?P<site_id>\d+)/delete/$',views.delete,name='delete'),
    #url(r'^(?P<site_id>\d+)/delete/$',views.delete,name='delete'),
    #url(r'^(?P<site_id>\d+)/delete/$',views.delete,name='delete'),
    #url(r'^testing_input$',views.testing_input,name='testing_input'),
    #url(r'^testing$',views.testing,name='testing'),
)
