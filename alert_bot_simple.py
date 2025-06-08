# alert_bot_simple.py
# Simple version that sends price updates to Telegram every 10 seconds

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
    conn.commit()
    return conn, c

conn, c = init_database()

# -----------------------------------------------------------------------------
# 3) Telegram Functions
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
# 5) Main price checking function - SIMPLIFIED
# -----------------------------------------------------------------------------
def check_prices_and_send_update():
    """Check prices and send consolidated update to Telegram"""
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    print(f"\n📊 Checking prices at {now}")
    print("-" * 50)
    
    # Collect all price data
    price_data = []
    
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
        
        # Add to price data for consolidated message
        price_data.append({
            'ticker': ticker,
            'price': latest_price
        })
        
        # Show in console
        print(f"📊 {ticker}: ${latest_price:.2f}")
    
    # Create consolidated Telegram message
    if price_data and telegram_configured:
        telegram_message = f"📊 *Stock Price Update*\n`{now}`\n\n"
        
        for item in price_data:
            ticker = item['ticker']
            price = item['price']
            telegram_message += f"`{ticker:8} ${price:8.2f}`\n"
        
        # Send to Telegram
        success = send_telegram_message(telegram_message)
        if success:
            print("✅ Price update sent to Telegram!")
        else:
            print("❌ Failed to send to Telegram")

# -----------------------------------------------------------------------------
# 6) Utility functions
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

# -----------------------------------------------------------------------------
# 7) Main execution
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    print("🚀 Stock Price Update System Starting...")
    print("=" * 60)
    
    # Show configuration
    print(f"📊 Watching {len(config.WATCHLIST)} tickers: {', '.join(config.WATCHLIST.keys())}")
    print(f"⏱️  Update interval: {config.POLL_INTERVAL} seconds")
    print(f"📱 Telegram configured: {'✅' if telegram_configured else '❌'}")
    print(f"🧪 Demo mode: {'✅' if config.DEMO_MODE else '❌'}")
    
    if config.DEMO_MODE:
        print("\n⚠️  DEMO MODE ENABLED - Using mock price data")
    
    print("\n" + "=" * 60)
    
    # Schedule the price checking
    schedule.every(config.POLL_INTERVAL).seconds.do(check_prices_and_send_update)
    
    # Run one check immediately on startup
    print("🔍 Running initial price check...")
    check_prices_and_send_update()
    
    # Show some history if available
    show_recent_history(3)
    
    print(f"\n⏰ Sending price updates every {config.POLL_INTERVAL} seconds...")
    print("Press Ctrl+C to stop\n")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n👋 Stopping price update system...")
        print("📊 Final statistics:")
        show_recent_history(10)
        conn.close()
        print("✅ Database connection closed. Goodbye!")
        sys.exit(0) 