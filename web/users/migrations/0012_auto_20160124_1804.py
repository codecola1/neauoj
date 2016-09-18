# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_oj_account_updating'),
    ]

    operations = [
        migrations.RenameField(
            model_name='oj_account',
            old_name='using',
            new_name='is_using',
        ),
    ]
