from rest_framework.routers import DefaultRouter
from .views import MarketplaceStrategyViewSet, SubscriptionViewSet

router = DefaultRouter()
router.register('strategies', MarketplaceStrategyViewSet)
router.register('subscriptions', SubscriptionViewSet)
urlpatterns = router.urls
