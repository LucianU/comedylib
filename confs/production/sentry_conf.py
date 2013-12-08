DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sentry',
        'USER': 'comedylib',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

SENTRY_KEY = 'RNHFkIOw/VvnLbNfizjM+yaBg5nTqmOvGpFo43jf2y60aldGV83/Pg=='

# Set this to false to require authentication
SENTRY_PUBLIC = False

# You should configure the absolute URI to Sentry. It will attempt topics
# guess it if you don't but proxies may interfere with this.
SENTRY_URL_PREFIX = 'http://sentry.comedylib.com'  # No trailing slash!
SENTRY_WEB_HOST = 'localhost'
SENTRY_WEB_PORT = 9000
SENTRY_WEB_OPTIONS = {
    'workers': 3,  # the number of gunicorn workers
}

# Mail server configuration

# For more information check Django's documentation:
# https://docs.djangoproject.com/en/1.3/topics/email/?from=olddocs#e-mail-backends

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'mail.comedylib.com'
EMAIL_HOST_USER = 'feedback@comedylib.com'
EMAIL_HOST_PASSWORD = 'nkcw07homrqZCx7'
EMAIL_PORT = 465
