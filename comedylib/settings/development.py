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
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.cache.CacheDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
    'johnny_panel.panel.JohnnyPanel'
)

GOOGLE_OAUTH2_CLIENT_ID = '448075750287.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET = 'UhpdrUFe7E4OdUGcxv98py30'

try:
    from comedylib.settings.local import *  # pylint: disable=W0614, W0401
except ImportError:
    pass
