# -*- coding: utf-8 -*-
from django.template import loader, Context, RequestContext, Template
from django.http import HttpResponse, Http404
from models import *
from django.conf import settings
from django.shortcuts import redirect
from django.views.static import serve


def index(request):
    number = Newspaper.objects.filter(active=True).latest()
    articles = Article.objects.filter(number=number)

    actual = ActualInfo.objects.filter(display=True)

    t = loader.get_template("index.html")
    c = RequestContext(request, {'number': number, 'articles': articles, 'actual':actual})
    return HttpResponse(t.render(c))

def mediaserver(request, path):
    return serve(request, path, settings.MEDIA_ROOT)