from django.db import models


class MonitoringEvent(models.Model):
    level = models.CharField(max_length=16)
    source = models.CharField(max_length=64)
    message = models.TextField()
    metadata = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
