# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_info_classes'),
    ]

    operations = [
        migrations.AddField(
            model_name='info',
            name='real_name',
            field=models.CharField(default=b'None', max_length=20),
        ),
    ]
