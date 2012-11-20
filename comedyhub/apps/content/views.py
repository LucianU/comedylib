import random

from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import TemplateView, ListView, DetailView

from content.models import Collection, Video
from profiles.models import Playlist, Feeling

class Home(TemplateView):
    template_name = 'content/home.html'

class About(TemplateView):
    template_name = 'content/about.html'

    def render_to_response(self, context, **response_kwargs):
        self.request.breadcrumbs("About", self.request.path)
        return super(About, self).render_to_response(context,
                                                     **response_kwargs)

class CollectionList(ListView):
    context_object_list = 'collection_list'
    template_name = 'content/collection_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Collection.objects.filter(**self.kwargs)

    def render_to_response(self, context, **response_kwargs):
        self.request.breadcrumbs("%s" % self.request.path.strip('/').title(),
                                 "")
        return super(CollectionList, self).render_to_response(context,
                                                              **response_kwargs)

class CollectionDetail(DetailView):
    context_object_name = 'collection'
    model = Collection

    def get_context_data(self, **kwargs):
        context = super(CollectionDetail, self).get_context_data(**kwargs)
        collection = context['collection']
        videos_list = collection.videos.all()
        paginator = Paginator(videos_list, 20)
        page = self.request.GET.get('page')
        try:
            videos = paginator.page(page)
        except PageNotAnInteger:
            videos = paginator.page(1)
        except EmptyPage:
            videos = paginator.page(paginator.num_pages)
        context.update({'videos': videos, 'paginator': paginator,
                        'page_obj': videos})
        return context

    def render_to_response(self, context, **response_kwargs):
        collection = context['collection']
        breadcrumbs = [(collection.name, "")]
        breadcrumbs.append((
            '%ss' % collection.get_role_display().title(),
            reverse('content:%ss' % collection.get_role_display())
        ))
        breadcrumbs.reverse()
        self.request.breadcrumbs(breadcrumbs)
        return super(CollectionDetail, self).render_to_response(context,
                                                                **response_kwargs)

class VideoDetail(DetailView):
    context_object_name = 'video'
    model = Video

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):
        return super(VideoDetail, self).dispatch(*args, **kwargs)

    def get_object(self, queryset=None):
        video = super(VideoDetail, self).get_object(queryset)
        video.views += 1
        video.save()
        return video

    def get_context_data(self, **kwargs):
        context = super(VideoDetail, self).get_context_data(**kwargs)
        video = context['video']

        # We check if this video is liked or disliked by the user
        if self.request.user.is_authenticated():
            profile = self.request.user.profile
            try:
                feeling = Feeling.objects.get(profile=profile, video=video)
            except Feeling.DoesNotExist:
                context['vid_feel'] = None
            else:
                context['vid_feel'] = feeling.name

        # If we are in a playlist, we send all the other videos
        # belonging to this playlist
        if 'pl' in kwargs:
            playlist = get_object_or_404(Playlist, id=kwargs['pl'])
            collection_vids = playlist.videos.all().exclude(id=video.id)
            context['related_videos'] = collection_vids
        else:
            collection = video.collection
            collection_vids = collection.videos.all().exclude(id=video.id)
            if len(collection_vids) < settings.RELATED_VIDS_NO:
                context['related_videos'] = collection_vids
            else:
                context['related_videos'] = random.sample(collection_vids, 12)

        return context

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
        return super(VideoDetail, self).render_to_response(context,
                                                           **response_kwargs)
