"""
LUMINA OS Server Runner with Automatic Backup
Enhanced server startup with backup integration

Author: HUNTER_AGENT_AI_MARKETING_DIGITAL
Version: 1.0.0
"""

import os
import sys
import signal
import atexit
import time
from datetime import datetime

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lumina_os.core_modules.config import config
from scripts.backup_db import DatabaseBackup

class ServerWithBackup:
    """Server runner with automatic backup functionality"""
    
    def __init__(self):
        self.backup_system = DatabaseBackup()
        self.server_process = None
        self.backup_on_shutdown = config.AUTO_BACKUP
        
        # Register shutdown handlers
        atexit.register(self._shutdown_handler)
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def start_server(self):
        """Start LUMINA OS server with backup integration"""
        print("🚀 LUMINA OS Property Intelligence System")
        print("📊 Advanced Analytics & Strategic Insights")
        print("💾 Enhanced with Automatic Backup System")
        print()
        
        # Create startup backup
        self._create_startup_backup()
        
        # Start Flask server
        print("🌐 Starting LUMINA OS Server...")
        print(f"📍 Server: http://{config.HOST}:{config.PORT}")
        print(f"📈 Dashboard: http://{config.HOST}:{config.PORT}/")
        print(f"🔧 API Test: http://{config.HOST}:{config.PORT}/api/test")
        print()
        
        try:
            # Import and run Flask app
            from lumina_os.app import app
            
            print("✅ Server ready! Press Ctrl+C to stop.")
            print("💾 Automatic backup will be created on shutdown.")
            print()
            
            # Start server
            app.run(
                host=config.HOST,
                port=config.PORT,
                debug=config.FLASK_DEBUG
            )
            
        except KeyboardInterrupt:
            print("\n🛑 Server stopped by user")
        except Exception as e:
            print(f"❌ Server error: {str(e)}")
        finally:
            self._shutdown_handler()
    
    def _create_startup_backup(self):
        """Create backup when server starts"""
        try:
            print("💾 Creating startup backup...")
            success = self.backup_system.create_backup("startup")
            
            if success:
                print("✅ Startup backup created successfully")
            else:
                print("⚠️ Startup backup failed (server will continue)")
                
        except Exception as e:
            print(f"⚠️ Startup backup error: {str(e)}")
    
    def _shutdown_handler(self):
        """Handle server shutdown with backup"""
        if self.backup_on_shutdown:
            try:
                print("\n💾 Creating shutdown backup...")
                success = self.backup_system.create_backup("shutdown")
                
                if success:
                    print("✅ Shutdown backup created successfully")
                    
                    # Show backup stats
                    stats = self.backup_system.get_backup_stats()
                    print(f"📊 Total backups: {stats['total_backups']}")
                    print(f"💾 Total size: {stats['total_size_mb']} MB")
                else:
                    print("⚠️ Shutdown backup failed")
                    
            except Exception as e:
                print(f"⚠️ Shutdown backup error: {str(e)}")
        
        print("👋 LUMINA OS Server stopped")
    
    def _signal_handler(self, signum, frame):
        """Handle system signals"""
        print(f"\n📡 Received signal {signum}")
        self._shutdown_handler()
        sys.exit(0)
    
    def create_manual_backup(self, custom_name=None):
        """Create manual backup on demand"""
        print("💾 Creating manual backup...")
        
        if not custom_name:
            custom_name = f"manual_{datetime.now().strftime('%H%M')}"
        
        success = self.backup_system.create_backup(custom_name)
        
        if success:
            print("✅ Manual backup created successfully")
            
            # Show recent backups
            backups = self.backup_system.list_backups()[:3]
            if backups:
                print("\n📋 Recent Backups:")
                for backup in backups:
                    print(f"  📁 {backup['filename']} ({backup['size_mb']} MB)")
        else:
            print("❌ Manual backup failed")
    
    def show_backup_status(self):
        """Show backup system status"""
        print("📊 LUMINA OS Backup System Status")
        print("=" * 50)
        
        stats = self.backup_system.get_backup_stats()
        
        print(f"📁 Total Backups: {stats['total_backups']}")
        print(f"💾 Total Size: {stats['total_size_mb']} MB")
        print(f"📅 Latest Backup: {stats['latest_backup']}")
        print(f"📅 Oldest Backup: {stats['oldest_backup']}")
        print(f"🔧 Auto Backup: {'Enabled' if self.backup_on_shutdown else 'Disabled'}")
        print(f"📂 Backup Folder: {config.BACKUP_FOLDER}")
        print(f"🗄️ Database: {config.DATABASE_PATH}")
        
        # Show recent backups
        backups = self.backup_system.list_backups()[:5]
        if backups:
            print("\n📋 Recent Backups:")
            for backup in backups:
                print(f"  📁 {backup['filename']}")
                print(f"     📅 {backup['created']} | 💾 {backup['size_mb']} MB")

def main():
    """Main function with command line options"""
    import argparse
    
    parser = argparse.ArgumentParser(description='LUMINA OS Server with Backup System')
    parser.add_argument('--no-backup', action='store_true', 
                       help='Disable automatic backup on shutdown')
    parser.add_argument('--backup-only', action='store_true',
                       help='Create manual backup only')
    parser.add_argument('--backup-name', help='Custom backup name')
    parser.add_argument('--backup-status', action='store_true',
                       help='Show backup system status')
    
    args = parser.parse_args()
    
    server = ServerWithBackup()
    
    if args.no_backup:
        server.backup_on_shutdown = False
        print("⚠️ Automatic backup disabled")
    
    if args.backup_status:
        server.show_backup_status()
        return
    
    if args.backup_only:
        server.create_manual_backup(args.backup_name)
        return
    
    # Start server normally
    server.start_server()

if __name__ == "__main__":
    main()
