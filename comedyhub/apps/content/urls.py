from django.conf.urls.defaults import patterns, url

from content.views import (Home, About, CollectionList,
                           CollectionDetail, VideoDetail,
                           VideoLike)

urlpatterns = patterns('',
    url(r'^$', Home.as_view(), name='home'),
    url(r'^about/$', About.as_view(), name='about'),
    url(r'^comedians/$', CollectionList.as_view(), {'role': 0},
        name='comedians'),
    url(r'^comedians/(?P<slug>[a-z-]+)-(?P<pk>\d+)$', CollectionDetail.as_view(),
        name='comedian'),
    url(r'^shows/$', CollectionList.as_view(), {'role': 1},
        name='shows'),
    url(r'^shows/(?P<slug>[a-z-]+)-(?P<pk>\d+)$', CollectionDetail.as_view(), name='show'),
    url(r'^movies/$', CollectionList.as_view(), {'role': 2},
        name='movies'),
    url(r'^movies/(?P<slug>[a-z-]+)-(?P<pk>\d+)$', CollectionDetail.as_view(), name='movie'),
    url(r'^(?:comedians|shows|movies)/.*?/(?P<pk>\d+)',
        VideoDetail.as_view(), name='video'),
    url(r'^v/like', VideoLike.as_view(), name='video_like'),
)
