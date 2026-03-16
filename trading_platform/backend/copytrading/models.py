from django.conf import settings
from django.db import models


class CopyRelationship(models.Model):
    master = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='masters')
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followers')
    allocation_pct = models.FloatField(default=1.0)
    active = models.BooleanField(default=True)
