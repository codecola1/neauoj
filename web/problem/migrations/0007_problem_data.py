# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0006_remove_problem_accepted'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='data',
            field=models.IntegerField(default=-1),
        ),
    ]
