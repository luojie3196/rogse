from django.contrib import admin
from blog import models
# Register your models here.


class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email']
    list_editable = ['name', 'email']

admin.site.register(models.Author, AuthorAdmin)
