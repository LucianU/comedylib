import datetime

from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from comedyhub.mixins import CreatedMixin
from content.models import Video

class Profile(models.Model):
    user = models.OneToOneField(User)
    feelings = models.ManyToManyField(Video, through='Feeling', null=True)
    picture = models.ImageField(upload_to='profiles', blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return u"%s: %s playlists" % (self.user.username,
                                      self.playlists.all().count())


class Playlist(CreatedMixin):
    profile = models.ForeignKey(Profile, related_name='playlists')
    videos = models.ManyToManyField(Video, related_name='playlists', null=True)
    title = models.CharField(max_length=255)

    def __unicode__(self):
        return u"%s: %s videos" % (self.title, self.profile.username)


class Feeling(models.Model):
    NAME_CHOICES = (
        ('L', 'like'),
        ('D', 'dislike'),
    )
    profile = models.ForeignKey(Profile)
    video = models.ForeignKey(Video, related_name='feelings')
    name = models.CharField(max_length=5, choices=NAME_CHOICES)
    timestamp = models.DateTimeField(default=datetime.datetime.utcnow)


class Bookmark(models.Model):
    profile = models.ForeignKey(Profile, related_name='bookmarks')
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    post = generic.GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return u"%s: %s" % (self.profile.user.username, self.post)


@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
    user = kwargs.get('instance')
    try:
        user.profile
    except Profile.DoesNotExist:
        Profile.objects.create(user=user)
