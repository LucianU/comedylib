from django.views.generic import TemplateView, ListView

from content.models import Collection

class HomeView(TemplateView):
    template_name = 'content/home.html'

class AboutView(TemplateView):
    template_name = 'content/about.html'

class ComediansView(ListView):
    context_object_list = 'collection_list'
    queryset = Collection.objects.filter(role=0)
    template_name = 'content/collection_list.html'

class ShowsView(ComediansView):
    queryset = Collection.objects.filter(role=1)

class MoviesView(ComediansView):
    queryset = Collection.objects.filter(role=2)
