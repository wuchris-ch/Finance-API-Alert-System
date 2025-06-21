"""
Simple test script for the Stock Alert MCP Server
"""

import asyncio
from fastmcp import Client
import json

async def quick_test():
    """Quick test of the MCP server"""
    print("🧪 Testing Stock Alert MCP Server...")
    
    try:
        # Connect to the MCP server using a single string command
        async with Client("python stock_alert_mcp_server.py") as client:
            print("✅ Connected to MCP server")
            
            # Test 1: Get watchlist status
            print("\n📋 Test 1: Getting watchlist status")
            result = await client.call_tool("get_watchlist_status")
            print(result.text)
            
            # Test 2: Add a stock
            print("\n➕ Test 2: Adding stock to watchlist")
            result = await client.call_tool("add_stock_to_watchlist", {
                "ticker": "TEST",
                "upper_threshold": 100.0,
                "lower_threshold": 50.0
            })
            print(result.text)
            
            # Test 3: Get current prices
            print("\n📊 Test 3: Getting current prices")
            result = await client.call_tool("get_current_prices", {
                "tickers": ["AAPL", "TEST"]
            })
            print(result.text)
            
            # Test 4: Toggle demo mode
            print("\n🎬 Test 4: Enabling demo mode")
            result = await client.call_tool("toggle_demo_mode", {
                "enabled": True
            })
            print(result.text)
            
            # Test 5: Check alert conditions
            print("\n🚨 Test 5: Checking alert conditions")
            result = await client.call_tool("check_alert_conditions")
            print(result.text)
            
            print("\n✅ All tests completed successfully!")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = asyncio.run(quick_test())
    exit(0 if success else 1) 