from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from .models import Publication, Article, Video


class PublicationAdmin(admin.ModelAdmin):
    list_display = ("title", "publisched_at")
    list_filter = ("publisched_at",)
    search_fields = ("title",)
    ordering = ("-publisched_at",)
    readonly_fields = ("title", "publisched_at",)

    fieldsets = (
        (None, {"fields": ("title", "content_type", "object_id")}),
        (
            "Расширенные параметры",
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


class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "author__username", "created_at")
    list_filter = ("title", "created_at",)
    search_fields = ("title", "author__username")
    filter_horizontal = ("tags",)
    ordering = ("title", "-created_at",)
    readonly_fields = ("author", "created_at", "updated_at")

    fieldsets = (
        (None, {"fields": ("title", "content", "category", "tags", "author", "image")}),
        (
            "Расширенные параметры",
            {
                "classes": ("collapse",),
                "fields": ("created_at", "updated_at"),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
        super().save_model(request, obj, form, change)


class VideoAdmin(admin.ModelAdmin):
    list_display = ("title", "author__username", "created_at")
    list_filter = ("title", "created_at",)
    search_fields = ("title", "author__username")
    filter_horizontal = ("tags",)
    ordering = ("title", "-created_at",)
    readonly_fields = ("author", "created_at", "updated_at")

    fieldsets = (
        (None, {"fields": ("title", "youtube_url", "category", "tags", "author")}),
        (
            "Расширенные параметры",
            {
                "classes": ("collapse",),
                "fields": ("created_at", "updated_at"),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Publication, PublicationAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Video, VideoAdmin)
