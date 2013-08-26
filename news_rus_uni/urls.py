from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from main.views import index, mediaserver

urlpatterns = staticfiles_urlpatterns() + patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^mce_filebrowser/', include('mce_filebrowser.urls')),
    url(r'^photologue/', include('photologue.urls')),
    url(r'^media/(?P<path>.*)$', mediaserver),
    url(r'^gallery/$', include('gallery.urls')),
    url(r'^', include('main.urls')),
)
