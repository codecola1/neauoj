# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0005_auto_20151113_1502'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contest',
            name='length',
        ),
    ]
