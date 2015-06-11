# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0011_auto_20150611_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='latest_data',
            field=models.CharField(blank=True, max_length=800, help_text='Last time this location was updated. Serialized JSON dict containing {"moduleName":"ISOdate", ... }'),
            preserve_default=True,
        ),
    ]
