# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_info_real_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='info',
            name='qq',
            field=models.CharField(default=b'None', max_length=15),
        ),
    ]
