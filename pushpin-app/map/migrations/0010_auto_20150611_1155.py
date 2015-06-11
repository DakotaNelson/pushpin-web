# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0009_auto_20150611_1151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='latest_data',
            field=models.DateTimeField(help_text='last time this location was updated', default=datetime.datetime(2013, 6, 11, 11, 55, 46, 141839)),
            preserve_default=True,
        ),
    ]
