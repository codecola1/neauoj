# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0004_auto_20150911_0622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solve',
            name='use_memory',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='solve',
            name='use_time',
            field=models.IntegerField(default=0),
        ),
    ]
