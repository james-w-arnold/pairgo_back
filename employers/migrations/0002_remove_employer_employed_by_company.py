# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-06 17:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employers', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employer',
            name='employed_by_company',
        ),
    ]
