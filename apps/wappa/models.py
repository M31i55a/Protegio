from django.db import models

class ScanResult(models.Model):
    url = models.URLField()
    scanned_at = models.DateTimeField(auto_now_add=True)
    technologies = models.JSONField(default=list)
    status_code = models.IntegerField(null=True, blank=True)
    raw_headers = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.url} — {self.scanned_at.strftime('%d/%m/%Y %H:%M')}"

    class Meta:
        ordering = ["-scanned_at"]
        verbose_name = "Résultat de scan"