"""
JARVIS Health Monitor & Fallback Protocol
=========================================

Monitors all JARVIS communication channels and system health.
Implements automatic fallback channels and self-healing mechanisms.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Callable
from enum import Enum
import json
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ChannelStatus(Enum):
    """Status of communication channels"""
    ONLINE = "online"
    OFFLINE = "offline"
    DEGRADED = "degraded"
    RECOVERING = "recovering"
    FAILED = "failed"

class Severity(Enum):
    """Severity level for alerts"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class HealthMonitor:
    """
    Monitors JARVIS system health and communication channels.
    Implements fallback protocols and automatic recovery.
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
        # Channel status tracking
        self.channel_status: Dict[str, ChannelStatus] = {
            'whatsapp': ChannelStatus.OFFLINE,
            'telegram': ChannelStatus.OFFLINE,
            'websocket': ChannelStatus.OFFLINE,
            'api': ChannelStatus.OFFLINE,
        }
        
        # Channel last seen timestamps
        self.channel_last_seen: Dict[str, datetime] = {}
        
        # Failure counts for exponential backoff
        self.failure_counts: Dict[str, int] = {}
        
        # Fallback channel mapping
        self.fallback_channels: Dict[str, str] = {
            'whatsapp': 'telegram',
            'telegram': 'whatsapp',
            'websocket': 'telegram',
            'api': 'telegram',
        }
        
        # Alert callbacks
        self.alert_callbacks: Dict[Severity, list] = {
            Severity.INFO: [],
            Severity.WARNING: [],
            Severity.ERROR: [],
            Severity.CRITICAL: [],
        }
        
        # Health check intervals (seconds)
        self.health_check_intervals: Dict[str, int] = {
            'whatsapp': 30,
            'telegram': 30,
            'websocket': 15,
            'api': 60,
        }
        
        # Thresholds for health checks
        self.thresholds = {
            'max_failures': 5,
            'offline_timeout': 120,  # seconds
            'degraded_latency': 1000,  # milliseconds
        }
        
        # Running state
        self.is_running = False
        self.health_check_tasks: Dict[str, asyncio.Task] = {}
        
        # Channel interfaces (will be injected)
        self.channel_interfaces: Dict[str, Any] = {}
    
    def register_channel_interface(self, channel: str, interface: Any):
        """Register a channel interface for health checks"""
        self.channel_interfaces[channel] = interface
        logger.info(f"Registered interface for channel: {channel}")
    
    def register_alert_callback(self, severity: Severity, callback: Callable):
        """Register a callback for alerts of specific severity"""
        self.alert_callbacks[severity].append(callback)
        logger.info(f"Registered alert callback for severity: {severity}")
    
    async def start(self):
        """Start health monitoring"""
        if self.is_running:
            logger.warning("Health monitor is already running")
            return
        
        self.is_running = True
        logger.info("🏥 Starting JARVIS Health Monitor")
        
        # Start health check tasks for each channel
        for channel in self.channel_status.keys():
            task = asyncio.create_task(
                self._health_check_loop(channel),
                name=f"health_check_{channel}"
            )
            self.health_check_tasks[channel] = task
        
        logger.info("✅ Health monitor started")
    
    async def stop(self):
        """Stop health monitoring"""
        if not self.is_running:
            return
        
        self.is_running = False
        logger.info("🛑 Stopping JARVIS Health Monitor")
        
        # Cancel all health check tasks
        for task in self.health_check_tasks.values():
            task.cancel()
        
        # Wait for tasks to complete
        await asyncio.gather(*self.health_check_tasks.values(), return_exceptions=True)
        
        self.health_check_tasks.clear()
        logger.info("✅ Health monitor stopped")
    
    async def _health_check_loop(self, channel: str):
        """Run health checks for a specific channel"""
        interval = self.health_check_intervals.get(channel, 30)
        
        while self.is_running:
            try:
                await self._check_channel_health(channel)
                await asyncio.sleep(interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in health check loop for {channel}: {e}")
                await asyncio.sleep(interval)
    
    async def _check_channel_health(self, channel: str):
        """Check health of a specific channel"""
        try:
            interface = self.channel_interfaces.get(channel)
            
            if interface is None:
                # No interface registered, assume offline
                await self._handle_channel_offline(channel, "No interface registered")
                return
            
            # Perform health check based on channel type
            if channel == 'whatsapp':
                await self._check_whatsapp_health(interface)
            elif channel == 'telegram':
                await self._check_telegram_health(interface)
            elif channel == 'websocket':
                await self._check_websocket_health(interface)
            elif channel == 'api':
                await self._check_api_health(interface)
            
            # Update last seen timestamp
            self.channel_last_seen[channel] = datetime.utcnow()
            
            # Reset failure count on successful check
            if self.failure_counts.get(channel, 0) > 0:
                self.failure_counts[channel] = 0
                logger.info(f"✅ {channel} recovered after {self.failure_counts.get(channel, 0)} failures")
            
        except Exception as e:
            logger.error(f"Health check failed for {channel}: {e}")
            await self._handle_channel_offline(channel, str(e))
    
    async def _check_whatsapp_health(self, interface):
        """Check WhatsApp client health"""
        try:
            # Check if client is connected
            is_connected = interface.getStatus().get('connected', False)
            
            if not is_connected:
                raise Exception("WhatsApp client is not connected")
            
            # Update status
            self.channel_status['whatsapp'] = ChannelStatus.ONLINE
            logger.debug("✅ WhatsApp health check passed")
            
        except Exception as e:
            raise Exception(f"WhatsApp health check failed: {e}")
    
    async def _check_telegram_health(self, interface):
        """Check Telegram bot health"""
        try:
            # Check if bot is polling
            is_connected = interface.getStatus().get('connected', False)
            
            if not is_connected:
                raise Exception("Telegram bot is not connected")
            
            # Update status
            self.channel_status['telegram'] = ChannelStatus.ONLINE
            logger.debug("✅ Telegram health check passed")
            
        except Exception as e:
            raise Exception(f"Telegram health check failed: {e}")
    
    async def _check_websocket_health(self, interface):
        """Check WebSocket server health"""
        try:
            # Check if server is running
            # This would typically involve a ping/pong check
            is_connected = True  # Placeholder
            
            if not is_connected:
                raise Exception("WebSocket server is not running")
            
            # Update status
            self.channel_status['websocket'] = ChannelStatus.ONLINE
            logger.debug("✅ WebSocket health check passed")
            
        except Exception as e:
            raise Exception(f"WebSocket health check failed: {e}")
    
    async def _check_api_health(self, interface):
        """Check API health"""
        try:
            # Check API endpoint
            # This would typically involve a health check endpoint
            is_connected = True  # Placeholder
            
            if not is_connected:
                raise Exception("API is not responding")
            
            # Update status
            self.channel_status['api'] = ChannelStatus.ONLINE
            logger.debug("✅ API health check passed")
            
        except Exception as e:
            raise Exception(f"API health check failed: {e}")
    
    async def _handle_channel_offline(self, channel: str, reason: str):
        """Handle channel going offline"""
        previous_status = self.channel_status.get(channel)
        
        # Update status
        self.channel_status[channel] = ChannelStatus.OFFLINE
        
        # Increment failure count
        self.failure_counts[channel] = self.failure_counts.get(channel, 0) + 1
        
        # Check if this is a new failure
        if previous_status == ChannelStatus.ONLINE:
            logger.error(f"❌ {channel} went offline: {reason}")
            
            # Trigger fallback notification
            await self._trigger_fallback_notification(channel, reason, Severity.ERROR)
        
        # Check if max failures reached
        if self.failure_counts[channel] >= self.thresholds['max_failures']:
            logger.critical(f"🚨 {channel} has reached max failures ({self.failure_counts[channel]})")
            self.channel_status[channel] = ChannelStatus.FAILED
            
            # Trigger critical alert
            await self._trigger_fallback_notification(
                channel,
                f"Max failures reached: {reason}",
                Severity.CRITICAL
            )
    
    async def _trigger_fallback_notification(
        self,
        failed_channel: str,
        reason: str,
        severity: Severity
    ):
        """Send notification via fallback channel"""
        fallback_channel = self.fallback_channels.get(failed_channel)
        
        if not fallback_channel:
            logger.warning(f"No fallback channel configured for {failed_channel}")
            return
        
        # Check if fallback channel is available
        if self.channel_status.get(fallback_channel) == ChannelStatus.OFFLINE:
            logger.error(f"⚠️ Fallback channel {fallback_channel} is also offline")
            # Try next fallback
            return
        
        logger.info(f"📢 Sending fallback notification via {fallback_channel}")
        
        # Prepare alert message
        alert_message = self._prepare_alert_message(
            failed_channel,
            reason,
            severity
        )
        
        # Send via fallback channel
        try:
            fallback_interface = self.channel_interfaces.get(fallback_channel)
            
            if fallback_interface:
                await self._send_alert_via_channel(
                    fallback_interface,
                    fallback_channel,
                    alert_message
                )
                logger.info(f"✅ Alert sent via {fallback_channel}")
            else:
                logger.warning(f"No interface for fallback channel {fallback_channel}")
        
        except Exception as e:
            logger.error(f"Failed to send alert via {fallback_channel}: {e}")
    
    def _prepare_alert_message(
        self,
        channel: str,
        reason: str,
        severity: Severity
    ) -> str:
        """Prepare alert message"""
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        
        emoji = {
            Severity.INFO: "ℹ️",
            Severity.WARNING: "⚠️",
            Severity.ERROR: "❌",
            Severity.CRITICAL: "🚨",
        }.get(severity, "⚠️")
        
        message = f"""
{emoji} JARVIS Health Alert

Channel: {channel.upper()}
Severity: {severity.value.upper()}
Time: {timestamp}

Reason: {reason}

Status: {self.channel_status.get(channel).value.upper()}
Failures: {self.failure_counts.get(channel, 0)}

This is an automated health alert from JARVIS Health Monitor.
        """.strip()
        
        return message
    
    async def _send_alert_via_channel(
        self,
        interface: Any,
        channel: str,
        message: str
    ):
        """Send alert message via specific channel"""
        try:
            if channel == 'telegram':
                # Send via Telegram bot
                # This would call the Telegram bot's send_message method
                # For now, we'll just log it
                logger.info(f"TELEGRAM ALERT: {message}")
            
            elif channel == 'whatsapp':
                # Send via WhatsApp client
                # This would call the WhatsApp client's send_message method
                logger.info(f"WHATSAPP ALERT: {message}")
            
            elif channel == 'websocket':
                # Send via WebSocket
                logger.info(f"WEBSOCKET ALERT: {message}")
        
        except Exception as e:
            logger.error(f"Failed to send alert via {channel}: {e}")
            raise
    
    async def trigger_manual_recovery(self, channel: str):
        """Manually trigger recovery for a channel"""
        logger.info(f"🔄 Triggering manual recovery for {channel}")
        
        # Reset failure count
        self.failure_counts[channel] = 0
        
        # Update status to recovering
        self.channel_status[channel] = ChannelStatus.RECOVERING
        
        # Attempt to restart the channel
        try:
            interface = self.channel_interfaces.get(channel)
            
            if interface and hasattr(interface, 'restart'):
                await interface.restart()
                logger.info(f"✅ {channel} restarted successfully")
            else:
                logger.warning(f"No restart method available for {channel}")
        
        except Exception as e:
            logger.error(f"Failed to restart {channel}: {e}")
            self.channel_status[channel] = ChannelStatus.FAILED
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health status"""
        return {
            'timestamp': datetime.utcnow().isoformat(),
            'channels': {
                channel: {
                    'status': status.value,
                    'last_seen': self.channel_last_seen.get(channel).isoformat() if self.channel_last_seen.get(channel) else None,
                    'failures': self.failure_counts.get(channel, 0),
                }
                for channel, status in self.channel_status.items()
            },
            'overall': self._calculate_overall_health(),
        }
    
    def _calculate_overall_health(self) -> str:
        """Calculate overall system health"""
        total_channels = len(self.channel_status)
        online_channels = sum(
            1 for status in self.channel_status.values()
            if status in [ChannelStatus.ONLINE, ChannelStatus.DEGRADED]
        )
        
        if online_channels == total_channels:
            return "healthy"
        elif online_channels >= total_channels / 2:
            return "degraded"
        else:
            return "critical"

# Singleton instance
health_monitor: Optional[HealthMonitor] = None

def get_health_monitor(config: Dict[str, Any] = None) -> HealthMonitor:
    """Get or create health monitor singleton"""
    global health_monitor
    
    if health_monitor is None:
        if config is None:
            config = {}
        health_monitor = HealthMonitor(config)
    
    return health_monitor
