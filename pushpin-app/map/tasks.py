from celery.task.schedules import crontab
from celery.task import periodic_task
from celery import shared_task
from datetime import timedelta

from modules import flickr, twitter, youtube, picasa, shodan, instagram
from map.models import Pushpin, Location

"""@shared_task
@periodic_task(run_every=crontab(minute=0,hour="*/1"))
def getData():
    print("Running getData task!")
    locations = list(Location.objects.order_by('-date'))

    modules = []
    #modules.append(flickr.Flickr())
    modules.append(twitter.Twitter())
    modules.append(youtube.Youtube())

    for location in locations:
        print('')
        print("Collecting data for: " + location.name)
        for module in modules:
            module.run(location.name,location.latitude,location.longitude,location.radius)
    return"""

@shared_task
@periodic_task(run_every=crontab(minute=0,hour="*/1"))
def twitterTask():
    locations = list(Location.objects.order_by('-date'))

    module = twitter.Twitter()

    for location in locations:
        module.run(location.name,location.latitude,location.longitude,location.radius)
    return

@shared_task
@periodic_task(run_every=crontab(minute=0,hour="*/1"))
def youtubeTask():
    locations = list(Location.objects.order_by('-date'))

    module = youtube.Youtube()

    for location in locations:
        module.run(location.name,location.latitude,location.longitude,location.radius)
    return

@shared_task
@periodic_task(run_every=crontab(minute=0,hour="*/1"))
def picasaTask():
    locations = list(Location.objects.order_by('-date'))

    module = picasa.Picasa()

    for location in locations:
        module.run(location.name,location.latitude,location.longitude,location.radius)
    return

@shared_task
@periodic_task(run_every=crontab(minute=0,hour="*/1"))
def shodanTask():
    locations = list(Location.objects.order_by('-date'))

    module = shodan.Shodan()

    for location in locations:
        module.run(location.name,location.latitude,location.longitude,location.radius)
    return

@shared_task
@periodic_task(run_every=crontab(minute=0,hour="*/1"))
def flickrTask():
    locations = list(Location.objects.order_by('-date'))

    module = flickr.Flickr()

    for location in locations:
        module.run(location.name,location.latitude,location.longitude,location.radius)
    return

@shared_task
@periodic_task(run_every=crontab(minute=0,hour="*/1"))
def instagramTask():
    locations = list(Location.objects.order_by('-date'))

    module = instagram.Instagram()

    for location in locations:
        module.run(location.name,location.latitude,location.longitude,location.radius)
    return
