"""
Database management for the API Alert System
"""

import psycopg2
from psycopg2.extras import DictCursor
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages database connections and operations for the alert system"""
    
    def __init__(self, host: str, port: str, database: str, user: str, password: str):
        """Initialize database connection parameters"""
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None
        
    def connect(self):
        """Create a new database connection"""
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            self.cursor = self.connection.cursor()
            logger.info("Database connection established")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        logger.info("Database connection closed")
    
    def init_tables(self):
        """Initialize database tables if they don't exist"""
        try:
            # Create price_history table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS price_history (
                    id          SERIAL PRIMARY KEY,
                    ticker      VARCHAR(10) NOT NULL,
                    fetched_at  TIMESTAMP NOT NULL,
                    price       DECIMAL(10,2) NOT NULL
                )
            """)
            
            # Create alert_history table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS alert_history (
                    id          SERIAL PRIMARY KEY,
                    ticker      VARCHAR(10) NOT NULL,
                    alert_type  VARCHAR(10) NOT NULL,
                    price       DECIMAL(10,2) NOT NULL,
                    threshold   DECIMAL(10,2) NOT NULL,
                    sent_at     TIMESTAMP NOT NULL
                )
            """)
            
            self.connection.commit()
            logger.info("Database tables initialized")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize tables: {e}")
            return False
    
    def insert_price(self, ticker: str, price: float, timestamp: datetime = None):
        """Insert a new price record"""
        if timestamp is None:
            timestamp = datetime.utcnow()
        
        try:
            self.cursor.execute(
                "INSERT INTO price_history (ticker, fetched_at, price) VALUES (%s, %s, %s)",
                (ticker, timestamp, price)
            )
            self.connection.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to insert price for {ticker}: {e}")
            return False
    
    def insert_alert(self, ticker: str, alert_type: str, price: float, threshold: float, timestamp: datetime = None):
        """Insert a new alert record"""
        if timestamp is None:
            timestamp = datetime.utcnow()
        
        try:
            self.cursor.execute(
                "INSERT INTO alert_history (ticker, alert_type, price, threshold, sent_at) VALUES (%s, %s, %s, %s, %s)",
                (ticker, alert_type, price, threshold, timestamp)
            )
            self.connection.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to insert alert for {ticker}: {e}")
            return False
    
    def get_recent_prices(self, ticker: str = None, limit: int = 10) -> List[Dict]:
        """Get recent price history"""
        try:
            if ticker:
                self.cursor.execute(
                    "SELECT ticker, fetched_at, price FROM price_history WHERE ticker = %s ORDER BY fetched_at DESC LIMIT %s",
                    (ticker, limit)
                )
            else:
                self.cursor.execute(
                    "SELECT ticker, fetched_at, price FROM price_history ORDER BY fetched_at DESC LIMIT %s",
                    (limit,)
                )
            
            results = []
            for row in self.cursor.fetchall():
                results.append({
                    'ticker': row[0],
                    'fetched_at': row[1],
                    'price': float(row[2])
                })
            return results
        except Exception as e:
            logger.error(f"Failed to get recent prices: {e}")
            return []
    
    def get_recent_alerts(self, ticker: str = None, limit: int = 10) -> List[Dict]:
        """Get recent alert history"""
        try:
            if ticker:
                self.cursor.execute(
                    "SELECT ticker, alert_type, price, threshold, sent_at FROM alert_history WHERE ticker = %s ORDER BY sent_at DESC LIMIT %s",
                    (ticker, limit)
                )
            else:
                self.cursor.execute(
                    "SELECT ticker, alert_type, price, threshold, sent_at FROM alert_history ORDER BY sent_at DESC LIMIT %s",
                    (limit,)
                )
            
            results = []
            for row in self.cursor.fetchall():
                results.append({
                    'ticker': row[0],
                    'alert_type': row[1],
                    'price': float(row[2]),
                    'threshold': float(row[3]),
                    'sent_at': row[4]
                })
            return results
        except Exception as e:
            logger.error(f"Failed to get recent alerts: {e}")
            return []
    
    def get_latest_price(self, ticker: str) -> Optional[float]:
        """Get the latest price for a specific ticker"""
        try:
            self.cursor.execute(
                "SELECT price FROM price_history WHERE ticker = %s ORDER BY fetched_at DESC LIMIT 1",
                (ticker,)
            )
            result = self.cursor.fetchone()
            return float(result[0]) if result else None
        except Exception as e:
            logger.error(f"Failed to get latest price for {ticker}: {e}")
            return None
    
    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect() 