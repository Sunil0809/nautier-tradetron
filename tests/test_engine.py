"""Test suite for engine components"""
import pytest
import asyncio
from app.engine import EventQueue
from app.engine.rules import RuleEngine
from app.events import (
    EventType, MarketEvent, SignalEvent, OrderEvent, FillEvent
)


@pytest.mark.asyncio
async def test_event_queue():
    """Test event queue"""
    queue = EventQueue()
    
    # Create and put event
    event = MarketEvent(
        symbol="NSE:SBIN-EQ",
        price=500.0,
        volume=1000,
    )
    
    await queue.put(event)
    
    assert queue.size() == 1
    
    # Get event
    retrieved = await queue.get()
    assert retrieved is not None
    assert retrieved.symbol == "NSE:SBIN-EQ"
    assert queue.size() == 0


@pytest.mark.asyncio
async def test_event_subscription():
    """Test event subscription"""
    queue = EventQueue()
    received_events = []
    
    async def callback(event: SignalEvent):
        received_events.append(event)
    
    queue.subscribe(EventType.SIGNAL, callback)
    
    signal = SignalEvent(symbol="NSE:INFY-EQ", signal="BUY")
    await queue.put(signal)
    
    await asyncio.sleep(0.1)
    assert len(received_events) == 1
    assert received_events[0].signal == "BUY"


def test_rule_engine():
    """Test rule engine"""
    engine = RuleEngine()
    
    rule_json = """{
        "name": "EMA Crossover",
        "conditions": [
            {"left": "EMA(9)", "op": ">", "right": "EMA(21)"},
            {"left": "RSI(14)", "op": "<", "right": 70}
        ],
        "operator": "AND",
        "action": "BUY"
    }"""
    
    assert engine.register_rule(1, rule_json)
    
    # Market data
    data = {
        "EMA_9": 100,
        "EMA_21": 99,
        "RSI_14": 65,
    }
    
    signal = engine.evaluate(1, data)
    assert signal == "BUY"
    
    # Condition fails
    data["RSI_14"] = 71
    signal = engine.evaluate(1, data)
    assert signal == "NONE"


def test_rule_engine_invalid_json():
    """Test rule engine with invalid JSON"""
    engine = RuleEngine()
    
    assert not engine.register_rule(1, "invalid json")


def test_rule_engine_or_operator():
    """Test rule with OR operator"""
    engine = RuleEngine()
    
    rule_json = """{
        "name": "EMA or RSI",
        "conditions": [
            {"left": "EMA(9)", "op": ">", "right": "EMA(21)"},
            {"left": "RSI(14)", "op": ">", "right": 70}
        ],
        "operator": "OR",
        "action": "SELL"
    }"""
    
    engine.register_rule(1, rule_json)
    
    # Only EMA condition true
    data = {
        "EMA_9": 100,
        "EMA_21": 99,
        "RSI_14": 50,
    }
    
    signal = engine.evaluate(1, data)
    assert signal == "SELL"  # OR: at least one true


@pytest.mark.asyncio
async def test_order_event_creation():
    """Test order event creation"""
    order = OrderEvent(
        user_id=1,
        strategy_id=1,
        symbol="NSE:SBIN-EQ",
        order_type="MARKET",
        side="BUY",
        quantity=10,
    )
    
    assert order.status == "CREATED"
    assert order.event_type == EventType.ORDER


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
