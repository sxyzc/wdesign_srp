# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-17 08:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Res',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('res_name', models.CharField(max_length=60)),
                ('res_path', models.CharField(max_length=100)),
                ('res_format', models.CharField(max_length=20)),
                ('res_size', models.CharField(max_length=20)),
                ('create_time', models.CharField(max_length=30)),
                ('upload_user', models.CharField(max_length=30)),
                ('key_word', models.CharField(max_length=100)),
                ('other_01', models.CharField(max_length=100)),
                ('other_02', models.CharField(max_length=100)),
                ('other_03', models.CharField(max_length=100)),
            ],
        ),
    ]
