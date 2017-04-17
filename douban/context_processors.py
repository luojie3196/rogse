#!/usr/bin/python
# encoding:utf-8

from douban.models import Douban
from django.http import Http404


def douban_obj(request):
    try:
        db_obj = Douban.objects.all()
    except Douban.DoesNotExist:
        raise Http404("Douban does not exist")
    return {'douban_obj': db_obj, 'douban_obj_lens': db_obj.count()}
