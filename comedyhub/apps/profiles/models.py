from django.contrib.auth.models import User
from django.db import models

from content.models import Video

class Profile(models.Model):
    user = models.OneToOneField(User)
    likes = models.ManyToManyField(Video, related_name='profiles')
    favorites = models.ManyToManyField(Video, related_name='profiles')
    lists = models.ManyToManyField(Video, related_name='profiles')
    photo = models.ImageField()
    description = models.TextField()

