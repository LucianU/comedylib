#-*- coding: utf-8 -*-
import json

from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, View

from content.models import Video
from profiles.models import Profile, Feeling, Playlist

class Home(TemplateView):
    template_name = 'profiles/home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        if 'pk' in kwargs:
            profile = get_object_or_404(Profile, user__pk=kwargs['pk'])
            context['profile'] = profile
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
        video_id = request.POST.get('id')
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
