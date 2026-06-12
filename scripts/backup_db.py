"""
LUMINA OS Database Backup Script
Automated backup system with time-based file naming

Author: HUNTER_AGENT_AI_MARKETING_DIGITAL
Version: 1.0.0
"""

import os
import sys
import shutil
from datetime import datetime
import logging

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lumina_os.core_modules.config import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/backup.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DatabaseBackup:
    """Automated database backup system"""
    
    def __init__(self):
        self.db_path = config.DATABASE_PATH
        self.backup_folder = config.BACKUP_FOLDER
        self.max_backups = 30  # Keep last 30 backups
        
        # Ensure backup folder exists
        os.makedirs(self.backup_folder, exist_ok=True)
        os.makedirs('logs', exist_ok=True)
    
    def create_backup(self, custom_name=None):
        """Create database backup with timestamp"""
        try:
            # Generate backup filename
            if custom_name:
                filename = f"database_backup_{custom_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db (SQLite - removed)
            else:
                filename = f"database_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db (SQLite - removed)
            
            backup_path = os.path.join(self.backup_folder, filename)
            
            # Verify source database exists
            if not os.path.exists(self.db_path):
                logger.error(f"Source database not found: {self.db_path}")
                return False
            
            # Create backup
            logger.info(f"Creating backup: {filename}")
            
            # Method 1: Direct file copy (faster)
            shutil.copy2(self.db_path, backup_path)
            
            # Method 2: SQLite backup (more reliable for active databases)
            # self._sqlite_backup(backup_path)
            
            # Verify backup
            if self._verify_backup(backup_path):
                logger.info(f"Backup created successfully: {backup_path}")
                
                # Clean old backups
                self._cleanup_old_backups()
                
                # Log backup info
                self._log_backup_info(backup_path)
                
                return True
            else:
                logger.error("Backup verification failed")
                return False
                
        except Exception as e:
            logger.error(f"Backup creation failed: {str(e)}")
            return False
    
    def _sqlite_backup(self, backup_path):
        """Create backup using SQLite backup API (more reliable)"""
        try:
            source = # SQLite connection removed
            backup = # SQLite connection removed
            
            source.backup(backup)
            
            source.close()
            backup.close()
            
        except Exception as e:
            logger.error(f"SQLite backup failed: {str(e)}")
            raise
    
    def _verify_backup(self, backup_path):
        """Verify backup integrity"""
        try:
            # Check file exists and has content
            if not os.path.exists(backup_path) or os.path.getsize(backup_path) == 0:
                return False
            
            # Try to connect to backup database
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # Check if main table exists
            # cursor.execute() removed"SELECT name FROM sqlite_master WHERE type='table' AND name='leads'")
            result = cursor.fetchone()
            
            # conn.close() removed
            
            return result is not None
            
        except Exception as e:
            logger.error(f"Backup verification failed: {str(e)}")
            return False
    
    def _cleanup_old_backups(self):
        """Remove old backups to save space"""
        try:
            backup_files = []
            
            # Get all backup files
            for filename in os.listdir(self.backup_folder):
                if filename.startswith('database_backup_') and filename.endswith('.db (SQLite - removed)):
                    file_path = os.path.join(self.backup_folder, filename)
                    backup_files.append((file_path, os.path.getmtime(file_path)))
            
            # Sort by modification time (newest first)
            backup_files.sort(key=lambda x: x[1], reverse=True)
            
            # Remove old backups if we have more than max_backups
            if len(backup_files) > self.max_backups:
                for file_path, _ in backup_files[self.max_backups:]:
                    try:
                        os.remove(file_path)
                        logger.info(f"Removed old backup: {os.path.basename(file_path)}")
                    except Exception as e:
                        logger.error(f"Failed to remove old backup {file_path}: {str(e)}")
            
        except Exception as e:
            logger.error(f"Backup cleanup failed: {str(e)}")
    
    def _log_backup_info(self, backup_path):
        """Log backup information"""
        try:
            # Get file size
            file_size = os.path.getsize(backup_path)
            file_size_mb = file_size / (1024 * 1024)
            
            # Get database stats
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # Count records in leads table
            # cursor.execute() removed"SELECT COUNT(*) FROM leads")
            lead_count = cursor.fetchone()[0]
            
            # Get database size info
            # cursor.execute() removed"SELECT page_count * page_size as size FROM pragma_page_count(), pragma_page_size()")
            db_size_info = cursor.fetchone()
            
            # conn.close() removed
            
            logger.info(f"Backup Info - Size: {file_size_mb:.2f}MB, Records: {lead_count}")
            
        except Exception as e:
            logger.warning(f"Failed to log backup info: {str(e)}")
    
    def restore_backup(self, backup_filename):
        """Restore database from backup"""
        try:
            backup_path = os.path.join(self.backup_folder, backup_filename)
            
            if not os.path.exists(backup_path):
                logger.error(f"Backup file not found: {backup_filename}")
                return False
            
            # Verify backup before restore
            if not self._verify_backup(backup_path):
                logger.error(f"Backup verification failed: {backup_filename}")
                return False
            
            # Create current database backup before restore
            pre_restore_backup = f"pre_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db (SQLite - removed)
            if os.path.exists(self.db_path):
                shutil.copy2(self.db_path, os.path.join(self.backup_folder, pre_restore_backup))
                logger.info(f"Created pre-restore backup: {pre_restore_backup}")
            
            # Restore backup
            logger.info(f"Restoring from backup: {backup_filename}")
            shutil.copy2(backup_path, self.db_path)
            
            logger.info("Database restored successfully")
            return True
            
        except Exception as e:
            logger.error(f"Database restore failed: {str(e)}")
            return False
    
    def list_backups(self):
        """List all available backups"""
        try:
            backups = []
            
            for filename in os.listdir(self.backup_folder):
                if filename.startswith('database_backup_') and filename.endswith('.db (SQLite - removed)):
                    file_path = os.path.join(self.backup_folder, filename)
                    file_size = os.path.getsize(file_path)
                    file_size_mb = file_size / (1024 * 1024)
                    mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                    
                    backups.append({
                        'filename': filename,
                        'size_mb': round(file_size_mb, 2),
                        'created': mod_time.strftime('%Y-%m-%d %H:%M:%S'),
                        'path': file_path
                    })
            
            # Sort by creation time (newest first)
            backups.sort(key=lambda x: x['created'], reverse=True)
            
            return backups
            
        except Exception as e:
            logger.error(f"Failed to list backups: {str(e)}")
            return []
    
    def get_backup_stats(self):
        """Get backup statistics"""
        try:
            backups = self.list_backups()
            
            if not backups:
                return {
                    'total_backups': 0,
                    'total_size_mb': 0,
                    'latest_backup': None,
                    'oldest_backup': None
                }
            
            total_size = sum(b['size_mb'] for b in backups)
            
            return {
                'total_backups': len(backups),
                'total_size_mb': round(total_size, 2),
                'latest_backup': backups[0]['created'] if backups else None,
                'oldest_backup': backups[-1]['created'] if backups else None
            }
            
        except Exception as e:
            logger.error(f"Failed to get backup stats: {str(e)}")
            return {}

def main():
    """Main function for command line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='LUMINA OS Database Backup System')
    parser.add_argument('action', choices=['create', 'restore', 'list', 'stats'], 
                       help='Action to perform')
    parser.add_argument('--name', help='Custom backup name')
    parser.add_argument('--file', help='Backup filename for restore')
    
    args = parser.parse_args()
    
    backup_system = DatabaseBackup()
    
    if args.action == 'create':
        success = backup_system.create_backup(args.name)
        if success:
            print("✅ Backup created successfully")
        else:
            print("❌ Backup creation failed")
    
    elif args.action == 'restore':
        if not args.file:
            print("❌ Please specify backup filename with --file")
            return
        
        success = backup_system.restore_backup(args.file)
        if success:
            print("✅ Database restored successfully")
        else:
            print("❌ Database restore failed")
    
    elif args.action == 'list':
        backups = backup_system.list_backups()
        if backups:
            print(f"\n📋 Available Backups ({len(backups)}):")
            print("-" * 80)
            for backup in backups:
                print(f"📁 {backup['filename']}")
                print(f"   📅 Created: {backup['created']}")
                print(f"   💾 Size: {backup['size_mb']} MB")
                print()
        else:
            print("📭 No backups found")
    
    elif args.action == 'stats':
        stats = backup_system.get_backup_stats()
        print(f"\n📊 Backup Statistics:")
        print("-" * 40)
        print(f"📁 Total Backups: {stats['total_backups']}")
        print(f"💾 Total Size: {stats['total_size_mb']} MB")
        print(f"📅 Latest: {stats['latest_backup']}")
        print(f"📅 Oldest: {stats['oldest_backup']}")

if __name__ == "__main__":
    main()
