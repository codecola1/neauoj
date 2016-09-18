# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0002_auto_20150728_1158'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solve_first',
            name='problem',
        ),
        migrations.RemoveField(
            model_name='solve_first',
            name='solve',
        ),
        migrations.RemoveField(
            model_name='solve_first',
            name='user',
        ),
        migrations.RemoveField(
            model_name='solve',
            name='is_site',
        ),
        migrations.RemoveField(
            model_name='solve',
            name='run_id',
        ),
        migrations.DeleteModel(
            name='Solve_first',
        ),
    ]
