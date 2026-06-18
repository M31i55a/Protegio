from django.contrib import admin
from .models import SqlmapScan


@admin.register(SqlmapScan)
class SqlmapScanAdmin(admin.ModelAdmin):
    list_display = ('url', 'status', 'created_at')
    search_fields = ('url',)
    readonly_fields = ('created_at',)
