# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0007_auto_20141128_1203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pushpin',
            name='source',
            field=models.CharField(choices=[('TW', 'Twitter'), ('FL', 'Flickr'), ('PI', 'Picasa'), ('SH', 'Shodan'), ('YU', 'Youtube'), ('FB', 'Facebook'), ('LI', 'LinkedIn'), ('IN', 'Instagram')], max_length=2),
            preserve_default=True,
        ),
    ]
