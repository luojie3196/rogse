#!/usr/bin/python
# encoding:utf-8

from django.forms import ModelForm, Textarea
from blog import models
from django.utils.translation import ugettext_lazy as _


class AuthorForm(ModelForm):
    class Meta:
        model = models.Author
        # fields = ['name', 'email']
        exclude = []
        # fields = '__all__'
        # widgets = {
        #     'name': Textarea(attrs={'cols': 20, 'rows': 20}),
        # }
        labels = {
            'name': _('Full name'),
        }
        help_texts = {
            'name': _('Please input your full name.<br/>'),
        }
        error_messages = {
            'name': {
                'max_length': _("This writer's name is too long."),
            },
        }


class BlogForm(ModelForm):
    class Meta:
        model = models.Blog
        fields = ['name', 'tagline']


class EntryForm(ModelForm):
    class Meta:
        model = models.Entry
        fields = ['blog', 'headline', 'body_text', 'pub_date', 'mod_date',
                  'authors', 'n_comments', 'n_pingbacks', 'rating']


class ArticleForm(ModelForm):
    class Meta:
        model = models.Article
        fields = '__all__'
