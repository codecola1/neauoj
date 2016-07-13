# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20160122_1402'),
    ]

    operations = [
        migrations.AddField(
            model_name='judge_account',
            name='last_sid',
            field=models.IntegerField(default=-1),
        ),
    ]
