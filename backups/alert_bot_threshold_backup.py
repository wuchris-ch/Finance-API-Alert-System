# alert_bot_v2.py
# Fixed version using requests instead of async telegram library

import sqlite3
import time
import requests
from datetime import datetime
import sys
import os

import yfinance as yf
import config
import schedule

# -----------------------------------------------------------------------------
# 1) Initialize Telegram Bot (if configured) - USING REQUESTS
# -----------------------------------------------------------------------------
telegram_configured = False

if hasattr(config, 'TELEGRAM_TOKEN') and hasattr(config, 'TELEGRAM_CHAT_ID'):
    if config.TELEGRAM_TOKEN != "YOUR_BOT_TOKEN_HERE" and config.TELEGRAM_CHAT_ID != "YOUR_CHAT_ID_HERE":
        telegram_configured = True
        print("✅ Telegram bot configured successfully")
    else:
        print("⚠️  Telegram credentials not configured. Using console notifications.")

# -----------------------------------------------------------------------------
# 2) Initialize SQLite and ensure table exists
# -----------------------------------------------------------------------------
def init_database():
    conn = sqlite3.connect("alerts.db")
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS price_history (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker      TEXT NOT NULL,
            fetched_at  DATETIME NOT NULL,
            price       REAL NOT NULL
        )
        """
    )
    
    # Create alerts table to track when we've sent alerts
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS alert_history (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker      TEXT NOT NULL,
            alert_type  TEXT NOT NULL,  -- 'upper' or 'lower'
            price       REAL NOT NULL,
            threshold   REAL NOT NULL,
            sent_at     DATETIME NOT NULL
        )
        """
    )
    conn.commit()
    return conn, c

conn, c = init_database()

# -----------------------------------------------------------------------------
# 3) Keep track of which tickers we've alerted within this run
# -----------------------------------------------------------------------------
alerted_status = {
    ticker: {"above": False, "below": False} for ticker in config.WATCHLIST
}

# -----------------------------------------------------------------------------
# 4) Notification Functions - USING REQUESTS (NO ASYNC)
# -----------------------------------------------------------------------------
def send_telegram_message_requests(text):
    """Send message via Telegram bot using requests library"""
    if not telegram_configured:
        return False
    
    try:
        url = f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/sendMessage"
        data = {
            'chat_id': config.TELEGRAM_CHAT_ID,
            'text': text,
            'parse_mode': 'Markdown'
        }
        
        response = requests.post(url, data=data, timeout=10)
        
        if response.status_code == 200:
            return True
        else:
            print(f"❌ Telegram API error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Failed to send Telegram message: {e}")
        return False

def send_console_notification(text):
    """Send notification to console with formatting"""
    print("\n" + "="*60)
    print("🚨 PRICE ALERT 🚨")
    print("="*60)
    # Remove markdown formatting for console
    clean_text = text.replace("*", "").replace("`", "").replace(">", "")
    print(clean_text)
    print("="*60 + "\n")

def send_notification(text):
    """Send notification via available channels"""
    # Try Telegram first
    telegram_sent = False
    if telegram_configured:
        telegram_sent = send_telegram_message_requests(text)
        if telegram_sent:
            print("✅ Telegram alert sent successfully!")
    
    # Always show in console if enabled or if Telegram failed
    if config.CONSOLE_NOTIFICATIONS or not telegram_sent:
        send_console_notification(text)

# -----------------------------------------------------------------------------
# 5) Price fetching with error handling
# -----------------------------------------------------------------------------
def get_stock_price(ticker):
    """Fetch current stock price with error handling"""
    try:
        if config.DEMO_MODE:
            # Return mock data for demo
            import random
            base_prices = {
                # Stocks
                "AAPL": 190, "TSLA": 250, "SPY": 470, "NVDA": 140,
                # Cryptocurrencies
                "BTC-USD": 95000, "LTC-USD": 110, "BCH-USD": 450
            }
            base = base_prices.get(ticker, 100)
            return base + random.uniform(-10, 10)
        
        data = yf.Ticker(ticker)
        # Use fast history method
        hist = data.history(period="1d", interval="1m")
        if hist.empty:
            print(f"⚠️  No data available for {ticker}")
            return None
        
        # Take the last available "Close" price
        latest_price = float(hist["Close"].iloc[-1])
        return latest_price
        
    except Exception as e:
        print(f"❌ Error fetching {ticker}: {e}")
        return None

# -----------------------------------------------------------------------------
# 6) Main alert checking function
# -----------------------------------------------------------------------------
def check_prices_and_alert():
    """Main function to check prices and send alerts"""
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    print(f"\n📊 Checking prices at {now}")
    print("-" * 50)
    
    for ticker, thresholds in config.WATCHLIST.items():
        latest_price = get_stock_price(ticker)
        
        if latest_price is None:
            continue
        
        # Insert into SQLite
        c.execute(
            "INSERT INTO price_history (ticker, fetched_at, price) VALUES (?, ?, ?)",
            (ticker, now, latest_price),
        )
        conn.commit()
        
        # Compare with thresholds
        upper = thresholds.get("upper")
        lower = thresholds.get("lower")
        
        # Status indicators
        status = "📈" if latest_price > (upper or float('inf')) else "📉" if latest_price < (lower or 0) else "📊"
        
        print(f"{status} {ticker}: ${latest_price:.2f} (Upper: ${upper or 'N/A'}, Lower: ${lower or 'N/A'})")
        
        # Check upper threshold
        if upper is not None and latest_price >= upper and not alerted_status[ticker]["above"]:
            text = (
                f"📈 *ALERT: {ticker} ABOVE THRESHOLD* 📈\n\n"
                f"💰 Current Price: `${latest_price:.2f}`\n"
                f"🎯 Upper Threshold: `${upper:.2f}`\n"
                f"📊 Difference: `+${latest_price - upper:.2f}`\n"
                f"🕐 Time: `{now}`"
            )
            send_notification(text)
            
            # Log to alert history
            c.execute(
                "INSERT INTO alert_history (ticker, alert_type, price, threshold, sent_at) VALUES (?, ?, ?, ?, ?)",
                (ticker, "upper", latest_price, upper, now)
            )
            conn.commit()
            
            alerted_status[ticker]["above"] = True
            
        elif upper is not None and latest_price < upper:
            # Reset flag when price goes back below threshold
            alerted_status[ticker]["above"] = False
        
        # Check lower threshold
        if lower is not None and latest_price <= lower and not alerted_status[ticker]["below"]:
            text = (
                f"📉 *ALERT: {ticker} BELOW THRESHOLD* 📉\n\n"
                f"💰 Current Price: `${latest_price:.2f}`\n"
                f"🎯 Lower Threshold: `${lower:.2f}`\n"
                f"📊 Difference: `-${lower - latest_price:.2f}`\n"
                f"🕐 Time: `{now}`"
            )
            send_notification(text)
            
            # Log to alert history
            c.execute(
                "INSERT INTO alert_history (ticker, alert_type, price, threshold, sent_at) VALUES (?, ?, ?, ?, ?)",
                (ticker, "lower", latest_price, lower, now)
            )
            conn.commit()
            
            alerted_status[ticker]["below"] = True
            
        elif lower is not None and latest_price > lower:
            # Reset flag when price goes back above threshold
            alerted_status[ticker]["below"] = False

# -----------------------------------------------------------------------------
# 7) Utility functions
# -----------------------------------------------------------------------------
def show_recent_history(limit=10):
    """Show recent price history"""
    print(f"\n📈 Recent Price History (Last {limit} entries):")
    print("-" * 70)
    
    c.execute(
        "SELECT ticker, fetched_at, price FROM price_history ORDER BY fetched_at DESC LIMIT ?",
        (limit,)
    )
    
    for row in c.fetchall():
        ticker, fetched_at, price = row
        print(f"{ticker:6} | {fetched_at} | ${price:8.2f}")

def show_alert_history(limit=5):
    """Show recent alert history"""
    print(f"\n🚨 Recent Alerts (Last {limit}):")
    print("-" * 80)
    
    c.execute(
        "SELECT ticker, alert_type, price, threshold, sent_at FROM alert_history ORDER BY sent_at DESC LIMIT ?",
        (limit,)
    )
    
    alerts = c.fetchall()
    if not alerts:
        print("No alerts sent yet.")
        return
    
    for row in alerts:
        ticker, alert_type, price, threshold, sent_at = row
        direction = "↗️" if alert_type == "upper" else "↘️"
        print(f"{direction} {ticker:6} | {alert_type:5} | ${price:8.2f} vs ${threshold:8.2f} | {sent_at}")

# -----------------------------------------------------------------------------
# 8) Main execution
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    print("🚀 Stock Price Alert System Starting (V2 - Fixed Telegram)...")
    print("=" * 60)
    
    # Show configuration
    print(f"📊 Watching {len(config.WATCHLIST)} tickers: {', '.join(config.WATCHLIST.keys())}")
    print(f"⏱️  Polling interval: {config.POLL_INTERVAL} seconds")
    print(f"📱 Telegram configured: {'✅' if telegram_configured else '❌'}")
    print(f"🖥️  Console notifications: {'✅' if config.CONSOLE_NOTIFICATIONS else '❌'}")
    print(f"🧪 Demo mode: {'✅' if config.DEMO_MODE else '❌'}")
    
    if config.DEMO_MODE:
        print("\n⚠️  DEMO MODE ENABLED - Using mock price data")
    
    print("\n" + "=" * 60)
    
    # Schedule the price checking
    schedule.every(config.POLL_INTERVAL).seconds.do(check_prices_and_alert)
    
    # Run one check immediately on startup
    print("🔍 Running initial price check...")
    check_prices_and_alert()
    
    # Show some history if available
    show_recent_history(5)
    show_alert_history(3)
    
    print(f"\n⏰ Scheduled to check prices every {config.POLL_INTERVAL} seconds...")
    print("Press Ctrl+C to stop\n")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n👋 Stopping alert system...")
        print("📊 Final statistics:")
        show_recent_history(10)
        show_alert_history(5)
        conn.close()
        print("✅ Database connection closed. Goodbye!")
        sys.exit(0) 