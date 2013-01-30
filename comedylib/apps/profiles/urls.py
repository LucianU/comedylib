from django.conf.urls.defaults import patterns, url

from profiles.views import (Home, Playlists, PlaylistDetail, CreatePlaylist,
                            EditPlaylist, DeletePlaylist, HandlePlaylistItems,
                            Bookmarks, HandleBookmarks, VideoFeeling, Likes)

urlpatterns = patterns('',
    url(r'^$', Home.as_view(), name='own_home'),
    url(r'^playlists/$', Playlists.as_view(), name='own_playlists'),
    url(r'^playlists/create$', CreatePlaylist.as_view(),
        name='create_playlist'),
    url(r'^playlists/delete$', DeletePlaylist.as_view(),
        name='delete_playlist'),
    url(r'^playlists/add$', HandlePlaylistItems.as_view(),
        name='add_to_playlist', kwargs={'action': 'add'}),
    url(r'^playlists/remove$', HandlePlaylistItems.as_view(),
        name='remove_from_playlist', kwargs={'action': 'remove'}),

    url(r'^playlists/(?P<slug>[a-z0-9-]+)_(?P<pk>\d+)/$',
        PlaylistDetail.as_view(), name='playlist'),
    url(r'^playlists/(?P<slug>[a-z0-9-]+)_(?P<pk>\d+)/edit$',
        EditPlaylist.as_view(), name='edit_playlist'),

    url(r'^bookmarks/$', Bookmarks.as_view(), name='own_bookmarks'),
    url(r'^bookmarks/add$', HandleBookmarks.as_view(),
        name='add_to_bookmarks', kwargs={'action': 'add'}),
    url(r'^bookmarks/remove$', HandleBookmarks.as_view(),
        name='remove_from_bookmarks', kwargs={'action': 'remove'}),

    url(r'^likes/$', Likes.as_view(), name='own_likes'),
    url(r'^vfeel$', VideoFeeling.as_view(), name='vid_feel'),
    url(r'^(?P<pk>\w+)$', Home.as_view(), name='user_home'),
    url(r'^(?P<pk>\w+)/playlists/$', Playlists.as_view(),
        name='user_playlists'),
)
