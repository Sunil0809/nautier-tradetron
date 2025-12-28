"""Configuration and logging setup"""
import logging
import logging.handlers
from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """App settings from environment"""
    
    # App
    APP_NAME: str = "AlgoTradingPlatform"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost/algo_platform"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # FYERS
    FYERS_APP_ID: str = ""
    FYERS_APP_SECRET: str = ""
    FYERS_REDIRECT_URL: str = "http://localhost:8000/auth/fyers/callback"
    
    # Telegram
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_CHAT_ID: str = ""
    
    # Trading
    MARKET_OPEN_TIME: str = "09:15"  # IST
    MARKET_CLOSE_TIME: str = "15:30"  # IST
    
    # Risk defaults
    DEFAULT_MAX_DAILY_LOSS: float = 5000.0
    DEFAULT_MAX_TRADES_PER_DAY: int = 50
    
    class Config:
        env_file = ".env"
        case_sensitive = True


def setup_logging(log_level: str = "INFO") -> None:
    """Setup structured logging"""
    
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # File handler
    file_handler = logging.handlers.RotatingFileHandler(
        log_dir / "app.log",
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    
    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)


settings = Settings()
