from django.db import models

class Collection(models.Model):
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

    def __unicode__(self):
        return u"%s:%s" % (self.name, self.get_role_display())

class Video(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    collection = models.ForeignKey(Collection, related_name='videos')

    def __unicode__(self):
        return u"%s:%s" % (self.title, "%s..." % self.url[:50]
                           if len(self.url) > 50 else self.url)
