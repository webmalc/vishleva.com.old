# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-12 11:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0014_event_expenses'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='notified_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]