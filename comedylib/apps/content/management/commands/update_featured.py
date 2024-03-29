import random

from django.core.cache import cache
from django.core.management.base import NoArgsCommand

from content.models import Collection, Featured


class Command(NoArgsCommand):
    help = "Updates the featured posts"

    def handle_noargs(self, **options):
        instance = Featured.instance.get()
        for role_id, role_name in Collection.ROLE_CHOICES:
            curr_obj_id = getattr(instance, role_name).id
            new_objs = (Collection.objects.filter(role=role_id)
                                          .exclude(id=curr_obj_id))
            if new_objs:
                setattr(instance, role_name, random.choice(new_objs))
        instance.save()

        # We update the cache
        cache.set(Featured.instance.cache_key, instance, 60 * 60 * 24)
