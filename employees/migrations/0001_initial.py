# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-12-12 13:53
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import employees.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=30, unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.')], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('skype_id', models.CharField(blank=True, max_length=200, null=True)),
                ('level', models.PositiveIntegerField(default=0)),
                ('reset_password_code', models.UUIDField(blank=True, default=None, null=True)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to=employees.models.avatar_filename)),
                ('is_base_profile_complete', models.BooleanField(default=False)),
                ('is_blocked', models.BooleanField(default=False)),
                ('is_password_reset_required', models.BooleanField(default=True)),
                ('yesterday_given', models.PositiveIntegerField(default=0)),
                ('today_given', models.PositiveIntegerField(default=0)),
                ('last_month_given', models.PositiveIntegerField(default=0)),
                ('last_year_given', models.PositiveIntegerField(default=0)),
                ('current_month_given', models.PositiveIntegerField(default=0)),
                ('current_year_given', models.PositiveIntegerField(default=0)),
                ('total_given', models.PositiveIntegerField(default=0)),
                ('yesterday_received', models.PositiveIntegerField(default=0)),
                ('today_received', models.PositiveIntegerField(default=0)),
                ('total_score', models.PositiveIntegerField(default=0)),
                ('last_month_score', models.PositiveIntegerField(default=0)),
                ('last_year_score', models.PositiveIntegerField(default=0)),
                ('current_month_score', models.PositiveIntegerField(default=0)),
                ('current_year_score', models.PositiveIntegerField(default=0)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'ordering': ['first_name', 'last_name', 'username'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('android_device', models.CharField(blank=True, max_length=200, null=True)),
                ('ios_device', models.CharField(blank=True, max_length=200, null=True)),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('icon', models.URLField(blank=True, null=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'locations',
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('weight', models.PositiveSmallIntegerField(default=1)),
            ],
            options={
                'ordering': ['weight'],
                'verbose_name_plural': 'positions',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'roles',
            },
        ),
        migrations.AddField(
            model_name='employee',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='employees.Location'),
        ),
        migrations.AddField(
            model_name='employee',
            name='position',
            field=models.ManyToManyField(blank=True, to='employees.Position'),
        ),
        migrations.AddField(
            model_name='employee',
            name='role',
            field=models.ManyToManyField(blank=True, to='employees.Role'),
        ),
        migrations.AddField(
            model_name='employee',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
