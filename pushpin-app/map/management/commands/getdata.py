from django.core.management.base import NoArgsCommand, CommandError
from django.db import models
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

        unique_fields = ['location', 'latitude', 'longitude', 'date', 'screen_name']
        # if two things are in the same location bin, at the same latitude and
        # longitude, created at the same date by the same person, they are
        # assumed to be the same thing

        # now de-dupe the database
        print('')
        print("Removing duplicates in database...")
        duplicates = (Pushpin.objects.values(*unique_fields)
                                     .order_by()
                                     .annotate(max_id=models.Max('id'),
                                               count_id=models.Count('id'))
                                     .filter(count_id__gt=1))

        for duplicate in duplicates:
            (Pushpin.objects.filter(**{x: duplicate[x] for x in unique_fields})
                            .exclude(id=duplicate['max_id'])
                            .delete())

        """
            Discussion time:
            This is slow. Really slow. However, the alternative is setting a
            unique constraint on pushpins, then inserting pins one at a time
            to the database... which is also really slow, and additionally
            requires some sort of external unique ID. (Twitter has this, but
            it may be difficult to get that from every API.) Enforcing
            uniqueness on insert instead of inserting blindly and cleaning
            later may be worth exploring, but this works for now.

            See:
        https://stackoverflow.com/questions/15261821/django-unique-bulk-inserts
        """
