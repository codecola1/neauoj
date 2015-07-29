# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='code',
            name='solve',
        ),
        migrations.AddField(
            model_name='solve',
            name='code',
            field=models.TextField(default=b'', max_length=5000),
        ),
        migrations.AddField(
            model_name='solve',
            name='is_site',
            field=models.BooleanField(default=True),
        ),
        migrations.DeleteModel(
            name='Code',
        ),
    ]
