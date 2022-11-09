from django import forms

from profiles.models import Playlist, Profile


class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ('title',)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'feelings')
