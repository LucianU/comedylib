from django.db import models

class Collection(models.Model):
    ROLE_CHOICES = (
        ('0', 'comedian'),
        ('1', 'show'),
        ('2', 'movie'),
    )
    name = models.CharField(max_length=255)
    picture = models.ImageField(upload_to='collections')
    description = models.TextField()
    connections = models.ManyToManyField('self', related_name='connections',
                                         null=True)
    role = models.SmallIntegerField(choices=ROLE_CHOICES)

class Video(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    collection = models.ForeignKey(Collection, related_name='videos')
