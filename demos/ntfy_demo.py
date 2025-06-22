#!/usr/bin/env python3
"""
ntfy_demo.py - Simple demonstration of ntfy.sh notifications for stock alerts

This script shows how to use ntfy.sh as an alternative to Telegram for notifications.
ntfy.sh is a simple pub/sub notification service that works without requiring API keys.

Usage:
1. Choose a unique topic name (e.g., "your-username-stock-alerts-xyz123")
2. Subscribe to notifications at https://ntfy.sh/your-topic-name
3. Run this script to see how notifications work
"""

import requests
import time
from datetime import datetime
import random

# Configuration
NTFY_SERVER = "https://ntfy.sh"
NTFY_TOPIC = "stock-alerts-demo-123"  # Change this to something unique!

def send_ntfy_notification(message, title="Stock Alert", priority="default", tags=None):
    """
    Send a notification via ntfy.sh
    
    Args:
        message (str): The notification message
        title (str): The notification title
        priority (str): Priority level: "max", "high", "default", "low", "min"
        tags (list or str): Tags for the notification (e.g., ["warning", "stock"])
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        url = f"{NTFY_SERVER}/{NTFY_TOPIC}"
        
        # Prepare headers
        headers = {
            "Title": title,
            "Priority": priority,
            "Content-Type": "text/plain"
        }
        
        # Add tags if provided
        if tags:
            if isinstance(tags, list):
                headers["Tags"] = ",".join(tags)
            else:
                headers["Tags"] = str(tags)
        
        # Send the notification
        response = requests.post(url, data=message, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print(f"✅ Notification sent successfully to ntfy.sh")
            return True
        else:
            print(f"❌ Failed to send notification: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error sending notification: {e}")
        return False

def demo_basic_notification():
    """Send a basic test notification"""
    print("\n📱 Sending basic notification...")
    
    message = f"Hello from ntfy.sh demo!\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    success = send_ntfy_notification(
        message=message,
        title="🧪 Test Notification",
        priority="low",
        tags=["test", "demo"]
    )
    
    return success

def demo_stock_alert():
    """Send a mock stock alert notification"""
    print("\n🚨 Sending stock alert notification...")
    
    # Mock stock data
    tickers = ["AAPL", "TSLA", "NVDA", "SPY"]
    ticker = random.choice(tickers)
    price = round(random.uniform(100, 300), 2)
    threshold = round(price * random.uniform(0.9, 1.1), 2)
    alert_type = random.choice(["UPPER", "LOWER"])
    
    message = f"🚨 {ticker} Alert!\n\n"
    message += f"Current Price: ${price:.2f}\n"
    message += f"{alert_type.title()} Threshold: ${threshold:.2f}\n"
    message += f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    success = send_ntfy_notification(
        message=message,
        title=f"🚨 {ticker} Stock Alert",
        priority="high",
        tags=["warning", "stock", ticker.lower()]
    )
    
    return success

def demo_price_update():
    """Send a mock price update notification"""
    print("\n📊 Sending price update notification...")
    
    # Mock multiple stock prices
    stocks = {
        "AAPL": round(random.uniform(180, 220), 2),
        "TSLA": round(random.uniform(250, 350), 2),
        "NVDA": round(random.uniform(120, 180), 2),
        "SPY": round(random.uniform(550, 600), 2),
    }
    
    message = f"📊 Stock Price Update\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    for ticker, price in stocks.items():
        message += f"{ticker}: ${price:.2f}\n"
    
    success = send_ntfy_notification(
        message=message,
        title="📊 Stock Prices",
        priority="default",
        tags=["stock", "update", "prices"]
    )
    
    return success

def demo_different_priorities():
    """Demonstrate different priority levels"""
    print("\n🔔 Demonstrating different priority levels...")
    
    priorities = [
        ("min", "💤 Low priority notification"),
        ("low", "📱 Low priority notification"),  
        ("default", "📢 Default priority notification"),
        ("high", "⚠️  High priority notification"),
        ("max", "🚨 Max priority notification")
    ]
    
    success_count = 0
    
    for priority, message in priorities:
        print(f"   Sending {priority} priority notification...")
        
        full_message = f"{message}\nPriority: {priority}\nTime: {datetime.now().strftime('%H:%M:%S')}"
        
        success = send_ntfy_notification(
            message=full_message,
            title=f"🔔 Priority Demo - {priority.upper()}",
            priority=priority,
            tags=["demo", "priority", priority]
        )
        
        if success:
            success_count += 1
        
        time.sleep(2)  # Wait between notifications
    
    print(f"✅ Sent {success_count}/{len(priorities)} priority notifications")
    return success_count == len(priorities)

def main():
    """Main demo function"""
    print("🚀 ntfy.sh Stock Alert System Demo")
    print("=" * 50)
    
    print(f"📡 ntfy.sh Server: {NTFY_SERVER}")
    print(f"📡 Topic: {NTFY_TOPIC}")
    print(f"📡 Subscribe at: {NTFY_SERVER}/{NTFY_TOPIC}")
    print(f"📱 Or use the ntfy mobile app and subscribe to: {NTFY_TOPIC}")
    
    print("\n" + "=" * 50)
    print("IMPORTANT: To receive notifications:")
    print(f"1. Open {NTFY_SERVER}/{NTFY_TOPIC} in your browser")
    print("2. Or install the ntfy mobile app and subscribe to the topic")
    print("3. Keep the page/app open to receive real-time notifications")
    print("=" * 50)
    
    input("\nPress Enter to start the demo (make sure you're subscribed first)...")
    
    # Run demos
    demos = [
        ("Basic Notification", demo_basic_notification),
        ("Stock Alert", demo_stock_alert),
        ("Price Update", demo_price_update),
        ("Priority Levels", demo_different_priorities),
    ]
    
    success_count = 0
    
    for demo_name, demo_func in demos:
        print(f"\n{'='*20} {demo_name} {'='*20}")
        
        try:
            if demo_func():
                success_count += 1
                print(f"✅ {demo_name} completed successfully")
            else:
                print(f"❌ {demo_name} failed")
        except Exception as e:
            print(f"❌ {demo_name} error: {e}")
        
        if demo_name != demos[-1][0]:  # Don't wait after the last demo
            print("\nWaiting 3 seconds before next demo...")
            time.sleep(3)
    
    print(f"\n{'='*50}")
    print(f"🎉 Demo completed! {success_count}/{len(demos)} demos successful")
    print(f"📡 You can continue to receive notifications at: {NTFY_SERVER}/{NTFY_TOPIC}")
    print(f"🔧 To use this in your stock alert system, update config.py with:")
    print(f"   NTFY_TOPIC = \"{NTFY_TOPIC}\"")
    print(f"   NTFY_ENABLED = True")

if __name__ == "__main__":
    main() 