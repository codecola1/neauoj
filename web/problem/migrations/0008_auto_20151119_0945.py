# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0007_problem_data'),
    ]

    operations = [
        migrations.RenameField(
            model_name='problem',
            old_name='data',
            new_name='data_number',
        ),
    ]
