# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dbmanage', '0003_auto_20150422_1443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registereddatabases',
            name='database',
            field=models.OneToOneField(related_name='registered', to='dbmanage.Databases'),
        ),
    ]
