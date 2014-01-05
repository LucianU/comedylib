from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.template.defaultfilters import slugify

from comedylib.mixins import CreatedMixin
from content.models import Video


class Profile(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    user = models.OneToOneField(User)
    feelings = models.ManyToManyField(Video, through='Feeling', null=True)
    picture = models.ImageField(upload_to='profiles', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES,
                              blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return u"%s: %s playlists" % (self.user.username,
                                      self.playlists.all().count())

    @models.permalink
    def get_absolute_url(self):
        return('user_home', (self.user.id,))


class Playlist(CreatedMixin):
    profile = models.ForeignKey(Profile, related_name='playlists')
    videos = models.ManyToManyField(Video, through='PlaylistVideo',
                                    related_name='playlists', null=True)
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

    @property
    def bookmarks_count(self):
        cache_key = 'pl_bmk_count_%s' % (self.pk,)
        count = cache.get(cache_key)
        if count is not None:
            return count

        count = Bookmark.objects.filter(
            content_type=ContentType.objects.get(name='playlist'),
            object_id=self.pk
        ).count()

        cache.set(cache_key, count, 60 * 60)
        return count


class PlaylistVideo(models.Model):
    playlist = models.ForeignKey(Playlist)
    video = models.ForeignKey(Video)
    order = models.IntegerField(null=True)


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


@receiver(post_save, sender=Playlist.videos.through)
def update_playlist_empty(sender, **kwargs):
    playlist = kwargs.get('instance').playlist
    if playlist.empty:
        playlist.empty = False
        playlist.save()
