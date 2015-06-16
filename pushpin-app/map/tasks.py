from celery.task.schedules import crontab
from celery.task import periodic_task
from celery import shared_task
from datetime import datetime, timedelta, timezone
import dateutil.parser
import json
import logging

from modules import flickr, twitter, youtube, picasa, shodan
from map.models import Pushpin, Location

logger = logging.getLogger('pushpin')

@shared_task
@periodic_task(run_every=crontab(minute=0,hour="*/1"))
def twitterTask():
    locations = list(Location.objects.order_by('-date'))

    module = twitter.Twitter()

    for location in locations:
        runModule(module, location)
    return

@shared_task
@periodic_task(run_every=crontab(minute="*/30"))
def youtubeTask():
    locations = list(Location.objects.order_by('-date'))

    module = youtube.Youtube()

    for location in locations:
        runModule(module, location)
    return

@shared_task
@periodic_task(run_every=crontab(minute=0,hour="*/1"))
def picasaTask():
    locations = list(Location.objects.order_by('-date'))

    module = picasa.Picasa()

    for location in locations:
        runModule(module, location)
    return

@shared_task
@periodic_task(run_every=crontab(hour="*/24"))
def shodanTask():
    locations = list(Location.objects.order_by('-date'))

    module = shodan.Shodan()

    for location in locations:
        runModule(module, location)
    return

@shared_task
@periodic_task(run_every=crontab(minute="*/15"))
def flickrTask():
    locations = list(Location.objects.order_by('-date'))

    module = flickr.Flickr()

    for location in locations:
        runModule(module, location)

##### Helper functions #####
def runModule(module, location):
    logger.debug("Running {} module for {}.".format(module.name, location.name))
    #logger.debug('latestData for {}: {}'.format(location.name,location.latest_data))

    try:
        latestData = json.loads(location.latest_data)
        latestData = latestData[module.name]
        #logger.debug('Unloaded latestData: {}'.format(latestData))
        latestData = dateutil.parser.parse(latestData)
    except (ValueError, KeyError) as e:
        # module hasn't been run before (no entry in "last run" column)
        logger.debug("First time running module for this location.")
        two_years_ago = datetime.now(timezone.utc).astimezone() - timedelta(days=365*2)
        logger.debug("Two years ago: {}".format(two_years_ago))
        #two_years_ago = datetime.now() - timedelta(days=365*2)
        latestData = two_years_ago

    logger.debug("{} module last run {} for this location.".format(module.name, latestData))

    module.run(location.name,location.latitude,location.longitude,location.radius, latestData)
    return
