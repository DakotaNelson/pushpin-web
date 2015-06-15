# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0013_auto_20150612_1917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='radius',
            field=models.PositiveSmallIntegerField(),
            preserve_default=True,
        ),
    ]
