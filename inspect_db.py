# inspect_db.py
# Utility script to inspect the alerts database

import sqlite3
from datetime import datetime

def inspect_database():
    """Inspect the alerts database and show statistics"""
    try:
        conn = sqlite3.connect("alerts.db")
        c = conn.cursor()
        
        print("📊 Stock Alert Database Inspection")
        print("=" * 50)
        
        # Check if tables exist
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = c.fetchall()
        print(f"📋 Tables: {[table[0] for table in tables]}")
        
        # Price history stats
        c.execute("SELECT COUNT(*) FROM price_history")
        price_count = c.fetchone()[0]
        print(f"📈 Total price records: {price_count}")
        
        if price_count > 0:
            # Latest prices
            print("\n🕐 Latest Prices:")
            c.execute("""
                SELECT ticker, price, fetched_at 
                FROM price_history 
                ORDER BY fetched_at DESC 
                LIMIT 10
            """)
            for ticker, price, fetched_at in c.fetchall():
                print(f"  {ticker:6} | ${price:8.2f} | {fetched_at}")
            
            # Price summary by ticker
            print("\n📊 Price Summary by Ticker:")
            c.execute("""
                SELECT ticker, 
                       COUNT(*) as records,
                       MIN(price) as min_price,
                       MAX(price) as max_price,
                       AVG(price) as avg_price,
                       MIN(fetched_at) as first_fetch,
                       MAX(fetched_at) as last_fetch
                FROM price_history 
                GROUP BY ticker
                ORDER BY ticker
            """)
            for row in c.fetchall():
                ticker, records, min_price, max_price, avg_price, first_fetch, last_fetch = row
                print(f"  {ticker:6} | {records:3} records | ${min_price:7.2f} - ${max_price:7.2f} (avg: ${avg_price:7.2f})")
                print(f"         | {first_fetch} to {last_fetch}")
        
        # Alert history stats
        c.execute("SELECT COUNT(*) FROM alert_history")
        alert_count = c.fetchone()[0]
        print(f"\n🚨 Total alerts sent: {alert_count}")
        
        if alert_count > 0:
            print("\n📢 Recent Alerts:")
            c.execute("""
                SELECT ticker, alert_type, price, threshold, sent_at 
                FROM alert_history 
                ORDER BY sent_at DESC 
                LIMIT 10
            """)
            for ticker, alert_type, price, threshold, sent_at in c.fetchall():
                direction = "↗️" if alert_type == "upper" else "↘️"
                print(f"  {direction} {ticker:6} | {alert_type:5} | ${price:8.2f} vs ${threshold:8.2f} | {sent_at}")
            
            # Alert summary
            print("\n📈 Alert Summary:")
            c.execute("""
                SELECT ticker, alert_type, COUNT(*) as count
                FROM alert_history 
                GROUP BY ticker, alert_type
                ORDER BY ticker, alert_type
            """)
            for ticker, alert_type, count in c.fetchall():
                print(f"  {ticker:6} | {alert_type:5} alerts: {count}")
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
    except FileNotFoundError:
        print("❌ Database file 'alerts.db' not found. Run the alert system first.")

if __name__ == "__main__":
    inspect_database() 