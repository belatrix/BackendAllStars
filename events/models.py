from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Event(models.Model):
    name = models.CharField(max_length=100)
    image = models.URLField(blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    registration_url = models.URLField(blank=True, null=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    is_upcoming = models.BooleanField(default=True)
    location = models.ForeignKey('employees.Location')

    def __str__(self):
        return self.name

    class Meta(object):
        verbose_name_plural = 'events'
        ordering = ['-datetime']


class EventActivity(models.Model):
    event = models.ForeignKey(Event)
    datetime = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=140)

    class Meta(object):
        verbose_name_plural = 'event activities'
        ordering = ['-datetime']


class EventParticipant(models.Model):
    event = models.ForeignKey(Event)
    participant = models.ForeignKey('employees.Employee')
    datetime = models.DateTimeField(auto_now_add=True)

    class Meta(object):
        verbose_name_plural = 'event participants'
        ordering = ['-datetime']
        unique_together = ("event", "participant")
