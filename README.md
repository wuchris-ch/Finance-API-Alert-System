# 📈 API Alert System

A comprehensive, modular stock price monitoring system that tracks your favorite stocks and sends alerts when prices cross your defined thresholds. Built with Python, PostgreSQL, and multiple notification systems including Telegram and NTFY.

## 🏗️ Project Structure

```
api-alert-system/
├── src/
│   └── api_alert_system/          # Main package
│       ├── core/                  # Core functionality
│       │   ├── alert_bot.py       # Main alert bot
│       │   ├── database.py        # Database operations
│       │   └── stock_monitor.py   # Stock price monitoring
│       ├── notifications/         # Notification systems
│       │   ├── telegram.py        # Telegram notifications
│       │   ├── ntfy.py           # NTFY notifications
│       │   └── console.py        # Console notifications
│       ├── mcp/                  # Model Context Protocol
│       │   ├── server.py         # MCP server
│       │   └── client.py         # MCP client
│       └── utils/                # Utilities
│           ├── config.py         # Configuration
│           └── helpers.py        # Helper functions
├── scripts/                      # Utility scripts
│   ├── setup_db.py              # Database setup
│   ├── inspect_db.py            # Database inspection
│   └── setup.py                 # General setup
├── tests/                       # Test files
├── demos/                       # Demo applications
├── backups/                     # Backup versions
├── docs/                        # Documentation
├── docker/                      # Docker files
├── data/                        # Data files
└── main.py                      # Main entry point
```

## ✨ Features

- 📊 **Real-time Stock Monitoring**: Uses Yahoo Finance API via `yfinance`
- 🚨 **Customizable Alerts**: Set upper and lower price thresholds
- 💾 **Historical Data**: PostgreSQL database stores all price history
- 📱 **Multiple Notifications**: Telegram, NTFY, and console notifications
- 🐳 **Docker Ready**: Easy containerized deployment
- 🎬 **Demo Mode**: Test with mock data before going live
- 📈 **Alert History**: Track all alerts sent over time
- 🔧 **Modular Design**: Clean, maintainable code structure

## 🚀 Quick Start

### 1. Clone and Install

```bash
git clone <your-repo>
cd api-alert-system

# Install dependencies
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

### 2. Configure Your Watchlist

Edit `src/api_alert_system/utils/config.py`:

```python
WATCHLIST = {
    "AAPL": {"upper": 200.00, "lower": 175.00},
    "TSLA": {"upper": 300.00, "lower": 200.00},
    "SPY": {"upper": 500.00, "lower": 450.00},
}
```

### 3. Set Up Environment Variables

Create a `.env` file:

```bash
# PostgreSQL Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=stock_alerts
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password_here

# Telegram Configuration (Optional)
TELEGRAM_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# NTFY Configuration (Optional)
NTFY_TOPIC=your-unique-topic-name
NTFY_SERVER=https://ntfy.sh

# System Configuration
DEMO_MODE=False
POLL_INTERVAL=10
```

### 4. Initialize Database

```bash
# Using the script
python scripts/setup_db.py

# Or using the entry point
setup-db
```

### 5. Run the System

```bash
# Using the main entry point
python main.py

# Or using the package directly
python -m api_alert_system.core.alert_bot

# Or using the entry point
alert-bot
```

## 📱 Notification Setup

### Telegram Setup

1. **Create a Bot**:
   - Message [@BotFather](https://t.me/BotFather) on Telegram
   - Send `/newbot` and follow instructions
   - Copy your bot token

2. **Get Your Chat ID**:
   - Message [@userinfobot](https://t.me/userinfobot) 
   - Copy your chat ID

3. **Update Environment**:
   ```bash
   TELEGRAM_TOKEN=your_bot_token_here
   TELEGRAM_CHAT_ID=your_chat_id_here
   ```

### NTFY Setup

1. **Choose a Topic**:
   - Pick a unique topic name (e.g., "your-username-stock-alerts-xyz123")

2. **Subscribe**:
   - Visit https://ntfy.sh/your-topic-name
   - Or use the NTFY app

3. **Update Environment**:
   ```bash
   NTFY_TOPIC=your-unique-topic-name
   NTFY_SERVER=https://ntfy.sh
   ```

## 🎬 Demo Mode

Try the system with mock data:

```bash
# Enable demo mode in .env
DEMO_MODE=True

# Run the system
python main.py
```

## 🐳 Docker Deployment

### Using Docker Compose

```bash
cd docker
docker-compose up -d
```

### Manual Docker Build

```bash
# Build the image
docker build -f docker/Dockerfile -t api-alert-system .

# Run with environment variables
docker run -d \
  --name api-alerts \
  --env-file .env \
  api-alert-system
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=api_alert_system

# Run specific tests
pytest tests/test_telegram.py
```

## 📚 Documentation

- [Quick Start Guide](docs/QUICKSTART.md)
- [MCP Integration](docs/MCP_README.md)
- [NTFY Setup](docs/NTFY_SETUP.md)

## 🔧 Development

### Project Structure Benefits

- **Modularity**: Each component is isolated and testable
- **Maintainability**: Clear separation of concerns
- **Extensibility**: Easy to add new notification systems
- **Testing**: Dedicated test directory with proper structure
- **Documentation**: Organized documentation in docs/

### Adding New Features

1. **New Notification System**: Add to `src/api_alert_system/notifications/`
2. **New Data Source**: Extend `src/api_alert_system/core/stock_monitor.py`
3. **New Database**: Extend `src/api_alert_system/core/database.py`
4. **New Scripts**: Add to `scripts/` directory

### Code Quality

```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📞 Support

For support and questions:
- Open an issue on GitHub
- Check the documentation in the `docs/` directory
- Review the demo applications in `demos/`
