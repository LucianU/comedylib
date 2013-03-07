from django import forms

from profiles.models import Playlist


class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ('title',)


class PictureForm(forms.Form):
    picture = forms.ImageField(required=False)
