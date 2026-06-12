"""
DOOM SENTINEL - Cost Management & Token Control
AI Token Cost Management with Hard Limits and Kill Switch
"""

import os
import logging
import json
import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum

# Database imports
from prisma import Prisma

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CostLevel(Enum):
    """Cost alert levels"""
    NORMAL = "normal"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"

@dataclass
class CostRecord:
    """Cost tracking record"""
    timestamp: datetime
    api_service: str
    operation_type: str
    tokens_used: int
    cost_usd: float
    operation_id: str
    metadata: Dict[str, Any]

@dataclass
class CostThreshold:
    """Cost threshold configuration"""
    daily_limit: float
    warning_threshold: float
    critical_threshold: float
    emergency_threshold: float
    kill_switch_enabled: bool

class CostManager:
    """
    AI Token Cost Management System
    Tracks costs, enforces limits, and provides kill switch functionality
    """
    
    def __init__(self):
        """Initialize cost manager"""
        self.logger = logging.getLogger(__name__)
        
        # Cost tracking
        self.cost_records: List[CostRecord] = []
        self.daily_costs: Dict[str, float] = {}
        self.monthly_costs: Dict[str, float] = {}
        
        # Thresholds (USD)
        self.thresholds = {
            'gemini': CostThreshold(
                daily_limit=50.0,
                warning_threshold=30.0,
                critical_threshold=40.0,
                emergency_threshold=48.0,
                kill_switch_enabled=True
            ),
            'openai': CostThreshold(
                daily_limit=100.0,
                warning_threshold=60.0,
                critical_threshold=80.0,
                emergency_threshold=95.0,
                kill_switch_enabled=True
            ),
            'twilio': CostThreshold(
                daily_limit=20.0,
                warning_threshold=15.0,
                critical_threshold=18.0,
                emergency_threshold=19.5,
                kill_switch_enabled=True
            )
        }
        
        # Kill switch states
        self.kill_switches: Dict[str, bool] = {}
        self.infinite_loop_detection: Dict[str, float] = {}
        
        # Database connection
        self.db = None
        self._initialize_database()
        
        self.logger.info("💰 Cost Manager initialized")
        self.logger.info(f"🚨 Kill switches enabled for: {[k for k,v in self.thresholds.items() if v.kill_switch_enabled]}")
    
    def _initialize_database(self):
        """Initialize database connection"""
        try:
            self.db = Prisma()
            self.logger.info("📊 Cost Manager database connected")
        except Exception as e:
            self.logger.error(f"❌ Database connection failed: {e}")
            self.db = None
    
    async def track_cost(self, api_service: str, operation_type: str, tokens_used: int, 
                        operation_id: str, metadata: Dict[str, Any] = None) -> bool:
        """
        Track API cost for an operation
        
        Args:
            api_service: Service name (gemini, openai, twilio)
            operation_type: Type of operation (chat, image, message)
            tokens_used: Number of tokens used
            operation_id: Unique operation identifier
            metadata: Additional operation metadata
            
        Returns:
            bool: True if cost tracking successful, False if blocked
        """
        try:
            # Check kill switch
            if self.kill_switches.get(api_service, False):
                self.logger.warning(f"🚫 Kill switch active for {api_service}")
                await self._send_alert(
                    CostLevel.EMERGENCY,
                    f"Kill Switch Active",
                    f"Operations blocked for {api_service} due to cost limits",
                    "cost_manager"
                )
                return False
            
            # Check infinite loop detection
            if self._detect_infinite_loop(api_service, operation_id):
                self.logger.error(f"🔄 Infinite loop detected for {api_service}")
                await self._activate_kill_switch(api_service, "Infinite loop detected")
                return False
            
            # Calculate cost
            cost_usd = self._calculate_cost(api_service, tokens_used)
            
            # Create cost record
            cost_record = CostRecord(
                timestamp=datetime.now(),
                api_service=api_service,
                operation_type=operation_type,
                tokens_used=tokens_used,
                cost_usd=cost_usd,
                operation_id=operation_id,
                metadata=metadata or {}
            )
            
            # Add to records
            self.cost_records.append(cost_record)
            
            # Update daily/monthly costs
            self._update_cost_aggregates(api_service, cost_usd)
            
            # Check thresholds
            await self._check_thresholds(api_service)
            
            # Save to database
            if self.db:
                await self._save_cost_record(cost_record)
            
            self.logger.info(f"💰 Cost tracked: {api_service} ${cost_usd:.4f} ({tokens_used} tokens)")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Cost tracking failed: {e}")
            return False
    
    def _calculate_cost(self, api_service: str, tokens_used: int) -> float:
        """Calculate cost based on service and tokens"""
        # Pricing per 1K tokens (USD)
        pricing = {
            'gemini': 0.00025,  # $0.00025 per 1K tokens
            'openai': 0.0020,   # $0.0020 per 1K tokens (gpt-3.5-turbo)
            'twilio': 0.0050    # $0.005 per WhatsApp message
        }
        
        price_per_token = pricing.get(api_service, 0.001) / 1000
        return tokens_used * price_per_token
    
    def _update_cost_aggregates(self, api_service: str, cost_usd: float):
        """Update daily and monthly cost aggregates"""
        today = datetime.now().strftime('%Y-%m-%d')
        this_month = datetime.now().strftime('%Y-%m')
        
        # Update daily costs
        if today not in self.daily_costs:
            self.daily_costs[today] = {}
        self.daily_costs[today][api_service] = self.daily_costs[today].get(api_service, 0) + cost_usd
        
        # Update monthly costs
        if this_month not in self.monthly_costs:
            self.monthly_costs[this_month] = {}
        self.monthly_costs[this_month][api_service] = self.monthly_costs[this_month].get(api_service, 0) + cost_usd
    
    async def _check_thresholds(self, api_service: str):
        """Check if cost thresholds are exceeded"""
        try:
            threshold = self.thresholds.get(api_service)
            if not threshold:
                return
            
            today = datetime.now().strftime('%Y-%m-%d')
            daily_cost = self.daily_costs.get(today, {}).get(api_service, 0)
            
            # Check thresholds
            if daily_cost >= threshold.emergency_threshold:
                await self._activate_kill_switch(api_service, f"Emergency threshold exceeded: ${daily_cost:.2f}")
            elif daily_cost >= threshold.critical_threshold:
                await self._send_alert(
                    CostLevel.CRITICAL,
                    f"Critical Cost Threshold",
                    f"{api_service} cost: ${daily_cost:.2f} (limit: ${threshold.daily_limit:.2f})",
                    "cost_manager"
                )
            elif daily_cost >= threshold.warning_threshold:
                await self._send_alert(
                    CostLevel.WARNING,
                    f"Cost Warning",
                    f"{api_service} cost: ${daily_cost:.2f} (warning: ${threshold.warning_threshold:.2f})",
                    "cost_manager"
                )
                
        except Exception as e:
            self.logger.error(f"❌ Threshold check failed: {e}")
    
    def _detect_infinite_loop(self, api_service: str, operation_id: str) -> bool:
        """Detect infinite loop patterns"""
        try:
            current_time = datetime.now()
            
            # Check if same operation_id appears too frequently
            if api_service not in self.infinite_loop_detection:
                self.infinite_loop_detection[api_service] = {}
            
            if operation_id in self.infinite_loop_detection[api_service]:
                last_time = self.infinite_loop_detection[api_service][operation_id]
                time_diff = (current_time - last_time).total_seconds()
                
                # If same operation within 1 second, potential infinite loop
                if time_diff < 1.0:
                    return True
            
            # Update last seen time
            self.infinite_loop_detection[api_service][operation_id] = current_time
            
            # Clean old entries (older than 5 minutes)
            cutoff_time = current_time - timedelta(minutes=5)
            self.infinite_loop_detection[api_service] = {
                op_id: time for op_id, time in self.infinite_loop_detection[api_service].items()
                if time > cutoff_time
            }
            
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Infinite loop detection failed: {e}")
            return False
    
    async def _activate_kill_switch(self, api_service: str, reason: str):
        """Activate kill switch for API service"""
        try:
            self.kill_switches[api_service] = True
            
            self.logger.error(f"🚨 KILL SWITCH ACTIVATED: {api_service} - {reason}")
            
            await self._send_alert(
                CostLevel.EMERGENCY,
                f"Kill Switch Activated",
                f"Service {api_service} has been disabled. Reason: {reason}",
                "cost_manager"
            )
            
            # Save to database
            if self.db:
                await self._save_kill_switch_event(api_service, reason)
                
        except Exception as e:
            self.logger.error(f"❌ Kill switch activation failed: {e}")
    
    async def _send_alert(self, level: CostLevel, title: str, message: str, source: str):
        """Send cost alert to admin"""
        try:
            # Format alert message
            level_emoji = {
                CostLevel.NORMAL: "ℹ️",
                CostLevel.WARNING: "⚠️",
                CostLevel.CRITICAL: "🔴",
                CostLevel.EMERGENCY: "🚨"
            }
            
            emoji = level_emoji.get(level, "📢")
            
            alert_message = (
                f"{emoji} **DOOM COST ALERT**\n\n"
                f"💰 **{title}**\n"
                f"📝 {message}\n"
                f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"📍 Source: {source}"
            )
            
            # Send to alert system
            from .doom_sentinel.alert_system import AlertSystem
            alert_system = AlertSystem()
            await alert_system.send_custom_alert(title, message, level.value)
            
        except Exception as e:
            self.logger.error(f"❌ Alert sending failed: {e}")
    
    async def _save_cost_record(self, cost_record: CostRecord):
        """Save cost record to database"""
        try:
            await self.db.costrecord.create({
                'timestamp': cost_record.timestamp,
                'apiService': cost_record.api_service,
                'operationType': cost_record.operation_type,
                'tokensUsed': cost_record.tokens_used,
                'costUsd': cost_record.cost_usd,
                'operationId': cost_record.operation_id,
                'metadata': cost_record.metadata
            })
        except Exception as e:
            self.logger.error(f"❌ Database save failed: {e}")
    
    async def _save_kill_switch_event(self, api_service: str, reason: str):
        """Save kill switch event to database"""
        try:
            await self.db.killevent.create({
                'timestamp': datetime.now(),
                'apiService': api_service,
                'reason': reason,
                'isActive': True
            })
        except Exception as e:
            self.logger.error(f"❌ Kill switch event save failed: {e}")
    
    def get_cost_summary(self) -> Dict[str, Any]:
        """Get comprehensive cost summary"""
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            this_month = datetime.now().strftime('%Y-%m')
            
            summary = {
                'today': {
                    'date': today,
                    'total_cost': sum(self.daily_costs.get(today, {}).values()),
                    'by_service': self.daily_costs.get(today, {}),
                    'operations_today': len([r for r in self.cost_records if r.timestamp.strftime('%Y-%m-%d') == today])
                },
                'this_month': {
                    'month': this_month,
                    'total_cost': sum(self.monthly_costs.get(this_month, {}).values()),
                    'by_service': self.monthly_costs.get(this_month, {})
                },
                'kill_switches': {
                    service: active for service, active in self.kill_switches.items()
                },
                'thresholds': {
                    service: {
                        'daily_limit': threshold.daily_limit,
                        'current_usage': self.daily_costs.get(today, {}).get(service, 0),
                        'percentage': (self.daily_costs.get(today, {}).get(service, 0) / threshold.daily_limit) * 100
                    }
                    for service, threshold in self.thresholds.items()
                }
            }
            
            return summary
            
        except Exception as e:
            self.logger.error(f"❌ Cost summary generation failed: {e}")
            return {}
    
    def reset_kill_switch(self, api_service: str) -> bool:
        """Manually reset kill switch"""
        try:
            if api_service in self.kill_switches:
                del self.kill_switches[api_service]
                self.logger.info(f"🔄 Kill switch reset for {api_service}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"❌ Kill switch reset failed: {e}")
            return False
    
    def get_daily_report(self) -> str:
        """Generate daily cost report"""
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            daily_data = self.daily_costs.get(today, {})
            
            if not daily_data:
                return "No cost data for today"
            
            report = f"📊 **Daily Cost Report - {today}**\n\n"
            
            for service, cost in daily_data.items():
                threshold = self.thresholds.get(service)
                if threshold:
                    percentage = (cost / threshold.daily_limit) * 100
                    status = "🟢" if percentage < 50 else "🟡" if percentage < 80 else "🔴"
                    
                    report += f"{status} **{service.upper()}**: ${cost:.2f} ({percentage:.1f}% of ${threshold.daily_limit:.2f})\n"
            
            total_cost = sum(daily_data.values())
            report += f"\n💰 **Total Today**: ${total_cost:.2f}"
            
            return report
            
        except Exception as e:
            self.logger.error(f"❌ Daily report generation failed: {e}")
            return "Error generating report"
    
    async def cleanup_old_records(self, days_to_keep: int = 30):
        """Clean up old cost records"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days_to_keep)
            
            # Remove old records from memory
            self.cost_records = [
                record for record in self.cost_records 
                if record.timestamp > cutoff_date
            ]
            
            # Clean up old daily costs
            old_dates = [
                date for date in self.daily_costs.keys()
                if datetime.strptime(date, '%Y-%m-%d') < cutoff_date
            ]
            
            for date in old_dates:
                del self.daily_costs[date]
            
            self.logger.info(f"🧹 Cleaned up cost records older than {days_to_keep} days")
            
        except Exception as e:
            self.logger.error(f"❌ Cleanup failed: {e}")

# Global cost manager instance
cost_manager = CostManager()
