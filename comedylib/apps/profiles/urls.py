from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page

from profiles.views import (Home, Settings, Playlists, PlaylistDetail,
                            CreatePlaylist, EditPlaylist, DeletePlaylist,
                            HandlePlaylistItems, Bookmarks, HandleBookmarks,
                            VideoFeeling, Likes, AutoPlay)

login_patterns = patterns('',
    url(r'^$', Home.as_view(), name='own_home'),
    url(r'^settings/$', Settings.as_view(), name='settings'),
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
    url(r'^autoplay/$', AutoPlay.as_view(), name='autoplay'),
)

open_patterns = patterns('',
    url(r'^(?P<pk>\w+)$', cache_page(Home.as_view(), 60 * 60),
        name='user_home'),
    url(r'^(?P<pk>\w+)/playlists/$',
        cache_page(Playlists.as_view(), 60 * 15),
        name='user_playlists'),
)

def apply_login_required(login_patterns):
    """
    Applies the ``login_required`` decorator to the views in
    ``patterns``.
    """
    urls = []
    for pattern in login_patterns:
        urls.append(
            url(pattern.regex.pattern,
                login_required(pattern.callback),
                name=pattern.name,
                kwargs=pattern.default_args)
        )
    return patterns('', *urls)

urlpatterns = apply_login_required(login_patterns) + open_patterns
