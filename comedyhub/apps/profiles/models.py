from django.contrib.auth.models import User
from django.db import models

from content.models import Video

class Profile(models.Model):
    user = models.OneToOneField(User)
    likes = models.ManyToManyField(Video, related_name='fans', null=True)
    dislikes = models.ManyToManyField(Video, related_name='haters', null=True)
    playlists = models.ManyToManyField(Video, related_name='list_makers',
                                       through='Playlist', null=True)
    picture = models.ImageField(upload_to='profiles', blank=True, null=True)
    description = models.TextField()

    def __unicode__(self):
        return u"%s: %s playlists" % (self.user.username,
                                      self.playlists.all().count())

class Playlist(models.Model):
    profile = models.ForeignKey(Profile)
    video = models.ForeignKey(Video)
    title = models.CharField(max_length=255)

    def __unicode__(self):
        return u"%s: %s videos" % (self.title, self.profile.username)
