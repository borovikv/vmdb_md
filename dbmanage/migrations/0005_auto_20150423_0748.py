# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dbmanage', '0004_auto_20150422_1443'),
    ]

    operations = [
        migrations.CreateModel(
            name='Database',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('database_id', models.CharField(unique=True, max_length=16, verbose_name='database_id')),
                ('database_password', models.CharField(max_length=32, verbose_name='password')),
                ('last_update', models.DateField(null=True, verbose_name='last_update', blank=True)),
                ('registration_type', models.PositiveSmallIntegerField(default=3, verbose_name='registration_type', choices=[(-1, b'perpetual'), (3, b'standard'), (10, b'extended')])),
                ('status', models.CharField(max_length=25, verbose_name='status', choices=[(b'unused', b'unused'), (b'sold', b'sold'), (b'registered', b'registered')])),
            ],
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('database', models.ForeignKey(related_name='registrations', to='dbmanage.Database')),
            ],
        ),
        migrations.RemoveField(
            model_name='registereddatabases',
            name='database',
        ),
        migrations.DeleteModel(
            name='Databases',
        ),
        migrations.DeleteModel(
            name='RegisteredDatabases',
        ),
    ]
