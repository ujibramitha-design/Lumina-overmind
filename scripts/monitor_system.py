"""
LUMINA OS Go-Live Dashboard - Real-time System Monitoring
Production Runner Status Monitoring for Enterprise Deployment

Author: HUNTER_AGENT_AI_MARKETING_DIGITAL
Version: 1.0.0
"""

import os
import sys
import time
import json
import psutil
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any
from dataclasses import dataclass
from enum import Enum

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class RunnerStatus(Enum):
    """Production Runner Status"""
    ACTIVE = "ACTIVE"
    IDLE = "IDLE"
    ERROR = "ERROR"
    STOPPED = "STOPPED"
    UNKNOWN = "UNKNOWN"

@dataclass
class ProductionRunner:
    """Production Runner Information"""
    id: str
    name: str
    status: RunnerStatus
    pid: int = None
    cpu_percent: float = 0.0
    memory_percent: float = 0.0
    memory_mb: float = 0.0
    uptime_seconds: float = 0.0
    last_activity: datetime = None
    error_count: int = 0
    success_count: int = 0
    tasks_completed: int = 0
    start_time: datetime = None
    last_error: str = ""

class SystemMonitor:
    """Real-time system monitoring dashboard"""
    
    def __init__(self):
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.runners: Dict[str, ProductionRunner] = {}
        self.system_stats = {}
        self.monitoring_active = False
        self.refresh_interval = 2  # seconds
        self.start_time = datetime.now()
        
        # Define production runners
        self.runner_configs = [
            {"id": "market_intelligence", "name": "Market Intelligence Agent", "module": "agents.scout_agent.market_intelligence"},
            {"id": "lead_hunter", "name": "Lead Hunter Agent", "module": "agents.scout_agent.lead_hunter"},
            {"id": "scoring_engine", "name": "Lead Scoring Engine", "module": "agents.scout_agent.scoring_logic"},
            {"id": "sales_consultant", "name": "Sales Consultant", "module": "agents.closer_agent.sales_consultant"},
            {"id": "follow_up_manager", "name": "Follow-up Manager", "module": "agents.closer_agent.follow_up_manager"},
            {"id": "geo_mapper", "name": "Geo Mapper", "module": "core_modules.geo_mapper"},
            {"id": "trend_analyzer", "name": "Trend Analyzer", "module": "core_modules.trend_analyzer"},
            {"id": "lead_validator", "name": "Lead Validator", "module": "core_modules.lead_validator"},
            {"id": "compliance_manager", "name": "Compliance Manager", "module": "core_modules.governance.compliance_manager"},
            {"id": "lumina_dashboard", "name": "LUMINA Dashboard", "module": "lumina_os.app"},
        ]
        
        # Initialize runners
        self._initialize_runners()
    
    def _initialize_runners(self):
        """Initialize production runners"""
        for config in self.runner_configs:
            runner = ProductionRunner(
                id=config["id"],
                name=config["name"],
                status=RunnerStatus.IDLE,
                start_time=datetime.now()
            )
            self.runners[config["id"]] = runner
    
    def start_monitoring(self):
        """Start real-time monitoring"""
        if self.monitoring_active:
            print("⚠️ Monitoring is already active")
            return
        
        self.monitoring_active = True
        print("🚀 Starting LUMINA OS System Monitoring...")
        print("=" * 60)
        
        try:
            while self.monitoring_active:
                self._update_system_stats()
                self._update_runner_stats()
                self._display_dashboard()
                time.sleep(self.refresh_interval)
        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped by user")
        finally:
            self.monitoring_active = False
    
    def _update_system_stats(self):
        """Update system-wide statistics"""
        try:
            # CPU and Memory
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Network I/O
            network = psutil.net_io_counters()
            
            # Process count
            process_count = len(psutil.pids())
            
            self.system_stats = {
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_used_gb': memory.used / (1024**3),
                'memory_total_gb': memory.total / (1024**3),
                'disk_used_gb': disk.used / (1024**3),
                'disk_total_gb': disk.total / (1024**3),
                'network_bytes_sent': network.bytes_sent,
                'network_bytes_recv': network.bytes_recv,
                'process_count': process_count,
                'uptime_seconds': (datetime.now() - self.start_time).total_seconds()
            }
        except Exception as e:
            print(f"⚠️ Error updating system stats: {e}")
    
    def _update_runner_stats(self):
        """Update individual runner statistics"""
        for runner_id, runner in self.runners.items():
            try:
                # Simulate runner status (in real implementation, this would check actual processes)
                if runner.status == RunnerStatus.ACTIVE:
                    # Simulate resource usage
                    runner.cpu_percent = min(95, runner.cpu_percent + (hash(runner_id) % 10))
                    runner.memory_percent = min(95, runner.memory_percent + (hash(runner_id) % 15))
                    runner.memory_mb = runner.memory_percent * 100  # Simulated memory usage
                    runner.uptime_seconds = (datetime.now() - runner.start_time).total_seconds()
                    
                    # Simulate task completion
                    if hash(runner_id) % 10 == 0:
                        runner.tasks_completed += 1
                        runner.success_count += 1
                    elif hash(runner_id) % 50 == 0:
                        runner.error_count += 1
                        runner.last_error = f"Simulated error in {runner.name}"
                        runner.status = RunnerStatus.ERROR
                    
                    # Random status changes
                    if hash(runner_id) % 100 == 0 and runner.status == RunnerStatus.ACTIVE:
                        runner.status = RunnerStatus.IDLE
                        runner.last_activity = datetime.now()
                    elif hash(runner_id) % 80 == 0 and runner.status == RunnerStatus.IDLE:
                        runner.status = RunnerStatus.ACTIVE
                        runner.last_activity = datetime.now()
                
                elif runner.status == RunnerStatus.ERROR:
                    # Auto-recover from errors
                    if runner.error_count < 3:
                        runner.status = RunnerStatus.IDLE
                        runner.last_error = ""
                    else:
                        runner.status = RunnerStatus.STOPPED
                
            except Exception as e:
                print(f"⚠️ Error updating runner {runner_id}: {e}")
                runner.status = RunnerStatus.ERROR
                runner.last_error = str(e)
    
    def _display_dashboard(self):
        """Display real-time monitoring dashboard"""
        # Clear screen (works on most terminals)
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("🔍 LUMINA OS GO-LIVE DASHBOARD")
        print("=" * 60)
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Uptime: {self._format_uptime(self.system_stats.get('uptime_seconds', 0))}")
        print()
        
        # System Overview
        print("🖥️ SYSTEM OVERVIEW")
        print("-" * 40)
        print(f"CPU Usage: {self.system_stats.get('cpu_percent', 0):.1f}%")
        print(f"Memory Usage: {self.system_stats.get('memory_percent', 0):.1f}% ({self.system_stats.get('memory_used_gb', 0):.1f}GB / {self.system_stats.get('memory_total_gb', 0):.1f}GB)")
        print(f"Disk Usage: {self.system_stats.get('disk_used_gb', 0):.1f}GB / {self.system_stats.get('disk_total_gb', 0):.1f}GB")
        print(f"Processes: {self.system_stats.get('process_count', 0)}")
        print(f"Network I/O: ↑{self._format_bytes(self.system_stats.get('network_bytes_sent', 0))} ↓{self._format_bytes(self.system_stats.get('network_bytes_recv', 0))}")
        print()
        
        # Production Runners Status
        print("🚀 PRODUCTION RUNNERS")
        print("-" * 40)
        
        # Status summary
        status_counts = {}
        for runner in self.runners.values():
            status_counts[runner.status] = status_counts.get(runner.status, 0) + 1
        
        print(f"🟢 Active: {status_counts.get(RunnerStatus.ACTIVE, 0)}")
        print(f"🟡 Idle: {status_counts.get(RunnerStatus.IDLE, 0)}")
        print(f"🔴 Error: {status_counts.get(RunnerStatus.ERROR, 0)}")
        print(f"⚫ Stopped: {status_counts.get(RunnerStatus.STOPPED, 0)}")
        print()
        
        # Detailed Runner Information
        print("📊 RUNNER DETAILS")
        print("-" * 40)
        
        # Sort runners by status (Active first, then by name)
        sorted_runners = sorted(
            self.runners.values(),
            key=lambda x: (x.status.value != RunnerStatus.ACTIVE.value, x.name.lower())
        )
        
        for runner in sorted_runners:
            status_icon = self._get_status_icon(runner.status)
            cpu_bar = self._create_progress_bar(runner.cpu_percent, 20)
            mem_bar = self._create_progress_bar(runner.memory_percent, 20)
            
            print(f"{status_icon} {runner.name:20} | {runner.status:8} | CPU: {cpu_bar} | MEM: {mem_bar}")
            print(f"    📊 Tasks: {runner.tasks_completed} | ✅ Success: {runner.success_count} | ❌ Errors: {runner.error_count}")
            print(f"    ⏱️ Uptime: {self._format_uptime(runner.uptime_seconds)}")
            
            if runner.last_error:
                print(f"    ⚠️ Last Error: {runner.last_error}")
            
            if runner.last_activity:
                print(f"    🕐 Last Activity: {runner.last_activity.strftime('%H:%M:%S')}")
            
            print()
        
        # Performance Metrics
        print("📈 PERFORMANCE METRICS")
        print("-" * 40)
        
        total_tasks = sum(runner.tasks_completed for runner in self.runners.values())
        total_success = sum(runner.success_count for runner in self.runners.values())
        total_errors = sum(runner.error_count for runner in self.runners.values())
        
        success_rate = (total_success / max(1, total_success + total_errors)) * 100 if (total_success + total_errors) > 0 else 100
        
        print(f"📊 Total Tasks Completed: {total_tasks}")
        print(f"✅ Success Rate: {success_rate:.1f}%")
        print(f"❌ Total Errors: {total_errors}")
        print(f"🚀 Active Runners: {status_counts.get(RunnerStatus.ACTIVE, 0)}")
        print()
        
        # Health Indicators
        print("🏥 HEALTH INDICATORS")
        print("-" * 40)
        
        health_score = self._calculate_health_score()
        health_status = self._get_health_status(health_score)
        
        print(f"🏥 Overall Health: {health_status} ({health_score}/100)")
        
        # Individual health checks
        health_checks = [
            ("CPU Usage", self.system_stats.get('cpu_percent', 0) < 80),
            ("Memory Usage", self.system_stats.get('memory_percent', 0) < 85),
            ("Disk Space", (self.system_stats.get('disk_used_gb', 0) / max(1, self.system_stats.get('disk_total_gb', 1))) < 0.9),
            ("Error Rate", total_errors < 5),
            ("Active Runners", status_counts.get(RunnerStatus.ACTIVE, 0) >= 3),
        ]
        
        for check_name, is_healthy in health_checks:
            status_icon = "✅" if is_healthy else "⚠️"
            print(f"{status_icon} {check_name}")
        
        print()
        print("📋 COMMANDS: [R]efresh [Q]uit [S]ave Report [H]elp")
    
    def _get_status_icon(self, status: RunnerStatus) -> str:
        """Get status icon for display"""
        icons = {
            RunnerStatus.ACTIVE: "🟢",
            RunnerStatus.IDLE: "🟡",
            RunnerStatus.ERROR: "🔴",
            RunnerStatus.STOPPED: "⚫",
            RunnerStatus.UNKNOWN: "❓"
        }
        return icons.get(status, "❓")
    
    def _create_progress_bar(self, percentage: float, width: int = 20) -> str:
        """Create a text progress bar"""
        filled = int(width * (percentage / 100))
        empty = width - filled
        return f"[{'█' * filled}{'░' * empty}] {percentage:5.1f}%"
    
    def _format_uptime(self, seconds: float) -> str:
        """Format uptime in human readable format"""
        if seconds < 60:
            return f"{seconds:.0f}s"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.0f}m"
        elif seconds < 86400:
            hours = seconds / 3600
            return f"{hours:.0f}h"
        else:
            days = seconds / 86400
            return f"{days:.1f}d"
    
    def _format_bytes(self, bytes_value: int) -> str:
        """Format bytes in human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.0f}{unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.0f}PB"
    
    def _calculate_health_score(self) -> int:
        """Calculate overall system health score"""
        score = 100
        
        # CPU penalty
        cpu_percent = self.system_stats.get('cpu_percent', 0)
        if cpu_percent > 90:
            score -= 20
        elif cpu_percent > 80:
            score -= 10
        elif cpu_percent > 70:
            score -= 5
        
        # Memory penalty
        memory_percent = self.system_stats.get('memory_percent', 0)
        if memory_percent > 90:
            score -= 20
        elif memory_percent > 85:
            score -= 10
        elif memory_percent > 75:
            score -= 5
        
        # Error penalty
        total_errors = sum(runner.error_count for runner in self.runners.values())
        if total_errors > 10:
            score -= 30
        elif total_errors > 5:
            score -= 15
        elif total_errors > 2:
            score -= 5
        
        # Active runners bonus/penalty
        active_count = sum(1 for runner in self.runners.values() if runner.status == RunnerStatus.ACTIVE)
        if active_count == 0:
            score -= 25
        elif active_count < 3:
            score -= 10
        elif active_count > 8:
            score -= 5
        
        return max(0, score)
    
    def _get_health_status(self, score: int) -> str:
        """Get health status based on score"""
        if score >= 90:
            return "EXCELLENT"
        elif score >= 75:
            return "GOOD"
        elif score >= 60:
            return "FAIR"
        else:
            return "POOR"
    
    def save_report(self, filename: str = None):
        """Save monitoring report to file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"monitoring_report_{timestamp}.json"
        
        report_path = os.path.join(self.project_root, 'logs', filename)
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'system_stats': self.system_stats,
            'runners': {
                runner_id: {
                    'name': runner.name,
                    'status': runner.status.value,
                    'cpu_percent': runner.cpu_percent,
                    'memory_percent': runner.memory_percent,
                    'memory_mb': runner.memory_mb,
                    'uptime_seconds': runner.uptime_seconds,
                    'tasks_completed': runner.tasks_completed,
                    'success_count': runner.success_count,
                    'error_count': runner.error_count,
                    'last_error': runner.last_error,
                    'last_activity': runner.last_activity.isoformat() if runner.last_activity else None,
                    'start_time': runner.start_time.isoformat()
                }
                for runner_id, runner in self.runners.items()
            },
            'health_score': self._calculate_health_score(),
            'uptime_seconds': self.system_stats.get('uptime_seconds', 0)
        }
        
        with open(report_path, 'w') as f:
            json.dump(report_data, f, indent=2, default=str)
        
        print(f"📄 Report saved to: {report_path}")
    
    def get_runner_status(self, runner_id: str) -> Dict[str, Any]:
        """Get detailed status for a specific runner"""
        if runner_id not in self.runners:
            return {"error": f"Runner '{runner_id}' not found"}
        
        runner = self.runners[runner_id]
        return {
            'id': runner.id,
            'name': runner.name,
            'status': runner.status.value,
            'cpu_percent': runner.cpu_percent,
            'memory_percent': runner.memory_percent,
            'memory_mb': runner.memory_mb,
            'uptime_seconds': runner.uptime_seconds,
            'tasks_completed': runner.tasks_completed,
            'success_count': runner.success_count,
            'error_count': runner.error_count,
            'last_error': runner.last_error,
            'last_activity': runner.last_activity.isoformat() if runner.last_activity else None,
            'start_time': runner.start_time.isoformat()
        }
    
    def start_runner(self, runner_id: str) -> bool:
        """Start a specific runner"""
        if runner_id not in self.runners:
            return False
        
        runner = self.runners[runner_id]
        if runner.status == RunnerStatus.STOPPED:
            runner.status = RunnerStatus.IDLE
            runner.start_time = datetime.now()
            runner.error_count = 0
            runner.last_error = ""
            return True
        
        return False
    
    def stop_runner(self, runner_id: str) -> bool:
        """Stop a specific runner"""
        if runner_id not in self.runners:
            return False
        
        runner = self.runners[runner_id]
        runner.status = RunnerStatus.STOPPED
        runner.last_activity = datetime.now()
        return True
    
    def get_system_summary(self) -> Dict[str, Any]:
        """Get system summary for API endpoints"""
        status_counts = {}
        for runner in self.runners.values():
            status_counts[runner.status] = status_counts.get(runner.status, 0) + 1
        
        return {
            'timestamp': datetime.now().isoformat(),
            'health_score': self._calculate_health_score(),
            'total_runners': len(self.runners),
            'active_runners': status_counts.get(RunnerStatus.ACTIVE, 0),
            'idle_runners': status_counts.get(RunnerStatus.IDLE, 0),
            'error_runners': status_counts.get(RunnerStatus.ERROR, 0),
            'stopped_runners': status_counts.get(RunnerStatus.STOPPED, 0),
            'system_cpu': self.system_stats.get('cpu_percent', 0),
            'system_memory': self.system_stats.get('memory_percent', 0),
            'total_tasks': sum(runner.tasks_completed for runner in self.runners.values()),
            'total_errors': sum(runner.error_count for runner in self.runners.values()),
            'uptime_seconds': self.system_stats.get('uptime_seconds', 0)
        }

def main():
    """Main function to run system monitor"""
    print("🔍 LUMINA OS Go-Live Dashboard")
    print("=" * 50)
    print("Real-time Production Runner Monitoring")
    print()
    
    monitor = SystemMonitor()
    
    try:
        # Start monitoring in a separate thread
        monitor_thread = threading.Thread(target=monitor.start_monitoring, daemon=True)
        monitor_thread.start()
        
        # Wait for user input
        while True:
            command = input("\n> ").strip().lower()
            
            if command == 'q' or command == 'quit':
                break
            elif command == 'r' or command == 'refresh':
                monitor._update_system_stats()
                monitor._update_runner_stats()
                monitor._display_dashboard()
            elif command == 's' or command == 'save':
                monitor.save_report()
            elif command == 'h' or command == 'help':
                print("\n🔧 AVAILABLE COMMANDS:")
                print("  [R]efresh - Force refresh dashboard")
                print("  [Q]uit - Exit monitoring")
                print("  [S]ave - Save monitoring report")
                print("  [H]elp - Show this help")
            else:
                print("❌ Unknown command. Type [H]elp for available commands.")
    
    except KeyboardInterrupt:
        pass
    finally:
        monitor.monitoring_active = False
        monitor_thread.join(timeout=5)
        print("\n👋 Monitoring stopped")

if __name__ == "__main__":
    main()
