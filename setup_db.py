#!/usr/bin/env python3
"""
Database setup script for the Stock Alert System.
This script creates the database and tables if they don't exist.
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import config
import sys

def create_database():
    """Create the database if it doesn't exist"""
    try:
        # Connect to PostgreSQL server
        conn = psycopg2.connect(
            host=config.POSTGRES_HOST,
            port=config.POSTGRES_PORT,
            user=config.POSTGRES_USER,
            password=config.POSTGRES_PASSWORD
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        # Check if database exists
        cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (config.POSTGRES_DB,))
        exists = cur.fetchone()
        
        if not exists:
            print(f"Creating database {config.POSTGRES_DB}...")
            cur.execute(f'CREATE DATABASE {config.POSTGRES_DB}')
            print("✅ Database created successfully!")
        else:
            print(f"✅ Database {config.POSTGRES_DB} already exists")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        sys.exit(1)

def create_tables():
    """Create the required tables if they don't exist"""
    try:
        # Connect to the database
        conn = psycopg2.connect(
            host=config.POSTGRES_HOST,
            port=config.POSTGRES_PORT,
            database=config.POSTGRES_DB,
            user=config.POSTGRES_USER,
            password=config.POSTGRES_PASSWORD
        )
        cur = conn.cursor()
        
        # Create price_history table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS price_history (
                id          SERIAL PRIMARY KEY,
                ticker      VARCHAR(10) NOT NULL,
                fetched_at  TIMESTAMP NOT NULL,
                price       DECIMAL(10,2) NOT NULL
            )
        """)
        
        # Create alert_history table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS alert_history (
                id          SERIAL PRIMARY KEY,
                ticker      VARCHAR(10) NOT NULL,
                alert_type  VARCHAR(10) NOT NULL,
                price       DECIMAL(10,2) NOT NULL,
                threshold   DECIMAL(10,2) NOT NULL,
                sent_at     TIMESTAMP NOT NULL
            )
        """)
        
        conn.commit()
        print("✅ Tables created successfully!")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("🚀 Setting up PostgreSQL database for Stock Alert System...")
    print("=" * 60)
    
    create_database()
    create_tables()
    
    print("\n✅ Database setup completed successfully!")
    print("You can now run the alert bot with: python alert_bot.py") 