"""
Development settings
"""
from comedyhub.settings.common import *  # pylint: disable=W0614, W0401

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INSTALLED_APPS += (
    'debug_toolbar',
)

INTERNAL_IPS = (
    '127.0.0.1',
)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

try:
    from comedyhub.settings.local import *  # pylint: disable=W0614, W0401
except ImportError:
    pass
