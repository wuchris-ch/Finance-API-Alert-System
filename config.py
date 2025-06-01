# config.py

# 1) Which symbols to track, and at what thresholds (you can expand this)
#    Format: { "TICKER": { "upper": float_or_None, "lower": float_or_None } }
WATCHLIST = {
    # Stocks - Expanded ranges for more realistic monitoring
    "AAPL": {"upper": 220.00, "lower": 180.00},    # Wider $40 range
    "TSLA": {"upper": 400.00, "lower": 250.00},    # Wider $150 range  
    "SPY": {"upper": 620.00, "lower": 550.00},     # Wider $70 range
    "NVDA": {"upper": 180.00, "lower": 120.00},    # Wider $60 range
    
    # Cryptocurrencies - Much wider ranges for volatility
    "BTC-USD": {"upper": 110000.00, "lower": 85000.00},    # $25k range for Bitcoin
    "LTC-USD": {"upper": 130.00, "lower": 70.00},          # $60 range for Litecoin
    "BCH-USD": {"upper": 550.00, "lower": 350.00},         # $200 range for Bitcoin Cash
}

# 2) Polling interval (in seconds) - Updated to 10 seconds for frequent monitoring
POLL_INTERVAL = 10  # Check every 10 seconds for real-time monitoring

# 3) Telegram Bot settings
# IMPORTANT: Replace these with your actual bot token and chat ID
# To get these:
# 1. Message @BotFather on Telegram to create a new bot
# 2. Get your chat ID by messaging @userinfobot
TELEGRAM_TOKEN = "YOUR_BOT_TOKEN_HERE"  # replace with your Bot token
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID_HERE"  # replace with your chat ID (can be negative for groups)

# 4) Demo mode - set to True to use mock data for testing
DEMO_MODE = False

# 5) Enable console notifications if Telegram is not configured
CONSOLE_NOTIFICATIONS = True 