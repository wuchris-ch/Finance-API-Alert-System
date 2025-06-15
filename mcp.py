"""
Model Context Protocol (MCP) for Stock Price Alert System

This protocol defines how an LLM can interact with the stock price alert system.
It provides a structured interface for the LLM to understand and operate the system.
"""

from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from datetime import datetime
import json

@dataclass
class StockThreshold:
    upper: Optional[float]
    lower: Optional[float]

@dataclass
class StockAlert:
    ticker: str
    alert_type: str  # "upper" or "lower"
    price: float
    threshold: float
    timestamp: datetime

class StockAlertMCP:
    """
    Model Context Protocol for Stock Price Alert System
    """
    
    def __init__(self):
        self.system_description = """
        A stock price monitoring system that tracks stocks and sends alerts when prices cross defined thresholds.
        The system uses Yahoo Finance API for real-time data and supports multiple notification channels.
        """
        
        self.capabilities = {
            "monitor_stocks": "Track stock prices in real-time",
            "set_thresholds": "Configure price thresholds for alerts",
            "send_alerts": "Send notifications when thresholds are crossed",
            "view_history": "Access price and alert history",
            "demo_mode": "Test system with mock data"
        }
        
        self.data_structures = {
            "StockThreshold": {
                "upper": "Optional[float] - Upper price threshold",
                "lower": "Optional[float] - Lower price threshold"
            },
            "StockAlert": {
                "ticker": "str - Stock symbol",
                "alert_type": "str - Type of alert (upper/lower)",
                "price": "float - Current price",
                "threshold": "float - Threshold that was crossed",
                "timestamp": "datetime - When alert was triggered"
            }
        }
        
        self.available_actions = {
            "add_stock": {
                "description": "Add a new stock to monitor",
                "parameters": {
                    "ticker": "str - Stock symbol",
                    "upper": "Optional[float] - Upper threshold",
                    "lower": "Optional[float] - Lower threshold"
                }
            },
            "remove_stock": {
                "description": "Remove a stock from monitoring",
                "parameters": {
                    "ticker": "str - Stock symbol"
                }
            },
            "update_thresholds": {
                "description": "Update price thresholds for a stock",
                "parameters": {
                    "ticker": "str - Stock symbol",
                    "upper": "Optional[float] - New upper threshold",
                    "lower": "Optional[float] - New lower threshold"
                }
            },
            "get_price_history": {
                "description": "Retrieve price history for a stock",
                "parameters": {
                    "ticker": "str - Stock symbol",
                    "start_date": "Optional[datetime] - Start date",
                    "end_date": "Optional[datetime] - End date"
                }
            },
            "get_alert_history": {
                "description": "Retrieve alert history",
                "parameters": {
                    "ticker": "Optional[str] - Filter by stock symbol",
                    "start_date": "Optional[datetime] - Start date",
                    "end_date": "Optional[datetime] - End date"
                }
            }
        }
        
        self.error_handling = {
            "invalid_ticker": "Stock symbol not found or invalid",
            "invalid_threshold": "Threshold value must be positive",
            "database_error": "Error accessing or updating database",
            "api_error": "Error fetching data from Yahoo Finance",
            "notification_error": "Error sending notification"
        }
        
        self.context_management = {
            "maintain_watchlist": "Keep track of monitored stocks",
            "track_thresholds": "Remember price thresholds for each stock",
            "log_alerts": "Record all triggered alerts",
            "store_price_history": "Maintain historical price data"
        }
    
    def to_json(self) -> str:
        """Convert MCP to JSON format for LLM consumption"""
        return json.dumps({
            "system_description": self.system_description,
            "capabilities": self.capabilities,
            "data_structures": self.data_structures,
            "available_actions": self.available_actions,
            "error_handling": self.error_handling,
            "context_management": self.context_management
        }, indent=2)
    
    def validate_action(self, action: str, parameters: Dict) -> bool:
        """Validate if an action and its parameters are valid"""
        if action not in self.available_actions:
            return False
        
        required_params = self.available_actions[action]["parameters"]
        for param in required_params:
            if param not in parameters:
                return False
        
        return True
    
    def format_alert(self, alert: StockAlert) -> str:
        """Format an alert message for the LLM"""
        return f"""
        Alert: {alert.ticker} {alert.alert_type} threshold crossed
        Current Price: ${alert.price:.2f}
        Threshold: ${alert.threshold:.2f}
        Time: {alert.timestamp}
        """
    
    def get_system_status(self) -> Dict:
        """Get current system status for context"""
        return {
            "monitored_stocks": [],  # To be populated from actual system
            "active_alerts": [],     # To be populated from actual system
            "last_update": datetime.now()
        }

# Example usage
if __name__ == "__main__":
    mcp = StockAlertMCP()
    print(mcp.to_json()) 