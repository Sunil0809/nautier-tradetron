from rest_framework import serializers
from .models import MarketplaceStrategy, Subscription


class MarketplaceStrategySerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketplaceStrategy
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
