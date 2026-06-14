"""
JARVIS Scheduler
================

Cron job scheduler for JARVIS automated tasks.
Handles nightly memory pruning, proactive messages, and other scheduled tasks.
"""

import asyncio
import logging
from datetime import datetime, time
from typing import Dict, Any, Callable, Optional
import schedule
import threading

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class JarvisScheduler:
    """
    Scheduler for JARVIS automated tasks.
    Runs scheduled jobs including memory pruning, proactive messages, etc.
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
        # Scheduled jobs
        self.jobs: Dict[str, Callable] = {}
        
        # Running state
        self.is_running = False
        self.scheduler_thread: Optional[threading.Thread] = None
        
        # Task configurations
        self.task_configs = {
            'memory_pruning': {
                'enabled': config.get('memory_pruning_enabled', True),
                'time': config.get('memory_pruning_time', '02:00'),
                'description': 'Nightly memory pruning and summarization',
            },
            'observer_loop': {
                'enabled': config.get('observer_loop_enabled', True),
                'day': config.get('observer_loop_day', 'sunday'),  # Weekly on Sunday
                'time': config.get('observer_loop_time', '03:00'),
                'description': 'Weekly self-refinement and autonomous fixes',
            },
            'spontaneity': {
                'enabled': config.get('spontaneity_enabled', True),
                'interval': config.get('spontaneity_interval', 4),  # Every 4 hours
                'description': 'Spontaneous conversation initiation based on inactivity',
            },
            'morning_greeting': {
                'enabled': config.get('morning_greeting_enabled', True),
                'time': config.get('morning_greeting_time', '08:00'),
                'description': 'Morning greeting message',
            },
            'daily_summary': {
                'enabled': config.get('daily_summary_enabled', True),
                'time': config.get('daily_summary_time', '18:00'),
                'description': 'Daily summary report',
            },
            'health_check': {
                'enabled': config.get('health_check_enabled', True),
                'interval': config.get('health_check_interval', 60),  # minutes
                'description': 'Periodic health check',
            },
        }
    
    def register_job(self, job_name: str, job_func: Callable):
        """Register a scheduled job"""
        self.jobs[job_name] = job_func
        logger.info(f"Registered job: {job_name}")
    
    async def start(self):
        """Start the scheduler"""
        if self.is_running:
            logger.warning("Scheduler is already running")
            return
        
        self.is_running = True
        logger.info("🕐 Starting JARVIS Scheduler")
        
        # Schedule jobs
        self._schedule_jobs()
        
        # Start scheduler thread
        self.scheduler_thread = threading.Thread(
            target=self._run_scheduler,
            daemon=True
        )
        self.scheduler_thread.start()
        
        logger.info("✅ Scheduler started")
    
    def stop(self):
        """Stop the scheduler"""
        if not self.is_running:
            return
        
        self.is_running = False
        schedule.clear()
        
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)
        
        logger.info("✅ Scheduler stopped")
    
    def _schedule_jobs(self):
        """Schedule all configured jobs"""
        # Memory pruning (nightly)
        if self.task_configs['memory_pruning']['enabled']:
            schedule.every().day.at(
                self.task_configs['memory_pruning']['time']
            ).do(self._run_job, 'memory_pruning')
            logger.info(f"Scheduled memory pruning at {self.task_configs['memory_pruning']['time']}")
        
        # Observer Loop (weekly)
        if self.task_configs['observer_loop']['enabled']:
            day = self.task_configs['observer_loop']['day']
            time = self.task_configs['observer_loop']['time']
            getattr(schedule.every(), day).at(time).do(self._run_job, 'observer_loop')
            logger.info(f"Scheduled observer loop on {day} at {time}")
        
        # Spontaneity (hourly)
        if self.task_configs['spontaneity']['enabled']:
            interval = self.task_configs['spontaneity']['interval']
            schedule.every(interval).hours.do(self._run_job, 'spontaneity')
            logger.info(f"Scheduled spontaneity every {interval} hours")
        
        # Morning greeting
        if self.task_configs['morning_greeting']['enabled']:
            schedule.every().day.at(
                self.task_configs['morning_greeting']['time']
            ).do(self._run_job, 'morning_greeting')
            logger.info(f"Scheduled morning greeting at {self.task_configs['morning_greeting']['time']}")
        
        # Daily summary
        if self.task_configs['daily_summary']['enabled']:
            schedule.every().day.at(
                self.task_configs['daily_summary']['time']
            ).do(self._run_job, 'daily_summary')
            logger.info(f"Scheduled daily summary at {self.task_configs['daily_summary']['time']}")
        
        # Health check (periodic)
        if self.task_configs['health_check']['enabled']:
            interval = self.task_configs['health_check']['interval']
            schedule.every(interval).minutes.do(self._run_job, 'health_check')
            logger.info(f"Scheduled health check every {interval} minutes")
    
    def _run_scheduler(self):
        """Run the scheduler loop"""
        while self.is_running:
            schedule.run_pending()
            threading.Event().wait(1)  # Sleep for 1 second
    
    def _run_job(self, job_name: str):
        """Run a scheduled job"""
        logger.info(f"🔄 Running job: {job_name}")
        
        job_func = self.jobs.get(job_name)
        
        if job_func is None:
            logger.warning(f"No function registered for job: {job_name}")
            return
        
        try:
            # Run the job function
            if asyncio.iscoroutinefunction(job_func):
                # Run async job in event loop
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    loop.run_until_complete(job_func())
                finally:
                    loop.close()
            else:
                # Run sync job
                job_func()
            
            logger.info(f"✅ Job completed: {job_name}")
        
        except Exception as e:
            logger.error(f"❌ Job failed: {job_name} - {e}")
    
    def get_scheduled_jobs(self) -> Dict[str, Any]:
        """Get information about scheduled jobs"""
        return {
            'jobs': [
                {
                    'name': name,
                    'enabled': config['enabled'],
                    'time': config.get('time', config.get('interval', 'N/A')),
                    'description': config['description'],
                    'next_run': str(schedule.next_run()) if schedule.next_run() else None,
                }
                for name, config in self.task_configs.items()
            ],
            'is_running': self.is_running,
        }

# Singleton instance
scheduler: Optional[JarvisScheduler] = None

def get_scheduler(config: Dict[str, Any] = None) -> JarvisScheduler:
    """Get or create scheduler singleton"""
    global scheduler
    
    if scheduler is None:
        if config is None:
            config = {}
        scheduler = JarvisScheduler(config)
    
    return scheduler
