from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    subscription_tier = models.CharField(max_length=32, default='free')
    api_key = models.CharField(max_length=128, blank=True)
