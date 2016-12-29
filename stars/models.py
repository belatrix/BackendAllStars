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
