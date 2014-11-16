# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0004_keys_twitter_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keys',
            name='facebook_api',
            field=models.CharField(blank=True, max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='keys',
            name='facebook_password',
            field=models.CharField(blank=True, max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='keys',
            name='facebook_secret',
            field=models.CharField(blank=True, max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='keys',
            name='facebook_username',
            field=models.CharField(blank=True, max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='keys',
            name='flickr_api',
            field=models.CharField(blank=True, max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='keys',
            name='google_api',
            field=models.CharField(blank=True, max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='keys',
            name='linkedin_api',
            field=models.CharField(blank=True, max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='keys',
            name='linkedin_secret',
            field=models.CharField(blank=True, max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='keys',
            name='shodan_api',
            field=models.CharField(blank=True, max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='keys',
            name='twitter_api',
            field=models.CharField(blank=True, max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='keys',
            name='twitter_secret',
            field=models.CharField(blank=True, max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='keys',
            name='twitter_token',
            field=models.CharField(blank=True, max_length=100, null=True),
            preserve_default=True,
        ),
    ]
