# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-16 08:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20160215_1409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadfile',
            name='file',
            field=models.FileField(upload_to='profile/%Y/%m/%d'),
        ),
    ]
