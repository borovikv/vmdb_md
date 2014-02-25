try:
    from django.conf.urls import url, patterns
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('dbmanage.views',
                       url(r'online/$', 'registry_online', name='db_registry-online'),
                       url(r'phone/$', 'registry_phone', name='db_registry-online'),
)
