#!/usr/bin/env python3
"""
Database Schema Update Script
Adds catatan_followup column to leads table if it doesn't exist
"""

import os

def update_database_schema():
    """Update database schema to add catatan_followup column"""
    db_path = os.path.join('data', 'leads.db (SQLite - removed))
    
    # Ensure database directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    try:
        conn = # SQLite connection removed
        cursor = conn.cursor()
        
        # Check if catatan_followup column exists
        # cursor.execute() removed"PRAGMA table_info(leads)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'catatan_followup' not in columns:
            print("🔧 Adding catatan_followup column to leads table...")
            
            # Add the column
            # cursor.execute() removed'''
                ALTER TABLE leads 
                ADD COLUMN catatan_followup TEXT
            ''')
            
            # conn.commit() removed
            print("✅ catatan_followup column added successfully")
        else:
            print("✅ catatan_followup column already exists")
        
        # Verify the column was added
        # cursor.execute() removed"PRAGMA table_info(leads)")
        updated_columns = [column[1] for column in cursor.fetchall()]
        
        if 'catatan_followup' in updated_columns:
            print("✅ Database schema updated successfully")
            return True
        else:
            print("❌ Failed to add catatan_followup column")
            return False
            
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    finally:
        if 'conn' in locals():
            # conn.close() removed

if __name__ == "__main__":
    print("🚀 Database Schema Update")
    print("=" * 40)
    
    if update_database_schema():
        print("\n🎉 Database schema update completed!")
        print("You can now run the inbox API test script.")
    else:
        print("\n❌ Database schema update failed!")
        exit(1)
