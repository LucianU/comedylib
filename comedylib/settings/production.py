"""
Production settings
"""
from comedylib.settings.common import *  # pylint: disable=W0614, W0401

DEBUG = False

DATABASES['default'].update({
    'NAME': 'comedylib',
    'USER': 'comedylib',
})
