#_*_ coding: utf8 _*_
import os
from django.conf.urls import patterns, include, url
from BookSite import *
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

media = os.path.join(
	os.path.dirname(__file__),'../media'		
)


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'UsedBookSite.views.home', name='home'),
    # url(r'^UsedBookSite/', include('UsedBookSite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    (r'^$','BookSite.views.main_page'),
	(r'^media/(?P<path>.*)/$','django.views.static.serve', { 'document_root': media }),
	(r'^search/(?P<keyword>\S+)/Page(?P<page>\d+)/$','BookSite.views.SearchPage'),
	(r'^search/(?P<keyword>\S+)/$','BookSite.views.SearchPage'),
    (r'^latest/$','BookSite.views.LatestPage'),
    (r'^latest/Page(?P<page>\d+)/$','BookSite.views.LatestPage'),
    (r'^evernote/$','BookSite.views.evernote'),
	#(r'^$',)
)
