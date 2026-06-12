"""
LUMINA OS - RUNNER TASKS
========================

Celery tasks for running Python scripts asynchronously
without blocking the main FastAPI server.
"""

import os
import sys
import subprocess
import psutil
import time
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from celery import Task
from tasks.celery_app import celery_app

# Add root directory to Python path
root_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root_dir)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ScriptRunnerTask(Task):
    """Custom Celery task class for running Python scripts"""
    
    def on_success(self, retval, task_id, args, kwargs):
        """Handle successful task completion"""
        logger.info(f"✅ Task {task_id} completed successfully")
        super().on_success(retval, task_id, args, kwargs)
    
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Handle task failure"""
        logger.error(f"❌ Task {task_id} failed: {exc}")
        super().on_failure(exc, task_id, args, kwargs, einfo)
    
    def on_progress(self, task_id, **kwargs):
        """Handle progress updates"""
        self.update_state(
            state='PROGRESS',
            meta=kwargs
        )


@celery_app.task(bind=True, base=ScriptRunnerTask)
def run_script_task(self, script_file: str, script_name: str, working_dir: str) -> Dict[str, Any]:
    """
    Run a Python script as a subprocess with progress monitoring
    
    Args:
        script_file: Path to the Python script file
        script_name: Name of the script for tracking
        working_dir: Working directory for the script
        
    Returns:
        Dict with execution results
    """
    try:
        logger.info(f"🚀 Starting script execution: {script_file}")
        
        # Update task state to running
        self.update_state(
            state='PROGRESS',
            meta={
                'status': 'starting',
                'script_name': script_name,
                'cpu_percent': 0,
                'memory_percent': 0,
                'start_time': datetime.now().isoformat()
            }
        )
        
        # Start the subprocess
        process = subprocess.Popen(
            ['python', script_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=working_dir
        )
        
        logger.info(f"📋 Process started with PID: {process.pid}")
        
        # Monitor the process
        start_time = time.time()
        last_update = start_time
        
        while process.poll() is None:
            try:
                # Get process metrics
                ps_process = psutil.Process(process.pid)
                cpu_percent = ps_process.cpu_percent()
                memory_percent = ps_process.memory_percent()
                
                # Update progress every 2 seconds
                current_time = time.time()
                if current_time - last_update >= 2:
                    self.update_state(
                        state='PROGRESS',
                        meta={
                            'status': 'running',
                            'script_name': script_name,
                            'pid': process.pid,
                            'cpu_percent': round(cpu_percent, 2),
                            'memory_percent': round(memory_percent, 2),
                            'runtime': round(current_time - start_time, 2)
                        }
                    )
                    last_update = current_time
                
                # Sleep to avoid excessive CPU usage
                time.sleep(0.5)
                
            except psutil.NoSuchProcess:
                logger.warning(f"⚠️ Process {process.pid} no longer exists")
                break
            except Exception as e:
                logger.error(f"❌ Error monitoring process: {e}")
                break
        
        # Get the final result
        stdout, stderr = process.communicate()
        return_code = process.returncode
        
        execution_time = time.time() - start_time
        
        # Prepare result
        result = {
            'script_name': script_name,
            'script_file': script_file,
            'pid': process.pid,
            'return_code': return_code,
            'execution_time': round(execution_time, 2),
            'stdout': stdout,
            'stderr': stderr,
            'success': return_code == 0,
            'end_time': datetime.now().isoformat()
        }
        
        if return_code == 0:
            logger.info(f"✅ Script {script_name} completed successfully in {execution_time:.2f}s")
        else:
            logger.error(f"❌ Script {script_name} failed with return code {return_code}")
            result['error'] = stderr if stderr else f"Process exited with code {return_code}"
        
        return result
        
    except Exception as e:
        logger.error(f"❌ Critical error running script {script_name}: {e}")
        return {
            'script_name': script_name,
            'script_file': script_file,
            'success': False,
            'error': str(e),
            'end_time': datetime.now().isoformat()
        }


@celery_app.task
def cleanup_runner_tasks() -> Dict[str, Any]:
    """
    Clean up completed/failed runner tasks
    
    Returns:
        Dict with cleanup results
    """
    try:
        inspect = celery_app.control.inspect()
        
        # Get active tasks
        active_tasks = inspect.active()
        if active_tasks is None:
            active_tasks = {}
        
        # Get scheduled tasks  
        scheduled_tasks = inspect.scheduled()
        if scheduled_tasks is None:
            scheduled_tasks = {}
        
        # Count tasks by worker
        total_active = sum(len(tasks) for tasks in active_tasks.values())
        total_scheduled = sum(len(tasks) for tasks in scheduled_tasks.values())
        
        logger.info(f"🧹 Cleanup check: {total_active} active, {total_scheduled} scheduled tasks")
        
        return {
            'success': True,
            'active_tasks': total_active,
            'scheduled_tasks': total_scheduled,
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Error during cleanup: {e}")
        return {
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }


@celery_app.task
def get_system_metrics() -> Dict[str, Any]:
    """
    Get system performance metrics for monitoring
    
    Returns:
        Dict with system metrics
    """
    try:
        # CPU metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        
        # Memory metrics
        memory = psutil.virtual_memory()
        
        # Disk metrics
        disk = psutil.disk_usage('/')
        
        # Network metrics (basic)
        network = psutil.net_io_counters()
        
        metrics = {
            'cpu': {
                'percent': cpu_percent,
                'count': cpu_count
            },
            'memory': {
                'total': memory.total,
                'available': memory.available,
                'percent': memory.percent,
                'used': memory.used
            },
            'disk': {
                'total': disk.total,
                'used': disk.used,
                'free': disk.free,
                'percent': (disk.used / disk.total) * 100
            },
            'network': {
                'bytes_sent': network.bytes_sent,
                'bytes_recv': network.bytes_recv,
                'packets_sent': network.packets_sent,
                'packets_recv': network.packets_recv
            },
            'timestamp': datetime.now().isoformat()
        }
        
        return metrics
        
    except Exception as e:
        logger.error(f"❌ Error getting system metrics: {e}")
        return {
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }
