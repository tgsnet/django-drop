# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-10-20 02:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drop', '0005_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(blank=True, to='drop.Category'),
        ),
    ]