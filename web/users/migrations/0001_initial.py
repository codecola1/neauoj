# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('oj', models.CharField(max_length=20)),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('last', models.PositiveIntegerField()),
                ('submit', models.PositiveIntegerField(default=0)),
                ('solved', models.PositiveIntegerField(default=0)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Info',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nickname', models.CharField(max_length=50)),
                ('submit', models.PositiveIntegerField(default=0)),
                ('solve', models.PositiveIntegerField(default=0)),
                ('submit_in', models.PositiveIntegerField(default=0)),
                ('solve_in', models.PositiveIntegerField(default=0)),
                ('submit_out', models.PositiveIntegerField(default=0)),
                ('solve_out', models.PositiveIntegerField(default=0)),
                ('school', models.CharField(max_length=20)),
                ('grade', models.PositiveIntegerField()),
                ('team', models.BooleanField(default=False)),
                ('account', models.ManyToManyField(to='users.Account')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('from_user', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=50)),
                ('content', models.TextField(max_length=500)),
                ('is_new', models.BooleanField(default=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
