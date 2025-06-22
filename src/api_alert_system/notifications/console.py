"""
Console notifications for the API Alert System
"""

from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ConsoleNotifier:
    """Handles console notifications"""
    
    def __init__(self, enabled: bool = True):
        """Initialize console notifier"""
        self.enabled = enabled
        
        if self.enabled:
            logger.info("✅ Console notifications enabled")
        else:
            logger.info("ℹ️  Console notifications disabled")
    
    def send_message(self, message: str, level: str = "INFO") -> bool:
        """Send message to console"""
        if not self.enabled:
            return False
        
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        
        if level == "ERROR":
            logger.error(f"[{timestamp}] {message}")
        elif level == "WARNING":
            logger.warning(f"[{timestamp}] {message}")
        elif level == "ALERT":
            print(f"\n🚨 [{timestamp}] {message}\n")
        else:
            logger.info(f"[{timestamp}] {message}")
        
        return True
    
    def send_price_update(self, message: str) -> bool:
        """Send price update message to console"""
        return self.send_message(message, "INFO")
    
    def send_alert(self, message: str) -> bool:
        """Send alert message to console"""
        return self.send_message(message, "ALERT")
    
    def print_separator(self, char: str = "-", length: int = 50) -> None:
        """Print a separator line"""
        if self.enabled:
            print(char * length)
    
    def print_header(self, title: str) -> None:
        """Print a formatted header"""
        if self.enabled:
            self.print_separator("=", 60)
            print(f"📊 {title}")
            self.print_separator("=", 60)
    
    def print_price_table(self, prices: dict) -> None:
        """Print prices in a formatted table"""
        if not self.enabled:
            return
        
        print("\n📊 Current Prices:")
        self.print_separator("-", 40)
        print(f"{'Ticker':<10} {'Price':<15} {'Time':<20}")
        self.print_separator("-", 40)
        
        for ticker, price in prices.items():
            if price is not None:
                print(f"{ticker:<10} ${price:<14.2f} {datetime.utcnow().strftime('%H:%M:%S'):<20}")
            else:
                print(f"{ticker:<10} {'N/A':<15} {datetime.utcnow().strftime('%H:%M:%S'):<20}")
        
        self.print_separator("-", 40)
        print() 