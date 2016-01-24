# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_oj_account_last_rid'),
    ]

    operations = [
        migrations.AddField(
            model_name='oj_account',
            name='using',
            field=models.BooleanField(default=False),
        ),
    ]
