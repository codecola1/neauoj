# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0009_auto_20151119_0007'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='clone',
            field=models.IntegerField(default=-1),
        ),
    ]
