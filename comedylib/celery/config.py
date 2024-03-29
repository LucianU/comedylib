"""
Celery configuration
"""
from celery import Celery
from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    # Executes every day at midnight
    'daily-at-midnight': {
        'task': 'comedylib.celery.tasks.midnight_caller',
        'schedule': crontab(minute=0, hour=0),
    },
    # Executes every fixed hour
    'every-fixed-hour': {
        'task': 'comedylib.celery.tasks.hourly_caller',
        'schedule': crontab(minute=0, hour='*'),
    },
    # Executes every five minutes
    'every-five-minutes': {
        'task': 'comedylib.celery.tasks.run_set_video_thumbs',
        'schedule': crontab(minute='*/5'),
    }
}
CELERY_IGNORE_RESULT = True

celery = Celery('comedylib.celery',
                backend='amqp',
                broker='amqp://',
                include=['comedylib.celery.tasks'])
celery.conf.update({
    'CELERYBEAT_SCHEDULE': CELERYBEAT_SCHEDULE,
    'CELERY_IGNORE_RESULT': CELERY_IGNORE_RESULT,
})

if __name__ == '__main__':
    celery.start()
