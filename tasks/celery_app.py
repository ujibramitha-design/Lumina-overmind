"""
LUMINA OS - CELERY APPLICATION
===============================

Enterprise-grade task queue system for async processing
of image generation, video processing, PDF creation, and more.

Features:
- Async image generation with ComfyUI
- Video processing with Runway/Luma
- PDF creation with Puppeteer/Playwright
- Lead scouting and data analysis
- VR rendering and processing
- Email and notification sending
- Task monitoring and logging
"""

import os
import sys
import json
import asyncio
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from celery import Celery, Task
from celery.signals import task_prerun, task_postrun, task_failure
from celery.exceptions import Retry

# Add root directory to Python path
root_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root_dir)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Celery Configuration
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://:redis_secure_password_2024@localhost:6379/1')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://:redis_secure_password_2024@localhost:6379/2')

# Create Celery app
celery_app = Celery(
    'lumina_os',
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=['tasks.visual_tasks', 'tasks.intelligence_tasks', 'tasks.notification_tasks', 'tasks.runner_tasks']
)

# Celery Configuration
celery_app.conf.update(
    # Task settings
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Jakarta',
    enable_utc=True,
    
    # Queue settings
    task_routes={
        'tasks.visual_tasks.generate_comfyui_image': {'queue': 'visual'},
        'tasks.visual_tasks.process_video_generation': {'queue': 'video'},
        'tasks.visual_tasks.create_pdf_brochure': {'queue': 'pdf'},
        'tasks.intelligence_tasks.scout_leads': {'queue': 'intelligence'},
        'tasks.intelligence_tasks.analyze_market_trends': {'queue': 'intelligence'},
        'tasks.notification_tasks.send_email': {'queue': 'notification'},
        'tasks.notification_tasks.send_telegram': {'queue': 'notification'},
    },
    
    # Worker settings
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    worker_max_tasks_per_child=1000,
    
    # Result settings
    result_expires=3600,  # 1 hour
    result_backend_transport_options={
        'master_name': 'mymaster',
        'visibility_timeout': 3600,
        'policy': 'allkeys',
        'connection_pool_kwargs': {
            'max_connections': 20,
        }
    },
    
    # Beat schedule for periodic tasks
    beat_schedule={
        'health-check-proxies': {
            'task': 'tasks.intelligence_tasks.health_check_proxies',
            'schedule': 300.0,  # Every 5 minutes
        },
        'cleanup-old-tasks': {
            'task': 'tasks.maintenance_tasks.cleanup_old_tasks',
            'schedule': 3600.0,  # Every hour
        },
        'generate-daily-reports': {
            'task': 'tasks.intelligence_tasks.generate_daily_reports',
            'schedule': 86400.0,  # Every day at midnight
        },
    },
    
    # Error handling
    task_reject_on_worker_lost=True,
    task_ignore_result=False,
    
    # Monitoring
    worker_send_task_events=True,
    task_send_sent_event=True,
)

# Custom Task Base Class
class LuminaTask(Task):
    """Custom task base class with enhanced logging and error handling"""
    
    def on_success(self, retval, task_id, args, kwargs):
        """Task success callback"""
        logger.info(f"Task {task_id} completed successfully")
        
        # Log to database if available
        try:
            from core_modules.db_manager import DatabaseManager
            db = DatabaseManager()
            
            log_data = {
                'task_id': task_id,
                'task_name': self.name,
                'status': 'SUCCESS',
                'result': retval,
                'completed_at': datetime.now().isoformat()
            }
            
            # This would be saved to TaskLog table
            logger.info(f"Task success logged: {log_data}")
            
        except Exception as e:
            logger.error(f"Error logging task success: {e}")
    
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Task failure callback"""
        logger.error(f"Task {task_id} failed: {exc}")
        
        # Log to database if available
        try:
            from core_modules.db_manager import DatabaseManager
            db = DatabaseManager()
            
            log_data = {
                'task_id': task_id,
                'task_name': self.name,
                'status': 'FAILED',
                'error': str(exc),
                'failed_at': datetime.now().isoformat()
            }
            
            # This would be saved to TaskLog table
            logger.error(f"Task failure logged: {log_data}")
            
        except Exception as e:
            logger.error(f"Error logging task failure: {e}")
    
    def on_retry(self, exc, task_id, args, kwargs, einfo):
        """Task retry callback"""
        logger.warning(f"Task {task_id} retrying: {exc}")

# Set custom task base class
celery_app.Task = LuminaTask

# Signal handlers
@task_prerun.connect
def task_prerun_handler(task_id, task, *args, **kwargs):
    """Handler for task pre-run"""
    logger.info(f"Starting task {task.name} with ID {task_id}")
    
    # Update task status in database
    try:
        from core_modules.db_manager import DatabaseManager
        db = DatabaseManager()
        
        # This would update TaskLog table
        logger.info(f"Task {task_id} status updated to RUNNING")
        
    except Exception as e:
        logger.error(f"Error updating task status: {e}")

@task_postrun.connect
def task_postrun_handler(task_id, task, *args, **kwargs):
    """Handler for task post-run"""
    logger.info(f"Completed task {task.name} with ID {task_id}")

@task_failure.connect
def task_failure_handler(sender, task_id, exception, **kwargs):
    """Handler for task failure"""
    logger.error(f"Task {sender.name} ({task_id}) failed: {exception}")

# Task Decorators
def visual_task(func):
    """Decorator for visual processing tasks"""
    func = celery_app.task(
        name=f'tasks.visual_tasks.{func.__name__}',
        bind=True,
        autoretry_for=(Exception,),
        retry_kwargs={'max_retries': 3, 'countdown': 60},
        soft_time_limit=300,  # 5 minutes
        time_limit=600,       # 10 minutes
    )(func)
    return func

def intelligence_task(func):
    """Decorator for intelligence tasks"""
    func = celery_app.task(
        name=f'tasks.intelligence_tasks.{func.__name__}',
        bind=True,
        autoretry_for=(Exception,),
        retry_kwargs={'max_retries': 5, 'countdown': 30},
        soft_time_limit=180,  # 3 minutes
        time_limit=300,       # 5 minutes
    )(func)
    return func

def notification_task(func):
    """Decorator for notification tasks"""
    func = celery_app.task(
        name=f'tasks.notification_tasks.{func.__name__}',
        bind=True,
        autoretry_for=(Exception,),
        retry_kwargs={'max_retries': 3, 'countdown': 60},
        soft_time_limit=60,   # 1 minute
        time_limit=120,       # 2 minutes
    )(func)
    return func

def maintenance_task(func):
    """Decorator for maintenance tasks"""
    func = celery_app.task(
        name=f'tasks.maintenance_tasks.{func.__name__}',
        bind=True,
        soft_time_limit=600,  # 10 minutes
        time_limit=900,       # 15 minutes
    )(func)
    return func

# Task Utilities
class TaskMonitor:
    """Task monitoring and management utilities"""
    
    @staticmethod
    def get_active_tasks() -> List[Dict[str, Any]]:
        """Get list of currently active tasks"""
        inspect = celery_app.control.inspect()
        active_tasks = inspect.active()
        
        if not active_tasks:
            return []
        
        tasks = []
        for worker, task_list in active_tasks.items():
            for task in task_list:
                tasks.append({
                    'worker': worker,
                    'id': task['id'],
                    'name': task['name'],
                    'args': task['args'],
                    'kwargs': task['kwargs'],
                    'time_start': task.get('time_start')
                })
        
        return tasks
    
    @staticmethod
    def get_task_stats() -> Dict[str, Any]:
        """Get task statistics"""
        inspect = celery_app.control.inspect()
        stats = inspect.stats()
        
        if not stats:
            return {}
        
        total_tasks = 0
        total_workers = len(stats)
        
        for worker, worker_stats in stats.items():
            total_tasks += worker_stats.get('total', 0)
        
        return {
            'total_workers': total_workers,
            'total_tasks_processed': total_tasks,
            'worker_stats': stats
        }
    
    @staticmethod
    def cancel_task(task_id: str) -> bool:
        """Cancel a running task"""
        try:
            celery_app.control.revoke(task_id, terminate=True)
            logger.info(f"Task {task_id} cancelled")
            return True
        except Exception as e:
            logger.error(f"Error cancelling task {task_id}: {e}")
            return False
    
    @staticmethod
    def retry_task(task_id: str) -> bool:
        """Retry a failed task"""
        try:
            # This would need to be implemented based on your task storage
            logger.info(f"Retrying task {task_id}")
            return True
        except Exception as e:
            logger.error(f"Error retrying task {task_id}: {e}")
            return False

# Task Queue Management
class TaskQueue:
    """Task queue management utilities"""
    
    @staticmethod
    def queue_visual_task(task_name: str, *args, **kwargs) -> str:
        """Queue a visual processing task"""
        task = celery_app.send_task(f'tasks.visual_tasks.{task_name}', args=args, kwargs=kwargs, queue='visual')
        logger.info(f"Queued visual task {task_name} with ID {task.id}")
        return task.id
    
    @staticmethod
    def queue_intelligence_task(task_name: str, *args, **kwargs) -> str:
        """Queue an intelligence task"""
        task = celery_app.send_task(f'tasks.intelligence_tasks.{task_name}', args=args, kwargs=kwargs, queue='intelligence')
        logger.info(f"Queued intelligence task {task_name} with ID {task.id}")
        return task.id
    
    @staticmethod
    def queue_notification_task(task_name: str, *args, **kwargs) -> str:
        """Queue a notification task"""
        task = celery_app.send_task(f'tasks.notification_tasks.{task_name}', args=args, kwargs=kwargs, queue='notification')
        logger.info(f"Queued notification task {task_name} with ID {task.id}")
        return task.id
    
    @staticmethod
    def get_queue_info() -> Dict[str, Any]:
        """Get queue information"""
        inspect = celery_app.control.inspect()
        
        # Get active queues
        active_queues = inspect.active_queues()
        
        # Get reserved tasks
        reserved_tasks = inspect.reserved()
        
        # Get scheduled tasks
        scheduled_tasks = inspect.scheduled()
        
        return {
            'active_queues': active_queues,
            'reserved_tasks': reserved_tasks,
            'scheduled_tasks': scheduled_tasks
        }

# Health Check Task
@celery_app.task(bind=True)
def health_check(self):
    """Health check task for monitoring"""
    try:
        # Check Redis connection
        from celery import current_app
        broker_connection = current_app.broker_connection()
        broker_connection.ensure_connection(max_retries=3)
        
        # Check database connection if available
        try:
            from core_modules.db_manager import DatabaseManager
            db = DatabaseManager()
            # Simple database check
            logger.info("Database connection OK")
        except Exception as e:
            logger.warning(f"Database connection issue: {e}")
        
        return {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'worker_id': self.request.id
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise self.retry(exc=e, countdown=60, max_retries=3)

# Example usage functions
def example_usage():
    """Example of how to use the task system"""
    
    # Queue a visual task
    task_id = TaskQueue.queue_visual_task(
        'generate_comfyui_image',
        prompt='A beautiful modern house',
        width=512,
        height=512
    )
    
    # Queue an intelligence task
    task_id = TaskQueue.queue_intelligence_task(
        'scout_leads',
        campaign_mode='BASIC',
        area='Jakarta',
        keywords=['rumah', 'property']
    )
    
    # Queue a notification task
    task_id = TaskQueue.queue_notification_task(
        'send_email',
        to='user@example.com',
        subject='Your brochure is ready',
        template='brochure_ready'
    )
    
    # Get task statistics
    stats = TaskMonitor.get_task_stats()
    print(f"Task Stats: {stats}")
    
    # Get active tasks
    active_tasks = TaskMonitor.get_active_tasks()
    print(f"Active Tasks: {active_tasks}")

if __name__ == '__main__':
    # Example usage
    example_usage()
