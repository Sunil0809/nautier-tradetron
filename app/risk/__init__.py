"""Risk management engine - Non-negotiable gatekeeper"""
import logging
from dataclasses import dataclass
from typing import Optional, Dict
from app.events import SignalEvent, RiskBlockEvent, OrderEvent

logger = logging.getLogger(__name__)


@dataclass
class RiskConfig:
    """Risk configuration per user/strategy"""
    max_daily_loss: float = 5000.0
    max_trades_per_day: int = 50
    max_position_size: float = 100000.0
    max_leverage: float = 1.0
    kill_switch_enabled: bool = True


class RiskEngine:
    """Validates signals before order creation
    
    Flow: Signal → Risk Check → Allowed? → Order
    """
    
    def __init__(self):
        self.configs: Dict[int, RiskConfig] = {}  # strategy_id -> RiskConfig
        self.daily_loss: Dict[int, float] = {}  # strategy_id -> loss amount
        self.trade_count: Dict[int, int] = {}  # strategy_id -> count today
    
    def register_strategy(self, strategy_id: int, config: RiskConfig) -> None:
        """Register strategy with risk config"""
        self.configs[strategy_id] = config
        self.daily_loss[strategy_id] = 0.0
        self.trade_count[strategy_id] = 0
        logger.info(f"Strategy {strategy_id} registered with risk config")
    
    async def validate_signal(
        self, 
        signal: SignalEvent
    ) -> Optional[RiskBlockEvent]:
        """Validate signal against risk rules
        
        Returns:
            None if signal is allowed
            RiskBlockEvent if signal is blocked
        """
        strategy_id = signal.strategy_id
        
        if strategy_id not in self.configs:
            logger.warning(f"Strategy {strategy_id} not registered")
            return RiskBlockEvent(
                user_id=signal.user_id,
                strategy_id=strategy_id,
                reason="Strategy not registered"
            )
        
        config = self.configs[strategy_id]
        
        # Check daily loss limit
        if self.daily_loss[strategy_id] >= config.max_daily_loss:
            logger.warning(f"Daily loss limit reached for strategy {strategy_id}")
            return RiskBlockEvent(
                user_id=signal.user_id,
                strategy_id=strategy_id,
                reason=f"Daily loss limit reached: {self.daily_loss[strategy_id]:.2f}",
                signal=signal
            )
        
        # Check max trades per day
        if self.trade_count[strategy_id] >= config.max_trades_per_day:
            logger.warning(f"Max trades reached for strategy {strategy_id}")
            return RiskBlockEvent(
                user_id=signal.user_id,
                strategy_id=strategy_id,
                reason=f"Max trades per day reached: {self.trade_count[strategy_id]}",
                signal=signal
            )
        
        # All checks passed
        logger.debug(f"Signal validated for strategy {strategy_id}")
        return None
    
    def record_loss(self, strategy_id: int, loss: float) -> None:
        """Record loss for strategy"""
        if strategy_id in self.daily_loss:
            self.daily_loss[strategy_id] += loss
            logger.info(f"Loss recorded: ${loss:.2f}, Total: ${self.daily_loss[strategy_id]:.2f}")
    
    def record_trade(self, strategy_id: int) -> None:
        """Record trade execution"""
        if strategy_id in self.trade_count:
            self.trade_count[strategy_id] += 1
            logger.info(f"Trade recorded: {self.trade_count[strategy_id]} today")
    
    def reset_daily(self, strategy_id: int) -> None:
        """Reset daily counters (call at market open)"""
        if strategy_id in self.daily_loss:
            self.daily_loss[strategy_id] = 0.0
            self.trade_count[strategy_id] = 0
            logger.info(f"Daily counters reset for strategy {strategy_id}")
