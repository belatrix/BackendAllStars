from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.utils.encoding import python_2_unicode_compatible
from rest_framework.authtoken.models import Token


@python_2_unicode_compatible
class Role(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Employee(AbstractUser):
    role = models.ForeignKey(Role, null=True, blank=True)
    skype_id = models.CharField(max_length=200, null=True, blank=True)
    last_month_score = models.PositiveIntegerField(default=0)
    current_month_score = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=0)
    score = models.PositiveIntegerField(default=0)
    avatar = models.ImageField(upload_to='avatar', null=True, blank=True)
    categories = models.ManyToManyField('categories.Category', blank=True)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)