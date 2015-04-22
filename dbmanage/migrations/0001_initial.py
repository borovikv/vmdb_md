# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Databases',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('database_id', models.CharField(max_length=25)),
                ('database_password', models.CharField(max_length=32)),
                ('last_update', models.DateField(null=True, blank=True)),
                ('registration_type', models.PositiveSmallIntegerField(default=3, choices=[(-1, b'perpetual'), (3, b'standard'), (10, b'extended')])),
            ],
        ),
        migrations.CreateModel(
            name='RegisteredDatabases',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('counter', models.PositiveSmallIntegerField(default=0)),
                ('first_date', models.DateField()),
                ('last_date', models.DateField(auto_now_add=True)),
                ('database', models.ForeignKey(to='dbmanage.Databases')),
            ],
        ),
        migrations.CreateModel(
            name='Updating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_update', models.DateField(null=True, blank=True)),
            ],
        ),
    ]
