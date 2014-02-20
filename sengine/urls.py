"""
Created on Jul 16, 2013

@author: drifter
"""
from django.conf.urls import patterns, url

urlpatterns = patterns('sengine.views',
    url(r'^$', 'search', name='search'),
)