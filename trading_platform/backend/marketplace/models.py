from django.conf import settings
from django.db import models


class MarketplaceStrategy(models.Model):
    strategy_id = models.BigIntegerField(unique=True)
    publisher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.FloatField(default=0.0)
    monthly_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    analytics = models.JSONField(default=dict)


class Subscription(models.Model):
    investor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    listing = models.ForeignKey(MarketplaceStrategy, on_delete=models.CASCADE)
    risk_scale = models.FloatField(default=1.0)
    created_at = models.DateTimeField(auto_now_add=True)
