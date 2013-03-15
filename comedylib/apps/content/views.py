import random

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import TemplateView, ListView, DetailView

from content.models import Collection, Video, Featured
from profiles.models import Playlist, Feeling


class Home(TemplateView):
    template_name = 'content/home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        recent_videos = self._get_recent_videos()
        for collection, vids in recent_videos.iteritems():
            context['%s_videos' % collection] = vids
        context['playlists'] = Playlist.objects.filter(empty=False)[:8]
        featured = Featured.instance.get()
        if featured is not None:
            for role_id, role_name in Collection.ROLE_CHOICES:
                context['feat_%s' % role_name] = getattr(featured, role_name)
        return context

    def _get_recent_videos(self):
        videos = {}
        for r_id, r_name in Collection.ROLE_CHOICES:
            videos[r_name] = Video.objects.filter(collection__role=r_id)[:6]
        return videos


class About(TemplateView):
    template_name = 'content/about.html'

    def render_to_response(self, context, **response_kwargs):
        self.request.breadcrumbs("About", self.request.path)
        return super(About, self).render_to_response(
            context,
            **response_kwargs
        )


class CollectionList(ListView):
    context_object_name = 'collection_list'
    template_name = 'content/collection_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Collection.objects.filter(**self.kwargs)

    def render_to_response(self, context, **response_kwargs):
        self.request.breadcrumbs(self.request.path.strip('/').title(), "")
        return super(CollectionList, self).render_to_response(
            context,
            **response_kwargs
        )


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
        return super(CollectionDetail, self).render_to_response(
            context,
            **response_kwargs
        )


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

        # We do some extra checks when the user is authenticated
        if self.request.user.is_authenticated():
            # If the user has expressed a feeling for the video
            profile = self.request.user.profile
            try:
                feeling = Feeling.objects.get(profile=profile, video=video)
            except Feeling.DoesNotExist:
                context['vid_feel'] = None
            else:
                context['vid_feel'] = feeling.name

            # If he has bookmarked the video
            video_type = ContentType.objects.get(app_label='content',
                                                 model='video')
            bookmarked = profile.bookmarks.filter(content_type=video_type,
                                                  object_id=video.id).exists()
            context['bookmarked'] = bookmarked

        # If we are in a playlist, we send all the other videos
        # belonging to this playlist
        if 'pl' in self.request.GET:
            playlist = get_object_or_404(Playlist, id=self.request.GET['pl'])
            collection_vids = playlist.videos.all().exclude(id=video.id)
            context.update({
                'related_videos': collection_vids,
                'current_pl': playlist,
            })
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
        return super(VideoDetail, self).render_to_response(
            context,
            **response_kwargs
        )


class Playlists(ListView):
    context_object_name = 'playlists'
    template_name = 'content/playlists.html'
    paginate_by = 20
    queryset = Playlist.objects.filter(empty=False)
