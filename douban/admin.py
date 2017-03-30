from django.contrib import admin
from douban import models

# Register your models here.


class DoubanAdmin(admin.ModelAdmin):
    list_display = ('colored_title', 'movie_id', 'rate', 'director', 'scriptwriter',
                    'protagonist', 'm_type', 'region', 'language', 'release_time',
                    'numbers', 'run_time', 'other_title')
    list_filter = ('rate',)
    search_fields = ['title', 'director']
    # fields = ('rate', 'title', 'other_title')
    list_editable = ('rate',)
    list_per_page = 20


admin.site.register(models.Douban, DoubanAdmin)
