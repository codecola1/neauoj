# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ce_info',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('info', models.TextField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Code',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.TextField(max_length=5000)),
            ],
        ),
        migrations.CreateModel(
            name='Solve',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('run_id', models.PositiveIntegerField()),
                ('submit_time', models.DateTimeField()),
                ('status', models.CharField(max_length=20)),
                ('use_time', models.IntegerField()),
                ('use_memory', models.IntegerField()),
                ('language', models.CharField(max_length=20)),
                ('length', models.IntegerField()),
                ('wait_show', models.BooleanField(default=True)),
                ('problem', models.ForeignKey(to='problem.Problem')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Solve_first',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('problem', models.ForeignKey(to='problem.Problem')),
                ('solve', models.ForeignKey(to='status.Solve')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='code',
            name='solve',
            field=models.ForeignKey(to='status.Solve'),
        ),
        migrations.AddField(
            model_name='ce_info',
            name='solve',
            field=models.ForeignKey(to='status.Solve'),
        ),
    ]
