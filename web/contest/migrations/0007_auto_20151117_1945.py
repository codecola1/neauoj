# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0006_remove_contest_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='in_problem',
            name='solve',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='in_problem',
            name='submit',
            field=models.IntegerField(default=0),
        ),
    ]
