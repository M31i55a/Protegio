from django.contrib import admin
from .models import ScanResult


@admin.register(ScanResult)
class ScanResultAdmin(admin.ModelAdmin):
    list_display = ('url', 'status_code', 'scanned_at', 'technology_count')
    list_filter = ('scanned_at', 'status_code')
    search_fields = ('url',)
    readonly_fields = ('scanned_at', 'url', 'technologies', 'raw_headers')
    
    def technology_count(self, obj):
        return len(obj.technologies)
    technology_count.short_description = "Nombre de technologies"
