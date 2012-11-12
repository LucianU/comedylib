from comedyhub.settings.common import *

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INSTALLED_APPS += (
    'debug_toolbar',
)

INTERNAL_IPS = (
    '127.0.0.1',
)

try:
    from comedyhub.settings.local import *
except ImportError:
    pass
