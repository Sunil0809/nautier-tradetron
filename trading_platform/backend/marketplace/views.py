from rest_framework import viewsets
from .models import MarketplaceStrategy, Subscription
from .serializers import MarketplaceStrategySerializer, SubscriptionSerializer


class MarketplaceStrategyViewSet(viewsets.ModelViewSet):
    queryset = MarketplaceStrategy.objects.all().order_by('-rating')
    serializer_class = MarketplaceStrategySerializer


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all().order_by('-id')
    serializer_class = SubscriptionSerializer
