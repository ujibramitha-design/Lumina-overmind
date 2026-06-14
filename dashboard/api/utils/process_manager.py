import asyncio
import psutil
import os
import signal
from typing import Dict, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from celery import Celery
from tasks.celery_app import celery_app

@dataclass
class ProcessInfo:
    """Data class for process information"""
    task_id: Optional[str] = None
    script_name: str = ""
    status: str = "idle"
    start_time: Optional[datetime] = None
    cpu_percent: float = 0.0
    memory_percent: float = 0.0
    command: str = ""
    result: Optional[Any] = None
    error: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response"""
        return {
            "task_id": self.task_id,
            "status": self.status,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "cpu_percent": self.cpu_percent,
            "memory_percent": self.memory_percent,
            "command": self.command,
            "result": self.result,
            "error": self.error
        }

class RunnerManager:
    """
    LUMINA OVERMIND SYSTEM - Async Process Manager
    
    Manages Python script execution via Celery distributed task queue.
    Provides start, stop, monitoring, and cleanup functionality for background processes.
    
    Attributes:
        processes (Dict[str, ProcessInfo]): In-memory tracking of active processes
        runner_mapping (Dict[str, str]): Maps runner names to script file paths
        celery_app (Celery): Celery application instance for task distribution
    """
    
    def __init__(self):
        """
        Initialize the RunnerManager with process tracking and script mappings.
        
        Sets up the process registry and defines available script runners
        for the Lumina Overmind System intelligence modules.
        """
        self.processes: Dict[str, ProcessInfo] = {}
        self.runner_mapping = {
            'lead_generation': 'run_lead_generation.py',
            'banten_government': 'run_banten_government_intelligence.py', 
            'ride_hailing': 'run_ride_hailing_intelligence.py',
            'property_scraper': 'run_property_market_scraper.py',
            'social_verifier': 'run_social_proof_verifier.py',
            'behavioral_tester': 'run_behavioral_velocity_tester.py'
        }
        self.celery_app = celery_app
    
    def start_runner(self, script_name: str) -> Dict[str, Any]:
        """
        Start a Python script as a Celery task (non-blocking)
        
        Args:
            script_name: Name of the script (mapped to actual file)
            
        Returns:
            Dict with success status and task info
        """
        try:
            # Check if already running
            if script_name in self.processes and self.processes[script_name].status in ['running', 'pending']:
                return {
                    "success": False,
                    "error": f"Runner {script_name} is already running",
                    "status": "Running"
                }
            
            # Get actual script file name
            script_file = self.runner_mapping.get(script_name, f"{script_name}.py")
            
            # Check if script file exists
            if not os.path.exists(script_file):
                return {
                    "success": False,
                    "error": f"Script file {script_file} not found",
                    "status": "Error"
                }
            
            # Create Celery task for running the script
            task = self.celery_app.send_task(
                'tasks.run_script_task',
                args=[script_file],
                kwargs={
                    'script_name': script_name,
                    'working_dir': os.getcwd()
                }
            )
            
            # Store task info
            process_info = ProcessInfo(
                task_id=task.id,
                script_name=script_name,
                status="pending",
                start_time=datetime.now(),
                command=f"python {script_file}"
            )
            
            self.processes[script_name] = process_info
            
            return {
                "success": True,
                "task_id": task.id,
                "script_name": script_name,
                "status": "pending",
                "start_time": process_info.start_time.isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "status": "Error"
            }
    
    def stop_runner(self, script_name: str) -> Dict[str, Any]:
        """
        Stop a running Celery task safely
        
        Args:
            script_name: Name of the script to stop
            
        Returns:
            Dict with success status and task info
        """
        try:
            if script_name not in self.processes:
                return {
                    "success": False,
                    "error": f"Runner {script_name} is not running",
                    "status": "Idle"
                }
            
            process_info = self.processes[script_name]
            
            if process_info.task_id:
                try:
                    # Revoke the Celery task
                    self.celery_app.control.revoke(process_info.task_id, terminate=True)
                    
                    # Update status
                    process_info.status = "stopped"
                    process_info.error = "Task revoked by user"
                    
                except Exception as revoke_error:
                    return {
                        "success": False,
                        "error": f"Failed to revoke task: {str(revoke_error)}",
                        "status": "Error"
                    }
            
            # Remove from tracking
            del self.processes[script_name]
            
            return {
                "success": True,
                "script_name": script_name,
                "status": "Stopped",
                "message": f"Runner {script_name} stopped successfully"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "status": "Error"
            }
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get status of all runners with live Celery task information
        
        Returns:
            Dict with status of all runners
        """
        runners_status = {}
        
        for script_name, process_info in list(self.processes.items()):
            try:
                if process_info.task_id:
                    # Get Celery task result
                    task_result = self.celery_app.AsyncResult(process_info.task_id)
                    
                    # Update status based on Celery task state
                    if task_result.state == 'PENDING':
                        process_info.status = 'pending'
                    elif task_result.state == 'PROGRESS':
                        process_info.status = 'running'
                        # Get progress info if available
                        if hasattr(task_result.info, 'get'):
                            process_info.cpu_percent = task_result.info.get('cpu_percent', 0)
                            process_info.memory_percent = task_result.info.get('memory_percent', 0)
                    elif task_result.state == 'SUCCESS':
                        process_info.status = 'completed'
                        process_info.result = task_result.result
                    elif task_result.state == 'FAILURE':
                        process_info.status = 'failed'
                        process_info.error = str(task_result.info)
                    else:
                        process_info.status = task_result.state.lower()
                    
                    runners_status[script_name] = {
                        "task_id": process_info.task_id,
                        "status": process_info.status,
                        "start_time": process_info.start_time.isoformat() if process_info.start_time else None,
                        "cpu_percent": process_info.cpu_percent,
                        "memory_percent": process_info.memory_percent,
                        "command": process_info.command,
                        "result": process_info.result,
                        "error": process_info.error
                    }
                else:
                    runners_status[script_name] = {
                        "status": "idle",
                        "message": "No task ID"
                    }
                    
            except Exception as e:
                runners_status[script_name] = {
                    "status": "error",
                    "message": str(e)
                }
        
        # Add idle runners that are not running
        for runner_name in self.runner_mapping.keys():
            if runner_name not in runners_status:
                runners_status[runner_name] = {
                    "status": "idle",
                    "message": "Not started"
                }
        
        # Clean up completed/failed tasks
        self.cleanup_dead_processes()
        
        return {
            "runners": runners_status,
            "total_running": len([p for p in self.processes.values() if p.status in ['running', 'pending']]),
            "timestamp": datetime.now().isoformat()
        }
    
    def get_runner_info(self, script_name: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific runner
        
        Args:
            script_name: Name of the script
            
        Returns:
            Dict with runner info or None if not found
        """
        if script_name not in self.processes:
            return None
        
        process_info = self.processes[script_name]
        
        try:
            process = psutil.Process(process_info.pid)
            
            return {
                "script_name": script_name,
                "pid": process_info.pid,
                "status": "Running" if process.is_running() else "Stopped",
                "start_time": process_info.start_time.isoformat(),
                "cpu_percent": round(process.cpu_percent(), 2),
                "memory_percent": round(process.memory_percent(), 2),
                "memory_mb": round(process.memory_info().rss / 1024 / 1024, 2),
                "command": process_info.command,
                "create_time": datetime.fromtimestamp(process.create_time()).isoformat()
            }
            
        except psutil.NoSuchProcess:
            return {
                "script_name": script_name,
                "pid": process_info.pid,
                "status": "Stopped",
                "message": "Process not found"
            }
        except Exception as e:
            return {
                "script_name": script_name,
                "pid": process_info.pid,
                "status": "Error",
                "message": str(e)
            }
    
    def cleanup_dead_processes(self) -> int:
        """
        Clean up completed/failed tasks from tracking
        
        Returns:
            Number of processes cleaned up
        """
        dead_tasks = []
        
        for script_name, process_info in self.processes.items():
            try:
                if process_info.task_id:
                    task_result = self.celery_app.AsyncResult(process_info.task_id)
                    
                    # Clean up if task is completed, failed, or revoked
                    if task_result.state in ['SUCCESS', 'FAILURE', 'REVOKED']:
                        dead_tasks.append(script_name)
                else:
                    # No task ID, consider it dead
                    dead_tasks.append(script_name)
                    
            except Exception:
                # Error checking task status, consider it dead
                dead_tasks.append(script_name)
        
        for script_name in dead_tasks:
            del self.processes[script_name]
        
        return len(dead_tasks)

# Global instance
runner_manager = RunnerManager()
