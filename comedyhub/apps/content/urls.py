from django.conf.urls.defaults import patterns, url

from content.views import (HomeView, AboutView, ComediansView,
                           ShowsView, MoviesView)

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view()),
    url(r'^about/$', AboutView.as_view()),
    url(r'^comedians/', ComediansView.as_view()),
    url(r'^shows/', ShowsView.as_view()),
    url(r'^movies/', MoviesView.as_view()),
)
