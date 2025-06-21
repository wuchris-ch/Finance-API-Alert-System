"""
Professional test for Stock Alert MCP Server using HTTP transport.
"""

import asyncio
import subprocess
import time
from fastmcp import Client

async def main():
    print("🧪 Testing Stock Alert MCP Server with HTTP transport...")
    
    # Start the server with HTTP transport
    print("🚀 Starting MCP server with HTTP transport...")
    server_process = subprocess.Popen([
        "python", "stock_alert_mcp_server.py",
        "--transport", "streamable-http",
        "--host", "127.0.0.1",
        "--port", "8000"
    ])
    
    try:
        # Wait for server to start
        print("⏳ Waiting for server to start...")
        time.sleep(3)
        
        # Connect to the server via HTTP
        print("🔗 Connecting to MCP server via HTTP...")
        async with Client("http://127.0.0.1:8000/mcp") as client:
            print("✅ Connected to MCP server via HTTP")
            
            # List available tools
            tools = await client.list_tools()
            print(f"📋 Available tools ({len(tools)}): {[t.name for t in tools]}")
            
            # Test a simple tool call
            print("\n🧪 Testing tool call...")
            result = await client.call_tool("get_watchlist_status")
            print("✅ Tool call successful:")
            print(result.text)
            
            print("\n✅ HTTP transport test completed successfully!")
            
    except Exception as e:
        print(f"❌ HTTP transport test failed: {e}")
        raise
    finally:
        # Clean up server process
        print("🧹 Cleaning up server process...")
        server_process.terminate()
        server_process.wait()
        print("✅ Server process terminated")

if __name__ == "__main__":
    asyncio.run(main()) 