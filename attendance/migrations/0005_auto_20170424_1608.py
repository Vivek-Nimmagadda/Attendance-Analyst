# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-24 10:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0004_student_last_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='last_updated',
            field=models.DateTimeField(blank=True),
        ),
    ]