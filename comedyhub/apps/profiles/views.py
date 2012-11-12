#-*- coding: utf-8 -*-
import json

from django.contrib.comments.models import Comment
from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, View

from content.models import Video
from profiles.models import Profile, Feeling, Playlist, Bookmark

class Home(TemplateView):
    template_name = 'profiles/home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        if 'pk' in kwargs:
            profile = get_object_or_404(Profile, user__pk=kwargs['pk'])
            context['profile'] = profile
            recent_comms = Comment.objects.filter(user=profile.user).\
                                            order_by('-submit_date')[:5]
            recent_likes = Feeling.objects.filter(profile=profile, name='L').\
                                            order_by('-created')[:5]
            recent_pls = Playlist.objects.filter(profile=profile).\
                                            order_by('-created')[:5]
            context.update({
                'recent_comments': recent_comms,
                'recent_likes': recent_likes,
                'recent_playlists': recent_pls,
            })
        else:
            context['profile'] = self.request.user.profile
        return context


class Playlists(Home):
    template_name = 'profiles/playlists.html'

    def get_context_data(self, **kwargs):
        context = super(Playlists, self).get_context_data(**kwargs)
        context['playlists'] = context['profile'].playlists.all()
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

        if feeling not in ['L', 'D']:
            raise SuspiciousOperation

        Feeling.objects.create(profile=profile, video=video, name=feeling)
        return HttpResponse(json.dumps({'status': 'OK'}))


class AddToPlaylist(View):
    def post(self, request, *args, **kwargs):
        profile = request.user.profile
        video_id = request.POST.get('vid')
        playlist_id = request.POST.get('pid')

        video = get_object_or_404(Video, id=video_id)
        playlist = get_object_or_404(Playlist, profile=profile, id=playlist_id)

        playlist.videos.add(video)
        playlist.save()
        return HttpResponse(json.dumps({'status': 'OK'}))


class BookmarkPost(View):
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
        obj = get_object_or_404(obj_model, id=obj_id)
        Bookmark.objects.create(profile=profile, post=obj)
        return HttpResponse(json.dumps({'status': 'OK'}))
