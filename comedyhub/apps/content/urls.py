from django.conf.urls.defaults import patterns, url

from content.views import (HomeView, AboutView, ComediansView,
                           ShowsView, MoviesView, CollectionDetailView)

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^about/$', AboutView.as_view(), name='about'),
    url(r'^comedians/$', ComediansView.as_view(), name='comedians'),
    url(r'^comedians/(?P<pk>\d+)', CollectionDetailView.as_view(),
        name='comedian'),
    url(r'^shows/$', ShowsView.as_view(), name='shows'),
    url(r'^shows/(?P<pk>\d+)', CollectionDetailView.as_view(), name='show'),
    url(r'^movies/$', MoviesView.as_view(), name='movies'),
    url(r'^movies/(?P<pk>\d+)', CollectionDetailView.as_view(), name='movie'),
)
