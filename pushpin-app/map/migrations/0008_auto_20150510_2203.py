# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0007_auto_20141128_1203'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='keys',
            options={'verbose_name_plural': 'keys'},
        ),
        migrations.RemoveField(
            model_name='keys',
            name='facebook_api',
        ),
        migrations.RemoveField(
            model_name='keys',
            name='facebook_password',
        ),
        migrations.RemoveField(
            model_name='keys',
            name='facebook_secret',
        ),
        migrations.RemoveField(
            model_name='keys',
            name='facebook_username',
        ),
        migrations.RemoveField(
            model_name='keys',
            name='linkedin_api',
        ),
        migrations.RemoveField(
            model_name='keys',
            name='linkedin_secret',
        ),
        migrations.AlterField(
            model_name='location',
            name='name',
            field=models.CharField(max_length=200, unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pushpin',
            name='source',
            field=models.CharField(max_length=2, choices=[('TW', 'Twitter'), ('FL', 'Flickr'), ('PI', 'Picasa'), ('SH', 'Shodan'), ('YU', 'Youtube')]),
            preserve_default=True,
        ),
    ]
