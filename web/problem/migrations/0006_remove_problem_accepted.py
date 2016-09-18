# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0005_auto_20151004_1739'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='problem',
            name='accepted',
        ),
    ]
