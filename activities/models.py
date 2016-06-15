from __future__ import unicode_literals

from django.db import models


class Activity(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    detail = models.TextField(editable=False)
    to_user = models.ForeignKey('employees.Employee',
                                related_name='%(class)s_to',
                                blank=True, null=True)
    from_user = models.ForeignKey('employees.Employee', related_name='%(class)s_from')

    class Meta:
        ordering = ['-datetime']
        verbose_name_plural = 'activities'


class Message(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    from_user = models.ForeignKey('employees.Employee', related_name='%(class)s_from')
    to_user = models.ForeignKey('employees.Employee', related_name='%(class)s_to')

    class Meta:
        ordering = ['-datetime']
        verbose_name_plural = 'messages'
