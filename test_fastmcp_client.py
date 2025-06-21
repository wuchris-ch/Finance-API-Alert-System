"""
Test client for the Stock Alert FastMCP Server
Demonstrates how to interact with the MCP server programmatically.
"""

import asyncio
from fastmcp import Client
import json

async def test_stock_alert_mcp():
    """Test the Stock Alert MCP server"""
    
    # Connect to the MCP server using a single string command
    async with Client("python stock_alert_mcp_server.py") as client:
        print("🔗 Connected to Stock Alert MCP Server")
        
        # Test 1: Get watchlist status
        print("\n📋 Test 1: Getting watchlist status")
        result = await client.call_tool("get_watchlist_status")
        print(result.text)
        
        # Test 2: Add a stock to watchlist
        print("\n➕ Test 2: Adding stock to watchlist")
        result = await client.call_tool("add_stock_to_watchlist", {
            "ticker": "MSFT",
            "upper_threshold": 400.0,
            "lower_threshold": 350.0
        })
        print(result.text)
        
        # Test 3: Get current prices
        print("\n📊 Test 3: Getting current prices")
        result = await client.call_tool("get_current_prices", {
            "tickers": ["AAPL", "MSFT"]
        })
        print(result.text)
        
        # Test 4: Check alert conditions
        print("\n🚨 Test 4: Checking alert conditions")
        result = await client.call_tool("check_alert_conditions")
        print(result.text)
        
        # Test 5: Get price history
        print("\n📈 Test 5: Getting price history")
        result = await client.call_tool("get_price_history", {
            "ticker": "AAPL",
            "days": 1
        })
        print(result.text)
        
        # Test 6: Toggle demo mode
        print("\n🎬 Test 6: Toggling demo mode")
        result = await client.call_tool("toggle_demo_mode", {
            "enabled": True
        })
        print(result.text)
        
        # Test 7: Get system configuration
        print("\n⚙️ Test 7: Getting system configuration")
        config = await client.read_resource("system_config")
        print(config.content)
        
        print("\n✅ All tests completed!")

if __name__ == "__main__":
    asyncio.run(test_stock_alert_mcp()) 