# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_info_qq'),
    ]

    operations = [
        migrations.AddField(
            model_name='info',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]
