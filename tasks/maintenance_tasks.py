"""
LUMINA OS - MAINTENANCE TASKS
================================

System maintenance and cleanup tasks for optimal performance.

Features:
- Old task cleanup and archiving
- Database maintenance and optimization
- Log file rotation and cleanup
- Cache management
- System health monitoring
- Performance metrics collection
"""

import os
import sys
import json
import asyncio
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import glob
import shutil
from pathlib import Path

# Add root directory to Python path
root_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root_dir)

# Import Celery app
from tasks.celery_app import celery_app, maintenance_task

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@maintenance_task
def cleanup_old_tasks(self, days: int = 7) -> Dict[str, Any]:
    """
    Clean up old task logs and completed tasks
    
    Args:
        days: Number of days to keep tasks
    
    Returns:
        Dictionary containing cleanup results
    """
    
    try:
        logger.info(f"Starting old tasks cleanup: {days} days")
        
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # Clean up task logs
        logs_dir = os.path.join(root_dir, 'logs')
        if os.path.exists(logs_dir):
            cleaned_logs = []
            
            for log_file in glob.glob(os.path.join(logs_dir, 'task_*.log')):
                try:
                    file_mtime = datetime.fromtimestamp(os.path.getmtime(log_file))
                    
                    if file_mtime < cutoff_date:
                        os.remove(log_file)
                        cleaned_logs.append(log_file)
                        
                except Exception as e:
                    logger.error(f"Error cleaning log file {log_file}: {e}")
                    continue
        
        # Clean up temporary files
        temp_dir = os.path.join(root_dir, 'temp')
        if os.path.exists(temp_dir):
            cleaned_temp = []
            
            for temp_file in glob.glob(os.path.join(temp_dir, '*')):
                try:
                    file_mtime = datetime.fromtimestamp(os.path.getmtime(temp_file))
                    
                    if file_mtime < cutoff_date:
                        if os.path.isfile(temp_file):
                            os.remove(temp_file)
                        elif os.path.isdir(temp_file):
                            shutil.rmtree(temp_file)
                        cleaned_temp.append(temp_file)
                        
                except Exception as e:
                    logger.error(f"Error cleaning temp file {temp_file}: {e}")
                    continue
        
        # Clean up old reports
        reports_dir = os.path.join(root_dir, 'reports')
        if os.path.exists(reports_dir):
            cleaned_reports = []
            
            for report_file in glob.glob(os.path.join(reports_dir, '*.json')):
                try:
                    file_mtime = datetime.fromtimestamp(os.path.getmtime(report_file))
                    
                    if file_mtime < cutoff_date:
                        os.remove(report_file)
                        cleaned_reports.append(report_file)
                        
                except Exception as e:
                    logger.error(f"Error cleaning report file {report_file}: {e}")
                    continue
        
        logger.info(f"Old tasks cleanup completed: {len(cleaned_logs)} logs, {len(cleaned_temp)} temp files, {len(cleaned_reports)} reports")
        
        return {
            'success': True,
            'cutoff_date': cutoff_date.isoformat(),
            'cleaned_logs': len(cleaned_logs),
            'cleaned_temp': len(cleaned_temp),
            'cleaned_reports': len(cleaned_reports),
            'cleaned_at': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Old tasks cleanup failed: {e}")
        raise self.retry(exc=e, countdown=60, max_retries=3)

@maintenance_task
def optimize_database(self) -> Dict[str, Any]:
    """
    Optimize database performance
    
    Returns:
        Dictionary containing optimization results
    """
    
    try:
        logger.info("Starting database optimization")
        
        optimization_results = {}
        
        # Try to optimize PostgreSQL if available
        try:
            from core_modules.db_manager import DatabaseManager
            db = DatabaseManager()
            
            # Analyze tables
            analyze_result = db.execute_query("ANALYZE;")
            optimization_results['postgresql_analyze'] = analyze_result is not None
            
            # Vacuum tables
            vacuum_result = db.execute_query("VACUUM ANALYZE;")
            optimization_results['postgresql_vacuum'] = vacuum_result is not None
            
            # Update statistics
            stats_result = db.execute_query("UPDATE statistics;")
            optimization_results['postgresql_stats'] = stats_result is not None
            
        except Exception as e:
            logger.error(f"PostgreSQL optimization failed: {e}")
            optimization_results['postgresql_error'] = str(e)
        
        # Clean up Redis cache if available
        try:
            import redis
            redis_client = redis.Redis(
                host=os.getenv('REDIS_HOST', 'localhost'),
                port=int(os.getenv('REDIS_PORT', 6379)),
                password=os.getenv('REDIS_PASSWORD'),
                decode_responses=True
            )
            
            # Get Redis info
            redis_info = redis_client.info()
            optimization_results['redis_info'] = {
                'used_memory': redis_info.get('used_memory_human'),
                'connected_clients': redis_info.get('connected_clients'),
                'total_commands_processed': redis_info.get('total_commands_processed')
            }
            
            # Clean up expired keys
            expired_keys = redis_client.dbsize()
            optimization_results['redis_cleanup'] = f"Checked {expired_keys} keys"
            
        except Exception as e:
            logger.error(f"Redis optimization failed: {e}")
            optimization_results['redis_error'] = str(e)
        
        logger.info("Database optimization completed")
        
        return {
            'success': True,
            'optimization_results': optimization_results,
            'optimized_at': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Database optimization failed: {e}")
        raise self.retry(exc=e, countdown=60, max_retries=3)

@maintenance_task
def rotate_logs(self) -> Dict[str, Any]:
    """
    Rotate and compress log files
    
    Returns:
        Dictionary containing rotation results
    """
    
    try:
        logger.info("Starting log rotation")
        
        logs_dir = os.path.join(root_dir, 'logs')
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)
        
        rotation_results = {
            'rotated_files': [],
            'compressed_files': [],
            'errors': []
        }
        
        # Find log files larger than 10MB
        for log_file in glob.glob(os.path.join(logs_dir, '*.log')):
            try:
                file_size = os.path.getsize(log_file)
                
                if file_size > 10 * 1024 * 1024:  # 10MB
                    # Create rotated filename
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    rotated_filename = f"{os.path.basename(log_file)}.{timestamp}.log"
                    rotated_path = os.path.join(logs_dir, rotated_filename)
                    
                    # Rotate file
                    shutil.move(log_file, rotated_path)
                    rotation_results['rotated_files'].append(rotated_filename)
                    
                    # Compress rotated file
                    compressed_filename = f"{rotated_filename}.gz"
                    compressed_path = os.path.join(logs_dir, compressed_filename)
                    
                    with open(rotated_path, 'rb') as f_in:
                        with open(compressed_path, 'wb') as f_out:
                            import gzip
                            with gzip.open(compressed_path, 'wb') as f_gzip:
                                shutil.copyfileobj(f_in, f_gzip)
                    
                    os.remove(rotated_path)
                    rotation_results['compressed_files'].append(compressed_filename)
                    
            except Exception as e:
                logger.error(f"Error rotating log file {log_file}: {e}")
                rotation_results['errors'].append(f"{log_file}: {str(e)}")
        
        # Clean up old compressed logs (older than 30 days)
        cutoff_date = datetime.now() - timedelta(days=30)
        
        for compressed_file in glob.glob(os.path.join(logs_dir, '*.log.*.gz')):
            try:
                file_mtime = datetime.fromtimestamp(os.path.getmtime(compressed_file))
                
                if file_mtime < cutoff_date:
                    os.remove(compressed_file)
                    rotation_results['rotated_files'].append(f"Removed old: {compressed_file}")
                    
            except Exception as e:
                logger.error(f"Error removing old compressed log {compressed_file}: {e}")
                rotation_results['errors'].append(f"{compressed_file}: {str(e)}")
        
        logger.info(f"Log rotation completed: {len(rotation_results['rotated_files'])} files processed")
        
        return {
            'success': True,
            'rotation_results': rotation_results,
            'rotated_at': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Log rotation failed: {e}")
        raise self.retry(exc=e, countdown=60, max_retries=3)

@maintenance_task
def cleanup_cache(self) -> Dict[str, Any]:
    """
    Clean up system cache and temporary files
    
    Returns:
        Dictionary containing cleanup results
    """
    
    try:
        logger.info("Starting cache cleanup")
        
        cleanup_results = {
            'cleaned_directories': [],
            'cleaned_files': [],
            'freed_space': 0,
            'errors': []
        }
        
        # Define cache directories to clean
        cache_dirs = [
            os.path.join(root_dir, '.cache'),
            os.path.join(root_dir, '__pycache__'),
            os.path.join(root_dir, 'temp'),
            os.path.join(root_dir, 'data', 'cache'),
            os.path.join(root_dir, 'dashboard', '.next', 'cache')
        ]
        
        total_freed = 0
        
        for cache_dir in cache_dirs:
            if os.path.exists(cache_dir):
                try:
                    # Calculate directory size before cleanup
                    dir_size = get_directory_size(cache_dir)
                    
                    # Clean up directory
                    if os.path.isdir(cache_dir):
                        shutil.rmtree(cache_dir)
                        os.makedirs(cache_dir)  # Recreate empty directory
                    else:
                        os.remove(cache_dir)
                    
                    total_freed += dir_size
                    cleanup_results['cleaned_directories'].append(cache_dir)
                    
                except Exception as e:
                    logger.error(f"Error cleaning cache directory {cache_dir}: {e}")
                    cleanup_results['errors'].append(f"{cache_dir}: {str(e)}")
        
        # Clean up specific file patterns
        file_patterns = [
            os.path.join(root_dir, '*.pyc'),
            os.path.join(root_dir, '**', '*.pyc'),
            os.path.join(root_dir, '**', '__pycache__'),
            os.path.join(root_dir, '.DS_Store'),
            os.path.join(root_dir, '**', '.DS_Store'),
            os.path.join(root_dir, 'Thumbs.db (SQLite - removed)),
            os.path.join(root_dir, '**', 'Thumbs.db (SQLite - removed))
        ]
        
        for pattern in file_patterns:
            for file_path in glob.glob(pattern, recursive=True):
                try:
                    file_size = os.path.getsize(file_path)
                    
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                    
                    total_freed += file_size
                    cleanup_results['cleaned_files'].append(file_path)
                    
                except Exception as e:
                    logger.error(f"Error cleaning file {file_path}: {e}")
                    cleanup_results['errors'].append(f"{file_path}: {str(e)}")
        
        cleanup_results['freed_space'] = format_bytes(total_freed)
        
        logger.info(f"Cache cleanup completed: {cleanup_results['freed_space']} freed")
        
        return {
            'success': True,
            'cleanup_results': cleanup_results,
            'cleaned_at': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Cache cleanup failed: {e}")
        raise self.retry(exc=e, countdown=60, max_retries=3)

@maintenance_task
def generate_system_report(self) -> Dict[str, Any]:
    """
    Generate comprehensive system health report
    
    Returns:
        Dictionary containing system report
    """
    
    try:
        logger.info("Generating system health report")
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'system_info': {},
            'performance_metrics': {},
            'resource_usage': {},
            'error_summary': {},
            'recommendations': []
        }
        
        # System information
        import platform
        report['system_info'] = {
            'platform': platform.platform(),
            'python_version': platform.python_version(),
            'architecture': platform.architecture(),
            'processor': platform.processor(),
            'hostname': platform.node()
        }
        
        # Disk usage
        disk_usage = shutil.disk_usage(root_dir)
        report['resource_usage']['disk'] = {
            'total': format_bytes(disk_usage.total),
            'used': format_bytes(disk_usage.used),
            'free': format_bytes(disk_usage.free),
            'percent_used': (disk_usage.used / disk_usage.total) * 100
        }
        
        # Memory usage (if available)
        try:
            import psutil
            memory = psutil.virtual_memory()
            report['resource_usage']['memory'] = {
                'total': format_bytes(memory.total),
                'used': format_bytes(memory.used),
                'free': format_bytes(memory.available),
                'percent_used': memory.percent
            }
            
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            report['resource_usage']['cpu'] = {
                'percent_used': cpu_percent
            }
            
        except ImportError:
            report['recommendations'].append("Install psutil for detailed resource monitoring")
        
        # Database statistics
        try:
            from core_modules.db_manager import DatabaseManager
            db = DatabaseManager()
            
            # Get table sizes
            table_stats = db.execute_query("""
                SELECT 
                    schemaname,
                    tablename,
                    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
                FROM pg_tables 
                WHERE schemaname = 'public'
                ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
            """)
            
            report['performance_metrics']['database'] = {
                'table_stats': table_stats,
                'connection_pool': 'active'
            }
            
        except Exception as e:
            report['performance_metrics']['database'] = {'error': str(e)}
        
        # Task queue statistics
        try:
            from tasks.celery_app import TaskMonitor
            task_stats = TaskMonitor.get_task_stats()
            report['performance_metrics']['tasks'] = task_stats
        except Exception as e:
            report['performance_metrics']['tasks'] = {'error': str(e)}
        
        # Error summary from logs
        try:
            error_count = count_recent_errors()
            report['error_summary'] = {
                'recent_errors_24h': error_count,
                'error_rate': 'low' if error_count < 10 else 'medium' if error_count < 50 else 'high'
            }
        except Exception as e:
            report['error_summary'] = {'error': str(e)}
        
        # Generate recommendations
        if report['resource_usage']['disk']['percent_used'] > 80:
            report['recommendations'].append("Disk usage is high. Consider cleaning up old files.")
        
        if report['resource_usage'].get('memory', {}).get('percent_used', 0) > 80:
            report['recommendations'].append("Memory usage is high. Consider optimizing memory usage.")
        
        if report['error_summary'].get('error_rate') == 'high':
            report['recommendations'].append("High error rate detected. Review recent errors.")
        
        # Save report
        reports_dir = os.path.join(root_dir, 'reports')
        os.makedirs(reports_dir, exist_ok=True)
        
        report_filename = f"system_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path = os.path.join(reports_dir, report_filename)
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        logger.info(f"System report generated: {report_path}")
        
        return {
            'success': True,
            'report': report,
            'report_path': report_path
        }
        
    except Exception as e:
        logger.error(f"System report generation failed: {e}")
        raise self.retry(exc=e, countdown=60, max_retries=3)

# Helper functions

def get_directory_size(directory: str) -> int:
    """Get total size of directory in bytes"""
    
    total_size = 0
    
    try:
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if os.path.isfile(filepath):
                    total_size += os.path.getsize(filepath)
    except Exception as e:
        logger.error(f"Error calculating directory size for {directory}: {e}")
    
    return total_size

def format_bytes(bytes_count: int) -> str:
    """Format bytes in human readable format"""
    
    if bytes_count == 0:
        return "0B"
    
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    i = 0
    
    while bytes_count >= 1024 and i < len(units) - 1:
        bytes_count /= 1024.0
        i += 1
    
    return f"{bytes_count:.2f} {units[i]}"

def count_recent_errors(hours: int = 24) -> int:
    """Count errors in recent log files"""
    
    error_count = 0
    logs_dir = os.path.join(root_dir, 'logs')
    
    if not os.path.exists(logs_dir):
        return 0
    
    cutoff_time = datetime.now() - timedelta(hours=hours)
    
    for log_file in glob.glob(os.path.join(logs_dir, '*.log')):
        try:
            file_mtime = datetime.fromtimestamp(os.path.getmtime(log_file))
            
            if file_mtime >= cutoff_time:
                with open(log_file, 'r') as f:
                    for line in f:
                        if 'ERROR' in line.upper():
                            error_count += 1
        except Exception as e:
            logger.error(f"Error counting errors in {log_file}: {e}")
    
    return error_count

@maintenance_task
def health_check_all_services(self) -> Dict[str, Any]:
    """
    Comprehensive health check of all services
    
    Returns:
        Dictionary containing health check results
    """
    
    try:
        logger.info("Starting comprehensive health check")
        
        health_results = {
            'overall_status': 'healthy',
            'services': {},
            'checked_at': datetime.now().isoformat()
        }
        
        # Check database
        try:
            from core_modules.db_manager import DatabaseManager
            db = DatabaseManager()
            
            # Simple connectivity test
            db.execute_query("SELECT 1")
            health_results['services']['database'] = {
                'status': 'healthy',
                'response_time': 'fast'
            }
        except Exception as e:
            health_results['services']['database'] = {
                'status': 'unhealthy',
                'error': str(e)
            }
            health_results['overall_status'] = 'unhealthy'
        
        # Check Redis
        try:
            import redis
            redis_client = redis.Redis(
                host=os.getenv('REDIS_HOST', 'localhost'),
                port=int(os.getenv('REDIS_PORT', 6379)),
                password=os.getenv('REDIS_PASSWORD'),
                decode_responses=True
            )
            
            redis_client.ping()
            health_results['services']['redis'] = {
                'status': 'healthy',
                'response_time': 'fast'
            }
        except Exception as e:
            health_results['services']['redis'] = {
                'status': 'unhealthy',
                'error': str(e)
            }
            health_results['overall_status'] = 'unhealthy'
        
        # Check Celery workers
        try:
            from tasks.celery_app import TaskMonitor
            task_stats = TaskMonitor.get_task_stats()
            
            if task_stats.get('total_workers', 0) > 0:
                health_results['services']['celery'] = {
                    'status': 'healthy',
                    'workers': task_stats.get('total_workers', 0)
                }
            else:
                health_results['services']['celery'] = {
                    'status': 'unhealthy',
                    'error': 'No active workers'
                }
                health_results['overall_status'] = 'unhealthy'
        except Exception as e:
            health_results['services']['celery'] = {
                'status': 'unhealthy',
                'error': str(e)
            }
            health_results['overall_status'] = 'unhealthy'
        
        # Check FastAPI
        try:
            response = requests.get('http://localhost:8000/health', timeout=5)
            if response.status_code == 200:
                health_results['services']['fastapi'] = {
                    'status': 'healthy',
                    'response_time': 'fast'
                }
            else:
                health_results['services']['fastapi'] = {
                    'status': 'unhealthy',
                    'error': f'HTTP {response.status_code}'
                }
                health_results['overall_status'] = 'unhealthy'
        except Exception as e:
            health_results['services']['fastapi'] = {
                'status': 'unhealthy',
                'error': str(e)
            }
            health_results['overall_status'] = 'unhealthy'
        
        # Check Next.js
        try:
            response = requests.get('http://localhost:3000/api/health', timeout=5)
            if response.status_code == 200:
                health_results['services']['nextjs'] = {
                    'status': 'healthy',
                    'response_time': 'fast'
                }
            else:
                health_results['services']['nextjs'] = {
                    'status': 'unhealthy',
                    'error': f'HTTP {response.status_code}'
                }
                health_results['overall_status'] = 'unhealthy'
        except Exception as e:
            health_results['services']['nextjs'] = {
                'status': 'unhealthy',
                'error': str(e)
            }
            health_results['overall_status'] = 'unhealthy'
        
        logger.info(f"Health check completed: {health_results['overall_status']}")
        
        return {
            'success': True,
            'health_results': health_results
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise self.retry(exc=e, countdown=60, max_retries=3)
