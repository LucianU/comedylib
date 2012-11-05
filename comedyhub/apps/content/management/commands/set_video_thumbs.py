from django.core.management.base import NoArgsCommand

from content.models import Video
from content.utils import set_video_thumb

class Command(NoArgsCommand):
    help = ("Downloads the thumbnails for the videos found in the database"
            " and makes them accessible through the 'picture' attribute")

    def handle_noargs(self, **options):
        for video in Video.objects.all():
            if video.picture.name is None:
                thumbed_vid = set_video_thumb(video)
                thumbed_vid.save()
