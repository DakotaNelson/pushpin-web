from django.db import models
from django.contrib.auth.models import User

class Location(models.Model):
    # one query made by a user into a certain location
    latitude = models.FloatField()
    longitude = models.FloatField()
    radius = models.FloatField()
    name = models.CharField(max_length = 200)
    date = models.DateTimeField('date created')
    latest_data = models.DateTimeField('last time this location was updated')
    user = models.ForeignKey(User)

    def __str__(self):
        return self.name

class Pushpin(models.Model):
    # one piece of information (one tweet, one flickr photo, etc.)
    TWITTER = "TW"
    FLICKR = "FL"
    PICASA = "PI"
    SHODAN = "SH"
    YOUTUBE = "YU"
    FACEBOOK = "FB"
    LINKEDIN = "LI"
    INSTAGRAM = "IN"

    SOURCES = (
                (TWITTER, "Twitter"),
                (FLICKR, "Flickr"),
                (PICASA, "Picasa"),
                (SHODAN, "Shodan"),
                (YOUTUBE, "Youtube"),
                (FACEBOOK, "Facebook"),
                (LINKEDIN, "LinkedIn"),
                (INSTAGRAM, "Instagram")
              )

    source = models.CharField(choices=SOURCES, max_length=2)
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
    instagram_api = models.CharField(max_length = 50, blank=True, null=True)
    instagram_secret = models.CharField(max_length = 50, blank=True, null=True)
    flickr_api = models.CharField(max_length = 50, blank=True, null=True)
    google_api = models.CharField(max_length = 50, blank=True, null=True)
    shodan_api = models.CharField(max_length = 50, blank=True, null=True)
    twitter_api = models.CharField(max_length = 50, blank=True, null=True)
    twitter_secret = models.CharField(max_length = 50, blank=True, null=True)
    twitter_token = models.CharField(max_length = 200, blank=True, null=True)
    linkedin_api = models.CharField(max_length = 50, blank=True, null=True)
    linkedin_secret = models.CharField(max_length = 50, blank=True, null=True)
    facebook_api = models.CharField(max_length = 50, blank=True, null=True)
    facebook_secret = models.CharField(max_length = 50, blank=True, null=True)
    facebook_username = models.CharField(max_length = 50, blank=True, null=True)
    facebook_password = models.CharField(max_length = 50, blank=True, null=True)
    user = models.OneToOneField(User, primary_key=True)

    def __str__(self):
        return str(self.user)
