# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20150917_0601'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='judge',
            name='solve',
        ),
        migrations.DeleteModel(
            name='Judge',
        ),
    ]
