# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-28 00:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies_app', '0004_movie_moveieid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='moveieID',
            field=models.IntegerField(default=0),
        ),
    ]
