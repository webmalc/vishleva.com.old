# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-04 12:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0007_galleryextended_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='galleryextended',
            name='is_special',
            field=models.BooleanField(default=False),
        ),
    ]
