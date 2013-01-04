"""
Mixins used throught the project
"""
import datetime

from django.db import models


class CreatedMixin(models.Model):
    """
    Mixin used to add a field storing the creation time
    """
    created = models.DateTimeField(default=datetime.datetime.now)

    class Meta:  # pylint: disable=C0111, W0232, R0903
        abstract = True
