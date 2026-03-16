from rest_framework import viewsets
from .models import Position, PortfolioSnapshot
from .serializers import PositionSerializer, PortfolioSnapshotSerializer


class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all().order_by('-id')
    serializer_class = PositionSerializer


class PortfolioSnapshotViewSet(viewsets.ModelViewSet):
    queryset = PortfolioSnapshot.objects.all().order_by('-created_at')
    serializer_class = PortfolioSnapshotSerializer
