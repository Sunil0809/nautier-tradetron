from rest_framework.routers import DefaultRouter
from .views import BacktestJobViewSet

router = DefaultRouter()
router.register('', BacktestJobViewSet)
urlpatterns = router.urls
