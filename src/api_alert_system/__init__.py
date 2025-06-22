"""
API Alert System - Stock Price Monitoring with Telegram Notifications and MCP Integration
"""

__version__ = "0.1.0"
__author__ = "API Alert System Team"

from .core.alert_bot import AlertBot
from .utils.config import *

__all__ = [
    "AlertBot",
    "WATCHLIST",
    "POLL_INTERVAL",
    "TELEGRAM_TOKEN",
    "TELEGRAM_CHAT_ID",
    "NTFY_ENABLED",
    "NTFY_TOPIC",
    "NTFY_SERVER",
    "ENABLE_TELEGRAM",
    "ENABLE_NTFY",
    "DEMO_MODE",
    "CONSOLE_NOTIFICATIONS",
    "POSTGRES_HOST",
    "POSTGRES_PORT",
    "POSTGRES_DB",
    "POSTGRES_USER",
    "POSTGRES_PASSWORD",
] 