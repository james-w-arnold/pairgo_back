# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-15 12:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matching', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='interest_score',
        ),
        migrations.RemoveField(
            model_name='match',
            name='location_score',
        ),
        migrations.RemoveField(
            model_name='match',
            name='psycho_score',
        ),
        migrations.RemoveField(
            model_name='match',
            name='skill_score',
        ),
    ]
