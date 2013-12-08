import datetime
import os
import random

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from south.modelsinspector import add_ignored_fields

from content.forms import CustomTaggableManager
from comedylib.mixins import CreatedMixin


# We make South ignore this custom field
add_ignored_fields(["^content\.forms\.CustomTaggableManager"])


class Collection(CreatedMixin):
    ROLE_CHOICES = (
        (0, u'comedian'),
        (1, u'show'),
        (2, u'movie'),
    )
    name = models.CharField(max_length=255)
    picture = models.ImageField(upload_to='collections')
    description = models.TextField()
    connections = models.ManyToManyField('self', related_name='connections',
                                         blank=True)
    role = models.SmallIntegerField(choices=ROLE_CHOICES)
    slug = models.SlugField(max_length=100, blank=True)
    tags = CustomTaggableManager(help_text = _("Choose one or more tags."))

    def __unicode__(self):
        return u"%s:%s" % (self.name, self.get_role_display())

    @models.permalink
    def get_absolute_url(self):
        return ('content:%s' % self.get_role_display(), (self.slug, self.id))

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Collection, self).save(*args, **kwargs)

    @property
    def rating(self):
        ratings = [v.rating for v in self.videos.all() if v.rating != 0]
        if len(ratings) == 0:
            return 0
        return sum(ratings) / len(ratings)


class Video(CreatedMixin):
    title = models.CharField(max_length=255)
    url = models.URLField()
    duration = models.CharField(max_length=20,
                                help_text='Format hh:mm:ss or mm:ss')
    views = models.IntegerField(default=0)
    collection = models.ForeignKey(Collection, related_name='videos')
    VID_THUMB_DUMMY = os.path.join(settings.STATIC_URL, 'img/dumvid.jpg')
    picture = models.ImageField(upload_to='videos', null=True, blank=True,
                                default=VID_THUMB_DUMMY)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    STATUS_CHOICES = (
        (0, u'private'),
        (1, u'public'),
    )
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=1,
                                      blank=True)

    class Meta:
        #FIXME: I don't like this, but I don't know another way to
        # have videos ordered by the `order` field when retrieved
        # from a collection.
        ordering = ['playlistvideo__order']

    def __unicode__(self):
        return u"%s:%s" % (self.title, "%s..." % self.url[:50]
                           if len(self.url) > 50 else self.url)

    def get_absolute_url(self):
        coll_url = reverse('content:%s' % self.collection.get_role_display(),
                           args=[self.collection.slug, self.collection.id])
        return '%s/%s' % (coll_url, self.id)

    @property
    def rating(self):
        likes = self.likes
        dislikes = self.dislikes
        if (likes + dislikes) == 0:
            return 0
        return (100 * likes) / (likes + dislikes)

    @property
    def total_votes(self):
        return self.likes + self.dislikes


class FeaturedManager(models.Manager):
    """
    Overrides the default manager's `get` method, to create
    the `Featured` instance (which is a singleton), in case it
    doesn't exist
    """
    def get(self, *args, **kwargs):
        try:
            instance = super(FeaturedManager, self).get(*args, **kwargs)
        except self.model.DoesNotExist:
            instance = self._create()
        return instance

    def _create(self):
        kwargs = {}
        for role_id, role_name in Collection.ROLE_CHOICES:
            new_objs = Collection.objects.filter(role=role_id)
            if not new_objs:
                return
            kwargs[role_name] = random.choice(new_objs)
        instance = self.create(**kwargs)
        return instance


class Featured(models.Model):
    comedian = models.OneToOneField(Collection, related_name='+')
    show = models.OneToOneField(Collection, related_name='+')
    movie = models.OneToOneField(Collection, related_name='+')
    updated = models.DateTimeField(blank=True)
    instance = FeaturedManager()

    def save(self, *args, **kwargs):
        self.updated = datetime.datetime.utcnow()
        super(Featured, self).save(*args, **kwargs)
