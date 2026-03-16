from core.backtesting_engine import run_backtest, optimize_parameters


def test_backtest_metrics_present():
    prices = [100 + (i * 0.5) for i in range(300)]
    out = run_backtest(prices, {'ema_fast': 10, 'ema_slow': 30})
    assert 'metrics' in out
    assert 'sharpe_ratio' in out['metrics']


def test_parameter_optimization_returns_best():
    prices = [100 + i for i in range(300)]
    best = optimize_parameters(prices, {'ema_fast': [5, 10], 'ema_slow': [20, 30]}, mode='grid')
    assert 'params' in best
