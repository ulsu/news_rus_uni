# -*- coding: utf-8 -*-
from django import forms
from yacaptcha.fields import YaCaptchaField, YaCaptcha

class ContactForm(forms.Form):
    name = forms.CharField(label='Имя')
    email = forms.EmailField(label='E-mail', widget=forms.TextInput(attrs={ 'required': 'true' }))
    body = forms.CharField(widget=forms.Textarea(attrs={'style': 'width: 500px;', 'required': 'true'}),
           label='Текст сообщения')
    captcha = YaCaptchaField(label='', widget=YaCaptcha(attrs={ 'required': 'true' }))