# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0009_auto_20160124_1830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='defunct',
            field=models.IntegerField(default=0),
        ),
    ]
