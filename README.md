# 📈 Stock Price Alert System

A simple, lightweight stock price monitoring system that tracks your favorite stocks and sends alerts when prices cross your defined thresholds using LLM. Built with Python, PostgreSQL, and optional Telegram notifications.

## ✨ Features

- 📊 **Real-time Stock Monitoring**: Uses Yahoo Finance API via `yfinance`
- 🚨 **Customizable Alerts**: Set upper and lower price thresholds
- 💾 **Historical Data**: PostgreSQL database stores all price history
- 📱 **Multiple Notifications**: Telegram bot + console notifications
- 🐳 **Docker Ready**: Easy containerized deployment
- 🎬 **Demo Mode**: Test with mock data before going live
- 📈 **Alert History**: Track all alerts sent over time

## 🚀 Quick Start

### 1. Clone and Install

```bash
git clone <your-repo>
cd stock-alert-system

# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies with uv
uv pip install -e .
```

### 2. Configure Your Watchlist

Edit `config.py`:

```python
WATCHLIST = {
    "AAPL": {"upper": 200.00, "lower": 175.00},
    "TSLA": {"upper": 300.00, "lower": 200.00},
    "SPY": {"upper": 500.00, "lower": 450.00},
}
```

### 3. Set Up PostgreSQL

Create a `.env` file with your PostgreSQL credentials:

```bash
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=stock_alerts
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password_here
```

Initialize the database:

```bash
python setup_db.py
```

### 4. Run the System

```bash
# Start monitoring (uses console notifications by default)
python alert_bot.py

# Or run a quick demo with mock data
python demo.py
```

## 📱 Telegram Setup (Optional)

To receive alerts via Telegram:

1. **Create a Bot**:
   - Message [@BotFather](https://t.me/BotFather) on Telegram
   - Send `/newbot` and follow instructions
   - Copy your bot token

2. **Get Your Chat ID**:
   - Message [@userinfobot](https://t.me/userinfobot) 
   - Copy your chat ID (or add bot to group and get group ID)

3. **Update Config**:
   ```python
   TELEGRAM_TOKEN = "1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZ"
   TELEGRAM_CHAT_ID = "123456789"  # Your user ID or group ID (can be negative)
   ```

## 🎬 Demo Mode

Try the system with mock data first:

```bash
python demo.py
```

This will:
- Enable mock price data
- Set thresholds that trigger alerts
- Show you how alerts work
- Display price and alert history

## 🐳 Docker Deployment

### Build and Run

```bash
# Build the image
docker build -t stock-alert .

# Run with environment variables
docker run -d \
  --name stock-alerts \
  -e POSTGRES_HOST=your_host \
  -e POSTGRES_PORT=5432 \
  -e POSTGRES_DB=stock_alerts \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=your_password \
  -e TELEGRAM_TOKEN="your_token_here" \
  -e TELEGRAM_CHAT_ID="your_chat_id" \
  stock-alert
```

### Docker Compose (Recommended)

Create `docker-compose.yml`:

```yaml
version: '3.8'
services:
  stock-alerts:
    build: .
    container_name: stock-alerts
    restart: unless-stopped
    environment:
      - POSTGRES_HOST=your_host
      - POSTGRES_PORT=5432
      - POSTGRES_DB=stock_alerts
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=your_password
      - TELEGRAM_TOKEN=your_token_here
      - TELEGRAM_CHAT_ID=your_chat_id
```

Run with:
```bash
docker-compose up -d
```

## ⚙️ Configuration Options

### `config.py` Settings

| Setting | Description | Default |
|---------|-------------|---------|
| `WATCHLIST` | Dict of tickers and thresholds | See config.py |
| `POLL_INTERVAL` | Seconds between price checks | 60 |
| `TELEGRAM_TOKEN` | Your Telegram bot token | Required for Telegram |
| `TELEGRAM_CHAT_ID` | Your chat/group ID | Required for Telegram |
| `DEMO_MODE` | Use mock data for testing | False |
| `CONSOLE_NOTIFICATIONS` | Show alerts in console | True |

### PostgreSQL Configuration

The following environment variables are required:

| Variable | Description | Default |
|----------|-------------|---------|
| `POSTGRES_HOST` | PostgreSQL server host | localhost |
| `POSTGRES_PORT` | PostgreSQL server port | 5432 |
| `POSTGRES_DB` | Database name | stock_alerts |
| `POSTGRES_USER` | Database user | postgres |
| `POSTGRES_PASSWORD` | Database password | postgres |

### Threshold Format

```python
WATCHLIST = {
    "TICKER": {
        "upper": 100.00,  # Alert when price >= this
        "lower": 80.00,   # Alert when price <= this
        # Set to None to disable: "upper": None
    }
}
```

## 📊 Database Schema

The system uses PostgreSQL with two tables:

### `price_history`
- `id`: SERIAL PRIMARY KEY
- `ticker`: VARCHAR(10) NOT NULL
- `fetched_at`: TIMESTAMP NOT NULL
- `price`: DECIMAL(10,2) NOT NULL

### `alert_history`
- `id`: SERIAL PRIMARY KEY
- `ticker`: VARCHAR(10) NOT NULL
- `alert_type`: VARCHAR(10) NOT NULL
- `price`: DECIMAL(10,2) NOT NULL
- `threshold`: DECIMAL(10,2) NOT NULL
- `sent_at`: TIMESTAMP NOT NULL

## 🔧 Troubleshooting

### Common Issues

**"No data available for TICKER"**
- Check if ticker symbol is correct
- Some tickers may not be available outside market hours
- Try with a major stock like AAPL first

**Telegram bot not working**
- Verify your bot token is correct
- Make sure you've messaged your bot at least once
- Check that chat ID is correct (can be negative for groups)

**PostgreSQL connection issues**
- Verify your PostgreSQL server is running
- Check your database credentials in `.env`
- Ensure the database and tables are created (run `setup_db.py`)

**Import errors**
- Make sure you're in the virtual environment
- Run `uv pip install -e .` again

### Testing Telegram

Quick test script:

```python
from telegram import Bot
import asyncio

async def test_telegram():
    bot = Bot(token="YOUR_TOKEN")
    await bot.send_message(chat_id="YOUR_CHAT_ID", text="Test message!")

asyncio.run(test_telegram())
```

## 📈 Usage Examples

### Basic Monitoring
```bash
# Monitor with default settings
python alert_bot.py
```

### Custom Polling Interval
Edit `config.py`:
```python
POLL_INTERVAL = 300  # Check every 5 minutes
```

### Production Deployment
```bash
# Run in background with nohup
nohup python alert_bot.py > alerts.log 2>&1 &

# Or use screen/tmux
screen -S stock-alerts
python alert_bot.py
# Ctrl+A, D to detach
```

## 🛠️ Extending the System

### Add New Notification Channels

```python
# In alert_bot.py, add to send_notification():
async def send_notification(text):
    # Existing Telegram code...
    
    # Add email
    if EMAIL_ENABLED:
        send_email_alert(text)
    
    # Add Slack
    if SLACK_WEBHOOK:
        send_slack_alert(text)
```

### Custom Alert Logic

```python
# Add to check_prices_and_alert():
# Custom logic for percentage changes
if latest_price > previous_price * 1.05:  # 5% increase
    send_notification(f"{ticker} up 5%!")
```

### Database Queries

```python
# Get price history for analysis
import psycopg2
conn = psycopg2.connect(
    host=config.POSTGRES_HOST,
    port=config.POSTGRES_PORT,
    database=config.POSTGRES_DB,
    user=config.POSTGRES_USER,
    password=config.POSTGRES_PASSWORD
)
cur = conn.cursor()

# Average price last 24 hours
cur.execute("""
    SELECT ticker, AVG(price) 
    FROM price_history 
    WHERE fetched_at > NOW() - INTERVAL '1 day'
    GROUP BY ticker
""")
```

## 📝 License

MIT License - feel free to modify and use for your own projects!

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## ⚠️ Disclaimer

This tool is for educational and personal use only. Not financial advice. Use at your own risk. 
