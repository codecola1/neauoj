# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20150729_0845'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='defunct',
            field=models.BooleanField(default=False),
        ),
    ]
