# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Keys',
            fields=[
                ('flickr_api', models.CharField(max_length=50)),
                ('google_api', models.CharField(max_length=50)),
                ('shodan_api', models.CharField(max_length=50)),
                ('twitter_api', models.CharField(max_length=50)),
                ('twitter_secret', models.CharField(max_length=50)),
                ('linkedin_api', models.CharField(max_length=50)),
                ('linkedin_secret', models.CharField(max_length=50)),
                ('facebook_api', models.CharField(max_length=50)),
                ('facebook_secret', models.CharField(max_length=50)),
                ('facebook_username', models.CharField(max_length=50)),
                ('facebook_password', models.CharField(max_length=50)),
                ('user', models.OneToOneField(serialize=False, to=settings.AUTH_USER_MODEL, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('radius', models.FloatField()),
                ('location_name', models.CharField(max_length=200)),
                ('date', models.DateTimeField(verbose_name='date created')),
                ('latest_data', models.DateTimeField(verbose_name='last time this location was updated')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pushpin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('source', models.CharField(choices=[('TW', 'Twitter'), ('FL', 'Flickr'), ('PI', 'Picasa'), ('SH', 'Shodan'), ('YU', 'Youtube'), ('FB', 'Facebook'), ('LI', 'LinkedIn')], max_length=2)),
                ('date', models.DateTimeField(verbose_name='date published')),
                ('screen_name', models.CharField(max_length=100)),
                ('profile_name', models.CharField(max_length=100)),
                ('profile_url', models.URLField()),
                ('media_url', models.URLField()),
                ('thumb_url', models.URLField()),
                ('message', models.TextField()),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('location', models.ForeignKey(to='map.Location')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
