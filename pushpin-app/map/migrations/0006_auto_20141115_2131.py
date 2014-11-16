# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0005_auto_20141115_2130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keys',
            name='twitter_token',
            field=models.CharField(blank=True, max_length=200, null=True),
            preserve_default=True,
        ),
    ]
