# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-07 13:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20170907_2117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birthday',
            field=models.DateField(blank=True, null=True, verbose_name='出生年月'),
        ),
    ]