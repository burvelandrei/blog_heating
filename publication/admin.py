from django.contrib import admin
from .models import Publication, Article, Video


class PublicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'publisched_at')
    list_filter = ('publisched_at',)
    search_fields = ('title',)
    ordering = ('-publisched_at',)

    fieldsets = (
        (None, {
            'fields': ('title', 'content_type', 'object_id')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('publisched_at',),
        }),
    )
    readonly_fields = ('title', 'publisched_at')

admin.site.register(Publication, PublicationAdmin)
admin.site.register(Article)
admin.site.register(Video)