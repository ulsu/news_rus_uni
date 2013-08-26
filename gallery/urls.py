from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
from views import *

urlpatterns = patterns('',
    url(r'^$', index),
)
