# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-01 20:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=200)),
                ('note_sequence', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='song',
            name='votes',
            field=models.ManyToManyField(to='core.Vote'),
        ),
    ]
