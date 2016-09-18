# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0008_auto_20151119_0945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='description',
            field=models.TextField(default=b'', max_length=2000),
        ),
        migrations.AlterField(
            model_name='problem',
            name='hint',
            field=models.TextField(default=b'', max_length=500, blank=True),
        ),
        migrations.AlterField(
            model_name='problem',
            name='input',
            field=models.TextField(default=b'', max_length=2000),
        ),
        migrations.AlterField(
            model_name='problem',
            name='output',
            field=models.TextField(default=b'', max_length=2000),
        ),
        migrations.AlterField(
            model_name='problem',
            name='sample_input',
            field=models.TextField(default=b'', max_length=500, blank=True),
        ),
        migrations.AlterField(
            model_name='problem',
            name='sample_output',
            field=models.TextField(default=b'', max_length=500),
        ),
        migrations.AlterField(
            model_name='problem',
            name='source',
            field=models.CharField(default=b'', max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='problem',
            name='title',
            field=models.CharField(default=b'', max_length=50),
        ),
    ]
