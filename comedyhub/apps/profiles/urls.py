from django.conf.urls.defaults import patterns, url

from profiles.views import LoginView

urlpatterns = patterns('',
    url('^login/$', LoginView.as_view(), name='login'),
)
