from rest_framework.routers import DefaultRouter
from .views import StrategyViewSet

router = DefaultRouter()
router.register('', StrategyViewSet)
urlpatterns = router.urls
