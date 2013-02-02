from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.template.defaultfilters import slugify

from comedylib.mixins import CreatedMixin
from content.models import Video


class Profile(models.Model):
    user = models.OneToOneField(User)
    feelings = models.ManyToManyField(Video, through='Feeling', null=True)
    picture = models.ImageField(upload_to='profiles', blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return u"%s: %s playlists" % (self.user.username,
                                      self.playlists.all().count())

    @models.permalink
    def get_absolute_url(self):
        return('user_home', (self.user.id,))

class Playlist(CreatedMixin):
    profile = models.ForeignKey(Profile, related_name='playlists')
    videos = models.ManyToManyField(Video, related_name='playlists', null=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100, blank=True)
    empty = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']

    def __unicode__(self):
        return u"%s: %s videos" % (self.title, self.profile.user.username)

    @models.permalink
    def get_absolute_url(self):
        return('playlist', (self.slug, self.id))

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(Playlist, self).save(*args, **kwargs)


class Feeling(CreatedMixin):
    NAME_CHOICES = (
        ('L', 'like'),
        ('D', 'dislike'),
    )
    profile = models.ForeignKey(Profile)
    video = models.ForeignKey(Video, related_name='feelings')
    name = models.CharField(max_length=5, choices=NAME_CHOICES)

    class Meta:
        unique_together = ('profile', 'video')


class Bookmark(models.Model):
    profile = models.ForeignKey(Profile, related_name='bookmarks')
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    post = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = ('profile', 'content_type', 'object_id')

    def __unicode__(self):
        return u"%s: %s" % (self.profile.user.username, self.post)


@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
    user = kwargs.get('instance')
    try:
        user.profile
    except Profile.DoesNotExist:
        Profile.objects.create(user=user)


@receiver(m2m_changed, sender=Playlist.videos.through)
def update_playlist_empty(sender, **kwargs):
    playlist = kwargs.get('instance')
    if playlist.videos.count() > 0:
        playlist.empty = False
    else:
        playlist.empty = True
    playlist.save()
