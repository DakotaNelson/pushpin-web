# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0012_auto_20150611_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pushpin',
            name='source',
            field=models.CharField(max_length=20),
            preserve_default=True,
        ),
    ]
