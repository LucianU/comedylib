from django.contrib import admin

from profiles.models import Profile, Playlist, RelevantLink

admin.site.register(Profile)
admin.site.register(Playlist)
admin.site.register(RelevantLink)
