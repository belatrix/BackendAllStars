from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Participant(models.Model):
    fullname = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    carreer = models.CharField(max_length=200, blank=True, null=True)
    educational_center = models.CharField(max_length=200, blank=True, null=True)
    english_level = models.CharField(max_length=200, blank=True, null=True)
    facebook_id = models.CharField(max_length=200, blank=True, null=True)
    facebook_link = models.URLField(max_length=200, blank=True, null=True)
    twitter_id = models.CharField(max_length=200, blank=True, null=True)
    twitter_link = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.fullname

    class Meta:
        verbose_name_plural = 'participants'
        ordering = ['-pk', 'fullname', 'email']


@python_2_unicode_compatible
class Event(models.Model):
    title = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    collaborators = models.ManyToManyField('employees.Employee', blank=True)
    participants = models.ManyToManyField(Participant, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'events'
        ordering = ['-datetime', 'title']


@python_2_unicode_compatible
class Talk(models.Model):
    title = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    url = models.URLField(max_length=200, blank=True, null=True)
    speaker = models.ForeignKey('employees.Employee', blank=True, null=True)
    participants = models.ManyToManyField(Participant, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'talks'
        ordering = ['-datetime', 'title']


class Comment(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    message = models.TextField()
    author = models.ForeignKey(Participant)
    approved_by = models.ForeignKey('employees.Employee', null=True, blank=True)
    event = models.ForeignKey(Event, null=True, blank=True)
    talk = models.ForeignKey(Talk, null=True, blank=True)

    class Meta:
        ordering = ['-datetime']
        verbose_name_plural = 'comments'
