# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0008_auto_20141209_0025'),
    ]

    operations = [
        migrations.AddField(
            model_name='keys',
            name='instagram_api',
            field=models.CharField(blank=True, max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='keys',
            name='instagram_secret',
            field=models.CharField(blank=True, max_length=50, null=True),
            preserve_default=True,
        ),
    ]
