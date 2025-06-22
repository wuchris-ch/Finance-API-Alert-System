"""
Stock price monitoring for the API Alert System
"""

import yfinance as yf
import random
from datetime import datetime
from typing import Dict, Optional, List
import logging

logger = logging.getLogger(__name__)


class StockMonitor:
    """Handles stock price fetching and monitoring"""
    
    def __init__(self, demo_mode: bool = False):
        """Initialize the stock monitor"""
        self.demo_mode = demo_mode
        self.base_prices = {
            # Stocks
            "AAPL": 190, "TSLA": 250, "SPY": 470, "NVDA": 140,
            # Cryptocurrencies
            "BTC-USD": 95000, "LTC-USD": 110, "BCH-USD": 450
        }
    
    def get_stock_price(self, ticker: str) -> Optional[float]:
        """Fetch current stock price with error handling"""
        try:
            if self.demo_mode:
                # Return mock data for demo
                base = self.base_prices.get(ticker, 100)
                return base + random.uniform(-10, 10)
            
            data = yf.Ticker(ticker)
            # Use fast history method
            hist = data.history(period="1d", interval="1m")
            if hist.empty:
                logger.warning(f"No data available for {ticker}")
                return None
            
            # Take the last available "Close" price
            latest_price = float(hist["Close"].iloc[-1])
            return latest_price
            
        except Exception as e:
            logger.error(f"Error fetching {ticker}: {e}")
            return None
    
    def get_prices_for_watchlist(self, watchlist: Dict) -> Dict[str, Optional[float]]:
        """Get prices for all tickers in the watchlist"""
        prices = {}
        for ticker in watchlist.keys():
            price = self.get_stock_price(ticker)
            prices[ticker] = price
            if price is not None:
                logger.info(f"📊 {ticker}: ${price:.2f}")
            else:
                logger.warning(f"⚠️  Could not fetch price for {ticker}")
        return prices
    
    def check_thresholds(self, ticker: str, price: float, thresholds: Dict) -> List[str]:
        """Check if price crosses any thresholds and return alert types"""
        alerts = []
        
        if price is None:
            return alerts
        
        upper_threshold = thresholds.get('upper')
        lower_threshold = thresholds.get('lower')
        
        if upper_threshold and price >= upper_threshold:
            alerts.append('UPPER')
        
        if lower_threshold and price <= lower_threshold:
            alerts.append('LOWER')
        
        return alerts
    
    def check_all_thresholds(self, watchlist: Dict, prices: Dict[str, Optional[float]]) -> Dict[str, List[str]]:
        """Check thresholds for all tickers in the watchlist"""
        alerts = {}
        
        for ticker, thresholds in watchlist.items():
            price = prices.get(ticker)
            if price is not None:
                ticker_alerts = self.check_thresholds(ticker, price, thresholds)
                if ticker_alerts:
                    alerts[ticker] = ticker_alerts
        
        return alerts
    
    def format_price_message(self, prices: Dict[str, Optional[float]], timestamp: datetime = None) -> str:
        """Format price data into a readable message"""
        if timestamp is None:
            timestamp = datetime.utcnow()
        
        message = f"📊 *Stock Price Update*\n`{timestamp}`\n\n"
        
        for ticker, price in prices.items():
            if price is not None:
                message += f"`{ticker:8} ${price:8.2f}`\n"
            else:
                message += f"`{ticker:8} N/A`\n"
        
        return message
    
    def format_alert_message(self, alerts: Dict[str, List[str]], prices: Dict[str, Optional[float]], watchlist: Dict) -> str:
        """Format alert data into a readable message"""
        if not alerts:
            return ""
        
        timestamp = datetime.utcnow()
        message = f"🚨 *Price Alert*\n`{timestamp}`\n\n"
        
        for ticker, alert_types in alerts.items():
            price = prices.get(ticker, "N/A")
            thresholds = watchlist.get(ticker, {})
            
            message += f"*{ticker}*: ${price}\n"
            
            for alert_type in alert_types:
                if alert_type == 'UPPER':
                    threshold = thresholds.get('upper', 'N/A')
                    message += f"  ⬆️  Above upper threshold: ${threshold}\n"
                elif alert_type == 'LOWER':
                    threshold = thresholds.get('lower', 'N/A')
                    message += f"  ⬇️  Below lower threshold: ${threshold}\n"
            
            message += "\n"
        
        return message 