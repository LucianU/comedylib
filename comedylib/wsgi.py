"""
The entry point used by the server to run the project.
"""
import django.core.handlers.wsgi
import newrelic.agent

newrelic.agent.initialize(
    '/home/comedylib/comedylib/confs/production/newrelic.ini'
)
application = django.core.handlers.wsgi.WSGIHandler()
