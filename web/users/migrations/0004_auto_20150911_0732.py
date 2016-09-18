# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_account_defunct'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='info',
            name='solve_in',
        ),
        migrations.RemoveField(
            model_name='info',
            name='solve_out',
        ),
        migrations.RemoveField(
            model_name='info',
            name='submit_in',
        ),
        migrations.RemoveField(
            model_name='info',
            name='submit_out',
        ),
    ]
