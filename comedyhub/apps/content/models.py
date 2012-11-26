import datetime
import random

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify

from comedyhub.mixins import CreatedMixin
from content.utils import set_video_thumb

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

    def __unicode__(self):
        return u"%s:%s" % (self.name, self.get_role_display())

    @models.permalink
    def get_absolute_url(self):
        return ('content:%s' % self.get_role_display(), (self.slug, self.id))

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Collection, self).save(*args, **kwargs)

class Video(CreatedMixin):
    title = models.CharField(max_length=255)
    url = models.URLField()
    duration = models.CharField(max_length=20,
                                help_text='Format hh:mm:ss or mm:ss')
    views = models.IntegerField(default=0)
    collection = models.ForeignKey(Collection, related_name='videos')
    picture = models.ImageField(upload_to='videos', null=True, blank=True)

    class Meta:
        ordering =['-created']

    def __unicode__(self):
        return u"%s:%s" % (self.title, "%s..." % self.url[:50]
                           if len(self.url) > 50 else self.url)

    def get_absolute_url(self):
        coll_url = reverse('content:%s' % self.collection.get_role_display(),
                           args=[self.collection.slug, self.collection.id])
        return '%s/%s' % (coll_url, self.id)

class Featured(models.Model):
    comedian = models.OneToOneField(Collection, related_name='+')
    show = models.OneToOneField(Collection, related_name='+')
    movie = models.OneToOneField(Collection, related_name='+')
    updated = models.DateTimeField(blank=True)

    def __init__(self, *args, **kwargs):
        super(Featured, self).__init__(*args, **kwargs)

        # If we're just creating the featured instance or the
        # collections have been featured for longer than the
        # specified duration, we set new ones
        now = datetime.datetime.utcnow()
        featured_td = datetime.timedelta(days=settings.FEATURED_DURATION)

        if self.updated is None or ((now - self.updated) > featured_td):
            for role_id, role_name in Collection.ROLE_CHOICES:
                curr_obj_id = getattr(self, role_name).id
                new_objs = (Collection.objects.filter(role=role_id)
                                              .exclude(id=curr_obj_id))
                setattr(self, role_name, random.choice(new_objs))
            self.save()

    def save(self, *args, **kwargs):
        self.updated = datetime.datetime.utcnow()
        return super(Featured, self).save(*args, **kwargs)

@receiver(post_save, sender=Video)
def set_thumbnail(sender, **kwargs):
    video = kwargs.get('instance')
    if video.picture.name is None:
        thumbed_vid = set_video_thumb(video)
        thumbed_vid.save()
