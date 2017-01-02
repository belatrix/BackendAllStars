# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-01-02 00:18
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('icon', models.URLField(blank=True, null=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'badges',
            },
        ),
        migrations.CreateModel(
            name='EmployeeBadge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('assigned_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                                  related_name='employeebadge_assigned_by',
                                                  to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                              related_name='employeebadge_to',
                                              to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['date', 'to_user'],
            },
        ),
        migrations.CreateModel(
            name='Star',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('text', models.CharField(blank=True, max_length=140, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories.Category')),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='star_from', to=settings.AUTH_USER_MODEL)),
                ('keyword', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories.Keyword')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='star_to', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['date', 'to_user'],
            },
        ),
    ]
