import collections
import random

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import TemplateView, ListView, DetailView

from content.forms import CategsForm
from content.models import Collection, Video, Featured
from profiles.models import Playlist, Feeling
from taggit.models import TaggedItem


class Home(TemplateView):
    template_name = 'content/home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        recent_videos = self._get_recent_videos()
        for collection, vids in recent_videos.iteritems():
            context['%s_videos' % collection] = vids
        F_PL_NO = settings.FRONTPAGE_PLAYLISTS_NO
        context['playlists'] = Playlist.objects.filter(empty=False)[:F_PL_NO]
        featured = Featured.instance.get()
        if featured is not None:
            for role_id, role_name in Collection.ROLE_CHOICES:
                context['feat_%s' % role_name] = getattr(featured, role_name)
        return context

    def _get_recent_videos(self):
        videos = {}
        RV_NO = settings.RECENT_VIDEOS_NO
        for r_id, r_name in Collection.ROLE_CHOICES:
            videos[r_name] = Video.objects.filter(collection__role=r_id)[:RV_NO]
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
    paginate_by = settings.COLLECTION_LIST_NO

    def get_queryset(self):
        form = CategsForm(self.request.GET)

        if form.is_valid():
            Q_args = Q()
            categs = form.cleaned_data['categs']
            # Using Q objects to retrieve all TaggedItems with our
            # categories. We're doing this, so that we can retrieve
            # in a single query all the items belonging to the
            # different categories
            for categ in categs:
                Q_args |= Q(tag__name=categ)

            items = TaggedItem.objects.filter(
                Q_args, collection__role=self.kwargs['role']
            )

            # We group by tag the objects that the tagged items point to.
            # This way we'll be able to find the objects belonging to
            # all tags by using set intersection
            categ_items = collections.defaultdict(set)
            for item in items:
                categ_items[item.tag].add(item.content_object)

            # Building a new form, so that we have the currently checked
            # categories still checked on page reload
            self.categs_form = CategsForm(initial={'categs': categs})

            return list(set.intersection(*categ_items.values()))
        else:
            return Collection.objects.filter(**self.kwargs)

    def get_context_data(self, **kwargs):
        context = super(CollectionList, self).get_context_data(**kwargs)
        categs_form = getattr(self, 'categs_form', None)
        context['categs_form'] = (CategsForm() if categs_form is None
                                               else categs_form)
        return context

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
        # Retrieving public videos only
        videos_list = collection.videos.filter(status=1)
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
            profile = self.request.user.profile

            # If the user has expressed a feeling for the video
            try:
                feeling = Feeling.objects.get(profile=profile, video=video)
            except Feeling.DoesNotExist:
                context['vid_feel'] = None
            else:
                context['vid_feel'] = feeling.name

            # If he has bookmarked the video
            video_type = ContentType.objects.get(app_label='content',
                                                 model='video')
            bookmarked_vid = profile.bookmarks.filter(
                content_type=video_type,
                object_id=video.id
            ).exists()
            context['bookmarked_vid'] = bookmarked_vid

        # If we are in a playlist, we send all the other videos
        # belonging to this playlist and other specific info
        if 'pl' in self.request.GET:
            playlist = get_object_or_404(Playlist, id=self.request.GET['pl'])

            # We check if the user is authenticated to see if he's already
            # bookmarked the playlist
            if self.request.user.is_authenticated():
                profile = self.request.user.profile

                playlist_type = ContentType.objects.get(app_label='profiles',
                                                        model='playlist')
                bookmarked_pl = profile.bookmarks.filter(
                    content_type=playlist_type,
                    object_id=playlist.id
                ).exists()
                context['bookmarked_pl'] = bookmarked_pl

            collection_vids = playlist.videos.all()
            collection_vids_list = list(collection_vids)
            videos_count = collection_vids.count()
            video_index = collection_vids_list.index(video)

            prev_video = collection_vids_list[video_index - 1]
            next_video = collection_vids_list[(video_index + 1) % videos_count]

            prev_video_url = '%s?pl=%s' % (prev_video.get_absolute_url(),
                                           playlist.id)
            next_video_url = '%s?pl=%s' % (next_video.get_absolute_url(),
                                           playlist.id)
            context.update({
                'related_videos': collection_vids.exclude(id=video.id),
                'video_no': video_index + 1,
                'videos_count': videos_count,
                'prev_video_url': prev_video_url,
                'next_video_url': next_video_url,
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
