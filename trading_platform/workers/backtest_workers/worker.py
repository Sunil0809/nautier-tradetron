"""Entrypoint for backtesting workers."""
from config.celery import app

if __name__ == '__main__':
    app.worker_main(['worker', '--loglevel=info', '-Q', 'backtests'])
