from celery import shared_task
from core.backtesting_engine import run_backtest
from .models import BacktestJob


@shared_task
def run_backtest_task(job_id: int) -> dict:
    job = BacktestJob.objects.get(id=job_id)
    job.status = 'RUNNING'
    job.save(update_fields=['status'])

    prices = job.params.get('close_prices', [])
    results = run_backtest(prices, job.params)

    job.status = 'DONE'
    job.results = results
    job.save(update_fields=['status', 'results'])
    return results
