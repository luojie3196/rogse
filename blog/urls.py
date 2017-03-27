#!/usr/bin/python
# encoding:utf-8

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^author/$', views.author),
]