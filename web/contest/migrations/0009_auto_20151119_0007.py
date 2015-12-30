# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0008_in_problem_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='in_problem',
            name='solve',
        ),
        migrations.RemoveField(
            model_name='in_problem',
            name='submit',
        ),
    ]
