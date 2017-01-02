from __future__ import unicode_literals

from django.db import models


class Star(models.Model):
    date = models.DateTimeField(auto_now=True)
    text = models.CharField(max_length=140, null=True, blank=True)
    from_user = models.ForeignKey('employees.Employee',
                                  related_name='%(class)s_from')
    to_user = models.ForeignKey('employees.Employee',
                                related_name='%(class)s_to')
    category = models.ForeignKey('categories.Category')
    keyword = models.ForeignKey('categories.Keyword')

    class Meta(object):
        ordering = ['date', 'to_user']


class Badge(models.Model):
    name = models.CharField(max_length=100)
    icon = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta(object):
        verbose_name_plural = 'badges'
        ordering = ['name']


class EmployeeBadge(models.Model):
    date = models.DateTimeField(auto_now=True)
    to_user = models.ForeignKey('employees.Employee',
                                related_name='%(class)s_to')
    assigned_by = models.ForeignKey('employees.Employee',
                                    related_name='%(class)s_assigned_by')
    badge = models.ForeignKey(Badge)

    class Meta(object):
        ordering = ['date', 'to_user']
        unique_together = ("to_user", "badge")
