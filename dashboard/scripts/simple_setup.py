#!/usr/bin/env python3
"""
Simple database setup for background services
"""

import os
from datetime import datetime

def setup_analytics_db():
    """Setup analytics database with basic tables"""
    db_path = os.path.join('..', 'data', 'analytics.db (SQLite - removed))
    
    try:
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        conn = # SQLite connection removed
        cursor = conn.cursor()
        
        print("Creating market_data table...")
        # cursor.execute() removed'''
            CREATE TABLE IF NOT EXISTS market_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                property_type TEXT NOT NULL,
                location TEXT NOT NULL,
                price_min REAL,
                price_max REAL,
                price_avg REAL,
                competitor TEXT NOT NULL,
                listing_count INTEGER DEFAULT 1,
                price_per_meter REAL,
                area_range TEXT,
                facilities TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        print("Creating price_analysis table...")
        # cursor.execute() removed'''
            CREATE TABLE IF NOT EXISTS price_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                location TEXT NOT NULL,
                property_type TEXT NOT NULL,
                avg_price REAL NOT NULL,
                price_trend TEXT,
                market_gap_percent REAL,
                competitor_count INTEGER,
                analysis_date DATE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # conn.commit() removed
        # conn.close() removed
        
        print("✅ Analytics database setup completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    setup_analytics_db()
