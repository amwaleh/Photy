# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-16 17:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20160216_0844'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadfile',
            name='effects',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]