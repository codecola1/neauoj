# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('problem_id', models.CharField(max_length=20)),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=2000)),
                ('input', models.TextField(max_length=2000)),
                ('output', models.TextField(max_length=2000)),
                ('sample_input', models.TextField(max_length=500)),
                ('sample_output', models.TextField(max_length=500)),
                ('hint', models.TextField(max_length=500)),
                ('source', models.CharField(max_length=50)),
                ('date', models.DateField(auto_now_add=True)),
                ('time_limit', models.IntegerField()),
                ('memory_limit', models.IntegerField()),
                ('defunct', models.BooleanField()),
                ('accepted', models.PositiveIntegerField()),
                ('submit', models.PositiveIntegerField()),
                ('solved', models.PositiveIntegerField()),
                ('type', models.CharField(max_length=20)),
                ('oj', models.CharField(max_length=20)),
                ('judge_type', models.PositiveIntegerField()),
            ],
        ),
    ]
