# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0002_auto_20141105_1134'),
    ]

    operations = [
        migrations.RenameField(
            model_name='location',
            old_name='location_name',
            new_name='name',
        ),
    ]
