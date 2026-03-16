from itertools import product
from math import sqrt
from typing import Any, Dict, List
import random


def _ema_series(values: List[float], span: int) -> List[float]:
    alpha = 2 / (span + 1)
    out = [values[0]]
    for value in values[1:]:
        out.append(alpha * value + (1 - alpha) * out[-1])
    return out


def run_backtest(prices: List[float], params: Dict[str, Any]) -> Dict[str, Any]:
    if not prices:
        return {'equity_curve': [], 'metrics': {}}

    fast = params.get('ema_fast', 10)
    slow = params.get('ema_slow', 30)
    fast_ema = _ema_series(prices, fast)
    slow_ema = _ema_series(prices, slow)
    returns = [0.0]
    for i in range(1, len(prices)):
        returns.append((prices[i] - prices[i - 1]) / prices[i - 1])

    signal = [1 if fast_ema[i] > slow_ema[i] else 0 for i in range(len(prices))]
    strat_returns = [returns[i] * signal[i - 1] if i > 0 else 0.0 for i in range(len(returns))]

    equity = [1.0]
    for r in strat_returns[1:]:
        equity.append(equity[-1] * (1 + r))

    max_so_far = equity[0]
    drawdown = []
    for e in equity:
        max_so_far = max(max_so_far, e)
        drawdown.append(e / max_so_far - 1)

    avg = sum(strat_returns) / len(strat_returns)
    var = sum((x - avg) ** 2 for x in strat_returns) / len(strat_returns)
    std = var ** 0.5

    wins = [x for x in strat_returns if x > 0]
    losses = [x for x in strat_returns if x < 0]
    metrics = {
        'cagr': equity[-1] ** (252 / max(len(prices), 1)) - 1,
        'sharpe_ratio': (avg / (std + 1e-9)) * sqrt(252),
        'drawdown': min(drawdown),
        'win_rate': len(wins) / len(strat_returns),
        'profit_factor': (sum(wins) / abs(sum(losses) + 1e-9)) if losses else 0,
    }
    trades = [{'index': i, 'ret': r} for i, r in enumerate(strat_returns) if r != 0]
    return {'equity_curve': equity, 'drawdown_curve': drawdown, 'trade_list': trades, 'metrics': metrics}


def optimize_parameters(prices: List[float], grid: Dict[str, List[int]], mode: str = 'grid') -> Dict[str, Any]:
    combos = list(product(grid['ema_fast'], grid['ema_slow'])) if mode == 'grid' else [
        (random.choice(grid['ema_fast']), random.choice(grid['ema_slow'])) for _ in range(20)
    ]

    best = {'score': -999.0, 'params': {}}
    for fast, slow in combos:
        if fast >= slow:
            continue
        result = run_backtest(prices, {'ema_fast': fast, 'ema_slow': slow})
        score = result['metrics'].get('sharpe_ratio', -999.0)
        if score > best['score']:
            best = {'score': score, 'params': {'ema_fast': fast, 'ema_slow': slow}, 'result': result}
    return best
