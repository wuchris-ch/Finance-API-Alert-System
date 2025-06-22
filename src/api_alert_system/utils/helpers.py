"""
Utility functions for the API Alert System
"""

import os
import logging
from datetime import datetime
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def setup_logging(level: str = "INFO") -> None:
    """Setup logging configuration"""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def validate_config() -> Dict[str, Any]:
    """Validate configuration and return status"""
    status = {
        'telegram': False,
        'ntfy': False,
        'database': False,
        'demo_mode': False
    }
    
    # Check Telegram configuration
    telegram_token = os.getenv("TELEGRAM_TOKEN")
    telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if (telegram_token and telegram_chat_id and 
        telegram_token != "YOUR_BOT_TOKEN_HERE" and 
        telegram_chat_id != "YOUR_CHAT_ID_HERE"):
        status['telegram'] = True
    
    # Check NTFY configuration
    ntfy_topic = os.getenv("NTFY_TOPIC")
    if ntfy_topic:
        status['ntfy'] = True
    
    # Check database configuration
    db_host = os.getenv("POSTGRES_HOST")
    db_user = os.getenv("POSTGRES_USER")
    db_password = os.getenv("POSTGRES_PASSWORD")
    
    if db_host and db_user and db_password:
        status['database'] = True
    
    # Check demo mode
    demo_mode = os.getenv("DEMO_MODE", "False").lower()
    status['demo_mode'] = demo_mode in ('true', '1', 'yes')
    
    return status


def format_timestamp(timestamp: datetime = None) -> str:
    """Format timestamp for display"""
    if timestamp is None:
        timestamp = datetime.utcnow()
    return timestamp.strftime("%Y-%m-%d %H:%M:%S UTC")


def format_price(price: float) -> str:
    """Format price for display"""
    if price is None:
        return "N/A"
    return f"${price:.2f}"


def format_percentage_change(old_price: float, new_price: float) -> str:
    """Format percentage change between two prices"""
    if old_price is None or new_price is None or old_price == 0:
        return "N/A"
    
    change = ((new_price - old_price) / old_price) * 100
    sign = "+" if change >= 0 else ""
    return f"{sign}{change:.2f}%"


def get_env_bool(key: str, default: bool = False) -> bool:
    """Get boolean value from environment variable"""
    value = os.getenv(key, str(default)).lower()
    return value in ('true', '1', 'yes', 'on')


def get_env_int(key: str, default: int = 0) -> int:
    """Get integer value from environment variable"""
    try:
        return int(os.getenv(key, str(default)))
    except ValueError:
        return default


def get_env_float(key: str, default: float = 0.0) -> float:
    """Get float value from environment variable"""
    try:
        return float(os.getenv(key, str(default)))
    except ValueError:
        return default 