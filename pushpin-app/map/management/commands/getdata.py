from django.core.management.base import NoArgsCommand, CommandError

from map.tasks import youtubeTask, twitterTask, picasaTask

class Command(NoArgsCommand):
    # TODO: enable specifying locations to pull as arguments

    def handle_noargs(self, **options):
        twitterTask.delay()
        youtubeTask.delay()
        picasaTask.delay()
