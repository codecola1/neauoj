# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20160122_1405'),
    ]

    operations = [
        migrations.AddField(
            model_name='oj_account',
            name='last_rid',
            field=models.CharField(default=0, max_length=15),
        ),
    ]
