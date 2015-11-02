# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0003_auto_20151005_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='description',
            field=models.TextField(max_length=200, blank=True),
        ),
    ]
