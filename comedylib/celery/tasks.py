"""
Celery tasks
"""
from django.core.management import call_command

from comedylib.celery.config import celery


@celery.task
def run_set_video_thumbs(video):
    """
    Calls the set_video_thumbs management command
    """
    return call_command('set_video_thumbs')


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
