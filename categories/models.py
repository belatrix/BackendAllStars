from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    weight = models.PositiveSmallIntegerField(default=1)
    comment_required = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta(object):
        verbose_name_plural = 'categories'
        ordering = ['weight']


@python_2_unicode_compatible
class Keyword(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta(object):
        verbose_name_plural = 'keywords'
        ordering = ['name']
