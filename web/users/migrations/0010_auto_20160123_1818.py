# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('problem', '0008_auto_20151119_0945'),
        ('users', '0009_oj_account_using'),
    ]

    operations = [
        migrations.CreateModel(
            name='submit_problem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ac', models.BooleanField(default=False)),
                ('problem', models.ForeignKey(to='problem.Problem')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='info',
            name='solve',
        ),
        migrations.RemoveField(
            model_name='info',
            name='submit',
        ),
    ]
