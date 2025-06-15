"""
Test client for StockAlertMCP
This script simulates an LLM client interacting with the MCP to test its functionality.
"""

from mcp import StockAlertMCP, StockAlert, StockThreshold
from datetime import datetime
import json
import asyncio
from typing import Dict, Any

class MockLLMClient:
    """Simulates an LLM client interacting with the MCP"""
    
    def __init__(self):
        self.mcp = StockAlertMCP()
        self.context = {}
    
    async def process_command(self, command: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Process a command as if it came from an LLM"""
        if not self.mcp.validate_action(command, params):
            return {
                "status": "error",
                "message": f"Invalid action or parameters for {command}"
            }
        
        # Simulate different actions
        if command == "add_stock":
            return await self._handle_add_stock(params)
        elif command == "remove_stock":
            return await self._handle_remove_stock(params)
        elif command == "update_thresholds":
            return await self._handle_update_thresholds(params)
        elif command == "get_price_history":
            return await self._handle_get_price_history(params)
        elif command == "get_alert_history":
            return await self._handle_get_alert_history(params)
        
        return {
            "status": "error",
            "message": f"Unknown command: {command}"
        }
    
    async def _handle_add_stock(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle adding a new stock"""
        ticker = params.get("ticker")
        upper = params.get("upper")
        lower = params.get("lower")
        
        # Validate thresholds
        if upper is not None and upper <= 0:
            return {
                "status": "error",
                "message": self.mcp.error_handling["invalid_threshold"]
            }
        
        if lower is not None and lower <= 0:
            return {
                "status": "error",
                "message": self.mcp.error_handling["invalid_threshold"]
            }
        
        # Store in context
        if "watchlist" not in self.context:
            self.context["watchlist"] = {}
        
        self.context["watchlist"][ticker] = StockThreshold(upper=upper, lower=lower)
        
        return {
            "status": "success",
            "message": f"Added {ticker} to watchlist",
            "data": {
                "ticker": ticker,
                "thresholds": {
                    "upper": upper,
                    "lower": lower
                }
            }
        }
    
    async def _handle_remove_stock(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle removing a stock"""
        ticker = params.get("ticker")
        
        if "watchlist" not in self.context or ticker not in self.context["watchlist"]:
            return {
                "status": "error",
                "message": f"Stock {ticker} not found in watchlist"
            }
        
        del self.context["watchlist"][ticker]
        
        return {
            "status": "success",
            "message": f"Removed {ticker} from watchlist"
        }
    
    async def _handle_update_thresholds(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle updating thresholds"""
        ticker = params.get("ticker")
        upper = params.get("upper")
        lower = params.get("lower")
        
        if "watchlist" not in self.context or ticker not in self.context["watchlist"]:
            return {
                "status": "error",
                "message": f"Stock {ticker} not found in watchlist"
            }
        
        self.context["watchlist"][ticker] = StockThreshold(upper=upper, lower=lower)
        
        return {
            "status": "success",
            "message": f"Updated thresholds for {ticker}",
            "data": {
                "ticker": ticker,
                "thresholds": {
                    "upper": upper,
                    "lower": lower
                }
            }
        }
    
    async def _handle_get_price_history(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle getting price history"""
        # Simulate price history data
        return {
            "status": "success",
            "data": {
                "ticker": params.get("ticker"),
                "prices": [
                    {"timestamp": datetime.now().isoformat(), "price": 150.0},
                    {"timestamp": datetime.now().isoformat(), "price": 151.0}
                ]
            }
        }
    
    async def _handle_get_alert_history(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle getting alert history"""
        # Simulate alert history data
        return {
            "status": "success",
            "data": {
                "alerts": [
                    {
                        "ticker": "AAPL",
                        "alert_type": "upper",
                        "price": 200.0,
                        "threshold": 195.0,
                        "timestamp": datetime.now().isoformat()
                    }
                ]
            }
        }

async def run_tests():
    """Run a series of tests to verify MCP functionality"""
    client = MockLLMClient()
    
    # Test 1: Add a stock
    print("\nTest 1: Adding a stock")
    result = await client.process_command("add_stock", {
        "ticker": "AAPL",
        "upper": 200.0,
        "lower": 150.0
    })
    print(json.dumps(result, indent=2))
    
    # Test 2: Update thresholds
    print("\nTest 2: Updating thresholds")
    result = await client.process_command("update_thresholds", {
        "ticker": "AAPL",
        "upper": 210.0,
        "lower": 160.0
    })
    print(json.dumps(result, indent=2))
    
    # Test 3: Get price history
    print("\nTest 3: Getting price history")
    result = await client.process_command("get_price_history", {
        "ticker": "AAPL",
        "start_date": datetime.now().isoformat(),
        "end_date": datetime.now().isoformat()
    })
    print(json.dumps(result, indent=2))
    
    # Test 4: Get alert history
    print("\nTest 4: Getting alert history")
    result = await client.process_command("get_alert_history", {
        "ticker": "AAPL",
        "start_date": datetime.now().isoformat(),
        "end_date": datetime.now().isoformat()
    })
    print(json.dumps(result, indent=2))
    
    # Test 5: Remove stock
    print("\nTest 5: Removing a stock")
    result = await client.process_command("remove_stock", {
        "ticker": "AAPL"
    })
    print(json.dumps(result, indent=2))
    
    # Test 6: Invalid action
    print("\nTest 6: Invalid action")
    result = await client.process_command("invalid_action", {})
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    asyncio.run(run_tests()) 