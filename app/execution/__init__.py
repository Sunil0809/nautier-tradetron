"""Order execution handlers - Paper vs Live separation"""
import logging
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import uuid
from app.events import OrderEvent, FillEvent
from app.broker import FyersClient

logger = logging.getLogger(__name__)


class ExecutionHandler(ABC):
    """Base execution handler"""
    
    @abstractmethod
    async def execute_order(self, order: OrderEvent) -> FillEvent:
        """Execute order and return fill event"""
        pass


class PaperExecutionHandler(ExecutionHandler):
    """Paper trading execution - simulates slippage, delays, partial fills"""
    
    def __init__(self):
        self.slippage_percent = 0.05  # 0.05% slippage
        self.partial_fill_chance = 0.10  # 10% chance of partial fill
    
    async def execute_order(self, order: OrderEvent) -> FillEvent:
        """Execute order in paper mode
        
        Simulates:
        - Slippage
        - Partial fills
        - Realistic delays
        """
        import asyncio
        import random
        
        # Simulate network delay
        await asyncio.sleep(random.uniform(0.1, 0.5))
        
        # Apply slippage
        fill_price = order.price
        if order.side == "BUY":
            fill_price *= (1 + self.slippage_percent / 100)
        else:
            fill_price *= (1 - self.slippage_percent / 100)
        
        # Simulate partial fill
        filled_qty = order.quantity
        is_partial = False
        if random.random() < self.partial_fill_chance:
            filled_qty = order.quantity * random.uniform(0.5, 0.9)
            is_partial = True
        
        # Commission 0.05%
        commission = (filled_qty * fill_price) * 0.0005
        
        fill_event = FillEvent(
            user_id=order.user_id,
            strategy_id=order.strategy_id,
            symbol=order.symbol,
            order_id=order.client_order_id,
            quantity=filled_qty,
            price=fill_price,
            commission=commission,
            is_partial=is_partial,
        )
        
        logger.info(
            f"Paper fill: {order.symbol} {filled_qty} @ {fill_price:.2f} "
            f"(slippage: {self.slippage_percent}%)"
        )
        
        return fill_event


class LiveFyersExecutionHandler(ExecutionHandler):
    """Live trading via FYERS broker"""
    
    def __init__(self, fyers_client: FyersClient):
        self.fyers = fyers_client
    
    async def execute_order(self, order: OrderEvent) -> Optional[FillEvent]:
        """Execute order on FYERS
        
        Critical rules:
        - Use idempotent client_order_id
        - Handle rejections
        - Verify fills
        """
        
        # Generate idempotent client order ID if not present
        if not order.client_order_id:
            order.client_order_id = f"order_{uuid.uuid4().hex[:12]}"
        
        # Place order
        result = self.fyers.place_order(
            symbol=order.symbol,
            order_type=order.order_type,
            side=order.side,
            quantity=int(order.quantity),
            price=order.price if order.order_type == "LIMIT" else 0,
            client_order_id=order.client_order_id,
        )
        
        if result.get("status") != "success":
            logger.error(f"Order rejected: {result}")
            return None
        
        # Get broker order ID
        broker_order_id = result.get("id")
        order.broker_order_id = broker_order_id
        
        # Poll order status (simplified - use websocket in production)
        import asyncio
        await asyncio.sleep(1)
        
        status = self.fyers.get_order_status(broker_order_id)
        
        # Create fill event
        filled_qty = status.get("filledqty", 0)
        fill_price = status.get("price", order.price)
        commission = (filled_qty * fill_price) * 0.0005
        
        fill_event = FillEvent(
            user_id=order.user_id,
            strategy_id=order.strategy_id,
            symbol=order.symbol,
            order_id=broker_order_id,
            quantity=filled_qty,
            price=fill_price,
            commission=commission,
            is_partial=status.get("status") == "PARTIAL",
        )
        
        logger.info(f"Live fill: {broker_order_id} {filled_qty} @ {fill_price}")
        
        return fill_event
