# demo_fixed.py
# Quick demo script that modifies config for immediate alerts

import config

def run_demo():
    """Run a quick demo with modified thresholds to trigger alerts"""
    print("🎬 DEMO MODE - Stock Alert System (FIXED VERSION)")
    print("=" * 50)
    print("This demo will:")
    print("1. Enable demo mode with mock price data")
    print("2. Set thresholds that will trigger alerts")
    print("3. Test Telegram notifications")
    print("=" * 50)
    
    # Temporarily modify config for demo
    original_demo_mode = config.DEMO_MODE
    original_watchlist = config.WATCHLIST.copy()
    
    # Enable demo mode
    config.DEMO_MODE = True
    
    # Set thresholds that will definitely trigger with our mock data
    config.WATCHLIST = {
        # Stocks - Set to trigger alerts with mock ~190, ~250, ~140
        "AAPL": {"upper": 185.00, "lower": 195.00},    # Will trigger both
        "TSLA": {"upper": 245.00, "lower": 255.00},    # Will trigger both
        "NVDA": {"upper": 135.00, "lower": 145.00},    # Will trigger both
    }
    
    print(f"📊 Demo watchlist: {list(config.WATCHLIST.keys())}")
    print("🎯 Thresholds set to trigger alerts with mock data")
    print("📱 Testing Telegram notifications...\n")
    
    # Import and run the fixed alert bot
    from alert_bot_fixed import check_prices_and_alert
    
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
    
    print("\n✅ Demo completed! Check your Telegram for alert messages.")
    print("If you received Telegram alerts, the fix worked! 🎉")

if __name__ == "__main__":
    run_demo() 