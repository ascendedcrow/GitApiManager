# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-17 15:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='git_login',
            fields=[
                ('login_name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=128)),
                ('loggedin', models.BooleanField()),
            ],
        ),
    ]
