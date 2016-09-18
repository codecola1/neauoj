# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_oj_account'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='oj_account',
            name='user',
        ),
        migrations.AddField(
            model_name='info',
            name='oj_account',
            field=models.ManyToManyField(to='users.OJ_account'),
        ),
    ]
