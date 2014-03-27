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
    'dsn': 'http://ba670bac2cac47dfbcf0b43e16715fa5:'
           '983c2bca1e424413ae0ae808c58c81c7@sentry.comedylib.com/2'
}

DEFAULT_FROM_EMAIL = 'noreply@comedylib.com'

EMAIL_USE_TLS = True
EMAIL_HOST = 'mail.comedylib.com'
EMAIL_HOST_USER = 'feedback@comedylib.com'
EMAIL_HOST_PASSWORD = 'nkcw07homrqZCx7'
EMAIL_PORT = 25
