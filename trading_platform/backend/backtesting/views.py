from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import BacktestJob
from .serializers import BacktestJobSerializer
from .tasks import run_backtest_task


class BacktestJobViewSet(viewsets.ModelViewSet):
    queryset = BacktestJob.objects.all().order_by('-id')
    serializer_class = BacktestJobSerializer

    @action(detail=True, methods=['post'])
    def run(self, request, pk=None):
        job = self.get_object()
        run_backtest_task.delay(job.id)
        return Response({'status': 'queued', 'job_id': job.id})
