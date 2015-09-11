# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0003_auto_20150911_0620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solve',
            name='submit_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
