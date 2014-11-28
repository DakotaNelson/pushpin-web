# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0006_auto_20141115_2131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pushpin',
            name='media_url',
            field=models.CharField(max_length=500),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pushpin',
            name='profile_url',
            field=models.CharField(max_length=500),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pushpin',
            name='thumb_url',
            field=models.CharField(max_length=500),
            preserve_default=True,
        ),
    ]
