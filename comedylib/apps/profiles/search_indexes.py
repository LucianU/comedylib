from haystack.indexes import CharField, Indexable, SearchIndex

from profiles.models import Bookmark, Playlist


class BookmarkIndex(SearchIndex, Indexable):
    text = CharField(document=True, use_template=True)

    def get_model(self):
        return Bookmark

    def index_queryset(self, using=None):
        return Bookmark.objects.all()


class PlaylistIndex(SearchIndex, Indexable):
    text = CharField(document=True, use_template=True)

    def get_model(self):
        return Playlist

    def index_queryset(self, using=None):
        return Playlist.objects.all()
