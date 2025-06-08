# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# 1) Which symbols to track, and at what thresholds (you can expand this)
#    Format: { "TICKER": { "upper": float_or_None, "lower": float_or_None } }
WATCHLIST = {
    # Stocks - Normal monitoring ranges
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
# IMPORTANT: Set these in your .env file
# To get these:
# 1. Message @BotFather on Telegram to create a new bot
# 2. Get your chat ID by messaging @userinfobot
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")  # Loaded from .env file
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")  # Loaded from .env file

# Example of what they should look like:
# TELEGRAM_TOKEN = "1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789"
# TELEGRAM_CHAT_ID = "123456789"  # Can be negative for groups: "-123456789"

# 4) ntfy.sh settings
# IMPORTANT: Set these in your .env file
# To use ntfy.sh:
# 1. Choose a unique topic name (e.g., "your-username-stock-alerts-xyz123")
# 2. Optionally set up a custom ntfy.sh server URL (default is ntfy.sh)
# 3. Subscribe to your topic at https://ntfy.sh/your-topic-name
NTFY_ENABLED = True  # Set to True to enable ntfy.sh notifications
NTFY_TOPIC = os.getenv("NTFY_TOPIC", "stock-alerts-api-system-123")  # Loaded from .env file with fallback
NTFY_SERVER = os.getenv("NTFY_SERVER", "https://ntfy.sh")  # Loaded from .env file with fallback

# Example of custom ntfy.sh setup:
# NTFY_ENABLED = True
# NTFY_TOPIC = "my-unique-stock-alerts-xyz789"
# NTFY_SERVER = "https://ntfy.sh"  # or your own server: "https://my-ntfy-server.com"

# 5) Notification preferences
# You can enable multiple notification methods simultaneously
ENABLE_TELEGRAM = True   # Enable/disable Telegram notifications
ENABLE_NTFY = True       # Enable/disable ntfy.sh notifications

# 6) Demo mode - set to True to use mock data for testing
DEMO_MODE = False

# 7) Enable console notifications if other methods are not configured
CONSOLE_NOTIFICATIONS = True 