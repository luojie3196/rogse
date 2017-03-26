# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
from django.utils.html import format_html


class Douban(models.Model):
    title = models.TextField()
    movie_id = models.IntegerField()
    rate = models.FloatField()
    url = models.CharField(max_length=128)
    cover = models.CharField(max_length=255)
    director = models.TextField()
    scriptwriter = models.TextField()
    protagonist = models.TextField()
    m_type = models.CharField(max_length=128)
    region = models.TextField()
    language = models.CharField(max_length=255)
    release_time = models.TextField()
    numbers = models.CharField(max_length=30)
    run_time = models.CharField(max_length=128)
    other_title = models.CharField(max_length=255)
    imdb_link = models.CharField(max_length=128)
    website = models.CharField(max_length=128)
    comment_num = models.IntegerField()
    summary = models.TextField()

    class Meta:
        managed = False
        db_table = 'douban'
        verbose_name_plural = '豆瓣'

    def __str__(self):
        return '%s %s' % (self.title, self.rate)

    def colored_title(self):
        return format_html(
            '<span style="color: #000000;">{}</span>',
            self.title,
        )

    colored_title.admin_order_field = 'title'

