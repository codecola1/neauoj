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
            name='Contest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('length', models.TimeField()),
                ('defunct', models.BooleanField(default=False)),
                ('description', models.TextField(max_length=200)),
                ('private', models.BooleanField()),
                ('impose', models.BooleanField(default=False)),
                ('type', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Discuss',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField(max_length=500)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('first', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='In_Problem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('problem_new_id', models.CharField(max_length=20)),
                ('title', models.CharField(max_length=50)),
                ('problem', models.ForeignKey(to='problem.Problem')),
            ],
        ),
        migrations.CreateModel(
            name='Judger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='discuss',
            name='problem',
            field=models.ForeignKey(to='contest.In_Problem'),
        ),
        migrations.AddField(
            model_name='discuss',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contest',
            name='discusses',
            field=models.ManyToManyField(to='contest.Discuss'),
        ),
        migrations.AddField(
            model_name='contest',
            name='judger',
            field=models.ManyToManyField(to='contest.Judger'),
        ),
        migrations.AddField(
            model_name='contest',
            name='problem',
            field=models.ManyToManyField(to='contest.In_Problem'),
        ),
        migrations.AddField(
            model_name='contest',
            name='student',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
