# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contest', '0002_contest_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contest',
            name='student',
        ),
        migrations.AddField(
            model_name='contest',
            name='creator',
            field=models.ForeignKey(default=None, to=settings.AUTH_USER_MODEL),
        ),
    ]
