from execution.brokers import get_adapter, BrokerOrder


def test_adapter_pattern_execution():
    adapter = get_adapter('fyers')
    result = adapter.place_order(BrokerOrder(symbol='NIFTY', side='BUY', quantity=1))
    assert result['broker'] == 'fyers'
    assert result['status'] == 'accepted'
