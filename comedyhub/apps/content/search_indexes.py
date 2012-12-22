from haystack import site
from haystack.indexes import CharField, SearchIndex

from content.models import Collection, Video


class CollectionIndex(SearchIndex):
    text = CharField(document=True, use_template=True)

    def index_queryset(self):
        return Collection.objects.all()


class VideoIndex(SearchIndex):
    text = CharField(document=True, use_template=True)

    def index_queryset(self):
        return Video.objects.all()


site.register(Collection, CollectionIndex)
site.register(Video, VideoIndex)
