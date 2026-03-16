from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Strategy
from .serializers import StrategySerializer
from core.strategy_builder import compile_graph_to_logic


class StrategyViewSet(viewsets.ModelViewSet):
    queryset = Strategy.objects.all().order_by('-id')
    serializer_class = StrategySerializer

    @action(detail=True, methods=['post'])
    def compile(self, request, pk=None):
        strategy = self.get_object()
        compiled = compile_graph_to_logic(strategy.node_graph)
        return Response({'compiled_logic': compiled})
