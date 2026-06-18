from django.db import models


class SqlmapScan(models.Model):
    url = models.URLField(max_length=500)
    status = models.CharField(max_length=50, default='pending')
    result = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'SQLMap Scan'
        verbose_name_plural = 'SQLMap Scans'

    def __str__(self):
        return f"SQLMap Scan - {self.url}"
