from django.conf import settings
from django.db import models


class Position(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=24)
    quantity = models.FloatField(default=0)
    avg_price = models.FloatField(default=0)
    unrealized_pnl = models.FloatField(default=0)


class PortfolioSnapshot(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    equity = models.FloatField()
    daily_pnl = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
