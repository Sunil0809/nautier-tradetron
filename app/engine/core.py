"""Complete trading engine - ties everything together"""
import logging
import asyncio
from datetime import datetime
from typing import Optional, Dict
from app.engine import EventQueue
from app.engine.rules import RuleEngine
from app.events import MarketEvent, SignalEvent, OrderEvent, FillEvent, EventType
from app.risk import RiskEngine, RiskConfig
from app.execution import ExecutionHandler, PaperExecutionHandler

logger = logging.getLogger(__name__)


class TradingEngine:
    """Main trading engine - orchestrates everything
    
    Flow:
    Market Event → Rule Engine → Signal → Risk Check → Order → Execution → Fill
    
    Everything is asynchronous and event-driven.
    No direct function calls - only events!
    """
    
    def __init__(self):
        self.event_queue = EventQueue()
        self.rule_engine = RuleEngine()
        self.risk_engine = RiskEngine()
        self.execution_handler: Optional[ExecutionHandler] = None
        self.running = False
        self.positions: Dict[str, float] = {}  # symbol -> quantity
    
    async def start(self):
        """Start the engine"""
        logger.info("🎯 Trading Engine Starting...")
        self.running = True
        
        # Default to paper trading
        self.execution_handler = PaperExecutionHandler()
        
        # Subscribe to all events
        self._subscribe_to_events()
        
        # Start event loop
        await self._event_loop()
    
    def stop(self):
        """Stop the engine"""
        logger.info("🛑 Trading Engine Stopping...")
        self.running = False
    
    def _subscribe_to_events(self):
        """Subscribe handlers to events"""
        self.event_queue.subscribe(EventType.MARKET, self._on_market_event)
        self.event_queue.subscribe(EventType.SIGNAL, self._on_signal_event)
        self.event_queue.subscribe(EventType.FILL, self._on_fill_event)
    
    async def _event_loop(self):
        """Main event loop - runs forever"""
        while self.running:
            event = await self.event_queue.get()
            if event:
                logger.debug(f"Processing: {event.event_type.value}")
            await asyncio.sleep(0.01)
    
    async def _on_market_event(self, event: MarketEvent):
        """Handle market event - evaluate all rules"""
        logger.debug(f"Market: {event.symbol} @ {event.price}")
        
        # Market data (simplified - in production, maintain full OHLCV)
        market_data = {
            "price": event.price,
            "volume": event.volume,
            "bid": event.bid,
            "ask": event.ask,
        }
        
        # Evaluate rules (simplified - in production, per-strategy)
        results = self.rule_engine.evaluate_all(market_data)
        
        for rule_id, signal_action in results.items():
            if signal_action != "NONE":
                signal = SignalEvent(
                    user_id=event.user_id,
                    strategy_id=event.strategy_id,
                    symbol=event.symbol,
                    signal=signal_action,
                    strength=0.8,
                )
                await self.event_queue.put(signal)
    
    async def _on_signal_event(self, event: SignalEvent):
        """Handle signal - validate against risk"""
        logger.info(f"Signal: {event.symbol} {event.signal} (strength: {event.strength})")
        
        # Risk validation
        risk_block = await self.risk_engine.validate_signal(event)
        
        if risk_block:
            logger.warning(f"Signal blocked by risk: {risk_block.reason}")
            await self.event_queue.put(risk_block)
            return
        
        # Create order
        order = OrderEvent(
            user_id=event.user_id,
            strategy_id=event.strategy_id,
            symbol=event.symbol,
            order_type="MARKET",
            side=event.signal,
            quantity=10,  # In production, calculate from position size
            status="CREATED",
        )
        
        await self.event_queue.put(order)
    
    async def _on_order_event(self, event: OrderEvent):
        """Handle order - execute"""
        logger.info(f"Order: {event.symbol} {event.side} {event.quantity}")
        
        # Execute
        if self.execution_handler:
            fill = await self.execution_handler.execute_order(event)
            if fill:
                await self.event_queue.put(fill)
    
    async def _on_fill_event(self, event: FillEvent):
        """Handle fill - update position"""
        logger.info(f"Fill: {event.symbol} {event.quantity} @ {event.price}")
        
        # Update position
        current = self.positions.get(event.symbol, 0)
        self.positions[event.symbol] = current + event.quantity
        
        # Record metrics
        self.risk_engine.record_trade(event.strategy_id)
        
        logger.info(f"Position updated: {event.symbol} = {self.positions[event.symbol]}")
    
    async def inject_market_data(
        self,
        symbol: str,
        price: float,
        volume: int,
        user_id: int = 1,
        strategy_id: int = 1
    ):
        """Inject market data (normally from broker/exchange)"""
        event = MarketEvent(
            user_id=user_id,
            strategy_id=strategy_id,
            symbol=symbol,
            price=price,
            volume=volume,
            bid=price * 0.99,
            ask=price * 1.01,
        )
        await self.event_queue.put(event)


# Global engine instance
engine: Optional[TradingEngine] = None


async def initialize_engine():
    """Initialize engine"""
    global engine
    engine = TradingEngine()


async def start_engine():
    """Start engine in background"""
    if engine:
        # Run in background
        asyncio.create_task(engine.start())
        logger.info("Engine started in background")


def get_engine() -> TradingEngine:
    """Get engine instance"""
    if not engine:
        raise RuntimeError("Engine not initialized")
    return engine
