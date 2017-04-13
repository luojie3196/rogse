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
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


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


class UserProfileManager(BaseUserManager):
    def create_user(self, username, email, sex, real_name,
                    phone_num, password=None, *args, **kwargs):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email or not username:
            raise ValueError('Users must have an username and email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            sex=sex,
            real_name=real_name,
            phone_num=phone_num,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, sex):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username=username,
            email=email,
            password=password,
            sex=sex,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


SEX_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'),
)


class UserProfile(AbstractBaseUser):
    username = models.CharField(
        verbose_name='login username',
        max_length=150,
        unique=True,
    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    real_name = models.CharField(
        verbose_name='real name',
        max_length=150,
    )
    sex = models.CharField(max_length=18, choices=SEX_CHOICES, default='male')
    phone_num = models.CharField(
        verbose_name='Phone number',
        max_length=255,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'sex']

    def get_full_name(self):
        # The user is identified by their username
        return self.username

    def get_short_name(self):
        # The user is identified by their username
        return self.username

    def __str__(self):              # __unicode__ on Python 2
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

