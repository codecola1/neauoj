# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0007_remove_solve_wait_show'),
        ('contest', '0007_auto_20151117_1945'),
    ]

    operations = [
        migrations.AddField(
            model_name='in_problem',
            name='status',
            field=models.ManyToManyField(to='status.Solve'),
        ),
    ]
