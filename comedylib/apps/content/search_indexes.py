from haystack.indexes import CharField, Indexable, SearchIndex

from content.models import Collection, Video


class CollectionIndex(SearchIndex, Indexable):
    text = CharField(document=True, use_template=True)

    def get_model(self):
        return Collection

    def index_queryset(self, using=None):
        return Collection.objects.all()


class VideoIndex(SearchIndex, Indexable):
    text = CharField(document=True, use_template=True)

    def get_model(self):
        return Video

    def index_queryset(self, using=None):
        return Video.objects.all()
