# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='problem',
            name='memory_limit',
        ),
        migrations.RemoveField(
            model_name='problem',
            name='time_limit',
        ),
        migrations.AddField(
            model_name='problem',
            name='memory_limit_c',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='problem',
            name='memory_limit_java',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='problem',
            name='time_limit_c',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='problem',
            name='time_limit_java',
            field=models.IntegerField(default=0),
        ),
    ]
