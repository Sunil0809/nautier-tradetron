"""Telegram alerts for critical events"""
import logging
import requests
from typing import Optional
from app.utils import settings

logger = logging.getLogger(__name__)


class TelegramAlerter:
    """Send alerts via Telegram bot"""
    
    BASE_URL = "https://api.telegram.org"
    
    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id
    
    async def send_alert(
        self,
        message: str,
        level: str = "INFO"
    ) -> Optional[bool]:
        """Send alert message
        
        Args:
            message: Alert text
            level: INFO, WARNING, ERROR, CRITICAL
        """
        
        if not self.bot_token or not self.chat_id:
            logger.warning("Telegram not configured")
            return False
        
        # Format message
        emoji = {
            "INFO": "ℹ️",
            "WARNING": "⚠️",
            "ERROR": "❌",
            "CRITICAL": "🚨",
        }.get(level, "📢")
        
        formatted_message = f"{emoji} *{level}*\n\n{message}"
        
        try:
            response = requests.post(
                f"{self.BASE_URL}/bot{self.bot_token}/sendMessage",
                json={
                    "chat_id": self.chat_id,
                    "text": formatted_message,
                    "parse_mode": "Markdown",
                },
                timeout=10,
            )
            response.raise_for_status()
            logger.info(f"Alert sent: {level}")
            return True
        except Exception as e:
            logger.error(f"Failed to send alert: {e}")
            return False


# Global alerter instance
alerter = TelegramAlerter(
    settings.TELEGRAM_BOT_TOKEN,
    settings.TELEGRAM_CHAT_ID
)


async def alert_broker_down():
    """Alert: Broker connection lost"""
    await alerter.send_alert(
        "🔴 Broker connection lost!\n\nAll live orders paused.",
        level="CRITICAL"
    )


async def alert_kill_switch_activated(user_id: int, cancelled_orders: int):
    """Alert: Kill switch activated"""
    await alerter.send_alert(
        f"🛑 Kill Switch Activated\n\n"
        f"User: {user_id}\n"
        f"Orders Cancelled: {cancelled_orders}",
        level="CRITICAL"
    )


async def alert_daily_loss_reached(strategy_id: int, loss: float):
    """Alert: Daily loss limit reached"""
    await alerter.send_alert(
        f"Daily loss limit reached!\n\n"
        f"Strategy: {strategy_id}\n"
        f"Loss: ₹{loss:.2f}",
        level="WARNING"
    )


async def alert_unknown_order(order_id: str):
    """Alert: Unknown order from broker"""
    await alerter.send_alert(
        f"Unknown order detected!\n\n"
        f"Order ID: {order_id}\n"
        f"Manual reconciliation required.",
        level="ERROR"
    )


async def alert_strategy_error(strategy_id: int, error: str):
    """Alert: Strategy execution error"""
    await alerter.send_alert(
        f"Strategy Error\n\n"
        f"Strategy: {strategy_id}\n"
        f"Error: {error}",
        level="ERROR"
    )
