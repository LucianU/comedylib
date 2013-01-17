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
EMAIL_HOST = 'localhost'
EMAIL_HOST_PASSWORD = ''
EMAIL_HOST_USER = ''
EMAIL_PORT = 25
EMAIL_USE_TLS = False

# http://twitter.com/apps/new
# It's important that input a callback URL, even if its useless.
# We have no idea why, consult Twitter.
TWITTER_CONSUMER_KEY = ''
TWITTER_CONSUMER_SECRET = ''

# http://developers.facebook.com/setup/
FACEBOOK_APP_ID = ''
FACEBOOK_API_SECRET = ''

# http://code.google.com/apis/accounts/docs/OAuth2.html#Registering
GOOGLE_OAUTH2_CLIENT_ID = ''
GOOGLE_OAUTH2_CLIENT_SECRET = ''

# https://github.com/settings/applications/new
GITHUB_APP_ID = ''
GITHUB_API_SECRET = ''

# https://trello.com/1/appKey/generate
TRELLO_API_KEY = '5a2e3827ba8ae413e0323102ac67ba2c'
TRELLO_API_SECRET = '54b176a81bfe50ea3546a1bf36f814b6ac3da0108699a58a49cc8daf498769ad'
