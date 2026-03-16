from datetime import datetime, timedelta


def mock_download_ohlcv(symbol: str, periods: int = 200) -> list[dict]:
    now = datetime.utcnow()
    rows = []
    for i in range(periods):
        close = 100 + i
        rows.append(
            {
                'ts': now - timedelta(hours=periods - i),
                'open': close - 0.5,
                'high': close + 1,
                'low': close - 1,
                'close': close,
                'volume': 1000,
                'symbol': symbol,
            }
        )
    return rows
