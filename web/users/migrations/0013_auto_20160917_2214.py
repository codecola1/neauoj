# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20160124_1804'),
    ]

    operations = [
        migrations.AddField(
            model_name='info',
            name='student_id',
            field=models.CharField(default=b'None', max_length=20),
        ),
        migrations.AddField(
            model_name='info',
            name='telephone',
            field=models.CharField(default=b'None', max_length=20),
        ),
        migrations.AlterField(
            model_name='info',
            name='school',
            field=models.CharField(default=b'None', max_length=20),
        ),
    ]
