# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2016-10-26 02:28
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0003_userprofile_settings'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('settings', models.CharField(choices=[('E', '富文本'), ('M', 'Markdown')], default='M', max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='settings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'indexes': [],
            },
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='settings',
            field=models.CharField(choices=[('E', '富文本'), ('M', 'Markdown')], default='M', max_length=10),
        ),
    ]