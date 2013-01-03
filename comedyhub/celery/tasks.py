from django.core.management import call_command

from comedyhub.celery.config import celery
from content.utils import set_video_thumb


@celery.task
def set_thumb(video):
    set_video = set_video_thumb(video)
    set_video.save()


@celery.task
def run_update_featured():
    return call_command('update_featured')


@celery.task
def run_update_ratings():
    return call_command('update_ratings')
