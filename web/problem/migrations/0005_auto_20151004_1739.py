# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0004_auto_20151004_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='sample_input',
            field=models.TextField(max_length=500, blank=True),
        ),
        migrations.AlterField(
            model_name='problem',
            name='source',
            field=models.CharField(max_length=50, blank=True),
        ),
    ]
