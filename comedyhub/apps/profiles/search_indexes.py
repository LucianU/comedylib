from haystack import site
from haystack.indexes import CharField, SearchIndex

from profiles.models import Bookmark, Playlist


class BookmarkIndex(SearchIndex):
    text = CharField(document=True, use_template=True)

    def index_queryset(self):
        return Bookmark.objects.all()


class PlaylistIndex(SearchIndex):
    text = CharField(document=True, use_template=True)

    def index_queryset(self):
        return Playlist.objects.all()


site.register(Bookmark, BookmarkIndex)
site.register(Playlist, PlaylistIndex)
