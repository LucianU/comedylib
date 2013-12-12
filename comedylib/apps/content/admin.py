from django.contrib import admin

from content.models import Collection, Video, Featured


class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'role')
    search_fields = ['name', 'role']

    def role(self, obj):
        return obj.get_role_display()


class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'collection_name', 'created')
    search_fields = ['title', 'collection__name']

    def collection_name(self, obj):
        return obj.collection.name


admin.site.register(Collection, CollectionAdmin)
admin.site.register(Featured)
admin.site.register(Video, VideoAdmin)
