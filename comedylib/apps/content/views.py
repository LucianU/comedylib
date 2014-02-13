import collections
import hashlib
import random
from urllib2 import urlparse

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
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

        # Getting recent videos
        context.update(self._get_recent_videos())

        # Getting featured collections
        context.update(self._get_featured())

        # Getting random playlists
        context['playlists'] = self._get_random_playlists()

        return context

    def _get_recent_videos(self):
        cache_key = 'content_home_rv'
        videos = cache.get(cache_key)
        if videos is not None:
            return videos

        videos = {}
        RV_NO = settings.RECENT_VIDEOS_NO
        for r_id, r_name in Collection.ROLE_CHOICES:
            videos['%s_videos' % r_name] = Video.objects.filter(
                collection__role=r_id
            )[:RV_NO]

        # Caching for 10 minutes
        cache.set(cache_key, videos, 60 * 10)
        return videos

    def _get_random_playlists(self):
        cache_key = 'content_home_rp'
        playlists = cache.get(cache_key)
        if playlists is not None:
            return playlists

        playlist_ids = (Playlist.objects.filter(empty=False)
                                        .values_list('id', flat=True))
        if len(playlist_ids) > settings.FRONTPAGE_PLAYLISTS_NO:
            random_ids = random.sample(playlist_ids,
                                       settings.FRONTPAGE_PLAYLISTS_NO)
        else:
            random_ids = playlist_ids
        playlists = Playlist.objects.filter(id__in=random_ids)

        # Caching for 10 minutes
        cache.set(cache_key, playlists, 60 * 10)
        return playlists

    def _get_featured(self):
        featured_inst = Featured.instance.get()
        featured = {}
        for role_id, role_name in Collection.ROLE_CHOICES:
            featured['feat_%s' % role_name] = getattr(featured_inst,
                                                      role_name)
        return featured


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

    def _get_collections(self, categs=None):
        if categs is not None:
            # There is a limit of 255 characters to a memcached key
            # This is a way to avoid going over that limit
            categs_indices = ''.join(categ[0] for categ in categs)
            categs_key = hashlib.sha1(categs_indices).hexdigest()
            cache_key = 'coll_list_%s_%s' % (self.kwargs['role'], categs_key)
        else:
            cache_key = 'coll_list_%s' % (self.kwargs['role'],)

        coll_list = cache.get(cache_key)
        if coll_list is not None:
            return coll_list

        if categs is not None:
            Q_args = Q()
            # Using Q objects to retrieve all TaggedItems with our
            # categories. We're doing this, so that we can retrieve
            # in a single query all the items belonging to the
            # different categories
            for categ in categs:
                Q_args |= Q(tag__name=categ)

            items = TaggedItem.objects.filter(
                Q_args, collection__role=self.kwargs['role']
            )

            # It's possible that there are no items that have all
            # the categs
            if not items:
                return items

            # We group by tag the objects that the tagged items point to.
            # This way we'll be able to find the objects belonging to
            # all tags by using set intersection
            categ_items = collections.defaultdict(set)
            for item in items:
                categ_items[item.tag].add(item.content_object)

            # We get the collections that are common to all tags
            coll_list = list(set.intersection(*categ_items.values()))
        else:
            coll_list = Collection.objects.filter(role=self.kwargs['role'])

        cache.set(cache_key, coll_list, 60 * 60)
        return coll_list

    def get_queryset(self):
        form = CategsForm(self.kwargs['role'], self.request.GET)
        categs = None

        if form.is_valid():
            categs = form.cleaned_data['categs']
            # Building a new form, so that we have the currently checked
            # categories still checked on page reload
            self.categs_form = CategsForm(self.kwargs['role'],
                                          initial={'categs': categs})

        return self._get_collections(categs)

    def get_context_data(self, **kwargs):
        context = super(CollectionList, self).get_context_data(**kwargs)
        categs_form = getattr(self, 'categs_form', None)
        context['categs_form'] = (CategsForm(self.kwargs['role'])
                                  if categs_form is None else categs_form)
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

    def _get_collection_videos(self, collection):
        cache_key = 'coll_videos_%s' % (collection.id,)
        videos = cache.get(cache_key)
        if videos is not None:
            return videos

        # Retrieving public videos only
        videos = collection.videos.filter(status=1)
        cache.set(cache_key, videos, 60 * 60)
        return videos

    def get_context_data(self, **kwargs):
        context = super(CollectionDetail, self).get_context_data(**kwargs)
        collection = context['collection']
        videos_list = self._get_collection_videos(collection)
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

    def _get_video_yt_id(self, video_url):
        """
        Returns the youtube ID of the video.
        """
        url_params = urlparse.urlparse(video_url).query
        return urlparse.parse_qs(url_params)['v'][0]

    def _get_video_feeling(self, profile, video):
        """
        Returns the feeling expressed for the video, if any.
        """
        try:
            feeling = Feeling.objects.get(profile=profile, video=video)
        except Feeling.DoesNotExist:
            return {'vid_feel': None}
        else:
            return {'vid_feel': feeling.name}

    def _get_obj_bookmark_status(self, profile, obj):
        """
        Returns the bookmark status of the object (video or playlist).
        """
        obj_contenttype = ContentType.objects.get_for_model(obj)
        bookmark_status = profile.bookmarks.filter(
            content_type=obj_contenttype,
            object_id=obj.id
        ).exists()
        return {'bookmarked_%s' % obj_contenttype.name: bookmark_status}

    def _get_playlist_context(self, playlist, current_video):
        """
        Returns the info needed to know where we are in the current
        playlist.
        """
        videos = playlist.videos.playlist_order()
        videos_list = list(videos)
        videos_count = len(videos_list)
        video_index = videos_list.index(current_video)

        prev_video = videos_list[video_index - 1]
        next_video = videos_list[(video_index + 1) % videos_count]

        prev_video_url = '%s?pl=%s' % (prev_video.get_absolute_url(),
                                       playlist.id)
        next_video_url = '%s?pl=%s' % (next_video.get_absolute_url(),
                                       playlist.id)
        return {
            'related_videos': videos.exclude(id=current_video.id),
            'video_no': video_index + 1,
            'videos_count': videos_count,
            'prev_video_url': prev_video_url,
            'next_video_url': next_video_url,
            'current_pl': playlist,
        }

    def _get_related_videos(self, video):
        """
        Returns videos related to the specified video when not running
        in a playlist.
        """
        cache_key = 'rel_video_%s' % video.id
        related_videos = cache.get(cache_key)
        if related_videos is not None:
            return {'related_videos': related_videos}

        collection = video.collection
        collection_vids = collection.videos.all().exclude(id=video.id)
        if len(collection_vids) < settings.RELATED_VIDS_NO:
            related_videos = collection_vids
        else:
            related_videos = random.sample(collection_vids, 12)

        cache.set(cache_key, related_videos, 60 * 60)
        return {'related_videos': related_videos}

    def get_context_data(self, **kwargs):
        context = super(VideoDetail, self).get_context_data(**kwargs)
        video = context['video']
        context['video_yt_id'] = self._get_video_yt_id(video.url)

        # We do some extra checks when the user is authenticated
        if self.request.user.is_authenticated():
            profile = self.request.user.profile

            # If the user has expressed a feeling for the video
            context.update(self._get_video_feeling(profile, video))
            # If he has bookmarked the video
            context.update(self._get_obj_bookmark_status(profile, video))

        # If we are in a playlist, we send all the other videos
        # belonging to this playlist and other specific info
        if 'pl' in self.request.GET:
            playlist = get_object_or_404(Playlist, id=self.request.GET['pl'])

            # We check if the user is authenticated to see if he's already
            # bookmarked the playlist
            if self.request.user.is_authenticated():
                profile = self.request.user.profile

                context.update(self._get_obj_bookmark_status(profile, playlist))

            context.update(self._get_playlist_context(playlist, video))
        else:
            context.update(self._get_related_videos(video))

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
    paginate_by = settings.PLAYLISTS_PER_PAGE_NO

    def get_queryset(self):
        cache_key = 'content_pls'
        playlists = cache.get(cache_key)
        if playlists is not None:
            return playlists

        playlists = Playlist.objects.filter(empty=False)

        # Caching for 30 minutes
        cache.set(cache_key, playlists, 60 * 30)
        return playlists
