# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0006_auto_20150917_0607'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solve',
            name='wait_show',
        ),
    ]
