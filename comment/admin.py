from django.contrib import admin
from .models import Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'author', 'publication', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'publication__title', 'author__username')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {
            'fields': ('content', 'author', 'publication')
        }),
        ('Расширенные параметры', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at'),
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Comment, CommentAdmin)