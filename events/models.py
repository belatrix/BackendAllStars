from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Participant(models.Model):
    name = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True)
    birth_date = models.DateField(blank=True, null=True)
    carreer = models.CharField(max_length=200, blank=True, null=True)
    educational_center = models.CharField(max_length=200, blank=True, null=True)
    english_level = models.CharField(max_length=200, blank=True, null=True)
    facebook_account = models.CharField(max_length=200, blank=True, null=True)
    twitter_account = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = 'participants'
        ordering = ['name', 'lastname', 'email']


class Event(models.Model):
    title = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    collaborators = models.ManyToManyField('employees.Employee', blank=True)
    participants = models.ManyToManyField(Participant, blank=True)

    class Meta:
        verbose_name_plural = 'events'
        ordering = ['-datetime', 'title']


class Talk(models.Model):
    title = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    speaker = models.ForeignKey('employees.Employee', blank=True, null=True)
    participants = models.ManyToManyField(Participant, blank=True)

    class Meta:
        verbose_name_plural = 'talks'
        ordering = ['-datetime', 'title']