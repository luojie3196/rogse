from django.db import models
from django.utils.html import format_html
# Create your models here.


class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __str__(self):              # __unicode__ on Python 2
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=200, unique=True)
    email = models.EmailField()

    def __str__(self):              # __unicode__ on Python 2
        return self.name

STATUS_CHOICES = (
    ('d', 'Draft'),
    ('p', 'Published'),
    ('w', 'Withdrawn'),
)


class Entry(models.Model):
    blog = models.ForeignKey(Blog)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField()
    authors = models.ManyToManyField(Author)
    n_comments = models.IntegerField()
    n_pingbacks = models.IntegerField()
    rating = models.IntegerField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='d')

    def __str__(self):              # __unicode__ on Python 2
        return self.headline

    def colored_status(self):
        if self.status == "p":
            format_td = format_html(
                '<span style="padding:2px;background-color:green;color:white">Published</span>')
        elif self.status == "d":
            format_td = format_html(
                '<span style="padding:2px;background-color:gray;color:white">Draft</span>')
        elif self.status == "w":
            format_td = format_html(
                '<span style="padding:2px;background-color:red;color:white">Withdrawn</span>')
        return format_td
    colored_status.short_description = 'status'


class Article(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='d')

    def __str__(self):              # __unicode__ on Python 2
        return self.title
