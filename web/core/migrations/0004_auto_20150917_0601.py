# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_judge_account_index'),
    ]

    operations = [
        migrations.RenameField(
            model_name='judge_account',
            old_name='index',
            new_name='user_index',
        ),
    ]
