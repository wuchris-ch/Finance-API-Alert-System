"""
Stock Alert MCP Server using FastMCP
Provides tools for managing stock alerts, monitoring prices, and handling notifications.
"""

from fastmcp import FastMCP, Context
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import yfinance as yf
import psycopg2
from psycopg2.extras import DictCursor
import json
import asyncio

# Import your existing config
import config

# Create the FastMCP server instance
mcp = FastMCP("Stock Alert System 📈")

@mcp.tool
async def add_stock_to_watchlist(
    ticker: str,
    upper_threshold: Optional[float] = None,
    lower_threshold: Optional[float] = None,
    ctx: Context = None
) -> str:
    """Add a stock to the watchlist with optional price thresholds"""
    try:
        # Validate ticker
        if not ticker or len(ticker) > 10:
            return "❌ Invalid ticker symbol"
        
        # Validate thresholds
        if upper_threshold is not None and upper_threshold <= 0:
            return "❌ Upper threshold must be positive"
        if lower_threshold is not None and lower_threshold <= 0:
            return "❌ Lower threshold must be positive"
        if upper_threshold is not None and lower_threshold is not None:
            if upper_threshold <= lower_threshold:
                return "❌ Upper threshold must be greater than lower threshold"
        
        # Add to config
        config.WATCHLIST[ticker] = {
            "upper": upper_threshold,
            "lower": lower_threshold
        }
        
        if ctx:
            await ctx.info(f"Added {ticker} to watchlist")
        
        return f"✅ Added {ticker} to watchlist with thresholds: upper={upper_threshold}, lower={lower_threshold}"
        
    except Exception as e:
        return f"❌ Error adding stock: {str(e)}"

@mcp.tool
async def remove_stock_from_watchlist(
    ticker: str,
    ctx: Context = None
) -> str:
    """Remove a stock from the watchlist"""
    try:
        if ticker not in config.WATCHLIST:
            return f"❌ {ticker} not found in watchlist"
        
        del config.WATCHLIST[ticker]
        
        if ctx:
            await ctx.info(f"Removed {ticker} from watchlist")
        
        return f"✅ Removed {ticker} from watchlist"
        
    except Exception as e:
        return f"❌ Error removing stock: {str(e)}"

@mcp.tool
async def update_stock_thresholds(
    ticker: str,
    upper_threshold: Optional[float] = None,
    lower_threshold: Optional[float] = None,
    ctx: Context = None
) -> str:
    """Update price thresholds for a stock"""
    try:
        if ticker not in config.WATCHLIST:
            return f"❌ {ticker} not found in watchlist"
        
        # Validate thresholds
        if upper_threshold is not None and upper_threshold <= 0:
            return "❌ Upper threshold must be positive"
        if lower_threshold is not None and lower_threshold <= 0:
            return "❌ Lower threshold must be positive"
        if upper_threshold is not None and lower_threshold is not None:
            if upper_threshold <= lower_threshold:
                return "❌ Upper threshold must be greater than lower threshold"
        
        # Update thresholds
        current = config.WATCHLIST[ticker]
        if upper_threshold is not None:
            current["upper"] = upper_threshold
        if lower_threshold is not None:
            current["lower"] = lower_threshold
        
        if ctx:
            await ctx.info(f"Updated thresholds for {ticker}")
        
        return f"✅ Updated {ticker} thresholds: upper={current['upper']}, lower={current['lower']}"
        
    except Exception as e:
        return f"❌ Error updating thresholds: {str(e)}"

@mcp.tool
async def get_current_prices(
    tickers: Optional[List[str]] = None,
    ctx: Context = None
) -> str:
    """Get current prices for stocks in watchlist or specified tickers"""
    try:
        if tickers is None:
            tickers = list(config.WATCHLIST.keys())
        
        if not tickers:
            return "❌ No tickers specified and watchlist is empty"
        
        prices = {}
        for ticker in tickers:
            try:
                if config.DEMO_MODE:
                    # Mock data for demo
                    import random
                    base_prices = {
                        "AAPL": 190, "TSLA": 250, "SPY": 470, "NVDA": 140,
                        "BTC-USD": 95000, "LTC-USD": 110, "BCH-USD": 450
                    }
                    base = base_prices.get(ticker, 100)
                    price = base + random.uniform(-10, 10)
                else:
                    data = yf.Ticker(ticker)
                    hist = data.history(period="1d", interval="1m")
                    if hist.empty:
                        prices[ticker] = None
                        continue
                    price = float(hist["Close"].iloc[-1])
                
                prices[ticker] = price
                
            except Exception as e:
                prices[ticker] = None
                if ctx:
                    await ctx.error(f"Error fetching {ticker}: {str(e)}")
        
        # Format response
        result = "📊 Current Prices:\n"
        for ticker, price in prices.items():
            if price is not None:
                result += f"  {ticker}: ${price:.2f}\n"
            else:
                result += f"  {ticker}: ❌ Error fetching price\n"
        
        if ctx:
            await ctx.info(f"Fetched prices for {len(tickers)} tickers")
        
        return result
        
    except Exception as e:
        return f"❌ Error fetching prices: {str(e)}"

@mcp.tool
async def check_alert_conditions(
    ticker: Optional[str] = None,
    ctx: Context = None
) -> str:
    """Check if any stocks have crossed their alert thresholds"""
    try:
        if ticker:
            tickers = [ticker]
        else:
            tickers = list(config.WATCHLIST.keys())
        
        if not tickers:
            return "❌ No tickers to check"
        
        alerts = []
        
        for ticker in tickers:
            if ticker not in config.WATCHLIST:
                continue
            
            thresholds = config.WATCHLIST[ticker]
            
            # Get current price
            try:
                if config.DEMO_MODE:
                    import random
                    base_prices = {"AAPL": 190, "TSLA": 250, "SPY": 470, "NVDA": 140}
                    base = base_prices.get(ticker, 100)
                    current_price = base + random.uniform(-10, 10)
                else:
                    data = yf.Ticker(ticker)
                    hist = data.history(period="1d", interval="1m")
                    if hist.empty:
                        continue
                    current_price = float(hist["Close"].iloc[-1])
                
                # Check thresholds
                if thresholds.get("upper") and current_price >= thresholds["upper"]:
                    alerts.append({
                        "ticker": ticker,
                        "type": "upper",
                        "price": current_price,
                        "threshold": thresholds["upper"]
                    })
                
                if thresholds.get("lower") and current_price <= thresholds["lower"]:
                    alerts.append({
                        "ticker": ticker,
                        "type": "lower",
                        "price": current_price,
                        "threshold": thresholds["lower"]
                    })
            
            except Exception as e:
                if ctx:
                    await ctx.error(f"Error checking {ticker}: {str(e)}")
        
        if not alerts:
            return "✅ No alert conditions met"
        
        # Format alerts
        result = "🚨 Alert Conditions Met:\n"
        for alert in alerts:
            direction = "↗️" if alert["type"] == "upper" else "↘️"
            result += f"  {direction} {alert['ticker']}: ${alert['price']:.2f} "
            result += f"({'above' if alert['type'] == 'upper' else 'below'}) "
            result += f"${alert['threshold']:.2f}\n"
        
        if ctx:
            await ctx.info(f"Found {len(alerts)} alert conditions")
        
        return result
        
    except Exception as e:
        return f"❌ Error checking alerts: {str(e)}"

@mcp.tool
async def get_price_history(
    ticker: str,
    days: int = 7,
    ctx: Context = None
) -> str:
    """Get price history for a stock from the database"""
    try:
        # Connect to database
        conn = psycopg2.connect(
            host=config.POSTGRES_HOST,
            port=config.POSTGRES_PORT,
            database=config.POSTGRES_DB,
            user=config.POSTGRES_USER,
            password=config.POSTGRES_PASSWORD
        )
        
        cur = conn.cursor(cursor_factory=DictCursor)
        
        # Get recent price history
        cur.execute("""
            SELECT ticker, fetched_at, price 
            FROM price_history 
            WHERE ticker = %s 
            ORDER BY fetched_at DESC 
            LIMIT %s
        """, (ticker, days * 24 * 6))  # Assuming 6 data points per hour
        
        rows = cur.fetchall()
        cur.close()
        conn.close()
        
        if not rows:
            return f"❌ No price history found for {ticker}"
        
        # Format response
        result = f"📈 Price History for {ticker} (Last {len(rows)} entries):\n"
        for row in rows:
            result += f"  {row['fetched_at']}: ${row['price']:.2f}\n"
        
        if ctx:
            await ctx.info(f"Retrieved {len(rows)} price records for {ticker}")
        
        return result
        
    except Exception as e:
        return f"❌ Error getting price history: {str(e)}"

@mcp.tool
async def get_alert_history(
    ticker: Optional[str] = None,
    days: int = 7,
    ctx: Context = None
) -> str:
    """Get alert history from the database"""
    try:
        # Connect to database
        conn = psycopg2.connect(
            host=config.POSTGRES_HOST,
            port=config.POSTGRES_PORT,
            database=config.POSTGRES_DB,
            user=config.POSTGRES_USER,
            password=config.POSTGRES_PASSWORD
        )
        
        cur = conn.cursor(cursor_factory=DictCursor)
        
        # Get recent alert history
        if ticker:
            cur.execute("""
                SELECT ticker, alert_type, price, threshold, sent_at 
                FROM alert_history 
                WHERE ticker = %s 
                ORDER BY sent_at DESC 
                LIMIT %s
            """, (ticker, days * 24 * 6))
        else:
            cur.execute("""
                SELECT ticker, alert_type, price, threshold, sent_at 
                FROM alert_history 
                ORDER BY sent_at DESC 
                LIMIT %s
            """, (days * 24 * 6,))
        
        rows = cur.fetchall()
        cur.close()
        conn.close()
        
        if not rows:
            return f"❌ No alert history found{f' for {ticker}' if ticker else ''}"
        
        # Format response
        result = f"🚨 Alert History{f' for {ticker}' if ticker else ''} (Last {len(rows)} alerts):\n"
        for row in rows:
            direction = "↗️" if row['alert_type'] == 'upper' else "↘️"
            result += f"  {direction} {row['ticker']}: ${row['price']:.2f} "
            result += f"({'above' if row['alert_type'] == 'upper' else 'below'}) "
            result += f"${row['threshold']:.2f} at {row['sent_at']}\n"
        
        if ctx:
            await ctx.info(f"Retrieved {len(rows)} alert records")
        
        return result
        
    except Exception as e:
        return f"❌ Error getting alert history: {str(e)}"

@mcp.tool
async def get_watchlist_status(
    ctx: Context = None
) -> str:
    """Get current status of all stocks in watchlist"""
    try:
        if not config.WATCHLIST:
            return "❌ Watchlist is empty"
        
        result = "📋 Watchlist Status:\n"
        
        for ticker, thresholds in config.WATCHLIST.items():
            result += f"\n  {ticker}:\n"
            result += f"    Upper threshold: ${thresholds.get('upper', 'Not set')}\n"
            result += f"    Lower threshold: ${thresholds.get('lower', 'Not set')}\n"
            
            # Get current price
            try:
                if config.DEMO_MODE:
                    import random
                    base_prices = {"AAPL": 190, "TSLA": 250, "SPY": 470, "NVDA": 140}
                    base = base_prices.get(ticker, 100)
                    current_price = base + random.uniform(-10, 10)
                else:
                    data = yf.Ticker(ticker)
                    hist = data.history(period="1d", interval="1m")
                    if not hist.empty:
                        current_price = float(hist["Close"].iloc[-1])
                    else:
                        current_price = None
                
                if current_price is not None:
                    result += f"    Current price: ${current_price:.2f}\n"
                    
                    # Check if thresholds are crossed
                    if thresholds.get("upper") and current_price >= thresholds["upper"]:
                        result += f"    ⚠️  PRICE ABOVE UPPER THRESHOLD!\n"
                    elif thresholds.get("lower") and current_price <= thresholds["lower"]:
                        result += f"    ⚠️  PRICE BELOW LOWER THRESHOLD!\n"
                    else:
                        result += f"    ✅ Price within thresholds\n"
                else:
                    result += f"    ❌ Unable to fetch current price\n"
            
            except Exception as e:
                result += f"    ❌ Error fetching price: {str(e)}\n"
        
        if ctx:
            await ctx.info("Retrieved watchlist status")
        
        return result
        
    except Exception as e:
        return f"❌ Error getting watchlist status: {str(e)}"

@mcp.tool
async def toggle_demo_mode(
    enabled: bool,
    ctx: Context = None
) -> str:
    """Enable or disable demo mode (uses mock data)"""
    try:
        config.DEMO_MODE = enabled
        
        if ctx:
            await ctx.info(f"Demo mode {'enabled' if enabled else 'disabled'}")
        
        return f"✅ Demo mode {'enabled' if enabled else 'disabled'}"
        
    except Exception as e:
        return f"❌ Error toggling demo mode: {str(e)}"

@mcp.resource("mcp://stock-alerts/watchlist_config")
async def watchlist_config() -> str:
    """Get current watchlist configuration"""
    return json.dumps(config.WATCHLIST, indent=2)

@mcp.resource("mcp://stock-alerts/system_config")
async def system_config() -> str:
    """Get current system configuration"""
    config_data = {
        "poll_interval": config.POLL_INTERVAL,
        "demo_mode": config.DEMO_MODE,
        "telegram_enabled": config.ENABLE_TELEGRAM,
        "ntfy_enabled": config.ENABLE_NTFY,
        "console_notifications": config.CONSOLE_NOTIFICATIONS
    }
    return json.dumps(config_data, indent=2)

# Run the server
if __name__ == "__main__":
    mcp.run() 