# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0004_auto_20151005_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='length',
            field=models.IntegerField(),
        ),
    ]
