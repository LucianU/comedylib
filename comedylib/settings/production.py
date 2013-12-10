"""
Production settings
"""
from comedylib.settings.common import *  # pylint: disable=W0614, W0401

DEBUG = False

DATABASES['default'].update({
    'NAME': 'comedylib',
    'USER': 'comedylib',
})

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': '127.0.0.1:11211',
    },
    'johnny': {
        'BACKEND': 'johnny.backends.memcached.PyLibMCCache',
        'LOCATION': '127.0.0.1:11211',
        'JOHNNY_CACHE': True,
    },
}
JOHNNY_MIDDLEWARE_KEY_PREFIX = 'jc_comedylib'

MIDDLEWARE_CLASSES = (
    # These need to go before any other middleware
    'johnny.middleware.LocalStoreClearMiddleware',
    'johnny.middleware.QueryCacheMiddleware',
) + MIDDLEWARE_CLASSES

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

ALLOWED_HOSTS = [
    '.comedylib.com',
    'django-dbbackup', # Used by the lib when sending traceback emails
]

INSTALLED_APPS += (
    'raven.contrib.django.raven_compat',
)

RAVEN_CONFIG = {
    'dsn': ('http://29f26e03533845338ccfcad3293a3bdf:'
            '29278d129e9643268a9f34f16902a54b@sentry.comedylib.com/2'),
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django': {
            'level': 'INFO',
            'handlers': ['sentry'],
            'propagate': False,
        },
        'celery': {
            'level': 'INFO',
            'handlers': ['sentry'],
            'propagate': True,
        },
    },
}

EMAIL_USE_TLS = True
EMAIL_HOST = 'mail.comedylib.com'
EMAIL_HOST_USER = 'feedback@comedylib.com'
EMAIL_HOST_PASSWORD = 'nkcw07homrqZCx7'
EMAIL_PORT = 25
