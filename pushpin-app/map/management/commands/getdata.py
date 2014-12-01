from django.core.management.base import NoArgsCommand, CommandError

from map.tasks import youtubeTask, twitterTask, picasaTask, shodanTask, flickrTask

class Command(NoArgsCommand):
    # TODO: enable specifying locations to pull as arguments

    def handle_noargs(self, **options):
        flickrTask.delay()
        twitterTask.delay()
        youtubeTask.delay()
        picasaTask.delay()
        shodanTask.delay()
