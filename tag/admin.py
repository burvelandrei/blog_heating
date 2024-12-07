from django.contrib import admin
from .models import Tag


class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    list_filter = ("name",)
    search_fields = ("name",)

admin.site.register(Tag, TagAdmin)