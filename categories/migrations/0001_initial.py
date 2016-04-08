# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-08 04:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('weight', models.PositiveSmallIntegerField(default=1)),
            ],
            options={
                'ordering': ['weight'],
                'verbose_name_plural': 'categories',
            },
        ),
    ]
