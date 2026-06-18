from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserProfile, ACCOUNT_TYPES


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'account_type', 'created_at', 'updated_at')
    list_filter = ('account_type', 'created_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Account Details', {
            'fields': ('account_type', 'avatar_url', 'bio')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
