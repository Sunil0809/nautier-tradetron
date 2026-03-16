from rest_framework.routers import DefaultRouter
from .views import PositionViewSet, PortfolioSnapshotViewSet

router = DefaultRouter()
router.register('positions', PositionViewSet)
router.register('snapshots', PortfolioSnapshotViewSet)
urlpatterns = router.urls
