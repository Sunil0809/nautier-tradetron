from django.db import models


class Candle(models.Model):
    symbol = models.CharField(max_length=24)
    timeframe = models.CharField(max_length=8)
    ts = models.DateTimeField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.FloatField(default=0)

    class Meta:
        unique_together = ('symbol', 'timeframe', 'ts')
