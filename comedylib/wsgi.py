"""
The entry point used by the server to run the project.
"""
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
