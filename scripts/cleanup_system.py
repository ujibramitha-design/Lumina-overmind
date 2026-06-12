"""
LUMINA OS System Cleanup Script
Cleans up old logs, temporary files, and test data for production deployment

Author: HUNTER_AGENT_AI_MARKETING_DIGITAL
Version: 1.0.0
"""

import os
import sys
import shutil
import glob
from datetime import datetime, timedelta
from typing import List, Tuple
import json

class SystemCleaner:
    """Comprehensive system cleanup utility"""
    
    def __init__(self):
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.cleanup_log = []
        self.files_deleted = 0
        self.space_freed = 0
        self.dry_run = False
        
        # Define cleanup targets
        self.cleanup_targets = {
            'old_logs': {
                'description': 'Old log files (older than 7 days)',
                'patterns': [
                    'logs/*.log',
                    'logs/*.txt',
                    'logs/*.json',
                    'logs/*.md',
                    'logs/**/*.log',
                    'logs/**/*.txt',
                    'logs/**/*.json',
                    'logs/**/*.md'
                ],
                'age_days': 7,
                'critical': False
            },
            'temp_files': {
                'description': 'Temporary files and cache',
                'patterns': [
                    'temp/**/*',
                    'tmp/**/*',
                    'cache/**/*',
                    '__pycache__/**/*',
                    '*.pyc',
                    '*.pyo',
                    '.pytest_cache/**/*',
                    '.coverage',
                    '*.tmp',
                    '*.temp'
                ],
                'age_days': 1,
                'critical': False
            },
            'test_data': {
                'description': 'Test data and dummy files',
                'patterns': [
                    'data/test_*.db (SQLite - removed),
                    'data/test_*.json',
                    'data/dummy_*.json',
                    'data/sample_*.json',
                    'data/*_test.db (SQLite - removed),
                    'data/*_backup_test.db (SQLite - removed),
                    'logs/test_*.log',
                    'logs/test_*.json'
                ],
                'age_days': 0,  # Delete all test files
                'critical': False
            },
            'old_backups': {
                'description': 'Old backup files (older than 30 days)',
                'patterns': [
                    'data/backups/*_backup_*.db (SQLite - removed),
                    'data/backups/*_backup_*.json',
                    'data/backups/*_backup_*.txt',
                    'data/backups/*_backup_*.md'
                ],
                'age_days': 30,
                'critical': False
            },
            'archive_files': {
                'description': 'Archive and old reports',
                'patterns': [
                    'reports/*_old_*',
                    'reports/*_archive_*',
                    'reports/*_backup_*',
                    'reports/*_temp_*'
                ],
                'age_days': 14,
                'critical': False
            }
        }
        
        # Files to NEVER delete
        self.protected_files = {
            'data/leads.db (SQLite - removed),
            'data/leads_database.json',
            '.env',
            'requirements.txt',
            'README.md',
            'README_SUPER.md',
            'config/config.py',
            'main.py',
            'app.py'
        }
        
        # Directories to protect (but clean contents)
        self.protected_dirs = {
            'data',
            'logs',
            'reports',
            'backups'
        }
    
    def run_cleanup(self, dry_run: bool = False, verbose: bool = True) -> dict:
        """Run comprehensive system cleanup"""
        self.dry_run = dry_run
        self.files_deleted = 0
        self.space_freed = 0
        self.cleanup_log = []
        
        print("🧹 LUMINA OS SYSTEM CLEANUP")
        print("=" * 50)
        print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🔍 Dry Run: {'YES' if dry_run else 'NO'}")
        print()
        
        # Check disk space before cleanup
        initial_space = self._get_disk_space()
        print(f"💾 Initial disk space: {initial_space['used_gb']:.1f}GB / {initial_space['total_gb']:.1f}GB")
        print()
        
        # Run cleanup for each target
        for target_name, target_config in self.cleanup_targets.items():
            if verbose:
                print(f"🧹 Cleaning: {target_config['description']}")
            
            self._cleanup_target(target_name, target_config, verbose)
            
            if verbose:
                print()
        
        # Clean up empty directories
        if verbose:
            print("🗂️ Cleaning empty directories...")
        self._cleanup_empty_dirs(verbose)
        
        # Generate cleanup report
        final_space = self._get_disk_space()
        space_freed = initial_space['used_gb'] - final_space['used_gb']
        
        print("=" * 50)
        print("📊 CLEANUP SUMMARY")
        print("=" * 50)
        print(f"📁 Files processed: {self.files_deleted}")
        print(f"💾 Space freed: {space_freed:.2f}GB")
        print(f"📅 Final disk space: {final_space['used_gb']:.1f}GB / {final_space['total_gb']:.1f}GB")
        print()
        
        # Save cleanup log
        self._save_cleanup_log()
        
        return {
            'files_deleted': self.files_deleted,
            'space_freed_gb': space_freed,
            'initial_space': initial_space,
            'final_space': final_space,
            'cleanup_log': self.cleanup_log
        }
    
    def _cleanup_target(self, target_name: str, target_config: dict, verbose: bool):
        """Clean up specific target"""
        patterns = target_config['patterns']
        age_days = target_config['age_days']
        critical = target_config['critical']
        
        files_to_delete = []
        
        for pattern in patterns:
            # Convert pattern to full path
            full_pattern = os.path.join(self.project_root, pattern)
            
            # Find matching files
            matching_files = glob.glob(full_pattern, recursive=True)
            
            for file_path in matching_files:
                # Skip protected files
                if self._is_protected_file(file_path):
                    continue
                
                # Check file age
                if age_days > 0:
                    file_age = self._get_file_age_days(file_path)
                    if file_age < age_days:
                        continue
                
                files_to_delete.append(file_path)
        
        # Delete files
        for file_path in files_to_delete:
            try:
                if os.path.isfile(file_path):
                    file_size = os.path.getsize(file_path)
                    
                    if not self.dry_run:
                        os.remove(file_path)
                    
                    self.files_deleted += 1
                    self.space_freed += file_size
                    
                    if verbose:
                        print(f"  🗑️ {os.path.relpath(file_path, self.project_root)} ({self._format_bytes(file_size)})")
                    
                    self.cleanup_log.append({
                        'action': 'delete_file',
                        'file': os.path.relpath(file_path, self.project_root),
                        'size': file_size,
                        'target': target_name,
                        'timestamp': datetime.now().isoformat()
                    })
                
                elif os.path.isdir(file_path):
                    if not self.dry_run:
                        shutil.rmtree(file_path)
                    
                    self.files_deleted += 1
                    
                    if verbose:
                        print(f"  🗂️ {os.path.relpath(file_path, self.project_root)} (directory)")
                    
                    self.cleanup_log.append({
                        'action': 'delete_directory',
                        'directory': os.path.relpath(file_path, self.project_root),
                        'target': target_name,
                        'timestamp': datetime.now().isoformat()
                    })
                
            except Exception as e:
                print(f"  ⚠️ Error deleting {file_path}: {e}")
                self.cleanup_log.append({
                    'action': 'error',
                    'file': os.path.relpath(file_path, self.project_root),
                    'error': str(e),
                    'target': target_name,
                    'timestamp': datetime.now().isoformat()
                })
    
    def _cleanup_empty_dirs(self, verbose: bool):
        """Clean up empty directories"""
        empty_dirs = []
        
        for root, dirs, files in os.walk(self.project_root):
            # Skip protected directories
            if any(protected in root for protected in self.protected_dirs):
                continue
            
            # Check if directory is empty
            if not dirs and not files:
                empty_dirs.append(root)
        
        # Remove empty directories (in reverse order to avoid path issues)
        for dir_path in sorted(empty_dirs, reverse=True):
            try:
                if not self.dry_run:
                    os.rmdir(dir_path)
                
                self.files_deleted += 1
                
                if verbose:
                    print(f"  🗂️ {os.path.relpath(dir_path, self.project_root)} (empty directory)")
                
                self.cleanup_log.append({
                    'action': 'delete_empty_dir',
                    'directory': os.path.relpath(dir_path, self.project_root),
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                print(f"  ⚠️ Error removing empty directory {dir_path}: {e}")
    
    def _is_protected_file(self, file_path: str) -> bool:
        """Check if file is protected"""
        relative_path = os.path.relpath(file_path, self.project_root)
        
        # Check exact matches
        if relative_path in self.protected_files:
            return True
        
        # Check if file is in protected directory but not a protected file
        for protected_dir in self.protected_dirs:
            if relative_path.startswith(protected_dir + '/'):
                # Check if it's a critical file type
                if relative_path.endswith('.db (SQLite - removed)):
                    return True
                if relative_path.endswith('.json') and 'leads' in relative_path:
                    return True
        
        return False
    
    def _get_file_age_days(self, file_path: str) -> int:
        """Get file age in days"""
        try:
            file_time = os.path.getmtime(file_path)
            file_date = datetime.fromtimestamp(file_time)
            age = datetime.now() - file_date
            return age.days
        except:
            return 0
    
    def _get_disk_space(self) -> dict:
        """Get disk space information"""
        try:
            usage = shutil.disk_usage(self.project_root)
            return {
                'total_gb': usage.total / (1024**3),
                'used_gb': usage.used / (1024**3),
                'free_gb': usage.free / (1024**3),
                'percent_used': (usage.used / usage.total) * 100
            }
        except:
            return {
                'total_gb': 0,
                'used_gb': 0,
                'free_gb': 0,
                'percent_used': 0
            }
    
    def _format_bytes(self, bytes_value: int) -> str:
        """Format bytes in human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.0f}{unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.0f}PB"
    
    def _save_cleanup_log(self):
        """Save cleanup log to file"""
        log_path = os.path.join(self.project_root, 'logs', 'cleanup_log.json')
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'dry_run': self.dry_run,
            'files_deleted': self.files_deleted,
            'space_freed_bytes': self.space_freed,
            'cleanup_log': self.cleanup_log
        }
        
        with open(log_path, 'w') as f:
            json.dump(log_data, f, indent=2, default=str)
        
        print(f"📄 Cleanup log saved to: {os.path.relpath(log_path, self.project_root)}")
    
    def analyze_cleanup_potential(self) -> dict:
        """Analyze what would be cleaned without actually cleaning"""
        print("🔍 ANALYZING CLEANUP POTENTIAL")
        print("=" * 50)
        
        analysis = {
            'targets': {},
            'total_files': 0,
            'total_size': 0
        }
        
        for target_name, target_config in self.cleanup_targets.items():
            target_files = []
            target_size = 0
            
            patterns = target_config['patterns']
            age_days = target_config['age_days']
            
            for pattern in patterns:
                full_pattern = os.path.join(self.project_root, pattern)
                matching_files = glob.glob(full_pattern, recursive=True)
                
                for file_path in matching_files:
                    if self._is_protected_file(file_path):
                        continue
                    
                    if age_days > 0:
                        file_age = self._get_file_age_days(file_path)
                        if file_age < age_days:
                            continue
                    
                    if os.path.isfile(file_path):
                        file_size = os.path.getsize(file_path)
                        target_files.append(file_path)
                        target_size += file_size
            
            analysis['targets'][target_name] = {
                'description': target_config['description'],
                'file_count': len(target_files),
                'size_bytes': target_size,
                'size_mb': target_size / (1024**2),
                'files': [os.path.relpath(f, self.project_root) for f in target_files[:10]]  # Show first 10
            }
            
            analysis['total_files'] += len(target_files)
            analysis['total_size'] += target_size
            
            print(f"📁 {target_config['description']}")
            print(f"   📊 Files: {len(target_files)}")
            print(f"   💾 Size: {target_size / (1024**2):.1f}MB")
            
            if target_files:
                print(f"   📋 Sample files:")
                for file_path in target_files[:5]:
                    print(f"     - {os.path.relpath(file_path, self.project_root)}")
                if len(target_files) > 5:
                    print(f"     ... and {len(target_files) - 5} more")
            print()
        
        print("=" * 50)
        print("📊 ANALYSIS SUMMARY")
        print("=" * 50)
        print(f"📁 Total files to delete: {analysis['total_files']}")
        print(f"💾 Total space to free: {analysis['total_size'] / (1024**2):.1f}MB")
        print()
        
        return analysis

def main():
    """Main function to run system cleanup"""
    import argparse
    
    parser = argparse.ArgumentParser(description='LUMINA OS System Cleanup')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be deleted without actually deleting')
    parser.add_argument('--analyze', action='store_true', help='Analyze cleanup potential without cleaning')
    parser.add_argument('--verbose', action='store_true', default=True, help='Verbose output')
    parser.add_argument('--silent', action='store_true', help='Silent mode (no output)')
    
    args = parser.parse_args()
    
    cleaner = SystemCleaner()
    
    if args.analyze:
        # Just analyze, don't clean
        analysis = cleaner.analyze_cleanup_potential()
        
        # Ask user if they want to proceed
        if analysis['total_files'] > 0:
            response = input(f"\n❓ Delete {analysis['total_files']} files ({analysis['total_size'] / (1024**2):.1f}MB)? [y/N]: ")
            if response.lower() in ['y', 'yes']:
                cleaner.run_cleanup(dry_run=False, verbose=not args.silent)
            else:
                print("❌ Cleanup cancelled")
        else:
            print("✅ No files to clean up")
    
    else:
        # Run cleanup
        if args.dry_run:
            print("🔍 DRY RUN MODE - No files will be deleted")
            print()
        
        result = cleaner.run_cleanup(dry_run=args.dry_run, verbose=not args.silent)
        
        if not args.dry_run and result['files_deleted'] > 0:
            print(f"\n✅ Cleanup completed successfully!")
            print(f"📁 {result['files_deleted']} files deleted")
            print(f"💾 {result['space_freed_gb']:.2f}GB freed")
        elif args.dry_run:
            print(f"\n🔍 Dry run completed")
            print(f"📁 {result['files_deleted']} files would be deleted")
            print(f"💾 {result['space_freed_gb']:.2f}GB would be freed")
        else:
            print("\n✅ System is already clean!")

if __name__ == "__main__":
    main()
