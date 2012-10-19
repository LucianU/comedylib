from django.views.generic import TemplateView, ListView, DetailView

from content.models import Collection

class HomeView(TemplateView):
    template_name = 'content/home.html'

class AboutView(TemplateView):
    template_name = 'content/about.html'

class CollectionListView(ListView):
    context_object_list = 'collection_list'
    template_name = 'content/collection_list.html'

    def get_queryset(self):
        return Collection.objects.filter(**self.kwargs)

class CollectionDetailView(DetailView):
    context_object_name = 'collection'
    model = Collection
