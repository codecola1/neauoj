# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_judge_account_last_sid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='judge_account',
            name='last_sid',
        ),
    ]
