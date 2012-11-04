from django.conf.urls.defaults import patterns, url

from profiles.views import Home

urlpatterns = patterns('',
    url(r'^$', Home, name='home'),
)
