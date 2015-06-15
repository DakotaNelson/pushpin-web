from django.db import models
from django.contrib.auth.models import User

class Location(models.Model):
    # one query made by a user into a certain location
    latitude = models.FloatField()
    longitude = models.FloatField()
    radius = models.PositiveSmallIntegerField()
    name = models.CharField(max_length = 200, unique=True)
    date = models.DateTimeField(help_text='date created')
    latest_data = models.CharField(max_length=800,blank=True,help_text='Last time this location was updated. Serialized JSON dict containing {"moduleName":"ISOdate", ... }')
    user = models.ForeignKey(User)

    def __str__(self):
        return self.name

class Pushpin(models.Model):
    # one piece of information (one tweet, one flickr photo, etc.)
    source = models.CharField(max_length=20)
    date = models.DateTimeField('date published')
    screen_name = models.CharField(max_length=100)
    profile_name = models.CharField(max_length=100)
    profile_url = models.CharField(max_length=500)
    media_url = models.CharField(max_length=500)
    thumb_url = models.CharField(max_length=500)
    message = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    location = models.ForeignKey(Location)

    def __str__(self):
        return "pin by " + self.screen_name + " from " + self.source

class Keys(models.Model):
    # holds a user's API keys
    flickr_api = models.CharField(max_length = 50, blank=True, null=True)
    google_api = models.CharField(max_length = 50, blank=True, null=True)
    shodan_api = models.CharField(max_length = 50, blank=True, null=True)
    twitter_api = models.CharField(max_length = 50, blank=True, null=True)
    twitter_secret = models.CharField(max_length = 50, blank=True, null=True)
    twitter_token = models.CharField(max_length = 200, blank=True, null=True)
    user = models.OneToOneField(User, primary_key=True)

    class Meta:
        verbose_name_plural = 'keys'

    def __str__(self):
        return str(self.user)
