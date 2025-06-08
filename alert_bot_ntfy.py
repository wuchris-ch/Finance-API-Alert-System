# alert_bot_ntfy.py
# Enhanced version that supports both Telegram and ntfy.sh notifications

import sqlite3
import time
import requests
from datetime import datetime
import sys
import os
import json

import yfinance as yf
import config
import schedule

# -----------------------------------------------------------------------------
# 1) Initialize notification services
# -----------------------------------------------------------------------------
telegram_configured = False
ntfy_configured = False

# Check Telegram configuration
if hasattr(config, 'TELEGRAM_TOKEN') and hasattr(config, 'TELEGRAM_CHAT_ID'):
    if (config.TELEGRAM_TOKEN != "YOUR_BOT_TOKEN_HERE" and 
        config.TELEGRAM_CHAT_ID != "YOUR_CHAT_ID_HERE" and
        getattr(config, 'ENABLE_TELEGRAM', True)):
        telegram_configured = True
        print("✅ Telegram bot configured successfully")
    else:
        print("⚠️  Telegram credentials not configured or disabled")

# Check ntfy.sh configuration
if (hasattr(config, 'NTFY_ENABLED') and config.NTFY_ENABLED and 
    hasattr(config, 'NTFY_TOPIC') and config.NTFY_TOPIC and
    getattr(config, 'ENABLE_NTFY', True)):
    ntfy_configured = True
    print("✅ ntfy.sh notifications configured successfully")
else:
    print("⚠️  ntfy.sh notifications not configured or disabled")

if not telegram_configured and not ntfy_configured:
    print("⚠️  No notification services configured. Using console notifications only.")

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
    conn.commit()
    return conn, c

conn, c = init_database()

# -----------------------------------------------------------------------------
# 3) Notification Functions
# -----------------------------------------------------------------------------
def send_telegram_message(text):
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

def send_ntfy_message(text, title="Stock Alert", priority="default", tags=None):
    """Send message via ntfy.sh"""
    if not ntfy_configured:
        return False
    
    try:
        url = f"{config.NTFY_SERVER}/{config.NTFY_TOPIC}"
        
        # Prepare headers and data
        headers = {
            "Title": title,
            "Priority": priority,
            "Content-Type": "text/plain"
        }
        
        if tags:
            headers["Tags"] = ",".join(tags) if isinstance(tags, list) else str(tags)
        
        response = requests.post(url, data=text, headers=headers, timeout=10)
        
        if response.status_code == 200:
            return True
        else:
            print(f"❌ ntfy.sh API error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Failed to send ntfy.sh message: {e}")
        return False

def send_multi_notification(text, title="Stock Alert", priority="default", tags=None):
    """Send notification via all configured services"""
    success_count = 0
    total_services = 0
    
    # Send via Telegram
    if telegram_configured:
        total_services += 1
        if send_telegram_message(text):
            success_count += 1
            print("✅ Sent to Telegram")
        else:
            print("❌ Failed to send to Telegram")
    
    # Send via ntfy.sh
    if ntfy_configured:
        total_services += 1
        if send_ntfy_message(text, title, priority, tags):
            success_count += 1
            print("✅ Sent to ntfy.sh")
        else:
            print("❌ Failed to send to ntfy.sh")
    
    # Console notification if configured or if no other services worked
    if config.CONSOLE_NOTIFICATIONS or success_count == 0:
        print(f"📱 NOTIFICATION: {title}")
        print(f"   {text}")
    
    return success_count, total_services

# -----------------------------------------------------------------------------
# 4) Price fetching with error handling
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
# 5) Threshold checking functions
# -----------------------------------------------------------------------------
def check_thresholds(ticker, price):
    """Check if price crosses any thresholds and return alert info"""
    if ticker not in config.WATCHLIST:
        return None
    
    thresholds = config.WATCHLIST[ticker]
    upper = thresholds.get("upper")
    lower = thresholds.get("lower")
    
    alert_info = None
    
    if upper is not None and price >= upper:
        alert_info = {
            "type": "UPPER",
            "threshold": upper,
            "price": price,
            "ticker": ticker
        }
    elif lower is not None and price <= lower:
        alert_info = {
            "type": "LOWER", 
            "threshold": lower,
            "price": price,
            "ticker": ticker
        }
    
    return alert_info

# -----------------------------------------------------------------------------
# 6) Main price checking function
# -----------------------------------------------------------------------------
def check_prices_and_send_update():
    """Check prices and send consolidated update"""
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    print(f"\n📊 Checking prices at {now}")
    print("-" * 50)
    
    # Collect all price data and alerts
    price_data = []
    alerts = []
    
    for ticker in config.WATCHLIST.keys():
        latest_price = get_stock_price(ticker)
        
        if latest_price is None:
            continue
        
        # Insert into SQLite
        c.execute(
            "INSERT INTO price_history (ticker, fetched_at, price) VALUES (?, ?, ?)",
            (ticker, now, latest_price),
        )
        conn.commit()
        
        # Check for threshold alerts
        alert_info = check_thresholds(ticker, latest_price)
        if alert_info:
            alerts.append(alert_info)
        
        # Add to price data for consolidated message
        price_data.append({
            'ticker': ticker,
            'price': latest_price
        })
        
        # Show in console
        threshold_info = ""
        if alert_info:
            threshold_info = f" ⚠️  {alert_info['type']} THRESHOLD"
        print(f"📊 {ticker}: ${latest_price:.2f}{threshold_info}")
    
    # Send threshold alerts immediately
    for alert in alerts:
        alert_text = f"🚨 {alert['ticker']} Alert!\n\n"
        alert_text += f"Price: ${alert['price']:.2f}\n"
        alert_text += f"{alert['type'].title()} threshold: ${alert['threshold']:.2f}\n"
        alert_text += f"Time: {now}"
        
        tags = ["warning", "stock", alert['ticker'].lower()]
        send_multi_notification(
            alert_text, 
            title=f"🚨 {alert['ticker']} Alert", 
            priority="high",
            tags=tags
        )
    
    # Send regular price update (less frequent or only if no other notifications)
    if price_data and (telegram_configured or ntfy_configured):
        # Create consolidated message
        if telegram_configured:
            # Telegram message with Markdown formatting
            telegram_message = f"📊 *Stock Price Update*\n`{now}`\n\n"
            for item in price_data:
                ticker = item['ticker']
                price = item['price']
                telegram_message += f"`{ticker:8} ${price:8.2f}`\n"
            send_telegram_message(telegram_message)
        
        if ntfy_configured:
            # ntfy.sh message (plain text, more readable)
            ntfy_message = f"Stock Price Update - {now}\n\n"
            for item in price_data:
                ticker = item['ticker']
                price = item['price']
                ntfy_message += f"{ticker}: ${price:.2f}\n"
            
            send_ntfy_message(
                ntfy_message, 
                title="📊 Stock Prices", 
                priority="default",
                tags=["stock", "update"]
            )
        
        if not alerts:  # Only show success message if no alerts were sent
            print("✅ Price update sent via configured services!")

# -----------------------------------------------------------------------------
# 7) Utility functions
# -----------------------------------------------------------------------------
def show_recent_history(limit=5):
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

def test_notifications():
    """Test all notification services"""
    print("\n🧪 Testing notification services...")
    print("-" * 50)
    
    test_message = f"🧪 Test notification from Stock Alert System\nTime: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}"
    
    success, total = send_multi_notification(
        test_message, 
        title="🧪 Test Alert", 
        priority="low",
        tags=["test"]
    )
    
    print(f"✅ Test completed: {success}/{total} services successful")

# -----------------------------------------------------------------------------
# 8) Main execution
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    print("🚀 Enhanced Stock Price Alert System Starting...")
    print("=" * 60)
    
    # Show configuration
    print(f"📊 Watching {len(config.WATCHLIST)} tickers: {', '.join(config.WATCHLIST.keys())}")
    print(f"⏱️  Update interval: {config.POLL_INTERVAL} seconds")
    print(f"📱 Telegram configured: {'✅' if telegram_configured else '❌'}")
    print(f"📡 ntfy.sh configured: {'✅' if ntfy_configured else '❌'}")
    print(f"🧪 Demo mode: {'✅' if config.DEMO_MODE else '❌'}")
    
    if config.DEMO_MODE:
        print("\n⚠️  DEMO MODE ENABLED - Using mock price data")
    
    if ntfy_configured:
        print(f"\n📡 ntfy.sh topic: {config.NTFY_TOPIC}")
        print(f"📡 Subscribe at: {config.NTFY_SERVER}/{config.NTFY_TOPIC}")
    
    print("\n" + "=" * 60)
    
    # Test notifications on startup
    test_notifications()
    
    # Schedule the price checking
    schedule.every(config.POLL_INTERVAL).seconds.do(check_prices_and_send_update)
    
    # Run one check immediately on startup
    print("\n🔍 Running initial price check...")
    check_prices_and_send_update()
    
    # Main loop
    print(f"\n🔄 Starting monitoring loop (checking every {config.POLL_INTERVAL} seconds)")
    print("Press Ctrl+C to stop...")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down gracefully...")
        conn.close()
        sys.exit(0) 