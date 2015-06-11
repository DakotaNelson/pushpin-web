# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0010_auto_20150611_1155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='latest_data',
            field=models.DateTimeField(help_text='last time this location was updated'),
            preserve_default=True,
        ),
    ]
