from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from views import *

urlpatterns = staticfiles_urlpatterns() + patterns('',
    url(r'^$', index),
    url(r'^actual/(?P<id>\d{1,})/$', actual),
    url(r'^about/$', static_page, {'id': '1'}),
    url(r'^contacts/$', static_page, {'id': '2'}),
    url(r'^partners/$', static_page, {'id': '3'}),
    )
