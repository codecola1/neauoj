# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0002_auto_20150809_0424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='accepted',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='problem',
            name='defunct',
            field=models.BooleanField(default=0),
        ),
        migrations.AlterField(
            model_name='problem',
            name='solved',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='problem',
            name='submit',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='problem',
            name='type',
            field=models.CharField(default=b'', max_length=20),
        ),
    ]
