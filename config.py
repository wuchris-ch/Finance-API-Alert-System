# config.py

# 1) Which symbols to track, and at what thresholds (you can expand this)
#    Format: { "TICKER": { "upper": float_or_None, "lower": float_or_None } }
WATCHLIST = {
    "AAPL": {"upper": 200.00, "lower": 175.00},
    "TSLA": {"upper": 300.00, "lower": 200.00},
    "SPY": {"upper": 500.00, "lower": 450.00},
    "NVDA": {"upper": 150.00, "lower": 120.00}
}

# 2) Polling interval (in seconds)
POLL_INTERVAL = 60  # every 1 minute for demo purposes (change to 300 for production)

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