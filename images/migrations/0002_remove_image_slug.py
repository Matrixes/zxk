# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2016-11-01 07:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='slug',
        ),
    ]
