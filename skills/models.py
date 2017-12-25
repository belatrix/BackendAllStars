from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible



@python_2_unicode_compatible
class SkillCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    icon = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta(object):
        verbose_name_plural = 'skill categories'
        ordering = ['name']


@python_2_unicode_compatible
class Skill(models.Model):
    name = models.CharField(max_length=50, unique=True)
    category = models.ManyToManyField(SkillCategory, blank=True)
    icon = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta(object):
        verbose_name_plural = 'skills'
        ordering = ['name']
