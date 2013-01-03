from celery import Celery
from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    # Executes every day at midnight
    'daily-at-midnight': {
        'task': 'comedyhub.celery.tasks.run_update_featured',
        'schedule': crontab(minute=0, hour=0),
    },
    # Executes every fixed hour
    'every-fixed-hour': {
        'task': 'comedyhub.celery.tasks.run_update_ratings',
        'schedule': crontab(minute=0, hour='*'),
    },
}

celery = Celery('comedyhub.celery',
                backend='amqp',
                broker='amqp://',
                include=['comedyhub.celery.tasks'])
celery.conf.update({'CELERYBEAT_SCHEDULE': CELERYBEAT_SCHEDULE})

if __name__ == '__main__':
    celery.start()
