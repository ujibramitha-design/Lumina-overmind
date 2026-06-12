"""
DOOM SENTINEL - Alert System
Proactive monitoring and alerting system for critical events
"""

import os
import logging
import asyncio
import psutil
import json
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AlertLevel(Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"

@dataclass
class Alert:
    """Alert data structure"""
    level: AlertLevel
    title: str
    message: str
    timestamp: datetime
    source: str
    metadata: Dict[str, Any] = None

class AlertSystem:
    """
    Proactive alert system for DOOM monitoring
    Monitors system health and sends alerts to admins
    """
    
    def __init__(self):
        """Initialize alert system"""
        self.logger = logging.getLogger(__name__)
        
        # Alert configuration
        self.alert_thresholds = {
            'cpu_usage': 80.0,        # CPU usage percentage
            'memory_usage': 85.0,     # Memory usage percentage
            'disk_usage': 90.0,       # Disk usage percentage
            'leads_per_hour': 50,     # Leads per hour threshold
            'error_rate': 5.0,        # Error rate percentage
            'response_time': 5000,    # Response time in milliseconds
        }
        
        # Alert history
        self.alert_history: List[Alert] = []
        self.last_alert_check = datetime.now()
        
        # Monitoring state
        self.monitoring_active = False
        self.alert_cooldown = 300  # 5 minutes cooldown between same alerts
        
        self.logger.info("🚨 DOOM Alert System initialized")
        self.logger.info(f"📊 Monitoring thresholds: {self.alert_thresholds}")
    
    async def start_monitoring(self):
        """Start proactive monitoring"""
        if self.monitoring_active:
            self.logger.warning("⚠️ Monitoring already active")
            return
        
        self.monitoring_active = True
        self.logger.info("🔍 Starting proactive monitoring...")
        
        # Start monitoring loop
        asyncio.create_task(self._monitoring_loop())
    
    async def stop_monitoring(self):
        """Stop proactive monitoring"""
        self.monitoring_active = False
        self.logger.info("🛑 Proactive monitoring stopped")
    
    async def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                # Check system metrics
                await self._check_system_metrics()
                
                # Check application metrics
                await self._check_application_metrics()
                
                # Check business metrics
                await self._check_business_metrics()
                
                # Clean old alerts
                self._cleanup_old_alerts()
                
                # Wait before next check
                await asyncio.sleep(60)  # Check every minute
                
            except Exception as e:
                self.logger.error(f"❌ Monitoring loop error: {e}")
                await asyncio.sleep(60)
    
    async def _check_system_metrics(self):
        """Check system health metrics"""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            if cpu_percent > self.alert_thresholds['cpu_usage']:
                await self._send_alert(
                    AlertLevel.WARNING,
                    "High CPU Usage",
                    f"CPU usage is {cpu_percent:.1f}%",
                    "system_monitor",
                    {"cpu_percent": cpu_percent, "threshold": self.alert_thresholds['cpu_usage']}
                )
            
            # Memory usage
            memory = psutil.virtual_memory()
            if memory.percent > self.alert_thresholds['memory_usage']:
                await self._send_alert(
                    AlertLevel.WARNING,
                    "High Memory Usage",
                    f"Memory usage is {memory.percent:.1f}%",
                    "system_monitor",
                    {"memory_percent": memory.percent, "threshold": self.alert_thresholds['memory_usage']}
                )
            
            # Disk usage
            disk = psutil.disk_usage('/')
            if disk.percent > self.alert_thresholds['disk_usage']:
                await self._send_alert(
                    AlertLevel.CRITICAL,
                    "High Disk Usage",
                    f"Disk usage is {disk.percent:.1f}%",
                    "system_monitor",
                    {"disk_percent": disk.percent, "threshold": self.alert_thresholds['disk_usage']}
                )
            
        except Exception as e:
            self.logger.error(f"❌ Error checking system metrics: {e}")
    
    async def _check_application_metrics(self):
        """Check application health metrics"""
        try:
            # Check database connection
            db_status = await self._check_database_health()
            if db_status != 'healthy':
                await self._send_alert(
                    AlertLevel.CRITICAL,
                    "Database Connection Issue",
                    f"Database status: {db_status}",
                    "application_monitor",
                    {"database_status": db_status}
                )
            
            # Check API response time
            api_response_time = await self._check_api_response_time()
            if api_response_time > self.alert_thresholds['response_time']:
                await self._send_alert(
                    AlertLevel.WARNING,
                    "Slow API Response",
                    f"API response time: {api_response_time}ms",
                    "application_monitor",
                    {"response_time": api_response_time, "threshold": self.alert_thresholds['response_time']}
                )
            
        except Exception as e:
            self.logger.error(f"❌ Error checking application metrics: {e}")
    
    async def _check_business_metrics(self):
        """Check business metrics"""
        try:
            # Check lead velocity
            leads_per_hour = await self._calculate_leads_per_hour()
            if leads_per_hour > self.alert_thresholds['leads_per_hour']:
                await self._send_alert(
                    AlertLevel.INFO,
                    "High Lead Velocity",
                    f"{leads_per_hour} leads in the last hour",
                    "business_monitor",
                    {"leads_per_hour": leads_per_hour, "threshold": self.alert_thresholds['leads_per_hour']}
                )
            
            # Check API usage/billing
            api_usage = await self._check_api_usage()
            if api_usage['usage_percent'] > 80:
                await self._send_alert(
                    AlertLevel.WARNING,
                    "High API Usage",
                    f"API usage at {api_usage['usage_percent']:.1f}%",
                    "business_monitor",
                    api_usage
                )
            
        except Exception as e:
            self.logger.error(f"❌ Error checking business metrics: {e}")
    
    async def _check_database_health(self) -> str:
        """Check database health status"""
        try:
            from core_modules.db_manager_postgres import postgres_db_manager
            health_status = await postgres_db_manager.health_check()
            return health_status.get('status', 'unknown')
        except Exception as e:
            self.logger.error(f"❌ Database health check error: {e}")
            return 'error'
    
    async def _check_api_response_time(self) -> int:
        """Check API response time"""
        try:
            import time
            import requests
            
            start_time = time.time()
            response = requests.get('http://localhost:8000/health', timeout=10)
            response_time = int((time.time() - start_time) * 1000)
            
            return response_time
        except Exception as e:
            self.logger.error(f"❌ API response time check error: {e}")
            return 9999  # Return high value to indicate error
    
    async def _calculate_leads_per_hour(self) -> int:
        """Calculate leads generated in the last hour"""
        try:
            from core_modules.db_manager_postgres import postgres_db_manager
            
            one_hour_ago = datetime.now() - timedelta(hours=1)
            query = f"""
                SELECT COUNT(*) as count 
                FROM leads 
                WHERE created_at >= '{one_hour_ago.strftime('%Y-%m-%d %H:%M:%S')}'
            """
            
            result = await postgres_db_manager.execute_query(query)
            return result[0]['count'] if result else 0
            
        except Exception as e:
            self.logger.error(f"❌ Error calculating leads per hour: {e}")
            return 0
    
    async def _check_api_usage(self) -> Dict[str, Any]:
        """Check API usage and billing status"""
        try:
            # This would integrate with actual billing/API usage monitoring
            # For now, return mock data
            return {
                'usage_percent': 65.0,
                'requests_today': 1250,
                'limit_daily': 2000,
                'cost_today': 45.50,
                'budget_daily': 100.0
            }
        except Exception as e:
            self.logger.error(f"❌ Error checking API usage: {e}")
            return {'usage_percent': 0}
    
    async def _send_alert(self, level: AlertLevel, title: str, message: str, source: str, metadata: Dict[str, Any] = None):
        """Send alert to all admin channels"""
        # Check cooldown
        if not self._should_send_alert(title, message):
            return
        
        # Create alert
        alert = Alert(
            level=level,
            title=title,
            message=message,
            timestamp=datetime.now(),
            source=source,
            metadata=metadata or {}
        )
        
        # Add to history
        self.alert_history.append(alert)
        
        # Format alert message
        formatted_message = self._format_alert_message(alert)
        
        # Send to all channels
        await self._send_to_all_channels(formatted_message)
        
        self.logger.info(f"🚨 Alert sent: {title} - {message}")
    
    def _should_send_alert(self, title: str, message: str) -> bool:
        """Check if alert should be sent (cooldown logic)"""
        # Find similar recent alerts
        recent_alerts = [
            alert for alert in self.alert_history
            if alert.title == title and 
            (datetime.now() - alert.timestamp).total_seconds() < self.alert_cooldown
        ]
        
        return len(recent_alerts) == 0
    
    def _format_alert_message(self, alert: Alert) -> str:
        """Format alert message for display"""
        level_emoji = {
            AlertLevel.INFO: "ℹ️",
            AlertLevel.WARNING: "⚠️",
            AlertLevel.CRITICAL: "🔴",
            AlertLevel.EMERGENCY: "🚨"
        }
        
        emoji = level_emoji.get(alert.level, "📢")
        
        message = (
            f"{emoji} **DOOM ALERT**\n\n"
            f"🔔 **{alert.title}**\n"
            f"📝 {alert.message}\n"
            f"🕐 {alert.timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"📍 Source: {alert.source}"
        )
        
        if alert.metadata:
            message += f"\n📊 Details: {json.dumps(alert.metadata, indent=2)}"
        
        return message
    
    async def _send_to_all_channels(self, message: str):
        """Send alert to all admin channels"""
        try:
            # Send to Telegram
            await self.send_telegram_alert(message)
            
            # Send to WhatsApp
            await self.send_whatsapp_alert(message)
            
        except Exception as e:
            self.logger.error(f"❌ Error sending alert to channels: {e}")
    
    async def send_telegram_alert(self, message: str):
        """Send alert to Telegram admin"""
        try:
            from .telegram_gateway import TelegramGateway
            
            # This would be initialized in the main application
            # For now, just log the message
            self.logger.info(f"📨 Telegram Alert: {message}")
            
        except Exception as e:
            self.logger.error(f"❌ Error sending Telegram alert: {e}")
    
    async def send_whatsapp_alert(self, message: str):
        """Send alert to WhatsApp admin"""
        try:
            from .whatsapp_gateway import WhatsAppGateway
            
            # This would be initialized in the main application
            # For now, just log the message
            self.logger.info(f"📱 WhatsApp Alert: {message}")
            
        except Exception as e:
            self.logger.error(f"❌ Error sending WhatsApp alert: {e}")
    
    def _cleanup_old_alerts(self):
        """Clean up old alerts from history"""
        # Keep only last 24 hours of alerts
        cutoff_time = datetime.now() - timedelta(hours=24)
        self.alert_history = [
            alert for alert in self.alert_history
            if alert.timestamp > cutoff_time
        ]
    
    async def send_custom_alert(self, title: str, message: str, level: AlertLevel = AlertLevel.INFO):
        """Send custom alert"""
        await self._send_alert(level, title, message, "custom")
    
    async def send_server_down_alert(self, service: str, error: str):
        """Send server down alert"""
        await self._send_alert(
            AlertLevel.EMERGENCY,
            f"Server Down: {service}",
            f"Service {service} is down: {error}",
            "server_monitor"
        )
    
    async def send_database_crash_alert(self, error: str):
        """Send database crash alert"""
        await self._send_alert(
            AlertLevel.EMERGENCY,
            "Database Crash",
            f"Database connection lost: {error}",
            "database_monitor"
        )
    
    async def send_traffic_spike_alert(self, lead_count: int, time_period: str):
        """Send traffic spike alert"""
        await self._send_alert(
            AlertLevel.INFO,
            "Traffic Spike Detected",
            f"{lead_count} new leads in {time_period}",
            "business_monitor",
            {"lead_count": lead_count, "time_period": time_period}
        )
    
    async def send_api_limit_alert(self, service: str, usage_percent: float):
        """Send API limit alert"""
        await self._send_alert(
            AlertLevel.WARNING,
            f"API Usage High: {service}",
            f"{service} API usage at {usage_percent:.1f}%",
            "api_monitor",
            {"service": service, "usage_percent": usage_percent}
        )
    
    def get_alert_statistics(self) -> Dict[str, Any]:
        """Get alert statistics"""
        last_24_hours = datetime.now() - timedelta(hours=24)
        recent_alerts = [
            alert for alert in self.alert_history
            if alert.timestamp > last_24_hours
        ]
        
        stats = {
            'total_alerts_24h': len(recent_alerts),
            'by_level': {},
            'by_source': {},
            'monitoring_active': self.monitoring_active
        }
        
        for alert in recent_alerts:
            # Count by level
            level_key = alert.level.value
            stats['by_level'][level_key] = stats['by_level'].get(level_key, 0) + 1
            
            # Count by source
            source_key = alert.source
            stats['by_source'][source_key] = stats['by_source'].get(source_key, 0) + 1
        
        return stats
    
    def get_recent_alerts(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent alerts"""
        recent_alerts = sorted(self.alert_history, key=lambda x: x.timestamp, reverse=True)
        
        return [
            {
                'level': alert.level.value,
                'title': alert.title,
                'message': alert.message,
                'timestamp': alert.timestamp.isoformat(),
                'source': alert.source
            }
            for alert in recent_alerts[:limit]
        ]
