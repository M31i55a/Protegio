from django.db import models


class ScanTarget(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=500)
    status = models.CharField(max_length=50, default='pending')
    scan_config = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'burp_suite'   # ← ajouté

    def __str__(self):
        return f"{self.name} - {self.url}"


class ScanResult(models.Model):
    SEVERITY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
        ('info', 'Info'),
    ]
    target = models.ForeignKey(ScanTarget, on_delete=models.CASCADE, related_name='results')
    url = models.URLField(max_length=500)
    issue_type = models.CharField(max_length=255)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    parameter = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    evidence = models.TextField(blank=True)
    remediation = models.TextField(blank=True)
    request_data = models.TextField(blank=True)
    response_data = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'burp_suite'   # ← ajouté

    def __str__(self):
        return f"{self.issue_type} - {self.severity}"


class ProxyRequest(models.Model):
    method = models.CharField(max_length=10, default='GET')
    url = models.TextField()
    host = models.CharField(max_length=255, blank=True)
    path = models.TextField(blank=True)
    request_headers = models.JSONField(default=dict, blank=True)
    request_body = models.TextField(blank=True)
    response_status = models.IntegerField(null=True, blank=True)
    response_headers = models.JSONField(default=dict, blank=True)
    response_body = models.TextField(blank=True)
    response_length = models.IntegerField(null=True, blank=True)
    response_time = models.FloatField(null=True, blank=True)
    intercepted = models.BooleanField(default=False)
    modified = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'burp_suite'   # ← ajouté
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.method} {self.url}"


class IntruderPayload(models.Model):
    name = models.CharField(max_length=255)
    attack_type = models.CharField(max_length=50, default='sniper')
    target_url = models.TextField(blank=True)
    request_template = models.TextField(blank=True)
    payloads = models.JSONField(default=list, blank=True)
    results = models.JSONField(default=list, blank=True)
    status = models.CharField(max_length=50, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'burp_suite'   # ← ajouté

    def __str__(self):
        return self.name


class RepeaterRequest(models.Model):
    name = models.CharField(max_length=255, default='Request')
    method = models.CharField(max_length=10, default='GET')
    url = models.TextField()
    headers = models.JSONField(default=dict, blank=True)
    body = models.TextField(blank=True)
    response_status = models.IntegerField(null=True, blank=True)
    response_headers = models.JSONField(default=dict, blank=True)
    response_body = models.TextField(blank=True)
    response_time = models.FloatField(null=True, blank=True)
    history = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'burp_suite'   # ← ajouté

    def __str__(self):
        return f"{self.name} - {self.method} {self.url}"


class SpiderResult(models.Model):
    target = models.ForeignKey(ScanTarget, on_delete=models.CASCADE, related_name='spider_results')
    url = models.TextField()
    status_code = models.IntegerField(null=True, blank=True)
    content_type = models.CharField(max_length=100, blank=True)
    content_length = models.IntegerField(null=True, blank=True)
    parent_url = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'burp_suite'   # ← ajouté

    def __str__(self):
        return self.url


class DecoderData(models.Model):
    input_data = models.TextField()
    output_data = models.TextField()
    encoding_type = models.CharField(max_length=50)
    operation = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'burp_suite'   # ← ajouté

    def __str__(self):
        return f"{self.encoding_type} - {self.operation}"