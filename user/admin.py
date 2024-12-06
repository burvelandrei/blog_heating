from django.contrib import admin
from .models import CustomUser

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'birth_date')
    list_filter = ('birth_date', 'username')
    search_fields = ('username', 'email')
    ordering = ('username',)

    fieldsets = (
        (None, {
            'fields': ('username', 'first_name', 'last_name', 'email', 'birth_date')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )

admin.site.register(CustomUser, UserAdmin)