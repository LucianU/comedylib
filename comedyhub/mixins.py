import datetime

from django.db import models

class CreatedMixin(models.Model):
    added = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        abstract = True
