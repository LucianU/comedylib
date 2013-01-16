"""
Celery tasks
"""
from django.core.management import call_command

from comedylib.celery.config import celery
from content.utils import set_video_thumb


@celery.task
def set_thumb(video):
    """
    Sets the thumbnail on a video
    """
    set_video = set_video_thumb(video)
    set_video.save()


@celery.task
def run_update_featured():
    """
    Runs the update_featured management command
    """
    return call_command('update_featured')


@celery.task
def run_update_ratings():
    """
    Runs the update_ratings management command
    """
    return call_command('update_ratings')
