from django.contrib.auth.models import User
from django.db import models

from content.models import Video

class Profile(models.Model):
    user = models.OneToOneField(User)
    likes = models.ManyToManyField(Video, related_name='profiles')
    playlists = models.ManyToManyField(Video, related_name='profiles',
                                   through='Playlist')
    photo = models.ImageField()
    description = models.TextField()

class Playlist(models.Model):
    profile = models.ForeignKey(Profile)
    video = models.ForeignKey(Video)
    title = models.CharField(max_length=255)
