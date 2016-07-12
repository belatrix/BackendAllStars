from __future__ import unicode_literals

from categories.models import Category
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.utils.encoding import python_2_unicode_compatible
from rest_framework.authtoken.models import Token
from uuid import uuid4
from time import time


@python_2_unicode_compatible
class Location(models.Model):
    name = models.CharField(max_length=100)
    icon = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'locations'
        ordering = ['name']


@python_2_unicode_compatible
class Role(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'roles'
        ordering = ['name']


def avatar_filename(instance, filename):
    timestamp = int(time())
    return 'avatar/%s%d.jpg' % (instance, timestamp)


def get_default_category():
    return Category.objects.get(name__icontains='Coworker')


class Employee(AbstractUser):
    role = models.ForeignKey(Role, null=True, blank=True)
    location = models.ForeignKey(Location, null=True, blank=True)
    skype_id = models.CharField(max_length=200, null=True, blank=True)
    level = models.PositiveIntegerField(default=0)
    categories = models.ManyToManyField('categories.Category', blank=True)
    reset_password_code = models.UUIDField(default=None, null=True, blank=True)
    avatar = models.ImageField(upload_to=avatar_filename, null=True, blank=True)
    is_base_profile_complete = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)

    # Given stars
    yesterday_given = models.PositiveIntegerField(default=0)
    today_given = models.PositiveIntegerField(default=0)
    last_month_given = models.PositiveIntegerField(default=0)
    last_year_given = models.PositiveIntegerField(default=0)
    current_month_given = models.PositiveIntegerField(default=0)
    current_year_given = models.PositiveIntegerField(default=0)
    total_given = models.PositiveIntegerField(default=0)

    # Received stars
    yesterday_received = models.PositiveIntegerField(default=0)
    today_received = models.PositiveIntegerField(default=0)
    total_score = models.PositiveIntegerField(default=0)
    last_month_score = models.PositiveIntegerField(default=0)
    last_year_score = models.PositiveIntegerField(default=0)
    current_month_score = models.PositiveIntegerField(default=0)
    current_year_score = models.PositiveIntegerField(default=0)

    def evaluate_level(self):
        if self.total_score == (self.level + 1) * settings.NEXT_LEVEL_SCORE:
            self.level += 1
            return

    def add_stars(self, number):
        self.today_received += number
        self.total_score += number
        self.current_month_score += number
        self.current_year_score += number
        return

    def add_stars_given(self, number):
        self.today_given += number
        self.total_given += number
        self.current_month_given += number
        self.current_year_given += number
        return

    def generate_reset_password_code(self):
        uuid_code = uuid4()
        self.reset_password_code = str(uuid_code)
        self.save()
        return self.reset_password_code

    def save(self, *args, **kwargs):
        is_new = False
        if not self.pk:
            is_new = True

        first_name = self.first_name
        last_name = self.last_name
        skype = self.skype_id
        if first_name and last_name and skype:
            self.is_base_profile_complete = True
        else:
            self.is_base_profile_complete = False
        super(Employee, self).save(*args, **kwargs)

        if is_new:
            self.categories.add(get_default_category())

    class Meta:
        ordering = ['first_name', 'last_name', 'username']


class EmployeeDevice(models.Model):
    username = models.ForeignKey(Employee)
    android_device = models.CharField(max_length=100, blank=True, null=True)
    ios_device = models.CharField(max_length=100, blank=True, null=True)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
