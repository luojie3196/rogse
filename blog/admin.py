from django.contrib import admin
from blog import models
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core import serializers
# Register your models here.


class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email']
    list_editable = ['name', 'email']


class EntryAdmin(admin.ModelAdmin):
    list_display = ['blog', 'headline', 'body_text', 'pub_date', 'mod_date',
                  'n_comments', 'n_pingbacks', 'rating']


class BlogAdmin(admin.ModelAdmin):
    list_display = ['name', 'tagline']


def make_published(modeladmin, request, queryset):
    queryset.update(status='p')
make_published.short_description = "Mark selected stories as published"


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    ordering = ['title']
    actions = [make_published]  # Model Admin action


def export_selected_objects(modeladmin, request, queryset):
    selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
    ct = ContentType.objects.get_for_model(queryset.model)
    return HttpResponseRedirect("/export/?ct=%s&ids=%s" % (ct.pk, ",".join(selected)))


def export_as_json(modeladmin, request, queryset):
    response = HttpResponse(content_type="application/json")
    serializers.serialize("json", queryset, stream=response)
    return response

admin.site.register(models.Author, AuthorAdmin)
admin.site.register(models.Entry, EntryAdmin)
admin.site.register(models.Blog, BlogAdmin)
admin.site.register(models.Article, ArticleAdmin)
admin.site.add_action(export_as_json, 'export_selected')  # global action

# Globally disable delete selected
# admin.site.disable_action('delete_selected')
