# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-06 18:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employers', '0002_remove_employer_employed_by_company'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employer',
            name='team',
        ),
    ]
