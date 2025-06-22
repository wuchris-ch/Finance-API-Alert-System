"""
Main Alert Bot for the API Alert System
"""

import time
import schedule
import logging
from datetime import datetime
from typing import Dict, Optional

from ..utils.config import *
from ..utils.helpers import setup_logging, validate_config
from .database import DatabaseManager
from .stock_monitor import StockMonitor
from ..notifications.telegram import TelegramNotifier
from ..notifications.ntfy import NTFYNotifier
from ..notifications.console import ConsoleNotifier

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


class AlertBot:
    """Main alert bot that coordinates all components"""
    
    def __init__(self):
        """Initialize the alert bot with all components"""
        self.config_status = validate_config()
        
        # Initialize components
        self.db_manager = DatabaseManager(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            database=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD
        )
        
        self.stock_monitor = StockMonitor(demo_mode=DEMO_MODE)
        
        # Initialize notifiers
        self.telegram_notifier = TelegramNotifier(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID) if ENABLE_TELEGRAM else None
        self.ntfy_notifier = NTFYNotifier(NTFY_TOPIC, NTFY_SERVER, NTFY_ENABLED) if ENABLE_NTFY else None
        self.console_notifier = ConsoleNotifier(CONSOLE_NOTIFICATIONS)
        
        # Initialize database
        self._init_database()
        
        logger.info("Alert Bot initialized successfully")
    
    def _init_database(self):
        """Initialize database connection and tables"""
        try:
            if self.db_manager.connect():
                self.db_manager.init_tables()
                logger.info("Database initialized successfully")
            else:
                logger.error("Failed to connect to database")
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
    
    def check_prices_and_send_alerts(self):
        """Main function to check prices and send alerts"""
        now = datetime.utcnow()
        logger.info(f"📊 Checking prices at {now}")
        
        # Get prices for all tickers
        prices = self.stock_monitor.get_prices_for_watchlist(WATCHLIST)
        
        # Store prices in database
        for ticker, price in prices.items():
            if price is not None:
                self.db_manager.insert_price(ticker, price, now)
        
        # Check for threshold alerts
        alerts = self.stock_monitor.check_all_thresholds(WATCHLIST, prices)
        
        # Send price updates
        if any(price is not None for price in prices.values()):
            price_message = self.stock_monitor.format_price_message(prices, now)
            self._send_price_update(price_message)
        
        # Send alerts if any thresholds are crossed
        if alerts:
            alert_message = self.stock_monitor.format_alert_message(alerts, prices, WATCHLIST)
            self._send_alert(alert_message)
            
            # Store alerts in database
            for ticker, alert_types in alerts.items():
                price = prices.get(ticker)
                thresholds = WATCHLIST.get(ticker, {})
                
                for alert_type in alert_types:
                    if alert_type == 'UPPER':
                        threshold = thresholds.get('upper', 0)
                        self.db_manager.insert_alert(ticker, 'UPPER', price, threshold, now)
                    elif alert_type == 'LOWER':
                        threshold = thresholds.get('lower', 0)
                        self.db_manager.insert_alert(ticker, 'LOWER', price, threshold, now)
        
        # Show console summary
        self.console_notifier.print_price_table(prices)
    
    def _send_price_update(self, message: str):
        """Send price update to all configured notifiers"""
        success_count = 0
        
        if self.telegram_notifier:
            if self.telegram_notifier.send_price_update(message):
                success_count += 1
        
        if self.ntfy_notifier:
            if self.ntfy_notifier.send_price_update(message):
                success_count += 1
        
        if self.console_notifier:
            if self.console_notifier.send_price_update(message):
                success_count += 1
        
        logger.info(f"Price update sent to {success_count} notifiers")
    
    def _send_alert(self, message: str):
        """Send alert to all configured notifiers"""
        success_count = 0
        
        if self.telegram_notifier:
            if self.telegram_notifier.send_alert(message):
                success_count += 1
        
        if self.ntfy_notifier:
            if self.ntfy_notifier.send_alert(message):
                success_count += 1
        
        if self.console_notifier:
            if self.console_notifier.send_alert(message):
                success_count += 1
        
        logger.info(f"Alert sent to {success_count} notifiers")
    
    def show_recent_history(self, limit: int = 5):
        """Show recent price and alert history"""
        logger.info(f"📈 Recent Price History (Last {limit} entries):")
        
        prices = self.db_manager.get_recent_prices(limit=limit)
        for price_data in prices:
            ticker = price_data['ticker']
            fetched_at = price_data['fetched_at']
            price = price_data['price']
            logger.info(f"{ticker:6} | {fetched_at} | ${price:8.2f}")
        
        logger.info(f"🚨 Recent Alerts (Last {limit} entries):")
        alerts = self.db_manager.get_recent_alerts(limit=limit)
        for alert_data in alerts:
            ticker = alert_data['ticker']
            alert_type = alert_data['alert_type']
            price = alert_data['price']
            threshold = alert_data['threshold']
            sent_at = alert_data['sent_at']
            logger.info(f"{ticker:6} | {alert_type:5} | ${price:8.2f} | ${threshold:8.2f} | {sent_at}")
    
    def test_notifications(self):
        """Test all notification systems"""
        test_message = "🧪 This is a test message from the API Alert System"
        
        logger.info("Testing notification systems...")
        
        if self.telegram_notifier:
            if self.telegram_notifier.test_connection():
                self.telegram_notifier.send_message(test_message)
        
        if self.ntfy_notifier:
            if self.ntfy_notifier.test_connection():
                self.ntfy_notifier.send_message(test_message)
        
        if self.console_notifier:
            self.console_notifier.send_message(test_message)
    
    def run(self):
        """Run the alert bot continuously"""
        logger.info("🚀 Starting Alert Bot...")
        logger.info(f"📊 Monitoring {len(WATCHLIST)} tickers")
        logger.info(f"⏰ Polling interval: {POLL_INTERVAL} seconds")
        
        if DEMO_MODE:
            logger.info("🎬 Running in DEMO MODE with mock data")
        
        # Schedule the price checking
        schedule.every(POLL_INTERVAL).seconds.do(self.check_prices_and_send_alerts)
        
        # Run initial check
        self.check_prices_and_send_alerts()
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("🛑 Alert Bot stopped by user")
        except Exception as e:
            logger.error(f"❌ Alert Bot error: {e}")
        finally:
            self.db_manager.disconnect()
            logger.info("👋 Alert Bot shutdown complete")


def main():
    """Main entry point"""
    bot = AlertBot()
    bot.run()


if __name__ == "__main__":
    main() 