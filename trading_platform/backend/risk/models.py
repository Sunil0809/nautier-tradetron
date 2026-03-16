from django.conf import settings
from django.db import models


class RiskProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    max_position_size = models.FloatField(default=100000)
    max_daily_loss = models.FloatField(default=5000)
    max_drawdown = models.FloatField(default=0.2)
    leverage_limit = models.FloatField(default=3.0)
