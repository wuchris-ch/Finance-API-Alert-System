# Stock Alert MCP Server

This directory contains the Model Context Protocol (MCP) server for the Stock Alert System, built using [FastMCP](https://github.com/jlowin/fastmcp).

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install FastMCP
pip install fastmcp

# Or update your existing installation
pip install -r requirements.txt
```

### 2. Run the MCP Server

```bash
# Run with stdio transport (default)
python stock_alert_mcp_server.py

# Run with HTTP transport
python stock_alert_mcp_server.py --transport streamable-http --host 127.0.0.1 --port 8000

# Run with SSE transport
python stock_alert_mcp_server.py --transport sse --host 127.0.0.1 --port 8000
```

### 3. Test the Server

```bash
# Quick test
python test_mcp_server.py

# Full test client
python test_fastmcp_client.py
```

## 🛠️ Available Tools

The MCP server provides the following tools:

### Stock Management
- **`add_stock_to_watchlist`**: Add a stock with optional price thresholds
- **`remove_stock_from_watchlist`**: Remove a stock from monitoring
- **`update_stock_thresholds`**: Update price thresholds for existing stocks
- **`get_watchlist_status`**: Get current status of all monitored stocks

### Price Monitoring
- **`get_current_prices`**: Fetch current prices for stocks
- **`check_alert_conditions`**: Check if any stocks have crossed thresholds
- **`get_price_history`**: Retrieve historical price data from database
- **`get_alert_history`**: Retrieve historical alert data from database

### System Control
- **`toggle_demo_mode`**: Enable/disable demo mode for testing

## 📊 Available Resources

- **`watchlist_config`**: Current watchlist configuration
- **`system_config`**: System settings and configuration

## 🔧 Integration Examples

### Using with Claude Desktop

1. Add to your Claude Desktop MCP configuration:

```json
{
  "mcpServers": {
    "stock-alerts": {
      "command": "python",
      "args": ["/path/to/stock_alert_mcp_server.py"]
    }
  }
}
```

### Using with Other MCP Clients

```python
from fastmcp import Client

async def main():
    async with Client("python stock_alert_mcp_server.py") as client:
        # Add a stock
        result = await client.call_tool("add_stock_to_watchlist", {
            "ticker": "AAPL",
            "upper_threshold": 200.0,
            "lower_threshold": 150.0
        })
        print(result.text)
        
        # Check prices
        result = await client.call_tool("get_current_prices")
        print(result.text)

asyncio.run(main())
```

### Using with HTTP Transport

```python
from fastmcp import Client

async def main():
    # Connect via HTTP
    async with Client("http://localhost:8000/mcp") as client:
        # Use the same tools as above
        result = await client.call_tool("get_watchlist_status")
        print(result.text)

asyncio.run(main())
```

## 🎯 Use Cases

### 1. LLM-Powered Stock Analysis
```python
# Ask an LLM to analyze your portfolio
result = await client.call_tool("get_watchlist_status")
# LLM can then provide insights based on current prices and thresholds
```

### 2. Automated Portfolio Management
```python
# LLM can automatically adjust thresholds based on market conditions
result = await client.call_tool("update_stock_thresholds", {
    "ticker": "AAPL",
    "upper_threshold": 210.0,
    "lower_threshold": 160.0
})
```

### 3. Market Research
```python
# Get historical data for analysis
result = await client.call_tool("get_price_history", {
    "ticker": "TSLA",
    "days": 30
})
```

## 🔒 Security Considerations

- The MCP server runs with the same permissions as your user account
- Database credentials are loaded from environment variables
- Consider using authentication for HTTP transport in production
- Demo mode should be disabled in production environments

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Ensure PostgreSQL is running
   - Check database credentials in `.env` file
   - Run `python setup_db.py` to initialize database

2. **Yahoo Finance API Errors**
   - Check internet connection
   - Verify ticker symbols are valid
   - Consider using demo mode for testing

3. **MCP Connection Issues**
   - Ensure FastMCP is installed: `pip install fastmcp`
   - Check transport configuration
   - Verify Python path in MCP client configuration

### Debug Mode

Enable debug logging by setting the `FASTMCP_LOG_LEVEL` environment variable:

```bash
export FASTMCP_LOG_LEVEL=DEBUG
python stock_alert_mcp_server.py
```

## 📚 Additional Resources

- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [MCP Specification](https://modelcontextprotocol.io/)
- [Claude Desktop MCP Setup](https://docs.anthropic.com/en/docs/claude-desktop-mcp) 