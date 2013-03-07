#-*- coding: utf-8 -*-
import json

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import SuspiciousOperation
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (TemplateView, View, ListView, CreateView,
                                  UpdateView, DetailView, FormView)

from content.models import Video
from profiles.forms import PlaylistForm, PictureForm
from profiles.models import Profile, Feeling, Playlist, Bookmark


class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def render_to_json_response(self, context, **response_kwargs):
        jsoned_context = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(jsoned_context, **response_kwargs)

    def form_invalid(self, form):
        if self.request.is_ajax():
            return self.render_to_json_response(form.errors, status=400)
        else:
            return super(AjaxableResponseMixin, self).form_invalid(form)

    def form_valid(self, form):
        if self.request.is_ajax():
            context = {
                'pk': form.instance.pk,
            }
            return self.render_to_json_response(context)
        else:
            return super(AjaxableResponseMixin, self).form_valid(form)


class Home(TemplateView):
    template_name = 'profiles/home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        if 'pk' in self.kwargs:
            profile = get_object_or_404(Profile, user__pk=self.kwargs['pk'])
        else:
            profile = self.request.user.profile

        recent_likes = (Feeling.objects.filter(profile=profile, name='L')
                                        .order_by('-created')[:5])
        recent_pls = (Playlist.objects.filter(profile=profile)
                                        .order_by('-created')[:5])
        context.update({
            'profile': profile,
            'recent_likes': recent_likes,
            'recent_playlists': recent_pls,
        })
        return context


class Settings(FormView):
    """
    This view actually handles two forms, a PictureForm and a
    PasswordChangeForm, because they are both displayed on the
    same page but in different tabs.
    """
    template_name = 'profiles/settings.html'
    picture_form = PictureForm
    password_form = PasswordChangeForm

    def get(self, request, *args, **kwargs):
        # Using the self.form_invalid method method just to avoid
        # code duplication, because the logic is the same
        return self.form_invalid(
            self.picture_form(), self.password_form(self.request.user)
        )

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            return self.form_valid(form)
        else:
            if type(form) == self.picture_form:
                return self.form_invalid(
                    form, self.password_form(self.request.user)
                )
            else:
                return self.form_invalid(self.picture_form(), form)

    def get_form(self, form_class):
        if form_class == self.picture_form:
            return form_class(**self.get_form_kwargs())

        return form_class(**self.get_password_form_kwargs())

    def get_form_class(self):
        """
        Only used when handling POST request in the case of
        this view, because on the GET request we send both forms.
        """
        if self.request.FILES:
            return self.picture_form
        else:
            return self.password_form

    def form_valid(self, form):
        user = self.request.user
        if type(form) == self.picture_form:
            user.profile.picture = self.request.FILES['picture']
            user.profile.save()
        else:
            form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, picture_form, password_form):
        return self.render_to_response(
            self.get_context_data(
                picture_form=picture_form,
                password_form=password_form,
            )
        )

    def get_success_url(self):
        return reverse('own_home')

    def get_password_form_kwargs(self):
        """
        This method has this special name, so as not to make checks
        in the generic `get_form_kwargs` method and adjust kwargs there
        """
        kwargs = self.get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(Settings, self).get_context_data(**kwargs)
        context['profile'] = self.request.user.profile
        return context


class Playlists(ListView):
    template_name = 'profiles/playlists.html'
    context_object_name = 'playlists'
    queryset = Playlist.objects.all()
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(Playlists, self).get_context_data(**kwargs)
        if 'pk' in self.kwargs:
            profile = get_object_or_404(Profile, user__pk=self.kwargs['pk'])
        else:
            profile = self.request.user.profile
        context['playlists'] = profile.playlists.all()
        context['profile'] = profile
        context['playlist_form'] = PlaylistForm()
        return context


class PlaylistDetail(DetailView):
    template_name = 'profiles/playlist_detail.html'
    context_object_name = 'playlist'
    model = Playlist

    def get_context_data(self, **kwargs):
        context = super(PlaylistDetail, self).get_context_data(**kwargs)
        context['profile'] = self.request.user.profile
        return context


class CreatePlaylist(AjaxableResponseMixin, CreateView):
    template_name = 'profiles/create_playlist.html'
    form_class = PlaylistForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.profile = self.request.user.profile
        self.object.save()
        return super(CreatePlaylist, self).form_valid(form)

    def get_success_url(self):
        return reverse('own_playlists')


class EditPlaylist(AjaxableResponseMixin, UpdateView):
    template_name = 'profiles/edit_playlist.html'
    form_class = PlaylistForm

    def get_queryset(self):
        return Playlist.objects.filter(profile=self.request.user.profile)


class DeletePlaylist(View):
    def post(self, request, *args, **kwargs):
        profile = request.user.profile
        playlist_id = request.POST.get('pid')
        playlist = get_object_or_404(Playlist, profile=profile, id=playlist_id)
        playlist.delete()

        if request.is_ajax():
            return HttpResponse(json.dumps({'status': 'OK'}))
        return redirect('own_playlists')


class HandlePlaylistItems(View):
    def post(self, request, *args, **kwargs):
        profile = request.user.profile
        video_id = request.POST.get('vid')
        playlist_id = request.POST.get('pid')
        action = kwargs.get('action')

        video = get_object_or_404(Video, id=video_id)
        playlist = get_object_or_404(Playlist, profile=profile, id=playlist_id)

        # Retrieving 'add' or 'remove' method from 'videos'
        action_method = getattr(playlist.videos, action)
        action_method(video)
        playlist.save()
        return HttpResponse(json.dumps({'status': 'OK'}))


class Bookmarks(ListView):
    template_name = 'profiles/bookmarks.html'
    context_object_name = 'bookmarks'
    paginate_by = 20

    def get_queryset(self):
        post_types_meta = {
            'V': {'app_label': 'content', 'model': 'video'},
            'P': {'app_label': 'profiles', 'model': 'playlist'},
        }
        bookmarks = self.request.user.profile.bookmarks.all()
        post = self.request.GET.get('post')
        if post is not None:
            try:
                post_type_meta = post_types_meta[post]
            except KeyError:
                raise SuspiciousOperation
            else:
                post_type = ContentType.objects.get(**post_type_meta)
                bookmarks = bookmarks.filter(content_type=post_type)
        return bookmarks

    def get_context_data(self, **kwargs):
        context = super(Bookmarks, self).get_context_data(**kwargs)
        post_types = {
            'V': 'Video',
            'P': 'Playlist',
        }
        post_type = post_types[self.request.GET.get('post')]
        context.update({
            'post_type': post_type,
            'profile': self.request.user.profile,
        })
        return context


class HandleBookmarks(View):
    def post(self, request, *args, **kwargs):
        objs = {
            'V': Video,
            'P': Playlist,
        }
        profile = request.user.profile
        obj_id = request.POST.get('id')
        try:
            obj_model = objs[request.POST['obj']]
        except KeyError:
            raise SuspiciousOperation

        # We're not using the object, but we are testing to
        # make sure that it exists before bookmarking it, thus
        # avoiding an error at that later stage
        get_object_or_404(obj_model, id=obj_id)

        obj_type = ContentType.objects.get_for_model(obj_model)
        # Making sure that we don't bookmark the same post twice
        bookmark, created = Bookmark.objects.get_or_create(
            profile=profile,
            content_type=obj_type,
            object_id=obj_id
        )
        if kwargs.get('action') == 'remove':
            bookmark.delete()

        return HttpResponse(json.dumps({'status': 'OK'}))


class Likes(ListView):
    template_name = 'profiles/liked_videos.html'
    context_object_name = 'liked_videos'
    paginate_by = 20

    def get_queryset(self):
        return self.request.user.profile.feelings.filter(feelings__name='L')

    def get_context_data(self, **kwargs):
        context = super(Likes, self).get_context_data(**kwargs)
        context['profile'] = self.request.user.profile
        return context


class VideoFeeling(View):
    def post(self, request, *args, **kwargs):
        profile = request.user.profile
        video_id = request.POST.get('vid')
        feeling = request.POST.get('feeling')
        try:
            video = Video.objects.get(id=video_id)
        except Video.ObjectDoesNotExist:
            raise SuspiciousOperation

        if feeling not in ['L', 'D', 'U']:
            raise SuspiciousOperation

        # Undoing the like or the dislike
        if feeling == 'U':
            Feeling.objects.get(profile=profile, video=video).delete()
        else:
            # Making sure the user doesn't like or dislike the same
            # video twice.
            obj, created = Feeling.objects.get_or_create(profile=profile,
                                                         video=video)
            # If the feeling has changed, we save this change
            if obj.name != feeling:
                obj.name = feeling
                obj.save()

        return HttpResponse(json.dumps({'status': 'OK'}))
