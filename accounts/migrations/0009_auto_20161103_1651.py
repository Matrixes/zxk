# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2016-11-03 08:51
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20161102_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collections',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collections', to=settings.AUTH_USER_MODEL),
        ),
    ]
