from django.contrib import admin
from douban import models
from douban.forms import UserProfileChangeForm, UserProfileCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

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


# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ('id', 'username', 'email', 'real_name',
#                     'sex', 'phone_num', 'is_active', 'is_admin')
#     list_filter = ('sex', 'is_active', 'is_admin')
#     search_fields = ('username', 'email', 'real_name', 'phone_num')
#     list_per_page = 20


class UserProfileAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserProfileChangeForm
    add_form = UserProfileCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('id', 'username', 'email', 'real_name',
                    'sex', 'phone_num', 'is_active', 'is_admin')
    list_filter = ('sex', 'is_active', 'is_admin',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('real_name', 'sex', 'phone_num',)}),
        ('Permissions', {'fields': ('is_active', 'is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password', 'password2',
                       'real_name', 'sex', 'phone_num')}
        ),
    )
    search_fields = ('username', 'email',)
    ordering = ('username', 'email',)
    filter_horizontal = ()

admin.site.register(models.Douban, DoubanAdmin)
# admin.site.register(models.UserProfile, UserProfileAdmin)

# Now register the new UserAdmin...
admin.site.register(models.UserProfile, UserProfileAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
