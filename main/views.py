# -*- coding: utf-8 -*-
from django.template import loader, Context, RequestContext, Template
from django.http import HttpResponse, Http404
from models import *
from django.conf import settings
from django.shortcuts import redirect
from django.views.static import serve


def index(request):
    n = Newspaper.objects.filter(active=True).latest()
    a = Article.objects.filter(number=n)
    t = loader.get_template("index.html")
    c = RequestContext(request, {'number': n, 'articles': a})
    return HttpResponse(t.render(c))

def mediaserver(request, path):
    return serve(request, path, settings.MEDIA_ROOT)