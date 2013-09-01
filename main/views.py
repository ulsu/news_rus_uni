# -*- coding: utf-8 -*-
from django.template import loader, Context, RequestContext, Template
from django.http import HttpResponse, Http404
from models import *
from django.conf import settings
from django.shortcuts import redirect
from django.views.static import serve
from forms import ContactForm
from django.core.mail import send_mail, BadHeaderError
from django.views.decorators.csrf import csrf_exempt


def index(request):
    number = Newspaper.objects.filter(active=True).latest()
    articles = Article.objects.filter(number=number).order_by('order')

    t = loader.get_template("index.html")
    c = RequestContext(request, {'number': number, 'articles': articles})
    return HttpResponse(t.render(c))


def actual(request, id):
    actual = ActualInfo.objects.get(id=id)
    t = loader.get_template("simple_page.html")
    c = RequestContext(request, {'item': actual})
    return HttpResponse(t.render(c))


def news(request, id):
    novelty = NewsInfo.objects.get(id=id)
    t = loader.get_template("simple_page.html")
    c = RequestContext(request, {'item': novelty})
    return HttpResponse(t.render(c))


def actual_archive(request):
    actual = ActualInfo.objects.all()
    t = loader.get_template("actual_archive.html")
    c = RequestContext(request, {'actual': actual})
    return HttpResponse(t.render(c))


def news_archive(request):
    news = NewsInfo.objects.all()
    t = loader.get_template("news_archive.html")
    c = RequestContext(request, {'news': news})
    return HttpResponse(t.render(c))


def article(request, id):
    article = Article.objects.get(id=id)
    t = loader.get_template("article.html")
    c = RequestContext(request, {'article': article})
    return HttpResponse(t.render(c))


def mediaserver(request, path):
    return serve(request, path, settings.MEDIA_ROOT)


def static_page(request, id):
    page = StaticPage.objects.get(id=id)
    t = loader.get_template("simple_page.html")
    c = RequestContext(request, {'item': page})
    return HttpResponse(t.render(c))


@csrf_exempt
def contacts(request):
    if request.method == "POST":
        cform = ContactForm(data = request.POST)
        if cform.is_valid():
            pass
            # subject = '"Новости Российских Университетов" (форма обратной связм)'
            # message = cform.body
            # email = cform.email
            # send_mail(subject, message, email, (settings.DEFAULT_FROM_EMAIL,))
            t = loader.get_template("message.html")
            c = RequestContext(request, cform.data)
            return HttpResponse(t.render(c))
        else:
            t = loader.get_template("form_errors.html")
            c = RequestContext(request, {'errors': cform.errors})
            return HttpResponse(t.render(c))
    else:
        page = StaticPage.objects.get(id=2)
        cform = ContactForm()
        t = loader.get_template("contacts_form.html")
        c = RequestContext(request, {'item': page, 'cform': cform})
        return HttpResponse(t.render(c))


def archive(request):
    numbers = Newspaper.objects.filter(active=True)

    t = loader.get_template("archive.html")
    c = RequestContext(request, {'numbers': numbers})
    return HttpResponse(t.render(c))