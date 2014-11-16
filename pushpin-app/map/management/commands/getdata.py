from django.core.management.base import NoArgsCommand, CommandError
from map.models import Pushpin, Location
from modules import flickr, twitter, youtube

class Command(NoArgsCommand):
    # TODO: enable specifying locations to pull as arguments

    def handle_noargs(self, **options):
        locations = list(Location.objects.order_by('-date'))

        #fl = flickr.Flickr()
        tw = twitter.Twitter()
        yu = youtube.Youtube()

        for location in locations:
            print('')
            print("Collecting data for: " + location.name)
            #fl.run(location.name,location.latitude,location.longitude,location.radius)
            tw.run(location.name,location.latitude,location.longitude,location.radius)
            yu.run(location.name,location.latitude,location.longitude,location.radius)
