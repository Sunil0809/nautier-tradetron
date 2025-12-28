"""Event queue - central nervous system of trading engine"""
from collections import deque
from typing import Optional, Callable, List
from app.events import Event, EventType
import asyncio
import logging

logger = logging.getLogger(__name__)


class EventQueue:
    """FIFO event queue for event-driven engine
    
    Everything flows through this queue:
    Market → Strategy → Signal → Risk Check → Order → Execution → Fill
    """
    
    def __init__(self, max_size: int = 10000):
        self.queue: deque = deque(maxlen=max_size)
        self.subscribers: dict[EventType, List[Callable]] = {}
        self.lock = asyncio.Lock()
    
    async def put(self, event: Event) -> None:
        """Put event in queue"""
        async with self.lock:
            self.queue.append(event)
            logger.debug(f"Event queued: {event.event_type.value}")
            
            # Notify subscribers
            if event.event_type in self.subscribers:
                for callback in self.subscribers[event.event_type]:
                    try:
                        await callback(event)
                    except Exception as e:
                        logger.error(f"Error in callback: {e}")
    
    async def get(self) -> Optional[Event]:
        """Get next event from queue"""
        async with self.lock:
            if len(self.queue) > 0:
                return self.queue.popleft()
        return None
    
    def subscribe(self, event_type: EventType, callback: Callable) -> None:
        """Subscribe to event type"""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)
        logger.info(f"Subscribed to {event_type.value}")
    
    def size(self) -> int:
        """Get queue size"""
        return len(self.queue)
    
    def clear(self) -> None:
        """Clear queue"""
        self.queue.clear()
