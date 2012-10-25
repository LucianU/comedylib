from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, ListView, DetailView

from content.models import Collection, Video

class HomeView(TemplateView):
    template_name = 'content/home.html'

class AboutView(TemplateView):
    template_name = 'content/about.html'

    def render_to_response(self, context, **response_kwargs):
        self.request.breadcrumbs("About", self.request.path)
        return super(AboutView, self).render_to_response(context,
                                                         **response_kwargs)

class CollectionListView(ListView):
    context_object_list = 'collection_list'
    template_name = 'content/collection_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Collection.objects.filter(**self.kwargs)

    def render_to_response(self, context, **response_kwargs):
        self.request.breadcrumbs("%s" % self.request.path.strip('/').title(),
                                 "")
        return super(CollectionListView, self).render_to_response(context,
                                                                  **response_kwargs)

class CollectionDetailView(DetailView):
    context_object_name = 'collection'
    model = Collection

    def render_to_response(self, context, **response_kwargs):
        collection = context['collection']
        breadcrumbs = [(collection.name, "")]
        breadcrumbs.append((
            '%ss' % collection.get_role_display().title(),
            reverse('content:%ss' % collection.get_role_display())
        ))
        breadcrumbs.reverse()
        self.request.breadcrumbs(breadcrumbs)
        return super(CollectionDetailView, self).render_to_response(context,
                                                                    **response_kwargs)

class VideoDetailView(DetailView):
    context_object_name = 'video'
    model = Video

    def render_to_response(self, context, **response_kwargs):
        breadcrumbs = [(context['video'].title, "")]
        collection = context['video'].collection
        breadcrumbs.append((
            collection.name,
            reverse('content:%s' % collection.get_role_display(),
                    args=[collection.slug, collection.pk])
        ))
        breadcrumbs.append((
            '%ss' % collection.get_role_display().title(),
            reverse('content:%ss' % collection.get_role_display())
        ))
        breadcrumbs.reverse()
        self.request.breadcrumbs(breadcrumbs)
        return super(VideoDetailView, self).render_to_response(context,
                                                                  **response_kwargs)
