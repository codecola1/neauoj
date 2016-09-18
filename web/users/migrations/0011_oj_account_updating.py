# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20160123_1818'),
    ]

    operations = [
        migrations.AddField(
            model_name='oj_account',
            name='updating',
            field=models.IntegerField(default=0),
        ),
    ]
