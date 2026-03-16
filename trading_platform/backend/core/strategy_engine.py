from dataclasses import dataclass
from typing import Dict, Any, List


@dataclass
class Signal:
    symbol: str
    side: str
    confidence: float


def _ema(values: List[float], span: int) -> float:
    alpha = 2 / (span + 1)
    ema = values[0]
    for value in values[1:]:
        ema = alpha * value + (1 - alpha) * ema
    return ema


def evaluate_strategy(market_data: List[float], compiled_strategy: Dict[str, Any], params: Dict[str, Any]) -> Signal | None:
    if not market_data:
        return None
    fast = params.get('ema_fast', 50)
    slow = params.get('ema_slow', 200)
    ema_fast = _ema(market_data, fast)
    ema_slow = _ema(market_data, slow)
    if ema_fast > ema_slow:
        return Signal(symbol=params.get('symbol', 'NIFTY'), side='BUY', confidence=min((ema_fast - ema_slow) / max(ema_slow, 1e-9), 1.0))
    if ema_fast < ema_slow:
        return Signal(symbol=params.get('symbol', 'NIFTY'), side='SELL', confidence=min((ema_slow - ema_fast) / max(ema_fast, 1e-9), 1.0))
    return None
