"""
Celery tasks
"""
from django.core.management import call_command

from comedylib.celery.config import celery


@celery.task
def run_set_video_thumbs():
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


# Backup tasks
@celery.task
def backup_db():
    """
    Backs up the database
    """
    return call_command('dbbackup', clean=True)


@celery.task
def backup_media():
    """
    Backs up the media files
    """
    return call_command('backup_media', clean=True)


@celery.task
def midnight_caller():
    run_update_ratings.delay()
    backup_db.delay()
    backup_media.delay()
