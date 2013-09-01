from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from views import *

urlpatterns = staticfiles_urlpatterns() + patterns('',
    url(r'^$', index),
    url(r'^actual/(?P<id>\d{1,})/$', actual),
    url(r'^actual/archive/$', actual_archive),
    url(r'^news/(?P<id>\d{1,})/$', news),
    url(r'^news/archive/$', news_archive),
    url(r'^article/(?P<id>\d{1,})/$', article),
    url(r'^about/$', static_page, {'id': '1'}),
    url(r'^contacts/$', contacts),
    url(r'^partners/$', static_page, {'id': '3'}),
    url(r'^archive/$', archive),
)
