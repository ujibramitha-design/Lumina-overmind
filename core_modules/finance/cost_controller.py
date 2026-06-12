"""
LUMINA OS - Cost Controller & Budget Management
Enterprise-grade financial control for AI API usage and operational costs
"""

import os
import logging
import asyncio
import json
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BudgetStatus(Enum):
    """Budget status levels"""
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    EXHAUSTED = "exhausted"
    BLOCKED = "blocked"

class CostCategory(Enum):
    """Cost categories"""
    AI_API = "ai_api"
    WHATSAPP_API = "whatsapp_api"
    TELEGRAM_API = "telegram_api"
    STORAGE = "storage"
    BANDWIDTH = "bandwidth"
    COMPUTE = "compute"

@dataclass
class CostRecord:
    """Cost tracking record"""
    id: str
    category: CostCategory
    provider: str  # openai, google, meta, etc.
    service: str   # gpt-4, gemini-pro, etc.
    cost_usd: float
    token_count: int
    request_count: int
    timestamp: datetime
    metadata: Dict[str, Any]

@dataclass
class BudgetLimit:
    """Budget limit configuration"""
    category: CostCategory
    daily_limit_usd: float
    monthly_limit_usd: float
    alert_threshold: float  # percentage (0.0-1.0)
    block_threshold: float  # percentage (0.0-1.0)
    is_active: bool

@dataclass
class CostAlert:
    """Cost alert notification"""
    id: str
    alert_type: str
    category: CostCategory
    current_spending: float
    budget_limit: float
    percentage_used: float
    message: str
    severity: str
    timestamp: datetime
    acknowledged: bool

class CostController:
    """
    Enterprise-grade cost control system
    Monitors AI API costs and enforces budget limits
    """
    
    def __init__(self):
        """Initialize cost controller"""
        self.logger = logging.getLogger(__name__)
        
        # Cost tracking
        self.cost_records: List[CostRecord] = []
        
        # Budget limits
        self.budget_limits: Dict[CostCategory, BudgetLimit] = {}
        
        # Cost alerts
        self.cost_alerts: List[CostAlert] = []
        
        # Cost tracking state
        self.current_daily_spending: Dict[CostCategory, float] = {}
        self.current_monthly_spending: Dict[CostCategory, float] = {}
        
        # Configuration
        self.cost_config = self._initialize_cost_config()
        
        # Initialize budget limits
        self._initialize_budget_limits()
        
        # Start monitoring task
        self._start_monitoring_task()
        
        self.logger.info("💰 Cost Controller initialized")
        self.logger.info(f"📊 Budget limits loaded: {len(self.budget_limits)}")
    
    def _initialize_cost_config(self) -> Dict[str, Any]:
        """Initialize cost configuration"""
        return {
            'monitoring_interval_minutes': 5,
            'alert_cooldown_minutes': 30,
            'cost_tracking_retention_days': 90,
            'auto_block_exceeded': True,
            'alert_webhook_url': os.getenv("COST_ALERT_WEBHOOK", ""),
            'admin_telegram_id': os.getenv("ADMIN_TELE_ID", ""),
            'enable_daily_reset': True,
            'enable_monthly_reset': True
        }
    
    def _initialize_budget_limits(self):
        """Initialize budget limits from environment"""
        try:
            # AI API Budget
            ai_daily = float(os.getenv("AI_DAILY_BUDGET_USD", "50.0"))
            ai_monthly = float(os.getenv("AI_MONTHLY_BUDGET_USD", "1500.0"))
            
            self.budget_limits[CostCategory.AI_API] = BudgetLimit(
                category=CostCategory.AI_API,
                daily_limit_usd=ai_daily,
                monthly_limit_usd=ai_monthly,
                alert_threshold=0.8,  # Alert at 80%
                block_threshold=0.95,  # Block at 95%
                is_active=True
            )
            
            # WhatsApp API Budget
            wa_daily = float(os.getenv("WHATSAPP_DAILY_BUDGET_USD", "20.0"))
            wa_monthly = float(os.getenv("WHATSAPP_MONTHLY_BUDGET_USD", "600.0"))
            
            self.budget_limits[CostCategory.WHATSAPP_API] = BudgetLimit(
                category=CostCategory.WHATSAPP_API,
                daily_limit_usd=wa_daily,
                monthly_limit_usd=wa_monthly,
                alert_threshold=0.8,
                block_threshold=0.95,
                is_active=True
            )
            
            # Telegram API Budget
            tg_daily = float(os.getenv("TELEGRAM_DAILY_BUDGET_USD", "5.0"))
            tg_monthly = float(os.getenv("TELEGRAM_MONTHLY_BUDGET_USD", "150.0"))
            
            self.budget_limits[CostCategory.TELEGRAM_API] = BudgetLimit(
                category=CostCategory.TELEGRAM_API,
                daily_limit_usd=tg_daily,
                monthly_limit_usd=tg_monthly,
                alert_threshold=0.8,
                block_threshold=0.95,
                is_active=True
            )
            
            # Initialize spending counters
            for category in self.budget_limits.keys():
                self.current_daily_spending[category] = 0.0
                self.current_monthly_spending[category] = 0.0
            
            self.logger.info("💰 Budget limits initialized from environment")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize budget limits: {e}")
    
    def _start_monitoring_task(self):
        """Start cost monitoring task"""
        try:
            # Start monitoring in background
            asyncio.create_task(self._monitor_costs())
            
            # Start daily reset task
            if self.cost_config['enable_daily_reset']:
                asyncio.create_task(self._daily_reset_task())
            
            # Start monthly reset task
            if self.cost_config['enable_monthly_reset']:
                asyncio.create_task(self._monthly_reset_task())
            
            self.logger.info("📊 Cost monitoring tasks started")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to start monitoring tasks: {e}")
    
    async def track_cost(self, category: CostCategory, provider: str, service: str,
                       cost_usd: float, token_count: int = 0, 
                       request_count: int = 1, metadata: Dict[str, Any] = None) -> bool:
        """
        Track cost for API usage
        
        Args:
            category: Cost category
            provider: Service provider
            service: Specific service
            cost_usd: Cost in USD
            token_count: Number of tokens used
            request_count: Number of requests
            metadata: Additional metadata
            
        Returns:
            True if tracked successfully
        """
        try:
            # Create cost record
            cost_record = CostRecord(
                id=f"cost_{int(datetime.now().timestamp() * 1000000)}",
                category=category,
                provider=provider,
                service=service,
                cost_usd=cost_usd,
                token_count=token_count,
                request_count=request_count,
                timestamp=datetime.now(),
                metadata=metadata or {}
            )
            
            # Add to records
            self.cost_records.append(cost_record)
            
            # Update spending counters
            self.current_daily_spending[category] += cost_usd
            self.current_monthly_spending[category] += cost_usd
            
            # Check budget limits
            await self._check_budget_limits(category)
            
            # Clean old records
            self._cleanup_old_records()
            
            self.logger.debug(f"💰 Cost tracked: {category.value} - ${cost_usd:.4f} ({provider}/{service})")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Cost tracking failed: {e}")
            return False
    
    async def _check_budget_limits(self, category: CostCategory):
        """Check budget limits and trigger alerts"""
        try:
            budget = self.budget_limits.get(category)
            if not budget or not budget.is_active:
                return
            
            # Calculate percentages
            daily_percentage = self.current_daily_spending[category] / budget.daily_limit_usd
            monthly_percentage = self.current_monthly_spending[category] / budget.monthly_limit_usd
            
            # Check alert threshold
            if daily_percentage >= budget.alert_threshold or monthly_percentage >= budget.alert_threshold:
                await self._trigger_cost_alert(category, daily_percentage, monthly_percentage, budget)
            
            # Check block threshold
            if daily_percentage >= budget.block_threshold or monthly_percentage >= budget.block_threshold:
                await self._trigger_cost_block(category, daily_percentage, monthly_percentage, budget)
            
        except Exception as e:
            self.logger.error(f"❌ Budget limit check failed: {e}")
    
    async def _trigger_cost_alert(self, category: CostCategory, daily_percentage: float,
                             monthly_percentage: float, budget: BudgetLimit):
        """Trigger cost alert"""
        try:
            # Check cooldown
            if self._is_alert_cooldown_active(category):
                return
            
            # Determine severity
            if daily_percentage >= 0.9 or monthly_percentage >= 0.9:
                severity = "critical"
                status = BudgetStatus.CRITICAL
            else:
                severity = "warning"
                status = BudgetStatus.WARNING
            
            # Create alert
            alert = CostAlert(
                id=f"alert_{int(datetime.now().timestamp() * 1000000)}",
                alert_type="budget_alert",
                category=category,
                current_spending=self.current_daily_spending[category],
                budget_limit=budget.daily_limit_usd,
                percentage_used=daily_percentage,
                message=f"Budget alert: {category.value} spending at {daily_percentage:.1%} of daily limit",
                severity=severity,
                timestamp=datetime.now(),
                acknowledged=False
            )
            
            self.cost_alerts.append(alert)
            
            # Send notification
            await self._send_cost_notification(alert, status)
            
            self.logger.warning(f"🚨 Cost alert triggered: {category.value} at {daily_percentage:.1%}")
            
        except Exception as e:
            self.logger.error(f"❌ Cost alert failed: {e}")
    
    async def _trigger_cost_block(self, category: CostCategory, daily_percentage: float,
                            monthly_percentage: float, budget: BudgetLimit):
        """Trigger cost block"""
        try:
            # Create critical alert
            alert = CostAlert(
                id=f"block_{int(datetime.now().timestamp() * 1000000)}",
                alert_type="budget_block",
                category=category,
                current_spending=self.current_daily_spending[category],
                budget_limit=budget.daily_limit_usd,
                percentage_used=daily_percentage,
                message=f"BUDGET EXHAUSTED: {category.value} spending blocked at {daily_percentage:.1%}",
                severity="critical",
                timestamp=datetime.now(),
                acknowledged=False
            )
            
            self.cost_alerts.append(alert)
            
            # Send critical notification
            await self._send_cost_notification(alert, BudgetStatus.BLOCKED)
            
            # Block further requests (this would be implemented in the actual API layer)
            if self.cost_config['auto_block_exceeded']:
                self._block_category_requests(category)
            
            self.logger.error(f"🚫 Cost block triggered: {category.value} blocked at {daily_percentage:.1%}")
            
        except Exception as e:
            self.logger.error(f"❌ Cost block failed: {e}")
    
    def _block_category_requests(self, category: CostCategory):
        """Block requests for category"""
        # This would integrate with the actual API layer
        self.logger.critical(f"🚫 All {category.value} requests blocked due to budget exhaustion")
    
    def _is_alert_cooldown_active(self, category: CostCategory) -> bool:
        """Check if alert cooldown is active"""
        try:
            cooldown_minutes = self.cost_config['alert_cooldown_minutes']
            cutoff_time = datetime.now() - timedelta(minutes=cooldown_minutes)
            
            recent_alerts = [
                alert for alert in self.cost_alerts
                if alert.category == category and 
                alert.timestamp >= cutoff_time and
                not alert.acknowledged
            ]
            
            return len(recent_alerts) > 0
            
        except Exception:
            return False
    
    async def _send_cost_notification(self, alert: CostAlert, status: BudgetStatus):
        """Send cost notification to admin"""
        try:
            message = f"""
🚨 COST CONTROL ALERT 🚨

Status: {status.value.upper()}
Category: {alert.category.value}
Spending: ${alert.current_spending:.4f} / ${alert.budget_limit:.4f}
Usage: {alert.percentage_used:.1%}

Message: {alert.message}

Time: {alert.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
            """.strip()
            
            # Send to Telegram
            if self.cost_config['admin_telegram_id']:
                await self._send_telegram_alert(message)
            
            # Send webhook
            if self.cost_config['alert_webhook_url']:
                await self._send_webhook_alert(alert, message)
            
            self.logger.info(f"📢 Cost notification sent: {alert.alert_type}")
            
        except Exception as e:
            self.logger.error(f"❌ Notification failed: {e}")
    
    async def _send_telegram_alert(self, message: str):
        """Send alert to Telegram"""
        # This would integrate with the Telegram gateway
        self.logger.info(f"📱 Telegram alert: {message[:100]}...")
    
    async def _send_webhook_alert(self, alert: CostAlert, message: str):
        """Send alert via webhook"""
        # This would send to webhook URL
        self.logger.info(f"🔗 Webhook alert: {alert.alert_type}")
    
    async def _monitor_costs(self):
        """Background cost monitoring task"""
        try:
            while True:
                await asyncio.sleep(self.cost_config['monitoring_interval_minutes'] * 60)
                
                # Check all budget limits
                for category in self.budget_limits.keys():
                    await self._check_budget_limits(category)
                
                # Log current status
                self._log_current_status()
                
        except Exception as e:
            self.logger.error(f"❌ Cost monitoring error: {e}")
            await asyncio.sleep(60)  # Wait before retry
    
    async def _daily_reset_task(self):
        """Daily reset task"""
        try:
            while True:
                # Wait until next day
                now = datetime.now()
                next_day = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
                sleep_seconds = (next_day - now).total_seconds()
                
                await asyncio.sleep(sleep_seconds)
                
                # Reset daily spending
                for category in self.budget_limits.keys():
                    self.current_daily_spending[category] = 0.0
                
                self.logger.info("📅 Daily spending reset completed")
                
        except Exception as e:
            self.logger.error(f"❌ Daily reset error: {e}")
            await asyncio.sleep(3600)  # Wait before retry
    
    async def _monthly_reset_task(self):
        """Monthly reset task"""
        try:
            while True:
                # Wait until next month
                now = datetime.now()
                next_month = (now.replace(day=1) + timedelta(days=32)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                sleep_seconds = (next_month - now).total_seconds()
                
                await asyncio.sleep(sleep_seconds)
                
                # Reset monthly spending
                for category in self.budget_limits.keys():
                    self.current_monthly_spending[category] = 0.0
                
                self.logger.info("📅 Monthly spending reset completed")
                
        except Exception as e:
            self.logger.error(f"❌ Monthly reset error: {e}")
            await asyncio.sleep(86400 * 7)  # Wait before retry
    
    def _log_current_status(self):
        """Log current cost status"""
        try:
            total_daily = sum(self.current_daily_spending.values())
            total_monthly = sum(self.current_monthly_spending.values())
            
            self.logger.info(f"💰 Current spending - Daily: ${total_daily:.2f}, Monthly: ${total_monthly:.2f}")
            
            for category, budget in self.budget_limits.items():
                daily_spent = self.current_daily_spending.get(category, 0)
                monthly_spent = self.current_monthly_spending.get(category, 0)
                
                daily_pct = (daily_spent / budget.daily_limit_usd) * 100 if budget.daily_limit_usd > 0 else 0
                monthly_pct = (monthly_spent / budget.monthly_limit_usd) * 100 if budget.monthly_limit_usd > 0 else 0
                
                self.logger.info(f"  {category.value}: Daily ${daily_spent:.2f} ({daily_pct:.1f}%), Monthly ${monthly_spent:.2f} ({monthly_pct:.1f}%)")
                
        except Exception as e:
            self.logger.error(f"❌ Status logging failed: {e}")
    
    def _cleanup_old_records(self):
        """Clean up old cost records"""
        try:
            retention_days = self.cost_config['cost_tracking_retention_days']
            cutoff_date = datetime.now() - timedelta(days=retention_days)
            
            # Remove old records
            original_count = len(self.cost_records)
            self.cost_records = [
                record for record in self.cost_records 
                if record.timestamp >= cutoff_date
            ]
            
            removed_count = original_count - len(self.cost_records)
            if removed_count > 0:
                self.logger.info(f"🧹 Cleaned up {removed_count} old cost records")
                
        except Exception as e:
            self.logger.error(f"❌ Record cleanup failed: {e}")
    
    def get_cost_statistics(self) -> Dict[str, Any]:
        """Get comprehensive cost statistics"""
        try:
            # Calculate totals
            total_daily = sum(self.current_daily_spending.values())
            total_monthly = sum(self.current_monthly_spending.values())
            
            # Category breakdown
            category_stats = {}
            for category in CostCategory:
                budget = self.budget_limits.get(category)
                if budget:
                    daily_spent = self.current_daily_spending.get(category, 0)
                    monthly_spent = self.current_monthly_spending.get(category, 0)
                    
                    category_stats[category.value] = {
                        'daily_spent': daily_spent,
                        'monthly_spent': monthly_spent,
                        'daily_limit': budget.daily_limit_usd,
                        'monthly_limit': budget.monthly_limit_usd,
                        'daily_percentage': (daily_spent / budget.daily_limit_usd) * 100 if budget.daily_limit_usd > 0 else 0,
                        'monthly_percentage': (monthly_spent / budget.monthly_limit_usd) * 100 if budget.monthly_limit_usd > 0 else 0,
                        'status': self._get_budget_status(category, daily_spent, monthly_spent, budget)
                    }
            
            # Recent costs
            recent_costs = [
                {
                    'category': record.category.value,
                    'provider': record.provider,
                    'service': record.service,
                    'cost_usd': record.cost_usd,
                    'timestamp': record.timestamp.isoformat()
                }
                for record in self.cost_records[-10:]  # Last 10 records
            ]
            
            return {
                'total_daily_spending': total_daily,
                'total_monthly_spending': total_monthly,
                'category_breakdown': category_stats,
                'recent_costs': recent_costs,
                'total_records': len(self.cost_records),
                'active_alerts': len([a for a in self.cost_alerts if not a.acknowledged]),
                'budget_limits_count': len(self.budget_limits)
            }
            
        except Exception as e:
            self.logger.error(f"❌ Failed to get cost statistics: {e}")
            return {}
    
    def _get_budget_status(self, category: CostCategory, daily_spent: float, 
                          monthly_spent: float, budget: BudgetLimit) -> BudgetStatus:
        """Get budget status"""
        try:
            daily_pct = (daily_spent / budget.daily_limit_usd) if budget.daily_limit_usd > 0 else 0
            monthly_pct = (monthly_spent / budget.monthly_limit_usd) if budget.monthly_limit_usd > 0 else 0
            
            max_pct = max(daily_pct, monthly_pct)
            
            if max_pct >= 1.0:
                return BudgetStatus.EXHAUSTED
            elif max_pct >= budget.block_threshold:
                return BudgetStatus.BLOCKED
            elif max_pct >= budget.alert_threshold:
                return BudgetStatus.CRITICAL
            elif max_pct >= 0.5:
                return BudgetStatus.WARNING
            else:
                return BudgetStatus.HEALTHY
                
        except Exception:
            return BudgetStatus.HEALTHY
    
    def acknowledge_alert(self, alert_id: str) -> bool:
        """Acknowledge cost alert"""
        try:
            for alert in self.cost_alerts:
                if alert.id == alert_id:
                    alert.acknowledged = True
                    self.logger.info(f"✅ Alert acknowledged: {alert_id}")
                    return True
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Alert acknowledgment failed: {e}")
            return False

# Global cost controller instance
cost_controller = CostController()
