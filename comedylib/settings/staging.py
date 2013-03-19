"""
Staging settings
"""
from comedylib.settings.common import *  # pylint: disable=W0614, W0401

DEBUG = False

DATABASES['default'].update({
    'NAME': 'stag_comedylib',
    'USER': 'comedylib',
})

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)
