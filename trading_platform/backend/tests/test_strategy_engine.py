from core.strategy_engine import evaluate_strategy


def test_strategy_engine_generates_signal():
    prices = [100 + i for i in range(250)]
    signal = evaluate_strategy(prices, {}, {'ema_fast': 10, 'ema_slow': 30, 'symbol': 'NIFTY'})
    assert signal is not None
    assert signal.side in {'BUY', 'SELL'}
