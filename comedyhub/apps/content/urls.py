from django.conf.urls.defaults import patterns, url

from content.views import (HomeView, AboutView, CollectionListView,
                           CollectionDetailView)

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^about/$', AboutView.as_view(), name='about'),
    url(r'^comedians/$', CollectionListView.as_view(), {'role': 0},
        name='comedians'),
    url(r'^comedians/(?P<slug>[a-z-]+)-(?P<pk>\d+)', CollectionDetailView.as_view(),
        name='comedian'),
    url(r'^shows/$', CollectionListView.as_view(), {'role': 1},
        name='shows'),
    url(r'^shows/(?P<slug>[a-z-])-(?P<pk>\d+)', CollectionDetailView.as_view(), name='show'),
    url(r'^movies/$', CollectionListView.as_view(), {'role': 2},
        name='movies'),
    url(r'^movies/(?P<slug>[a-z-])-(?P<pk>\d+)', CollectionDetailView.as_view(), name='movie'),
)
