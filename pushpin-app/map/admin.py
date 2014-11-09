from django.contrib import admin
from map.models import Location, Keys, Pushpin

class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude', 'radius', 'date', 'user')

admin.site.register(Location, LocationAdmin)


class KeysAdmin(admin.ModelAdmin):
    fieldsets = [
            (None,         {'fields': ['flickr_api', 'google_api', 'shodan_api']}),
            ('Twitter',    {'fields': ['twitter_api', 'twitter_secret'], 'classes': ['collapse']}),
            ('Facebook',   {'fields': ['facebook_api', 'facebook_secret', 'facebook_username', 'facebook_password'], 'classes': ['collapse']}),
            ('LinkedIn',   {'fields': ['linkedin_api', 'linkedin_secret'], 'classes': ['collapse']})
            ]

admin.site.register(Keys, KeysAdmin)

admin.site.register(Pushpin)
