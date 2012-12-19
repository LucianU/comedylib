from collections import defaultdict

from django.core.management.base import NoArgsCommand

from profiles.models import Feeling

class Command(NoArgsCommand):
    help = "Updates likes and dislikes on videos"

    def handle_noargs(self, **options):
        feelings = Feeling.objects.all()

        # defaultdict accepts any callable, so we pass a lambda
        # that returns another defaultdict with int (a counter)
        videos = defaultdict(lambda: defaultdict(int))
        for feeling in feelings:
            videos[feeling.video][feeling.name] += 1

        for video, ratings in videos.iteritems():
            video.likes = ratings['L']
            video.dislikes = ratings['D']
            video.save()
