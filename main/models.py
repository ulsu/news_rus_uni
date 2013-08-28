# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from tinymce.models import HTMLField
from datetime import datetime
import os
from django.utils.encoding import force_unicode
import news_rus_uni.settings as SETTINGS
from django.utils.safestring import mark_safe
from django import forms
from mce_filebrowser.admin import MCEFilebrowserAdmin
from photologue.models import Gallery


class RenameFilesModel(models.Model):
    """
    Abstract model implementing a two-phase save in order to rename
    `FileField` and `ImageField` filenames after saving.  This allows the
    final filenames to contain information like the primary key of the model.

    Example:

        class Photo(RenameFilesModel):
            file = models.ImageField(upload_to='uploads/temp')

            RENAME_FILES = {
                'file': {'dest': 'uploads/photos', 'keep_ext': True}
            }

        >>> photo = Photo(file='uploads/temp/photo.jpg')
        >>> photo.pk

        >>> photo.save()
        >>> photo.pk
        1
        >>> photo.file
        <ImageFieldFile: uploads/photos/1.jpg>

    If the 'dest' option is a callable, it will be called with the model
    instance (guaranteed to be saved) and the currently saved filename, and
    must return the new filename.  Otherwise, the filename is determined by
    'dest' and the model's primary key.

    If a file already exists at the resulting path, it is deleted.  This is
    desirable if the filename should always be the primary key, for instance.
    To avoid this behavior, write a 'dest' handler that results in a unique
    filename.

    If 'keep_ext' is True (the default), the extension of the previously saved
    filename will be appended to the primary key to construct the filename.
    The value of 'keep_ext' is not considered if 'dest' is a callable.

    """
    RENAME_FILES = {}

    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False):
        rename_files = getattr(self, 'RENAME_FILES', None)
        if rename_files:
            super(RenameFilesModel, self).save(force_insert, force_update)
            force_insert, force_update = False, True

            for field_name, options in rename_files.iteritems():
                field = getattr(self, field_name)
                file_name = force_unicode(field)
                name, ext = os.path.splitext(file_name)
                keep_ext = options.get('keep_ext', True)
                final_dest = options['dest']
                if callable(final_dest):
                    final_name = final_dest(self, file_name)
                else:
                    final_name = os.path.join(final_dest, '%s' % (self.pk,))
                    final_name = '/'.join(final_name.split('\\'))
                    if keep_ext:
                        final_name += ext
                if file_name != final_name:
                    field.storage.delete(final_name)
                    field.storage.save(final_name, field)
                    field.close()
                    field.storage.delete(file_name)
                    setattr(self, field_name, final_name)

        super(RenameFilesModel, self).save(force_insert, force_update)


class Newspaper(models.Model):
    title = models.CharField(max_length=255)
    intro = RichTextField()
    number = models.FileField(upload_to='newspapers')
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
    intro = RichTextField()
    body = RichTextField()
    order = models.IntegerField()
    author = models.CharField(max_length=255)
    number = models.ForeignKey(Newspaper)
    gallery = models.ForeignKey(Gallery, null=True, blank=True)

    def __unicode__(self):
        return '%s (%s)' % (self.title, self.number.title)

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author',)

admin.site.register(Article, ArticleAdmin)


class ActualInfo(RenameFilesModel):
    title = models.CharField(max_length=255)
    intro = HTMLField()
    body = HTMLField()
    publish = models.DateTimeField(default=datetime.now())
    display = models.BooleanField(default=True)
    picture = models.ImageField(upload_to='temp')

    def media_path(self):
        return SETTINGS.MEDIA_URL + self.picture.name

    RENAME_FILES = {
        'picture': {'dest': 'actual_thumbs', 'keep_ext': True}
    }

    def picture_extension(self):
        name, extension = os.path.splitext(self.picture.name)
        return extension

    def __unicode__(self):
        return self.title

    class Media:
        js = ("/js/tiny_mce.js", "/js/textareas.js")

class ActualInfoAdmin(MCEFilebrowserAdmin):
    list_display = ('title', 'publish',)

admin.site.register(ActualInfo, ActualInfoAdmin)



class StaticPage(models.Model):
    title = models.CharField(max_length=255)
    body = HTMLField()

    def __unicode__(self):
        return self.title

class StaticPageAdmin(MCEFilebrowserAdmin):
    list_display = ('title',)

admin.site.register(StaticPage, StaticPageAdmin)