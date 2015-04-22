# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dbmanage', '0002_auto_20150422_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registereddatabases',
            name='database',
            field=models.ForeignKey(related_name='registered', to='dbmanage.Databases', unique=True),
        ),
        migrations.AlterField(
            model_name='registereddatabases',
            name='first_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='registereddatabases',
            name='last_date',
            field=models.DateField(auto_now=True),
        ),
    ]
