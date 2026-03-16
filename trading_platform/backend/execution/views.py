from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer
from .brokers import BrokerOrder, get_adapter
from risk.services import validate_order_risk


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-id')
    serializer_class = OrderSerializer

    @action(detail=True, methods=['post'])
    def execute(self, request, pk=None):
        order = self.get_object()
        risk = validate_order_risk(order.user_id, order.symbol, order.quantity)
        if not risk['allowed']:
            order.status = 'REJECTED'
            order.save(update_fields=['status'])
            return Response({'status': 'rejected', 'reason': risk['reason']}, status=400)
        adapter = get_adapter(order.broker)
        result = adapter.place_order(BrokerOrder(symbol=order.symbol, side=order.side, quantity=order.quantity))
        order.status = 'FILLED'
        order.save(update_fields=['status'])
        return Response(result)
