# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_judge_account_defunct'),
    ]

    operations = [
        migrations.AddField(
            model_name='judge_account',
            name='index',
            field=models.IntegerField(default=-1),
        ),
    ]
