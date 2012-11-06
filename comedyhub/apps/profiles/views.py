#-*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from profiles.models import Profile

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

