"""
Telegram notifications for the API Alert System
"""

import requests
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class TelegramNotifier:
    """Handles Telegram bot notifications"""
    
    def __init__(self, token: str, chat_id: str):
        """Initialize Telegram notifier"""
        self.token = token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{token}"
        self.configured = bool(token and chat_id and token != "YOUR_BOT_TOKEN_HERE" and chat_id != "YOUR_CHAT_ID_HERE")
        
        if self.configured:
            logger.info("✅ Telegram bot configured successfully")
        else:
            logger.warning("⚠️  Telegram credentials not configured")
    
    def send_message(self, text: str, parse_mode: str = 'Markdown') -> bool:
        """Send message via Telegram bot"""
        if not self.configured:
            logger.warning("Telegram not configured, skipping message")
            return False
        
        try:
            url = f"{self.base_url}/sendMessage"
            data = {
                'chat_id': self.chat_id,
                'text': text,
                'parse_mode': parse_mode
            }
            
            response = requests.post(url, data=data, timeout=10)
            
            if response.status_code == 200:
                logger.info("✅ Telegram message sent successfully")
                return True
            else:
                logger.error(f"❌ Telegram API error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Failed to send Telegram message: {e}")
            return False
    
    def send_price_update(self, message: str) -> bool:
        """Send price update message"""
        return self.send_message(message)
    
    def send_alert(self, message: str) -> bool:
        """Send alert message"""
        return self.send_message(message)
    
    def test_connection(self) -> bool:
        """Test Telegram bot connection"""
        if not self.configured:
            return False
        
        try:
            url = f"{self.base_url}/getMe"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                bot_info = response.json()
                logger.info(f"✅ Telegram bot connected: {bot_info['result']['username']}")
                return True
            else:
                logger.error(f"❌ Failed to connect to Telegram bot: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Failed to test Telegram connection: {e}")
            return False 