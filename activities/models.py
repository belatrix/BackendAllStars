from __future__ import unicode_literals

from django.db import models


class Activity(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=140)
    to_user = models.ForeignKey('employees.Employee', related_name='%(class)s_to', blank=True, null=True)

    class Meta(object):
        ordering = ['-datetime']
        verbose_name_plural = 'activities'


class Message(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=140)
    from_user = models.ForeignKey('employees.Employee', related_name='%(class)s_from')
    to_user = models.CharField(max_length=250)

    class Meta(object):
        ordering = ['-datetime']
        verbose_name_plural = 'messages'
