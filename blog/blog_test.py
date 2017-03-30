#!/usr/bin/python
# encoding:utf-8

import os
import django
from blog import models

os.environ['DJANGO_SETTINGS_MODULE'] = 'rogse.settings'
django.setup()

# do your test
entry = models.Entry.objects.get(pk=1)
print(entry)
