from __future__ import unicode_literals

from django.db import models


class Participant(models.Model):
    name = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    birth_date = models.DateField(blank=True, null=True)
    carreer = models.CharField(max_length=200, blank=True, null=True)
    educational_center = models.CharField(max_length=200, blank=True, null=True)
    english_level = models.CharField(max_length=200, blank=True, null=True)
    facebook_account = models.CharField(max_length=200, blank=True, null=True)
    twitter_account = models.CharField(max_length=200, blank=True, null=True)


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200, blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    collaborators = models.ManyToManyField('employees.Employee', blank=True)
    participants = models.ManyToManyField(Participant, blank=True)


class Talk(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200, blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    speaker = models.ForeignKey('employees.Employee', blank=True)
    participants = models.ManyToManyField(Participant, blank=True)