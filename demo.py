# demo.py
# Quick demo script that modifies config for immediate alerts

import config
import asyncio
from alert_bot import check_prices_and_alert, show_recent_history, show_alert_history

def run_demo():
    """Run a quick demo with modified thresholds to trigger alerts"""
    print("🎬 DEMO MODE - Stock Alert System")
    print("=" * 50)
    print("This demo will:")
    print("1. Enable demo mode with mock price data")
    print("2. Set thresholds that will trigger alerts")
    print("3. Run a few price checks to show alerts")
    print("=" * 50)
    
    # Temporarily modify config for demo
    original_demo_mode = config.DEMO_MODE
    original_watchlist = config.WATCHLIST.copy()
    
    # Enable demo mode
    config.DEMO_MODE = True
    
    # Set thresholds that will definitely trigger with our mock data
    config.WATCHLIST = {
        "AAPL": {"upper": 185.00, "lower": 195.00},  # Will trigger lower alert
        "TSLA": {"upper": 245.00, "lower": 255.00},  # Will trigger lower alert  
        "NVDA": {"upper": 135.00, "lower": 145.00},  # Will trigger lower alert
    }
    
    print(f"📊 Demo watchlist: {list(config.WATCHLIST.keys())}")
    print("🎯 Thresholds set to trigger alerts with mock data\n")
    
    try:
        # Run several checks to demonstrate alerts
        for i in range(3):
            print(f"\n🔄 Demo Check #{i+1}")
            asyncio.run(check_prices_and_alert())
            
            if i < 2:  # Don't sleep after last iteration
                print("⏳ Waiting 2 seconds before next check...")
                import time
                time.sleep(2)
        
        # Show results
        print("\n" + "="*60)
        print("📊 DEMO RESULTS")
        print("="*60)
        show_recent_history(10)
        show_alert_history(10)
        
    finally:
        # Restore original config
        config.DEMO_MODE = original_demo_mode
        config.WATCHLIST = original_watchlist
        print("\n✅ Demo completed! Original config restored.")

if __name__ == "__main__":
    run_demo() 