from django.contrib import admin
from .models import Publication, Article, Video


class PublicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title',)
    ordering = ('-created_at',)

    fieldsets = (
        (None, {
            'fields': ('title', 'content_type', 'object_id')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at'),
        }),
    )
    readonly_fields = ('title', 'created_at', 'updated_at')

admin.site.register(Publication, PublicationAdmin)
admin.site.register(Article)
admin.site.register(Video)