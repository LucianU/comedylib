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
