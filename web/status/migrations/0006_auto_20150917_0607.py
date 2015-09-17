# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0005_auto_20150911_0732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solve',
            name='status',
            field=models.CharField(max_length=200),
        ),
    ]
