from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.shortcuts import render

admin.autodiscover()

urlpatterns = patterns('',

                       # Uncomment the admin/doc line below to enable admin documentation:
                       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       url(r'^$', lambda request: render(request, 'main.html'), name="login"),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^registry/', include('dbmanage.urls')),
                       url(r'^manage/', include('dbmanage.urls')),

                       url(r'^accounts/login/$', login, name="login"),
                       url(r'^accounts/logout/$', logout, name="logout"),
)