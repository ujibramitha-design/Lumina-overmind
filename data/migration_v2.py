#!/usr/bin/env python3
"""
DATABASE LAYER MIGRATION V2 - ELITE HUNTER
Executive Blueprint Database Architecture Upgrade

Author: HUNTER_AGENT_AI_MARKETING_DIGITAL
Version: 2.0.0
"""

import logging
import json
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ANSI Color Codes for hacker-style logging
GREEN = '\033[92m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
RED = '\033[91m'
MAGENTA = '\033[95m'
BOLD = '\033[1m'
END = '\033[0m'

class DatabaseMigrationV2:
    """
    Elite Hunter Database Migration System
    Advanced database architecture upgrade with SQLite compatibility
    """
    
    def __init__(self):
        """Initialize migration system"""
        self.logger = logging.getLogger(__name__)
        
        # Database configuration
        self.db_path = 'data/database/leads.db (SQLite - removed)
        self.backup_path = f'data/database/leads_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db (SQLite - removed)
        
        # Migration configuration
        self.migration_config = {
            'version': '2.0.0',
            'create_backup': True,
            'verify_integrity': True,
            'force_migration': False
        }
        
        # New columns for leads table
        self.new_columns = {
            'intent_category': 'TEXT DEFAULT "Informational"',
            'contact_info': 'TEXT',
            'entities_extracted': 'TEXT',
            'behavioral_signals': 'TEXT',
            'urgency_score': 'INTEGER DEFAULT 0',
            'data_quality_score': 'INTEGER DEFAULT 0',
            'metadata': 'TEXT'
        }
        
        # Satellite tables definitions
        self.satellite_tables = {
            'scoring_log': '''
                CREATE TABLE IF NOT EXISTS scoring_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    lead_id INTEGER NOT NULL,
                    score INTEGER NOT NULL,
                    analysis_type TEXT DEFAULT 'traditional',
                    llm_response TEXT,
                    intent_category TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (lead_id) REFERENCES leads(id) ON DELETE CASCADE
                )
            ''',
            'alerts': '''
                CREATE TABLE IF NOT EXISTS alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    alert_type TEXT NOT NULL,
                    alert_priority TEXT DEFAULT 'medium',
                    title TEXT NOT NULL,
                    message TEXT NOT NULL,
                    delivery_status TEXT DEFAULT 'pending',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    delivered_at DATETIME,
                    error_message TEXT
                )
            ''',
            'ai_logs': '''
                CREATE TABLE IF NOT EXISTS ai_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ai_model TEXT NOT NULL,
                    processing_type TEXT NOT NULL,
                    input_tokens INTEGER DEFAULT 0,
                    output_tokens INTEGER DEFAULT 0,
                    processing_time_ms INTEGER DEFAULT 0,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    request_data TEXT,
                    response_data TEXT,
                    error_message TEXT
                )
            '''
        }
        
        # Performance indexes
        self.indexes = {
            'idx_leads_score_status': 'CREATE INDEX IF NOT EXISTS idx_leads_score_status ON leads(score, status)',
            'idx_leads_intent_category': 'CREATE INDEX IF NOT EXISTS idx_leads_intent_category ON leads(intent_category)',
            'idx_leads_urgency_score': 'CREATE INDEX IF NOT EXISTS idx_leads_urgency_score ON leads(urgency_score)',
            'idx_leads_data_quality': 'CREATE INDEX IF NOT EXISTS idx_leads_data_quality ON leads(data_quality_score)',
            'idx_leads_created_at': 'CREATE INDEX IF NOT EXISTS idx_leads_created_at ON leads(created_at)',
            'idx_scoring_lead_id': 'CREATE INDEX IF NOT EXISTS idx_scoring_lead_id ON scoring_log(lead_id)',
            'idx_scoring_timestamp': 'CREATE INDEX IF NOT EXISTS idx_scoring_timestamp ON scoring_log(timestamp)',
            'idx_alerts_type_status': 'CREATE INDEX IF NOT EXISTS idx_alerts_type_status ON alerts(alert_type, delivery_status)',
            'idx_alerts_created_at': 'CREATE INDEX IF NOT EXISTS idx_alerts_created_at ON alerts(created_at)',
            'idx_ai_logs_model_type': 'CREATE INDEX IF NOT EXISTS idx_ai_logs_model_type ON ai_logs(ai_model, processing_type)',
            'idx_ai_logs_timestamp': 'CREATE INDEX IF NOT EXISTS idx_ai_logs_timestamp ON ai_logs(timestamp)'
        }
        
        print(f"{GREEN}🗄️ DATABASE MIGRATION V2 INITIATED{END}")
        print(f"{CYAN}├── Migration Version: {self.migration_config['version']}{END}")
        print(f"{CYAN}├── Database Path: {self.db_path}{END}")
        print(f"{CYAN}├── Backup Path: {self.backup_path}{END}")
        print(f"{CYAN}├── New Columns: {len(self.new_columns)}{END}")
        print(f"{CYAN}├── Satellite Tables: {len(self.satellite_tables)}{END}")
        print(f"{CYAN}├── Performance Indexes: {len(self.indexes)}{END}")
        print(f"{CYAN}├── Timestamp: {datetime.now().isoformat()}{END}")
    
    def execute_migration(self) -> bool:
        """
        Execute complete database migration
        
        Returns:
            True if migration successful, False otherwise
        """
        try:
            print(f"{GREEN}🚀 EXECUTING DATABASE MIGRATION{END}")
            
            # Step 1: Create backup
            if self.migration_config['create_backup']:
                self._create_backup()
            
            # Step 2: Connect to database
            conn = self._connect_database()
            
            # Step 3: Create leads table if not exists
            self._create_leads_table_if_not_exists(conn)
            
            # Step 4: Upgrade leads table
            self._upgrade_leads_table(conn)
            
            # Step 5: Create satellite tables
            self._create_satellite_tables(conn)
            
            # Step 6: Create performance indexes
            self._create_performance_indexes(conn)
            
            # Step 7: Verify migration
            if self.migration_config['verify_integrity']:
                self._verify_migration(conn)
            
            # Step 8: Update migration metadata
            self._update_migration_metadata(conn)
            
            # conn.close() removed
            
            print(f"{GREEN}✅ DATABASE MIGRATION COMPLETED{END}")
            print(f"{CYAN}├── Database: {self.db_path}{END}")
            print(f"{CYAN}├── Version: {self.migration_config['version']}{END}")
            print(f"{CYAN}├── Tables: Upgraded successfully{END}")
            print(f"{CYAN}├── Indexes: Created for performance{END}")
            print(f"{GREEN}└── Status: Migration completed successfully{END}")
            
            return True
            
        except Exception as e:
            print(f"{RED}❌ DATABASE MIGRATION FAILED{END}")
            print(f"{RED}├── Error: {e}{END}")
            print(f"{RED}└── Status: Migration failed{END}")
            self.logger.error(f"Database migration failed: {e}")
            return False
    
    def _connect_database(self) -> sqlite3.Connection:
        """
        Connect to SQLite database
        
        Returns:
            Database connection object
        """
        try:
            # Ensure data directory exists
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            
            # Connect to database
            conn = # SQLite connection removed
            conn.row_factory = sqlite3.Row  # Enable dict-like access
            
            # Enable foreign keys
            conn.execute('PRAGMA foreign_keys = ON')
            
            # Set journal mode to WAL for better performance
            conn.execute('PRAGMA journal_mode = WAL')
            
            # Enable synchronous mode for safety
            conn.execute('PRAGMA synchronous = NORMAL')
            
            print(f"{CYAN}├── Database connected: {self.db_path}{END}")
            return conn
            
        except Exception as e:
            error_msg = f"Failed to connect to database: {e}"
            print(f"{RED}❌ {error_msg}{END}")
            raise
    
    def _create_backup(self) -> None:
        """
        Create backup of existing database
        """
        try:
            if os.path.exists(self.db_path):
                import shutil
                shutil.copy2(self.db_path, self.backup_path)
                print(f"{GREEN}├── Backup created: {self.backup_path}{END}")
            else:
                print(f"{YELLOW}├── No existing database to backup{END}")
                
        except Exception as e:
            print(f"{YELLOW}⚠️ Backup failed (continuing): {e}{END}")
    
    def _create_leads_table_if_not_exists(self, conn: sqlite3.Connection) -> None:
        """
        Create leads table with complete schema if not exists
        """
        try:
            cursor = conn.cursor()
            
            print(f"{CYAN}├── Creating leads table if not exists...{END}")
            
            # Create complete leads table with all columns
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS leads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    content_snippet TEXT,
                    score INTEGER DEFAULT 1,
                    source TEXT DEFAULT 'DuckDuckGo',
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'new',
                    competitor_price REAL,
                    lead_type TEXT DEFAULT 'unknown',
                    location TEXT DEFAULT 'unknown',
                    query_used TEXT,
                    contact_info TEXT,  -- JSON string
                    urgency_score INTEGER DEFAULT 0,
                    potential_value TEXT,
                    data_quality_score INTEGER DEFAULT 0,
                    metadata TEXT,  -- JSON string
                    behavioral_signals TEXT,  -- JSON string
                    system_info TEXT,  -- JSON string
                    entity_data TEXT,  -- JSON string for extracted entities
                    intent_category TEXT DEFAULT 'Informational',  -- Intent classification
                    is_trend BOOLEAN DEFAULT 0,  -- Trend flag
                    validation_status TEXT DEFAULT 'pending',
                    nama TEXT,  -- Lead name
                    no_hp TEXT,  -- Phone number
                    email TEXT,  -- Email address
                    pekerjaan TEXT,  -- Job/profession
                    sumber TEXT,  -- Source
                    catatan TEXT,  -- Notes
                    skor_akhir REAL DEFAULT 0,  -- Final score
                    kategori TEXT DEFAULT 'Cold',  -- Category (Hot/Warm/Cold)
                    catatan_followup TEXT,  -- Follow-up notes
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            print(f"{GREEN}├── Leads table created/verified{END}")
            
        except Exception as e:
            print(f"{RED}❌ Failed to create leads table: {e}{END}")
            raise
    
    def _upgrade_leads_table(self, conn: sqlite3.Connection) -> None:
        """
        Upgrade leads table with new columns
        """
        try:
            cursor = conn.cursor()
            
            print(f"{CYAN}├── Upgrading leads table...{END}")
            
            # Get current table schema
            # cursor.execute() removed"PRAGMA table_info(leads)")
            existing_columns = {row['name'] for row in cursor.fetchall()}
            
            # Add new columns if they don't exist
            for column_name, column_def in self.new_columns.items():
                if column_name not in existing_columns:
                    try:
                        alter_sql = f"ALTER TABLE leads ADD COLUMN {column_name} {column_def}"
                        # cursor.execute() removedalter_sql)
                        print(f"{GREEN}│   ✅ Added column: {column_name}{END}")
                    except sqlite3.OperationalError as e:
                        if "duplicate column name" in str(e).lower():
                            print(f"{YELLOW}│   ⚠️ Column exists: {column_name}{END}")
                        else:
                            raise
                else:
                    print(f"{YELLOW}│   ⚠️ Column exists: {column_name}{END}")
            
            # conn.commit() removed
            print(f"{GREEN}├── Leads table upgraded successfully{END}")
            
        except Exception as e:
            print(f"{RED}❌ Failed to upgrade leads table: {e}{END}")
            raise
    
    def _create_satellite_tables(self, conn: sqlite3.Connection) -> None:
        """
        Create satellite tables for advanced functionality
        """
        try:
            cursor = conn.cursor()
            
            print(f"{CYAN}├── Creating satellite tables...{END}")
            
            for table_name, table_sql in self.satellite_tables.items():
                try:
                    # cursor.execute() removedtable_sql)
                    print(f"{GREEN}│   ✅ Created table: {table_name}{END}")
                except sqlite3.Error as e:
                    print(f"{RED}│   ❌ Failed to create {table_name}: {e}{END}")
                    raise
            
            # conn.commit() removed
            print(f"{GREEN}├── Satellite tables created successfully{END}")
            
        except Exception as e:
            print(f"{RED}❌ Failed to create satellite tables: {e}{END}")
            raise
    
    def _create_performance_indexes(self, conn: sqlite3.Connection) -> None:
        """
        Create performance indexes for optimized queries
        """
        try:
            cursor = conn.cursor()
            
            print(f"{CYAN}├── Creating performance indexes...{END}")
            
            for index_name, index_sql in self.indexes.items():
                try:
                    # cursor.execute() removedindex_sql)
                    print(f"{GREEN}│   ✅ Created index: {index_name}{END}")
                except sqlite3.Error as e:
                    print(f"{YELLOW}│   ⚠️ Index exists: {index_name}{END}")
            
            # conn.commit() removed
            print(f"{GREEN}├── Performance indexes created successfully{END}")
            
        except Exception as e:
            print(f"{RED}❌ Failed to create performance indexes: {e}{END}")
            raise
    
    def _verify_migration(self, conn: sqlite3.Connection) -> None:
        """
        Verify migration integrity
        """
        try:
            cursor = conn.cursor()
            
            print(f"{CYAN}├── Verifying migration integrity...{END}")
            
            # Check leads table structure
            # cursor.execute() removed"PRAGMA table_info(leads)")
            leads_columns = {row['name'] for row in cursor.fetchall()}
            
            missing_columns = set(self.new_columns.keys()) - set(leads_columns)
            if missing_columns:
                raise Exception(f"Missing columns in leads table: {missing_columns}")
            
            # Check satellite tables
            for table_name in self.satellite_tables.keys():
                # cursor.execute() removedf"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
                if not cursor.fetchone():
                    raise Exception(f"Missing satellite table: {table_name}")
            
            # Check indexes
            for index_name in self.indexes.keys():
                # cursor.execute() removedf"SELECT name FROM sqlite_master WHERE type='index' AND name='{index_name}'")
                if not cursor.fetchone():
                    print(f"{YELLOW}│   ⚠️ Missing index: {index_name}{END}")
            
            print(f"{GREEN}├── Migration integrity verified{END}")
            
        except Exception as e:
            print(f"{RED}❌ Migration verification failed: {e}{END}")
            raise
    
    def _update_migration_metadata(self, conn: sqlite3.Connection) -> None:
        """
        Update migration metadata
        """
        try:
            cursor = conn.cursor()
            
            # Create migration metadata table if not exists
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS migration_metadata (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    version TEXT NOT NULL,
                    migration_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    description TEXT,
                    status TEXT DEFAULT 'completed'
                )
            ''')
            
            # Insert migration record
            # cursor.execute() removed'''
                INSERT INTO migration_metadata (version, description, status)
                VALUES (?, ?, ?)
            ''', (
                self.migration_config['version'],
                'DATABASE LAYER MIGRATION V2 - ELITE HUNTER',
                'completed'
            ))
            
            # conn.commit() removed
            print(f"{GREEN}├── Migration metadata updated{END}")
            
        except Exception as e:
            print(f"{YELLOW}⚠️ Failed to update migration metadata: {e}{END}")
    
    def rollback_migration(self) -> bool:
        """
        Rollback migration to previous state
        
        Returns:
            True if rollback successful, False otherwise
        """
        try:
            print(f"{YELLOW}🔄 ROLLING BACK DATABASE MIGRATION{END}")
            
            # Restore from backup if exists
            if os.path.exists(self.backup_path):
                import shutil
                shutil.copy2(self.backup_path, self.db_path)
                print(f"{GREEN}✅ Database restored from backup{END}")
                return True
            else:
                print(f"{RED}❌ No backup found for rollback{END}")
                return False
                
        except Exception as e:
            print(f"{RED}❌ Rollback failed: {e}{END}")
            return False
    
    def get_migration_status(self) -> Dict[str, Any]:
        """
        Get current migration status
        
        Returns:
            Dictionary with migration status information
        """
        try:
            conn = self._connect_database()
            cursor = conn.cursor()
            
            # Check if migration metadata table exists
            # cursor.execute() removed"SELECT name FROM sqlite_master WHERE type='table' AND name='migration_metadata'")
            if cursor.fetchone():
                # cursor.execute() removed"SELECT * FROM migration_metadata ORDER BY id DESC LIMIT 1")
                migration = cursor.fetchone()
                
                return {
                    'version': migration['version'],
                    'migration_date': migration['migration_date'],
                    'description': migration['description'],
                    'status': migration['status'],
                    'database_exists': os.path.exists(self.db_path),
                    'backup_exists': os.path.exists(self.backup_path)
                }
            else:
                return {
                    'version': '1.0.0',
                    'migration_date': None,
                    'description': 'Original database',
                    'status': 'pre-migration',
                    'database_exists': os.path.exists(self.db_path),
                    'backup_exists': os.path.exists(self.backup_path)
                }
                
        except Exception as e:
            return {
                'error': str(e),
                'version': 'unknown',
                'status': 'error'
            }
        finally:
            if 'conn' in locals():
                # conn.close() removed

def main():
    """
    Main function to execute database migration
    """
    print("🗄️ DATABASE LAYER MIGRATION V2 - ELITE HUNTER")
    print("=" * 80)
    print("🔐 Executive Blueprint Database Architecture Upgrade")
    print("=" * 80)
    
    # Initialize migration
    migration = DatabaseMigrationV2()
    
    # Show current status
    print(f"\n📊 CURRENT DATABASE STATUS")
    print("-" * 40)
    status = migration.get_migration_status()
    
    if 'error' in status:
        print(f"❌ Error: {status['error']}")
    else:
        print(f"✅ Version: {status['version']}")
        print(f"✅ Status: {status['status']}")
        print(f"✅ Database: {'Exists' if status['database_exists'] else 'Not Found'}")
        print(f"✅ Backup: {'Exists' if status['backup_exists'] else 'Not Found'}")
    
    # Execute migration
    if status['version'] == '1.0.0' or status['status'] == 'pre-migration':
        print(f"\n🚀 STARTING MIGRATION")
        print("-" * 40)
        
        success = migration.execute_migration()
        
        if success:
            print(f"\n✅ MIGRATION COMPLETED SUCCESSFULLY")
            print(f"📊 New database version: {migration.migration_config['version']}")
            print(f"📊 Database path: {migration.db_path}")
            print(f"📊 Backup path: {migration.backup_path}")
        else:
            print(f"\n❌ MIGRATION FAILED")
            print(f"⚠️ Please check the error messages above")
    else:
        print(f"\n✅ DATABASE ALREADY UPGRADED")
        print(f"📊 Current version: {status['version']}")
    
    # Show final status
    print(f"\n📊 FINAL DATABASE STATUS")
    print("-" * 40)
    final_status = migration.get_migration_status()
    
    if 'error' not in final_status:
        print(f"✅ Version: {final_status['version']}")
        print(f"✅ Status: {final_status['status']}")
        print(f"✅ Migration Date: {final_status['migration_date']}")
        print(f"✅ Description: {final_status['description']}")
    
    print("\n" + "=" * 80)
    print("✅ DATABASE LAYER MIGRATION V2 COMPLETE")
    print("🔐 Elite Hunter database architecture ready")
    print("=" * 80)

if __name__ == "__main__":
    main()
