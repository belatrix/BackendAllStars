from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    weight = models.PositiveSmallIntegerField(default=1)
    comment_required = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['weight']


@python_2_unicode_compatible
class Subcategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'subcategories'
        ordering = ['name']


@python_2_unicode_compatible
class Keyword(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'keywords'
        ordering = ['name']
