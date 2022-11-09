"""
The entry point used by the server to run the project.
"""
from django.conf import settings
import django.core.handlers.wsgi
import newrelic.agent

newrelic.agent.initialize(
    '/usr/local/etc/newrelic/comedylib/newrelic.ini',
    settings.ENV
)
application = django.core.handlers.wsgi.WSGIHandler()
