# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0008_auto_20150510_2203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='date',
            field=models.DateTimeField(help_text='date created'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='location',
            name='latest_data',
            field=models.DateTimeField(help_text='last time this location was updated', default=datetime.datetime(2013, 6, 11, 11, 51, 16, 779077)),
            preserve_default=True,
        ),
    ]
