from django.conf import settings
from django.db import models


class Order(models.Model):
    STATUS = [('NEW', 'NEW'), ('FILLED', 'FILLED'), ('REJECTED', 'REJECTED')]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    strategy_id = models.BigIntegerField()
    broker = models.CharField(max_length=24)
    symbol = models.CharField(max_length=24)
    side = models.CharField(max_length=8)
    quantity = models.FloatField()
    status = models.CharField(max_length=16, choices=STATUS, default='NEW')
    created_at = models.DateTimeField(auto_now_add=True)
