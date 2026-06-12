"""
Enhanced Backup System with Cloud Storage Integration
Automated backup with S3, Google Drive, and local storage redundancy
"""

import os
import sys
import logging
import asyncio
import boto3
import json
import gzip
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.backup_db import DatabaseBackup

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/enhanced_backup.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class BackupConfig:
    """Backup configuration"""
    local_enabled: bool = True
    s3_enabled: bool = False
    gdrive_enabled: bool = False
    compression_enabled: bool = True
    encryption_enabled: bool = False
    retention_days: int = 30
    backup_frequency: str = "daily"  # daily, weekly, monthly

@dataclass
class BackupResult:
    """Backup operation result"""
    success: bool
    backup_type: str
    location: str
    file_size: int
    duration: float
    error_message: Optional[str] = None
    backup_path: Optional[str] = None

class EnhancedBackupSystem:
    """
    Enhanced backup system with multiple storage options
    Supports local, S3, and Google Drive backups
    """
    
    def __init__(self, config: BackupConfig = None):
        """Initialize enhanced backup system"""
        self.logger = logging.getLogger(__name__)
        self.config = config or BackupConfig()
        
        # Initialize backup components
        self.db_backup = DatabaseBackup()
        
        # Cloud storage clients
        self.s3_client = None
        self.gdrive_client = None
        
        # Initialize cloud clients
        self._initialize_cloud_clients()
        
        # Backup statistics
        self.backup_history: List[BackupResult] = []
        
        self.logger.info("🔄 Enhanced Backup System initialized")
        self.logger.info(f"📊 Storage options: Local={self.config.local_enabled}, S3={self.config.s3_enabled}, GDrive={self.config.gdrive_enabled}")
    
    def _initialize_cloud_clients(self):
        """Initialize cloud storage clients"""
        try:
            # Initialize S3 client
            if self.config.s3_enabled:
                aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
                aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
                aws_region = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
                s3_bucket = os.getenv('S3_BACKUP_BUCKET')
                
                if all([aws_access_key, aws_secret_key, s3_bucket]):
                    self.s3_client = boto3.client(
                        's3',
                        aws_access_key_id=aws_access_key,
                        aws_secret_access_key=aws_secret_key,
                        region_name=aws_region
                    )
                    self.s3_bucket = s3_bucket
                    self.logger.info("☁️ S3 client initialized")
                else:
                    self.logger.warning("⚠️ S3 credentials not configured")
            
            # Initialize Google Drive client
            if self.config.gdrive_enabled:
                # Google Drive API initialization would go here
                # For now, just log that it's not implemented
                self.logger.info("📁 Google Drive integration not yet implemented")
                
        except Exception as e:
            self.logger.error(f"❌ Cloud client initialization failed: {e}")
    
    async def create_comprehensive_backup(self, backup_name: str = None) -> List[BackupResult]:
        """
        Create comprehensive backup across all configured storage locations
        
        Args:
            backup_name: Custom backup name
            
        Returns:
            List[BackupResult]: Results from all backup locations
        """
        start_time = datetime.now()
        results = []
        
        # Generate backup name
        if not backup_name:
            backup_name = f"backup_{start_time.strftime('%Y%m%d_%H%M%S')}"
        
        self.logger.info(f"🚀 Starting comprehensive backup: {backup_name}")
        
        # Create local backup
        if self.config.local_enabled:
            local_result = await self._create_local_backup(backup_name)
            results.append(local_result)
        
        # Create S3 backup
        if self.config.s3_enabled and self.s3_client:
            s3_result = await self._create_s3_backup(backup_name)
            results.append(s3_result)
        
        # Create Google Drive backup
        if self.config.gdrive_enabled:
            gdrive_result = await self._create_gdrive_backup(backup_name)
            results.append(gdrive_result)
        
        # Update backup history
        self.backup_history.extend(results)
        
        # Generate backup summary
        success_count = len([r for r in results if r.success])
        total_size = sum(r.file_size for r in results if r.success)
        
        self.logger.info(f"✅ Backup completed: {success_count}/{len(results)} locations, {total_size} bytes total")
        
        # Send alert if backup failed
        if success_count < len(results):
            await self._send_backup_alert(backup_name, results)
        
        return results
    
    async def _create_local_backup(self, backup_name: str) -> BackupResult:
        """Create local backup"""
        try:
            start_time = datetime.now()
            
            # Use existing DatabaseBackup
            success = self.db_backup.create_backup(backup_name)
            
            if success:
                # Get backup file info
                backup_files = self.db_backup.list_backups()
                latest_backup = backup_files[0] if backup_files else None
                
                if latest_backup:
                    file_size = os.path.getsize(latest_backup['path'])
                    duration = (datetime.now() - start_time).total_seconds()
                    
                    result = BackupResult(
                        success=True,
                        backup_type="local",
                        location=latest_backup['path'],
                        file_size=file_size,
                        duration=duration,
                        backup_path=latest_backup['path']
                    )
                    
                    self.logger.info(f"💾 Local backup created: {latest_backup['filename']}")
                    return result
            
            return BackupResult(
                success=False,
                backup_type="local",
                location="unknown",
                file_size=0,
                duration=0,
                error_message="Local backup creation failed"
            )
            
        except Exception as e:
            self.logger.error(f"❌ Local backup failed: {e}")
            return BackupResult(
                success=False,
                backup_type="local",
                location="unknown",
                file_size=0,
                duration=0,
                error_message=str(e)
            )
    
    async def _create_s3_backup(self, backup_name: str) -> BackupResult:
        """Create S3 backup"""
        try:
            start_time = datetime.now()
            
            # Get latest local backup
            local_backups = self.db_backup.list_backups()
            if not local_backups:
                return BackupResult(
                    success=False,
                    backup_type="s3",
                    location="s3",
                    file_size=0,
                    duration=0,
                    error_message="No local backup found to upload"
                )
            
            latest_backup = local_backups[0]
            local_path = latest_backup['path']
            
            # Prepare S3 key
            s3_key = f"backups/{backup_name}.db (SQLite - removed)
            
            # Upload to S3
            if self.config.compression_enabled:
                # Compress before upload
                compressed_path = await self._compress_file(local_path)
                s3_key += ".gz"
                upload_path = compressed_path
            else:
                upload_path = local_path
            
            # Upload file
            self.s3_client.upload_file(
                Filename=upload_path,
                Bucket=self.s3_bucket,
                Key=s3_key,
                Callback=self._upload_progress_callback
            )
            
            # Get file info
            file_size = os.path.getsize(upload_path)
            duration = (datetime.now() - start_time).total_seconds()
            
            # Clean up compressed file
            if self.config.compression_enabled and os.path.exists(compressed_path):
                os.remove(compressed_path)
            
            result = BackupResult(
                success=True,
                backup_type="s3",
                location=f"s3://{self.s3_bucket}/{s3_key}",
                file_size=file_size,
                duration=duration,
                backup_path=s3_key
            )
            
            self.logger.info(f"☁️ S3 backup created: {s3_key}")
            return result
            
        except Exception as e:
            self.logger.error(f"❌ S3 backup failed: {e}")
            return BackupResult(
                success=False,
                backup_type="s3",
                location="s3",
                file_size=0,
                duration=0,
                error_message=str(e)
            )
    
    async def _create_gdrive_backup(self, backup_name: str) -> BackupResult:
        """Create Google Drive backup"""
        # Placeholder for Google Drive integration
        return BackupResult(
            success=False,
            backup_type="gdrive",
            location="gdrive",
            file_size=0,
            duration=0,
            error_message="Google Drive integration not yet implemented"
        )
    
    async def _compress_file(self, file_path: str) -> str:
        """Compress file using gzip"""
        compressed_path = f"{file_path}.gz"
        
        try:
            with open(file_path, 'rb') as f_in:
                with gzip.open(compressed_path, 'wb') as f_out:
                    f_out.writelines(f_in)
            
            return compressed_path
            
        except Exception as e:
            self.logger.error(f"❌ File compression failed: {e}")
            raise
    
    def _upload_progress_callback(self, bytes_transferred):
        """S3 upload progress callback"""
        self.logger.debug(f"📤 Uploaded {bytes_transferred} bytes")
    
    async def schedule_automatic_backups(self):
        """Schedule automatic backups based on configuration"""
        while True:
            try:
                # Calculate next backup time
                next_backup = self._calculate_next_backup_time()
                
                self.logger.info(f"⏰ Next automatic backup scheduled for: {next_backup}")
                
                # Wait until next backup time
                await asyncio.sleep((next_backup - datetime.now()).total_seconds())
                
                # Create backup
                backup_name = f"auto_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                await self.create_comprehensive_backup(backup_name)
                
                # Clean up old backups
                await self.cleanup_old_backups()
                
            except Exception as e:
                self.logger.error(f"❌ Automatic backup failed: {e}")
                await asyncio.sleep(3600)  # Wait 1 hour before retrying
    
    def _calculate_next_backup_time(self) -> datetime:
        """Calculate next backup time based on frequency"""
        now = datetime.now()
        
        if self.config.backup_frequency == "daily":
            # Next backup at 2 AM tomorrow
            next_backup = now.replace(hour=2, minute=0, second=0, microsecond=0)
            if next_backup <= now:
                next_backup += timedelta(days=1)
        elif self.config.backup_frequency == "weekly":
            # Next backup on Sunday at 2 AM
            days_ahead = (6 - now.weekday()) % 7
            next_backup = now + timedelta(days=days_ahead)
            next_backup = next_backup.replace(hour=2, minute=0, second=0, microsecond=0)
        elif self.config.backup_frequency == "monthly":
            # Next backup on 1st of month at 2 AM
            if now.month == 12:
                next_backup = now.replace(year=now.year + 1, month=1, day=1, hour=2, minute=0, second=0, microsecond=0)
            else:
                next_backup = now.replace(month=now.month + 1, day=1, hour=2, minute=0, second=0, microsecond=0)
        else:
            # Default to daily
            next_backup = now + timedelta(days=1)
            next_backup = next_backup.replace(hour=2, minute=0, second=0, microsecond=0)
        
        return next_backup
    
    async def cleanup_old_backups(self):
        """Clean up old backups based on retention policy"""
        try:
            cutoff_date = datetime.now() - timedelta(days=self.config.retention_days)
            
            # Clean up local backups
            if self.config.local_enabled:
                old_files = []
                for filename in os.listdir(self.db_backup.backup_folder):
                    if filename.startswith('database_backup_') and filename.endswith('.db (SQLite - removed)):
                        file_path = os.path.join(self.db_backup.backup_folder, filename)
                        file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                        
                        if file_time < cutoff_date:
                            os.remove(file_path)
                            old_files.append(filename)
                
                if old_files:
                    self.logger.info(f"🗑️ Cleaned up {len(old_files)} old local backups")
            
            # Clean up S3 backups
            if self.config.s3_enabled and self.s3_client:
                s3_objects = self.s3_client.list_objects_v2(Bucket=self.s3_bucket, Prefix="backups/")
                
                old_objects = []
                for obj in s3_objects.get('Contents', []):
                    obj_time = obj['LastModified'].replace(tzinfo=None)
                    
                    if obj_time < cutoff_date:
                        self.s3_client.delete_object(Bucket=self.s3_bucket, Key=obj['Key'])
                        old_objects.append(obj['Key'])
                
                if old_objects:
                    self.logger.info(f"🗑️ Cleaned up {len(old_objects)} old S3 backups")
            
        except Exception as e:
            self.logger.error(f"❌ Backup cleanup failed: {e}")
    
    async def _send_backup_alert(self, backup_name: str, results: List[BackupResult]):
        """Send backup alert to admin"""
        try:
            success_count = len([r for r in results if r.success])
            failed_count = len(results) - success_count
            
            alert_message = f"""
🔄 **Backup Report - {backup_name}**

✅ **Successful**: {success_count}/{len(results)} locations
❌ **Failed**: {failed_count}/{len(results)} locations

**Results**:
"""
            
            for result in results:
                status = "✅" if result.success else "❌"
                alert_message += f"{status} **{result.backup_type.upper()}**: {result.location}\n"
                if result.error_message:
                    alert_message += f"   Error: {result.error_message}\n"
            
            # Send to alert system
            from core_modules.doom_sentinel.alert_system import AlertSystem
            alert_system = AlertSystem()
            await alert_system.send_custom_alert(
                "Backup System Alert",
                alert_message.strip(),
                "warning" if failed_count > 0 else "info"
            )
            
        except Exception as e:
            self.logger.error(f"❌ Backup alert failed: {e}")
    
    def get_backup_statistics(self) -> Dict[str, Any]:
        """Get comprehensive backup statistics"""
        try:
            # Local backup stats
            local_stats = self.db_backup.get_backup_stats()
            
            # S3 backup stats
            s3_stats = {}
            if self.config.s3_enabled and self.s3_client:
                try:
                    s3_objects = self.s3_client.list_objects_v2(Bucket=self.s3_bucket, Prefix="backups/")
                    s3_stats = {
                        'total_backups': len(s3_objects.get('Contents', [])),
                        'total_size': sum(obj['Size'] for obj in s3_objects.get('Contents', [])),
                        'latest_backup': max([obj['LastModified'] for obj in s3_objects.get('Contents', [])]) if s3_objects.get('Contents') else None
                    }
                except Exception as e:
                    self.logger.error(f"❌ S3 stats failed: {e}")
            
            # Recent backup history
            recent_backups = self.backup_history[-10:] if self.backup_history else []
            
            return {
                'local': local_stats,
                's3': s3_stats,
                'gdrive': {'status': 'not_implemented'},
                'recent_backups': [
                    {
                        'type': r.backup_type,
                        'success': r.success,
                        'location': r.location,
                        'file_size': r.file_size,
                        'duration': r.duration,
                        'timestamp': r.backup_path
                    }
                    for r in recent_backups
                ],
                'configuration': {
                    'local_enabled': self.config.local_enabled,
                    's3_enabled': self.config.s3_enabled,
                    'gdrive_enabled': self.config.gdrive_enabled,
                    'compression_enabled': self.config.compression_enabled,
                    'retention_days': self.config.retention_days,
                    'backup_frequency': self.config.backup_frequency
                }
            }
            
        except Exception as e:
            self.logger.error(f"❌ Backup statistics failed: {e}")
            return {}
    
    async def test_backup_system(self) -> Dict[str, Any]:
        """Test backup system functionality"""
        test_results = {}
        
        try:
            # Test local backup
            if self.config.local_enabled:
                local_result = await self._create_local_backup("test_backup")
                test_results['local_backup'] = {
                    'success': local_result.success,
                    'file_size': local_result.file_size,
                    'duration': local_result.duration
                }
            
            # Test S3 backup
            if self.config.s3_enabled and self.s3_client:
                s3_result = await self._create_s3_backup("test_backup")
                test_results['s3_backup'] = {
                    'success': s3_result.success,
                    'file_size': s3_result.file_size,
                    'duration': s3_result.duration
                }
            
            # Test compression
            if self.config.compression_enabled:
                compression_test = await self._test_compression()
                test_results['compression'] = compression_test
            
            test_results['overall_status'] = 'passed'
            
        except Exception as e:
            test_results['overall_status'] = 'failed'
            test_results['error'] = str(e)
        
        return test_results
    
    async def _test_compression(self) -> Dict[str, Any]:
        """Test file compression"""
        try:
            # Create test file
            test_file = "test_compression.txt"
            test_content = "Test content for compression" * 1000
            
            with open(test_file, 'w') as f:
                f.write(test_content)
            
            original_size = os.path.getsize(test_file)
            
            # Compress file
            compressed_file = await self._compress_file(test_file)
            compressed_size = os.path.getsize(compressed_file)
            
            # Calculate compression ratio
            compression_ratio = (original_size - compressed_size) / original_size * 100
            
            # Clean up
            os.remove(test_file)
            os.remove(compressed_file)
            
            return {
                'success': True,
                'original_size': original_size,
                'compressed_size': compressed_size,
                'compression_ratio': compression_ratio,
                'compression_working': compression_ratio > 0
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

# Global enhanced backup system instance
enhanced_backup = EnhancedBackupSystem()

# Example usage
async def main():
    """Main function for testing"""
    config = BackupConfig(
        local_enabled=True,
        s3_enabled=False,  # Set to True if S3 credentials are configured
        gdrive_enabled=False,
        compression_enabled=True,
        retention_days=30,
        backup_frequency="daily"
    )
    
    backup_system = EnhancedBackupSystem(config)
    
    # Test backup system
    test_results = await backup_system.test_backup_system()
    print(f"🧪 Backup System Test Results: {test_results}")
    
    # Create comprehensive backup
    if test_results.get('overall_status') == 'passed':
        backup_results = await backup_system.create_comprehensive_backup("manual_test")
        print(f"📦 Backup Results: {len(backup_results)} locations")
        
        # Show statistics
        stats = backup_system.get_backup_statistics()
        print(f"📊 Backup Statistics: {stats}")

if __name__ == "__main__":
    asyncio.run(main())
