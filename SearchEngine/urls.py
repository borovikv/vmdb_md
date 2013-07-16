'''
Created on Jul 16, 2013

@author: drifter
'''
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('SearchEngine.views',
    url(r'^$', 'search', name='search'),
    url(r'^result/$', 'result', name='search-result'),
)