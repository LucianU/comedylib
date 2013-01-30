from django.conf import settings
from django.conf.urls.defaults import patterns, url, include
from django.contrib.auth.views import login, logout

from registration.views import register

from accounts.forms import CustomAuthForm, SignUpForm

urlpatterns = patterns('',
    url('^login/$', login,
        {'authentication_form': CustomAuthForm},
        name='accounts_login'),
    url('^logout/$', logout,
        {'next_page': settings.LOGOUT_REDIRECT_URL},
        name='accounts_logout'),
    url(r'^register/$',
        register,
        {'backend': 'registration.backends.default.DefaultBackend',
         'form_class': SignUpForm},
        name='accounts_register'),

    url('^', include('registration.backends.default.urls')),
    url('^', include('social_auth.urls')),
)
