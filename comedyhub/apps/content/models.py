from django.contrib.auth.models import User
from django.db import models

class Collection(models.Model):
    ROLE_CHOICES = (
        '0', 'performer',
        '1', 'show',
        '2', 'movie',
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    connections = models.ManyToManyField('self', related_name='siblings')
    role = models.SmallIntegerField(choices=ROLE_CHOICES)

class Video(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    collection = models.ForeignKey(Collection, related_name='videos')
    fans = models.ManyToManyField(User, related_name='likes')
    admirers = models.ManyToManyField(User, related_name='favorites')
