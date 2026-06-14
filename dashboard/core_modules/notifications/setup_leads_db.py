#!/usr/bin/env python3
"""
Setup leads database for WhatsApp Gateway testing
"""

import os

def setup_leads_database():
    """Create leads database with sample data"""
    db_path = os.path.join('..', 'data', 'leads.db (SQLite - removed))
    
    try:
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        conn = # SQLite connection removed
        cursor = conn.cursor()
        
        print("Creating leads table...")
        # cursor.execute() removed'''
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                business_name TEXT NOT NULL,
                contact TEXT,
                url TEXT,
                keywords TEXT,
                source TEXT DEFAULT 'web_scraping',
                score REAL DEFAULT 0.0,
                status TEXT DEFAULT 'new',
                location TEXT,
                date_found DATETIME DEFAULT CURRENT_TIMESTAMP,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                catatan_followup TEXT,
                message_sent_time TEXT
            )
        ''')
        
        # Insert sample data
        print("Adding sample leads...")
        sample_leads = [
            ('Test User 1', 'Phone: 628123456789, Email: test1@example.com', 'webhook_test_1', 'test', 'webhook', 85.0, 'Contacted', 'Serang'),
            ('Test User 2', 'Phone: 628223456789, Email: test2@example.com', 'webhook_test_2', 'test', 'webhook', 75.0, 'Contacted', 'Jakarta'),
            ('Test User 3', 'Phone: 628323456789, Email: test3@example.com', 'webhook_test_3', 'test', 'webhook', 90.0, 'New', 'Tangerang'),
        ]
        
        for lead in sample_leads:
            # cursor.execute() removed'''
                INSERT INTO leads (business_name, contact, url, keywords, source, score, status, location)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', lead)
        
        # conn.commit() removed
        # conn.close() removed
        
        print("✅ Leads database setup completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    setup_leads_database()
