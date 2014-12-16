"""
Development settings
"""
from comedylib.settings.common import *  # pylint: disable=W0614, W0401

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INSTALLED_APPS += (
    'debug_toolbar',
    'johnny_panel',
)

INTERNAL_IPS = (
    '127.0.0.1',
)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'johnny_panel.panel.JohnnyPanel'
)

GOOGLE_OAUTH2_CLIENT_ID = '448075750287.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET = 'UhpdrUFe7E4OdUGcxv98py30'

try:
    from comedylib.settings.local import *  # pylint: disable=W0614, W0401
except ImportError:
    pass
