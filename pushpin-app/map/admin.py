from django.contrib import admin
from map.models import Location, Keys, Pushpin

class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude', 'radius', 'date', 'user')

admin.site.register(Location, LocationAdmin)


class KeysAdmin(admin.ModelAdmin):
    fieldsets = [
            (None,         {'fields': ['flickr_api', 'google_api', 'shodan_api']}),
            ('Twitter',    {'fields': ['twitter_api', 'twitter_secret'], 'classes': ['collapse']}),
            ]

admin.site.register(Keys, KeysAdmin)

admin.site.register(Pushpin)
