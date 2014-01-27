"""
Staging settings
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
]

INSTALLED_APPS += (
    'raven.contrib.django.raven_compat',
)

RAVEN_CONFIG = {
    'dsn': 'http://09c6fa4884924637800194cab7e0c920:'
           'cb72c14a3a6c42bc9a6250c62f7dcb44@sentry.comedylib.com/3'
}

EMAIL_USE_TLS = True
EMAIL_HOST = 'mail.comedylib.com'
EMAIL_HOST_USER = 'feedback@comedylib.com'
EMAIL_HOST_PASSWORD = 'nkcw07homrqZCx7'
EMAIL_PORT = 25
