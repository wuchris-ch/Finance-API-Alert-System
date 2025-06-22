"""
NTFY notifications for the API Alert System
"""

import requests
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class NTFYNotifier:
    """Handles NTFY notifications"""
    
    def __init__(self, topic: str, server: str = "https://ntfy.sh", enabled: bool = True):
        """Initialize NTFY notifier"""
        self.topic = topic
        self.server = server.rstrip('/')
        self.enabled = enabled and bool(topic)
        self.url = f"{self.server}/{topic}"
        
        if self.enabled:
            logger.info(f"✅ NTFY configured: {self.url}")
        else:
            logger.warning("⚠️  NTFY not configured or disabled")
    
    def send_message(self, message: str, title: str = None, priority: int = 3, tags: list = None) -> bool:
        """Send message via NTFY"""
        if not self.enabled:
            logger.warning("NTFY not enabled, skipping message")
            return False
        
        try:
            headers = {
                'Content-Type': 'text/plain',
            }
            
            if title:
                headers['Title'] = title
            
            if priority:
                headers['Priority'] = str(priority)
            
            if tags:
                headers['Tags'] = ','.join(tags)
            
            response = requests.post(
                self.url,
                data=message.encode('utf-8'),
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info("✅ NTFY message sent successfully")
                return True
            else:
                logger.error(f"❌ NTFY API error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Failed to send NTFY message: {e}")
            return False
    
    def send_price_update(self, message: str) -> bool:
        """Send price update message"""
        return self.send_message(
            message=message,
            title="📊 Stock Price Update",
            priority=2,
            tags=["chart-increasing", "money"]
        )
    
    def send_alert(self, message: str) -> bool:
        """Send alert message"""
        return self.send_message(
            message=message,
            title="🚨 Price Alert",
            priority=4,
            tags=["warning", "money", "chart-decreasing"]
        )
    
    def test_connection(self) -> bool:
        """Test NTFY connection"""
        if not self.enabled:
            return False
        
        try:
            response = requests.get(self.server, timeout=10)
            
            if response.status_code == 200:
                logger.info("✅ NTFY server connection successful")
                return True
            else:
                logger.error(f"❌ Failed to connect to NTFY server: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Failed to test NTFY connection: {e}")
            return False 