# ntfy.sh Setup Guide for Stock Alert System

This guide explains how to use **ntfy.sh** as an alternative notification service to Telegram for your stock alert system.

## What is ntfy.sh?

[ntfy.sh](https://ntfy.sh) is a simple, free, and open-source pub/sub notification service that allows you to send notifications to your phone, desktop, or browser without requiring API keys or registration.

### Advantages of ntfy.sh over Telegram:
- ✅ **No API keys required** - No need to create bot tokens or get chat IDs
- ✅ **No registration required** - Just choose a topic name and start using
- ✅ **Cross-platform** - Works on web, mobile (iOS/Android), desktop
- ✅ **Real-time** - Instant notifications via WebSocket
- ✅ **Free and open-source** - No rate limits for basic usage
- ✅ **Self-hostable** - Can run your own ntfy server if desired
- ✅ **Rich notifications** - Supports priorities, tags, and emojis

## Quick Start

### 1. Choose a Unique Topic Name

Pick a unique topic name (like a private channel). Examples:
- `your-username-stock-alerts-abc123`
- `stock-monitoring-xyz789`
- `my-portfolio-alerts-2024`

⚠️ **Important**: Topic names are public, so make them unique and hard to guess!

### 2. Subscribe to Notifications

Choose one of these methods to receive notifications:

#### Option A: Web Browser
1. Open https://ntfy.sh/your-topic-name (replace with your topic)
2. Bookmark the page
3. Keep the tab open to receive real-time notifications

#### Option B: Mobile App
1. Install the ntfy app:
   - [iOS App Store](https://apps.apple.com/us/app/ntfy/id1625396347)
   - [Android Play Store](https://play.google.com/store/apps/details?id=io.heckel.ntfy)
2. Open the app and subscribe to your topic name
3. Enable push notifications when prompted

#### Option C: Desktop App
1. Download from [ntfy.sh/docs/subscribe/phone/](https://ntfy.sh/docs/subscribe/phone/)
2. Subscribe to your topic

### 3. Configure Your Stock Alert System

Edit your `config.py` file:

```python
# ntfy.sh settings
NTFY_ENABLED = True
NTFY_TOPIC = "your-unique-topic-name-here"  # Replace with your topic
NTFY_SERVER = "https://ntfy.sh"

# Notification preferences
ENABLE_TELEGRAM = False  # Disable Telegram if you prefer ntfy.sh only
ENABLE_NTFY = True       # Enable ntfy.sh notifications
```

### 4. Test the Setup

Run the demo script to test your configuration:

```bash
python ntfy_demo.py
```

This will send various test notifications to verify everything is working.

### 5. Run the Enhanced Alert Bot

Use the enhanced version that supports both Telegram and ntfy.sh:

```bash
python alert_bot_ntfy.py
```

## Configuration Options

### Basic Configuration

```python
# Enable/disable ntfy.sh
NTFY_ENABLED = True

# Your unique topic name
NTFY_TOPIC = "your-topic-name"

# ntfy.sh server (default is the public server)
NTFY_SERVER = "https://ntfy.sh"
```

### Advanced Configuration

```python
# Enable multiple notification methods simultaneously
ENABLE_TELEGRAM = True   # Keep Telegram enabled
ENABLE_NTFY = True       # Also enable ntfy.sh

# Custom ntfy.sh server (if you're self-hosting)
NTFY_SERVER = "https://your-ntfy-server.com"
```

## How Notifications Work

### Priority Levels
ntfy.sh supports different priority levels:

- **min** (💤): Silent notifications
- **low** (📱): Quiet notifications  
- **default** (📢): Normal notifications
- **high** (⚠️): Important notifications with sound
- **max** (🚨): Urgent notifications that bypass Do Not Disturb

### Tags
Notifications can include tags for better organization:
- `warning` - For threshold alerts
- `stock` - For stock-related notifications
- `update` - For regular price updates
- Ticker symbols (e.g., `aapl`, `tsla`)

### Example Notifications

**Threshold Alert (High Priority):**
```
🚨 AAPL Alert!

Price: $195.50
Upper threshold: $220.00
Time: 2024-01-15 14:30:00 UTC
```

**Regular Price Update (Default Priority):**
```
📊 Stock Price Update - 2024-01-15 14:30:00

AAPL: $195.50
TSLA: $275.20
NVDA: $145.80
SPY: $585.40
```

## Troubleshooting

### Not Receiving Notifications?

1. **Check your topic name**: Make sure it matches exactly in config.py and your subscription
2. **Verify subscription**: 
   - Web: Make sure the browser tab is open and not blocked
   - Mobile: Check that notifications are enabled in app settings
   - Desktop: Ensure the app is running
3. **Test with the demo**: Run `python ntfy_demo.py` to verify the connection
4. **Check network**: Ensure you can access https://ntfy.sh

### Common Issues

**"Failed to send notification" errors:**
- Check your internet connection
- Verify the NTFY_SERVER URL is correct
- Try a different topic name if yours might be blocked

**Notifications delayed:**
- Web: Refresh the page or check if browser is blocking WebSockets
- Mobile: Check if the app is allowed to run in background
- Network: Corporate firewalls might block WebSocket connections

**Too many notifications:**
- Adjust the `POLL_INTERVAL` in config.py (increase from 10 seconds)
- Disable regular price updates and only keep threshold alerts

## Security Considerations

### Topic Privacy
- **Public topics**: Anyone who knows your topic name can subscribe to it
- **Use unique names**: Include random numbers/letters in your topic name
- **Don't use personal info**: Avoid including your name, email, etc.

### Message Content
- **No sensitive data**: Don't include account numbers, passwords, etc.
- **Public server**: Remember that ntfy.sh is a public service
- **Self-hosting option**: Consider running your own ntfy server for maximum privacy

### Recommended Topic Naming
```python
# Good examples:
NTFY_TOPIC = "stock-alerts-user123-xyz789"
NTFY_TOPIC = "portfolio-monitor-abc456"
NTFY_TOPIC = "trading-bot-notifications-def789"

# Avoid:
NTFY_TOPIC = "john-smith-stocks"  # Too identifiable
NTFY_TOPIC = "stocks"             # Too generic, others might use it
```

## Self-Hosting ntfy.sh (Advanced)

For maximum privacy and control, you can run your own ntfy server:

### Using Docker:
```bash
docker run -p 80:80 -it binwiederhier/ntfy serve
```

### Configuration:
```python
# Use your own server
NTFY_SERVER = "https://your-domain.com"  # Your self-hosted instance
NTFY_TOPIC = "any-topic-name"            # Can be simpler since it's private
```

See the [official ntfy.sh documentation](https://ntfy.sh/docs/) for detailed self-hosting instructions.

## Comparison: Telegram vs ntfy.sh

| Feature | Telegram | ntfy.sh |
|---------|----------|---------|
| **Setup Complexity** | Medium (need API keys) | Easy (just pick a topic) |
| **Registration** | Required | Not required |
| **Privacy** | Good (private bots) | Fair (topic-based) |
| **Mobile Apps** | Excellent | Good |
| **Rich Formatting** | Excellent (Markdown) | Good (emojis, priorities) |
| **Rate Limits** | Yes | No (for basic usage) |
| **Self-Hosting** | Not possible | Yes |
| **Cross-Platform** | Excellent | Good |
| **Reliability** | Excellent | Good |

## Examples and Use Cases

### Personal Portfolio Monitoring
```python
NTFY_TOPIC = "my-portfolio-alerts-2024-xyz"
ENABLE_NTFY = True
ENABLE_TELEGRAM = False

# Get notifications for threshold breaks only
POLL_INTERVAL = 30  # Check every 30 seconds
```

### Multi-User Setup (Family/Team)
```python
# Each person uses their own topic
NTFY_TOPIC = "family-stocks-john-abc123"    # John's notifications
# NTFY_TOPIC = "family-stocks-jane-def456"  # Jane's notifications

# Or use a shared topic for team alerts
NTFY_TOPIC = "trading-team-alerts-xyz789"
```

### Development and Testing
```python
# Separate topics for different environments
NTFY_TOPIC = "stock-bot-dev-abc123"    # Development/testing
# NTFY_TOPIC = "stock-bot-prod-xyz789" # Production alerts
```

## Next Steps

1. **Start with the demo**: Run `python ntfy_demo.py` to see how it works
2. **Choose your topic**: Pick a unique topic name and subscribe to it
3. **Update config**: Edit `config.py` with your ntfy.sh settings
4. **Test notifications**: Run `python alert_bot_ntfy.py` to start monitoring
5. **Customize alerts**: Adjust thresholds and polling intervals as needed

## Support and Resources

- **ntfy.sh Documentation**: https://ntfy.sh/docs/
- **Mobile Apps**: https://ntfy.sh/docs/subscribe/phone/
- **GitHub Repository**: https://github.com/binwiederhier/ntfy
- **Community**: Join the ntfy.sh Discord or GitHub discussions

---

🎉 **That's it!** You now have a simple, reliable notification system for your stock alerts without the complexity of API keys or registration requirements. 