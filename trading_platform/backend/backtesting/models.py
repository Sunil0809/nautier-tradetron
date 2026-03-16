from django.conf import settings
from django.db import models


class BacktestJob(models.Model):
    STATUS = [('QUEUED', 'QUEUED'), ('RUNNING', 'RUNNING'), ('DONE', 'DONE'), ('FAILED', 'FAILED')]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    strategy_id = models.BigIntegerField()
    params = models.JSONField(default=dict)
    status = models.CharField(max_length=12, choices=STATUS, default='QUEUED')
    results = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
