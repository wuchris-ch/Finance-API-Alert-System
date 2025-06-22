# demo_v2.py
# Demo script for the V2 version with fixed Telegram

import config

def run_demo():
    """Run a quick demo with modified thresholds to trigger alerts"""
    print("🎬 DEMO MODE - Stock Alert System V2 (REQUESTS-BASED TELEGRAM)")
    print("=" * 60)
    print("This demo will:")
    print("1. Enable demo mode with mock price data")
    print("2. Set thresholds that will trigger alerts")
    print("3. Test Telegram notifications using requests (no async issues)")
    print("=" * 60)
    
    # Temporarily modify config for demo
    original_demo_mode = config.DEMO_MODE
    original_watchlist = config.WATCHLIST.copy()
    
    # Enable demo mode
    config.DEMO_MODE = True
    
    # Set thresholds that will definitely trigger with our mock data
    config.WATCHLIST = {
        # Just test with 2 stocks to keep it simple
        "AAPL": {"upper": 185.00, "lower": 195.00},    # Will trigger both
        "TSLA": {"upper": 245.00, "lower": 255.00},    # Will trigger both
    }
    
    print(f"📊 Demo watchlist: {list(config.WATCHLIST.keys())}")
    print("🎯 Thresholds set to trigger alerts with mock data")
    print("📱 Testing Telegram notifications with requests library...\n")
    
    # Import and run the V2 alert bot
    from alert_bot_v2 import check_prices_and_alert
    
    print("🔄 Demo Check #1")
    check_prices_and_alert()
    
    print("\n⏳ Waiting 3 seconds before next check...")
    import time
    time.sleep(3)
    
    print("🔄 Demo Check #2")
    check_prices_and_alert()
    
    # Restore original config
    config.DEMO_MODE = original_demo_mode
    config.WATCHLIST = original_watchlist
    
    print("\n✅ Demo completed!")
    print("🔍 Check your Telegram for alert messages.")
    print("📱 If you received alerts, the V2 fix worked! 🎉")

if __name__ == "__main__":
    run_demo() 