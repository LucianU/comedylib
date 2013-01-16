from django.conf.urls.defaults import patterns, url

from profiles.views import (Home, Playlists, VideoFeeling, AddToPlaylist,
                            BookmarkPost, Bookmarks, Likes, CreatePlaylist)

urlpatterns = patterns('',
    url(r'^$', Home.as_view(), name='own_home'),
    url(r'^playlists/$', Playlists.as_view(), name='own_playlists'),
    url(r'^bookmarks/$', Bookmarks.as_view(), name='own_bookmarks'),
    url(r'^likes/$', Likes.as_view(), name='own_likes'),
    url(r'^vfeel$', VideoFeeling.as_view(), name='vid_feel'),
    url(r'^addtopl$', AddToPlaylist.as_view(), name='add_to_playlist'),
    url(r'^createpl$', CreatePlaylist.as_view(), name='create_playlist'),
    url(r'^bookmark$', BookmarkPost.as_view(), name='bookmark'),
    url(r'^(?P<pk>\w+)$', Home.as_view(), name='user_home'),
    url(r'^(?P<pk>\w+)/playlists/$', Playlists.as_view(),
        name='user_playlists'),
)
