from django.conf.urls.defaults import patterns, url

from registration.views import register

from profiles.forms import SignUpForm
from profiles.views import LoginView, logout

urlpatterns = patterns('',
    url('^login/$', LoginView.as_view(), name='login'),
    url('^logout/$', logout, name='logout'),
    url(r'^register/$',
        register,
        {'backend': 'registration.backends.default.DefaultBackend',
         'form_class': SignUpForm},
        name='register'),
)
