from django.conf import settings
from django.db import models


class Strategy(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    node_graph = models.JSONField(default=dict)
    parameters = models.JSONField(default=dict)
    timeframe = models.CharField(max_length=16, default='1h')
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class StrategySignal(models.Model):
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=24)
    signal = models.CharField(max_length=8)
    confidence = models.FloatField(default=0.0)
    generated_at = models.DateTimeField(auto_now_add=True)
