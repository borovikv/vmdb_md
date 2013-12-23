try:
    from django.conf.urls import url, patterns
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('DBAuthentication.views',
   url(r'online/$', 'registry_online', name='registry-online'),
   url(r'phone/$', 'registry_phone', name='registry-online'),
)
