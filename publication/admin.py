from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from .models import Publication, Article, Video


class PublicationAdmin(admin.ModelAdmin):
    list_display = ("title", "publisched_at")
    list_filter = ("publisched_at",)
    search_fields = ("title",)
    ordering = ("-publisched_at",)

    fieldsets = (
        (None, {"fields": ("title", "content_type", "object_id")}),
        (
            "Advanced options",
            {
                "classes": ("collapse",),
                "fields": ("publisched_at",),
            },
        ),
    )
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'content_type':
            kwargs['queryset'] = ContentType.objects.filter(
                model__in=['article', 'video']
            )
        return super().formfield_for_dbfield(db_field, request, **kwargs)
    readonly_fields = ("title", "publisched_at")


class ArticleAdmin(admin.ModelAdmin):
    search_fields = ("title",)
    filter_horizontal = ("tags",)


class VideoAdmin(admin.ModelAdmin):
    search_fields = ("title",)
    filter_horizontal = ("tags",)


admin.site.register(Publication, PublicationAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Video, VideoAdmin)
