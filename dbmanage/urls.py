try:
    from django.conf.urls import url, patterns
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('dbmanage.views',
                       url(r'online/$', 'registry_online', name='db_registry-online'),
                       url(r'phone/$', 'registry_phone', name='db_registry-phone'),
                       url(r'update/$', 'update', name='db_export'),
                       url(r'update/check/$', 'check', name='update-check'),
                       url(r'update/confirm/$', 'confirm', name='update-confirm'),
                       url(r'upload/$', 'upload'),
)