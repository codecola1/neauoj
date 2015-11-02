# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0003_auto_20150813_0230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='hint',
            field=models.TextField(max_length=500, blank=True),
        ),
    ]
