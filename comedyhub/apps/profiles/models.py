import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from content.models import Video

class Profile(models.Model):
    user = models.OneToOneField(User)
    feelings = models.ManyToManyField(Video, related_name='feelers',
                                      through='Feeling', null=True)
    playlists = models.ManyToManyField(Video, related_name='list_makers',
                                       through='Playlist', null=True)
    picture = models.ImageField(upload_to='profiles', blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return u"%s: %s playlists" % (self.user.username,
                                      self.playlists.all().count())


class Playlist(models.Model):
    profile = models.ForeignKey(Profile)
    video = models.ForeignKey(Video)
    title = models.CharField(max_length=255)

    def __unicode__(self):
        return u"%s: %s videos" % (self.title, self.profile.username)


class Feeling(models.Model):
    profile = models.ForeignKey(Profile)
    video = models.ForeignKey(Video)
    name = models.CharField(max_length=5)
    timestamp = models.DateTimeField(default=datetime.datetime.utcnow)


@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
    user = kwargs.get('instance')
    try:
        user.profile
    except Profile.DoesNotExist:
        Profile.objects.create(user=user)
