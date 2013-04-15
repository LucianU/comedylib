from django.conf.urls.defaults import patterns, url
from django.views.decorators.cache import cache_page

from content.views import (Home, About, CollectionList,
                           CollectionDetail, VideoDetail, Playlists)

urlpatterns = patterns('',
    url(r'^$', Home.as_view(), name='home'),
    url(r'^about/$', About.as_view(), name='about'),
    url(r'^comedians/$', cache_page(CollectionList.as_view(), 60 * 60),
        {'role': 0},
        name='comedians'),
    url(r'^comedians/(?P<slug>[a-z-]+)-(?P<pk>\d+)$',
        cache_page(CollectionDetail.as_view(), 60 * 60),
        name='comedian'),
    url(r'^shows/$', cache_page(CollectionList.as_view(), 60 * 60),
        {'role': 1},
        name='shows'),
    url(r'^shows/(?P<slug>[a-z-]+)-(?P<pk>\d+)$',
        cache_page(CollectionDetail.as_view(), 60 * 60),
        name='show'),
    url(r'^movies/$', cache_page(CollectionList.as_view(), 60 * 60),
        {'role': 2},
        name='movies'),
    url(r'^movies/(?P<slug>[a-z-]+)-(?P<pk>\d+)$',
        cache_page(CollectionDetail.as_view(), 60 * 60),
        name='movie'),
    url(r'^(?:comedians|shows|movies)/.*?/(?P<pk>\d+)',
        VideoDetail.as_view(),
        name='video'),
    url(r'^playlists/$', cache_page(Playlists.as_view(), 60 * 15),
        name='playlists'),
)
