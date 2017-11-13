# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-10-25 14:45
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employees', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.URLField(blank=True, null=True)),
                ('datetime', models.DateTimeField(blank=True, null=True)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('registration_url', models.URLField(blank=True, null=True)),
                ('description', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
                ('is_upcoming', models.BooleanField(default=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employees.Location')),
            ],
            options={
                'ordering': ['-datetime'],
                'verbose_name_plural': 'events',
            },
        ),
        migrations.CreateModel(
            name='EventActivity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('text', models.CharField(max_length=140)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.Event')),
            ],
            options={
                'ordering': ['-datetime'],
                'verbose_name_plural': 'event activities',
            },
        ),
        migrations.CreateModel(
            name='EventParticipant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.Event')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-datetime'],
                'verbose_name_plural': 'event participants',
            },
        ),
        migrations.AlterUniqueTogether(
            name='eventparticipant',
            unique_together=set([('event', 'participant')]),
        ),
    ]
