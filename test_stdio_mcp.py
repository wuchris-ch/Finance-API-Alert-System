#!/usr/bin/env python3
"""
Simple test for the Stock Alert MCP Server using stdio transport.
"""

import asyncio
import subprocess
from fastmcp import Client

async def test_stdio_mcp():
    """Test the Stock Alert MCP server via stdio"""
    
    print("🧪 Testing Stock Alert MCP Server with stdio transport...")
    
    try:
        # Connect to the server via stdio
        print("🔗 Connecting to MCP server via stdio...")
        from fastmcp.client.transports import PythonStdioTransport
        transport = PythonStdioTransport("stock_alert_mcp_server.py")
        async with Client(transport) as client:
            print("✅ Connected to MCP server via stdio")
            
            # List available tools
            tools = await client.list_tools()
            print(f"📋 Available tools ({len(tools)}):")
            for tool in tools:
                print(f"  - {tool.name}: {tool.description}")
            
            # List available resources
            resources = await client.list_resources()
            print(f"📚 Available resources ({len(resources)}):")
            for resource in resources:
                print(f"  - {resource.uri}: {resource.name}")
            
            # Test a simple tool call
            print("\n🧪 Testing tool call: get_watchlist_status")
            result = await client.call_tool("get_watchlist_status")
            print("✅ Tool call successful:")
            if hasattr(result, 'text'):
                print(result.text)
            elif isinstance(result, list) and len(result) > 0:
                print(result[0].text if hasattr(result[0], 'text') else str(result[0]))
            else:
                print(str(result))
            
            # Test enabling demo mode
            # Test enabling demo mode
            print("\n🎬 Testing tool call: toggle_demo_mode")
            result = await client.call_tool("toggle_demo_mode", {"enabled": True})
            print("✅ Demo mode toggle successful:")
            if hasattr(result, 'text'):
                print(result.text)
            elif isinstance(result, list) and len(result) > 0:
                print(result[0].text if hasattr(result[0], 'text') else str(result[0]))
            else:
                print(str(result))
            
            # Test getting current prices in demo mode
            print("\n📊 Testing tool call: get_current_prices")
            result = await client.call_tool("get_current_prices", {"tickers": ["AAPL", "TSLA"]})
            print("✅ Get current prices successful:")
            if hasattr(result, 'text'):
                print(result.text)
            elif isinstance(result, list) and len(result) > 0:
                print(result[0].text if hasattr(result[0], 'text') else str(result[0]))
            else:
                print(str(result))
            
            # Test reading a resource
            print("\n📖 Testing resource access: system_config")
            config = await client.read_resource("mcp://stock-alerts/system_config")
            print("✅ Resource access successful:")
            if hasattr(config, 'content'):
                print(config.content)
            elif isinstance(config, list) and len(config) > 0:
                print(config[0].content if hasattr(config[0], 'content') else str(config[0]))
            else:
                print(str(config))
            print("\n✅ All stdio tests completed successfully!")
            
    except Exception as e:
        print(f"❌ Stdio test failed: {e}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == "__main__":
    asyncio.run(test_stdio_mcp())