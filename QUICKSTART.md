# 🚀 Quick Start Guide

Get your stock alert system running in under 5 minutes!

## ⚡ Super Quick Setup

```bash
# 1. Install dependencies
python3 setup.py

# 2. Start monitoring (uses console alerts by default)
source venv/bin/activate
python alert_bot.py
```

That's it! The system is now monitoring AAPL, TSLA, SPY, and NVDA with default thresholds.

## 🎬 Try the Demo First

```bash
source venv/bin/activate
python demo.py
```

This runs with mock data and shows you exactly how alerts work.

## ⚙️ Customize Your Watchlist

Edit `config.py`:

```python
WATCHLIST = {
    "AAPL": {"upper": 200.00, "lower": 175.00},
    "MSFT": {"upper": 450.00, "lower": 400.00},
    "GOOGL": {"upper": 180.00, "lower": 150.00},
}
```

## 📱 Add Telegram Notifications (Optional)

1. Message [@BotFather](https://t.me/BotFather) → `/newbot` → get your token
2. Message [@userinfobot](https://t.me/userinfobot) → get your chat ID
3. Update `config.py`:
   ```python
   TELEGRAM_TOKEN = "1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZ"
   TELEGRAM_CHAT_ID = "123456789"
   ```

## 📊 Monitor Your Data

```bash
# View stored price history and alerts
python inspect_db.py

# Check what's in your database
ls -la alerts.db
```

## 🐳 Run with Docker

```bash
# Build and run
docker build -t stock-alert .
docker run -d --name stock-alerts -v $(pwd)/alerts.db:/app/alerts.db stock-alert

# Or use docker-compose
docker-compose up -d
```

## 🔧 Common Configurations

### High-Frequency Trading Simulation
```python
POLL_INTERVAL = 30  # Check every 30 seconds
```

### Conservative Long-term Monitoring
```python
POLL_INTERVAL = 3600  # Check every hour
```

### Demo Mode for Testing
```python
DEMO_MODE = True  # Uses mock data
```

## 🚨 Example Alert

When AAPL crosses $200:

```
============================================================
🚨 PRICE ALERT 🚨
============================================================
📈 ALERT: AAPL ABOVE THRESHOLD 📈

💰 Current Price: $200.66
🎯 Upper Threshold: $200.00
📊 Difference: +$0.66
🕐 Time: 2025-06-01 05:29:34 UTC
============================================================
```

## 🛠️ Troubleshooting

**"No data available for TICKER"**
- Check ticker symbol is correct
- Try during market hours
- Test with AAPL first

**Import errors**
- Run `python3 setup.py` again
- Make sure you're in the virtual environment

**Telegram not working**
- Verify bot token and chat ID
- Message your bot first
- Check the token format

## 📈 What You Get

- ✅ Real-time stock price monitoring
- ✅ Customizable price thresholds  
- ✅ SQLite database with full history
- ✅ Console + Telegram notifications
- ✅ Docker deployment ready
- ✅ Demo mode for testing
- ✅ Database inspection tools

## 🎯 Perfect For

- Personal stock monitoring
- Learning finance APIs
- Building trading alerts
- Portfolio management
- Educational projects
- Weekend coding projects

---

**Ready to start?** Run `python3 setup.py` and you'll be monitoring stocks in minutes! 🚀 