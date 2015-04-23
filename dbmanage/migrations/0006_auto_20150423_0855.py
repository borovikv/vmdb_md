# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dbmanage', '0005_auto_20150423_0748'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='database',
            name='registration_type',
        ),
        migrations.AddField(
            model_name='database',
            name='is_perpetual',
            field=models.BooleanField(default=False, verbose_name='is_perpetual'),
        ),
        migrations.AddField(
            model_name='database',
            name='max_registrations',
            field=models.PositiveSmallIntegerField(default=3, verbose_name='max_registrations'),
        ),
    ]
