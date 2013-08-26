# -*- coding: utf-8 -*-
from django.template import loader, Context, RequestContext, Template
from django.http import HttpResponse, Http404
from models import *
from django.conf import settings
from django.shortcuts import redirect
from django.views.static import serve
from photologue.models import Gallery, Photo


def index(request):
    galleries = Gallery.objects.filter(is_public=True)
    t = loader.get_template("gallery/main.html")
    c = RequestContext(request, {'galleries': galleries})
    return HttpResponse(t.render(c))
