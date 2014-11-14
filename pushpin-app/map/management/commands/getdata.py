from django.core.management.base import NoArgsCommand, CommandError
from map.models import Pushpin, Location
from modules import flickr

class Command(NoArgsCommand):
    # TODO: enable specifying locations to pull as arguments

    def handle_noargs(self, **options):
        locations = list(Location.objects.order_by('-date'))

        fl = flickr.Flickr()

        for location in locations:
            fl.run(1,1,1)
