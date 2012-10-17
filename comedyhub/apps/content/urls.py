from django.conf.urls.defaults import patterns, url

from content.views import (HomeView, AboutView, ComediansView,
                           ShowsView, MoviesView, CollectionView)

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view()),
    url(r'^about/$', AboutView.as_view()),
    url(r'^comedians/', ComediansView.as_view()),
    url(r'^comedians/(?P<pk>\d+)', CollectionView.as_view()),
    url(r'^shows/', ShowsView.as_view()),
    url(r'^shows/(?P<pk>\d+)', CollectionView.as_view()),
    url(r'^movies/', MoviesView.as_view()),
    url(r'^movies/(?P<pk>\d+)', CollectionView.as_view()),
)
