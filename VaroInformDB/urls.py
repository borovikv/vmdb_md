from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'VaroInformDB.views.home', name='home'),
    # url(r'^VaroInformDB/', include('VaroInformDB.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^search/', include('SearchEngine.urls')),
    url(r'^login/$', login, name="login"),
    url(r'^logout/$', logout, name="logout"),
    #url(r'^register/$', register, name="register"),
)


