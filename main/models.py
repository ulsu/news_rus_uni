# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from datetime import datetime

class Newspaper(models.Model):
    title = models.CharField(max_length=255)
    intro = RichTextField()
    number = models.FileField(upload_to='/home/naawha/PycharmProjects/news_rus_uni/media/newspapers/')
    active = models.BooleanField(default=False)
    date = models.DateTimeField(default=datetime.now())

    class Meta:
      get_latest_by = 'date'

    def __unicode__(self):
        return self.title

class NewspaperAdmin(admin.ModelAdmin):
    list_display = ('title', 'number', 'active',)

admin.site.register(Newspaper, NewspaperAdmin)


class Article(models.Model):
    title = models.CharField(max_length=255)
    body = RichTextField()
    order = models.IntegerField()
    author = models.CharField(max_length=255)
    number = models.ForeignKey(Newspaper)

    def __unicode__(self):
        return '%s (%s)' % (self.title, self.number.title)

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author',)

admin.site.register(Article, ArticleAdmin)