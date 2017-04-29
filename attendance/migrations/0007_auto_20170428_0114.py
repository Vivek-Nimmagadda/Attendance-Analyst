# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-27 19:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0006_auto_20170425_0034'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='display_image',
            field=models.ImageField(default='profiles/default_pic.png', upload_to='profiles/'),
        ),
        migrations.AlterField(
            model_name='student',
            name='last_updated',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]