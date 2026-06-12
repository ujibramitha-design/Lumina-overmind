"""
LUMINA OS - Internal Rate Limiter & Abuse Prevention
Enterprise-grade internal rate limiting to prevent abuse and control costs
"""

import os
import logging
import asyncio
import json
import time
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
from collections import defaultdict, deque

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RateLimitType(Enum):
    """Types of rate limiting"""
    PER_USER = "per_user"
    PER_IP = "per_ip"
    PER_SESSION = "per_session"
    GLOBAL = "global"
    PER_ENDPOINT = "per_endpoint"

class ResourceType(Enum):
    """Types of resources to limit"""
    AI_REQUESTS = "ai_requests"
    EMAIL_SEND = "email_send"
    WHATSAPP_SEND = "whatsapp_send"
    FILE_UPLOAD = "file_upload"
    API_CALLS = "api_calls"
    REPORT_GENERATION = "report_generation"
    CAMPAIGN_CREATION = "campaign_creation"

class RateLimitAction(Enum):
    """Actions when rate limit is exceeded"""
    BLOCK = "block"
    QUEUE = "queue"
    THROTTLE = "throttle"
    WARN = "warn"
    ESCALATE = "escalate"

@dataclass
class RateLimitRule:
    """Rate limit rule configuration"""
    id: str
    name: str
    description: str
    resource_type: ResourceType
    limit_type: RateLimitType
    max_requests: int
    time_window_seconds: int
    action: RateLimitAction
    penalty_seconds: int
    escalation_threshold: int
    is_active: bool
    created_at: datetime
    last_updated: datetime

@dataclass
class RateLimitState:
    """Rate limit state tracking"""
    key: str  # user_id, ip_address, session_id, etc.
    resource_type: ResourceType
    request_timestamps: deque  # Timestamps of recent requests
    blocked_until: Optional[datetime]
    violation_count: int
    last_violation: Optional[datetime]
    escalation_level: int
    is_warned: bool

@dataclass
class RateLimitResult:
    """Rate limit check result"""
    allowed: bool
    remaining_requests: int
    reset_time: datetime
    action_taken: RateLimitAction
    penalty_until: Optional[datetime]
    warning_message: Optional[str]
    escalation_level: int

class InternalRateLimiter:
    """
    Enterprise-grade internal rate limiting system
    Prevents abuse and controls costs for internal operations
    """
    
    def __init__(self):
        """Initialize internal rate limiter"""
        self.logger = logging.getLogger(__name__)
        
        # Rate limit rules
        self.rate_limit_rules: Dict[str, RateLimitRule] = {}
        
        # Rate limit states
        self.rate_limit_states: Dict[str, RateLimitState] = {}
        
        # Global counters
        self.global_counters: Dict[ResourceType, deque] = {}
        
        # Debounce tracking
        self.debounce_tracking: Dict[str, float] = {}
        
        # Configuration
        self.limiter_config = self._initialize_limiter_config()
        
        # Initialize default rules
        self._initialize_default_rules()
        
        # Cleanup task
        self.cleanup_task = None
        self._start_cleanup_task()
        
        self.logger.info("🚦 Internal Rate Limiter initialized")
        self.logger.info(f"📋 Default rules loaded: {len(self.rate_limit_rules)}")
    
    def _initialize_limiter_config(self) -> Dict[str, Any]:
        """Initialize rate limiter configuration"""
        return {
            'cleanup_interval_seconds': 300,  # 5 minutes
            'max_state_age_hours': 24,
            'debounce_delay_ms': 1000,  # 1 second default
            'max_violations_per_hour': 10,
            'escalation_threshold': 5,
            'penalty_multiplier': 2,
            'warn_threshold': 0.8,  # Warn at 80% of limit
            'global_limits_enabled': True,
            'per_user_limits_enabled': True,
            'per_ip_limits_enabled': True,
            'logging_enabled': True,
            'metrics_enabled': True
        }
    
    def _initialize_default_rules(self):
        """Initialize default rate limit rules"""
        default_rules = [
            # AI Request Limits
            RateLimitRule(
                id="ai_requests_per_user",
                name="AI Requests Per User",
                description="Limit AI requests per user to prevent cost explosion",
                resource_type=ResourceType.AI_REQUESTS,
                limit_type=RateLimitType.PER_USER,
                max_requests=50,
                time_window_seconds=3600,  # 50 requests per hour
                action=RateLimitAction.THROTTLE,
                penalty_seconds=300,  # 5 minutes penalty
                escalation_threshold=5,
                is_active=True,
                created_at=datetime.now(),
                last_updated=datetime.now()
            ),
            RateLimitRule(
                id="ai_requests_global",
                name="AI Requests Global",
                description="Global AI request limit to control overall costs",
                resource_type=ResourceType.AI_REQUESTS,
                limit_type=RateLimitType.GLOBAL,
                max_requests=1000,
                time_window_seconds=3600,  # 1000 requests per hour globally
                action=RateLimitAction.QUEUE,
                penalty_seconds=600,  # 10 minutes penalty
                escalation_threshold=10,
                is_active=True,
                created_at=datetime.now(),
                last_updated=datetime.now()
            ),
            
            # Email Send Limits
            RateLimitRule(
                id="email_send_per_user",
                name="Email Send Per User",
                description="Limit email sending per user to prevent spam",
                resource_type=ResourceType.EMAIL_SEND,
                limit_type=RateLimitType.PER_USER,
                max_requests=100,
                time_window_seconds=3600,  # 100 emails per hour
                action=RateLimitAction.BLOCK,
                penalty_seconds=900,  # 15 minutes penalty
                escalation_threshold=3,
                is_active=True,
                created_at=datetime.now(),
                last_updated=datetime.now()
            ),
            
            # WhatsApp Send Limits
            RateLimitRule(
                id="whatsapp_send_per_user",
                name="WhatsApp Send Per User",
                description="Limit WhatsApp sending per user for compliance",
                resource_type=ResourceType.WHATSAPP_SEND,
                limit_type=RateLimitType.PER_USER,
                max_requests=200,
                time_window_seconds=3600,  # 200 messages per hour
                action=RateLimitAction.BLOCK,
                penalty_seconds=1800,  # 30 minutes penalty
                escalation_threshold=3,
                is_active=True,
                created_at=datetime.now(),
                last_updated=datetime.now()
            ),
            
            # File Upload Limits
            RateLimitRule(
                id="file_upload_per_user",
                name="File Upload Per User",
                description="Limit file uploads per user to prevent abuse",
                resource_type=ResourceType.FILE_UPLOAD,
                limit_type=RateLimitType.PER_USER,
                max_requests=50,
                time_window_seconds=3600,  # 50 uploads per hour
                action=RateLimitAction.BLOCK,
                penalty_seconds=600,  # 10 minutes penalty
                escalation_threshold=5,
                is_active=True,
                created_at=datetime.now(),
                last_updated=datetime.now()
            ),
            
            # API Call Limits
            RateLimitRule(
                id="api_calls_per_user",
                name="API Calls Per User",
                description="Limit API calls per user to prevent abuse",
                resource_type=ResourceType.API_CALLS,
                limit_type=RateLimitType.PER_USER,
                max_requests=1000,
                time_window_seconds=3600,  # 1000 calls per hour
                action=RateLimitAction.THROTTLE,
                penalty_seconds=300,  # 5 minutes penalty
                escalation_threshold=10,
                is_active=True,
                created_at=datetime.now(),
                last_updated=datetime.now()
            ),
            
            # Report Generation Limits
            RateLimitRule(
                id="report_generation_per_user",
                name="Report Generation Per User",
                description="Limit report generation per user to control resources",
                resource_type=ResourceType.REPORT_GENERATION,
                limit_type=RateLimitType.PER_USER,
                max_requests=20,
                time_window_seconds=3600,  # 20 reports per hour
                action=RateLimitAction.QUEUE,
                penalty_seconds=300,  # 5 minutes penalty
                escalation_threshold=3,
                is_active=True,
                created_at=datetime.now(),
                last_updated=datetime.now()
            ),
            
            # Campaign Creation Limits
            RateLimitRule(
                id="campaign_creation_per_user",
                name="Campaign Creation Per User",
                description="Limit campaign creation per user to prevent spam",
                resource_type=ResourceType.CAMPAIGN_CREATION,
                limit_type=RateLimitType.PER_USER,
                max_requests=10,
                time_window_seconds=3600,  # 10 campaigns per hour
                action=RateLimitAction.ESCALATE,
                penalty_seconds=1800,  # 30 minutes penalty
                escalation_threshold=2,
                is_active=True,
                created_at=datetime.now(),
                last_updated=datetime.now()
            ),
            
            # Rapid Click Prevention (Debounce)
            RateLimitRule(
                id="rapid_click_prevention",
                name="Rapid Click Prevention",
                description="Prevent rapid clicking on critical buttons",
                resource_type=ResourceType.API_CALLS,
                limit_type=RateLimitType.PER_SESSION,
                max_requests=1,
                time_window_seconds=1,  # 1 request per second
                action=RateLimitAction.WARN,
                penalty_seconds=5,  # 5 seconds penalty
                escalation_threshold=5,
                is_active=True,
                created_at=datetime.now(),
                last_updated=datetime.now()
            )
        ]
        
        for rule in default_rules:
            self.rate_limit_rules[rule.id] = rule
    
    async def check_rate_limit(self, resource_type: ResourceType, 
                               identifier: str, limit_type: RateLimitType = RateLimitType.PER_USER,
                               user_id: Optional[str] = None,
                               ip_address: Optional[str] = None,
                               session_id: Optional[str] = None) -> RateLimitResult:
        """
        Check if request is allowed based on rate limits
        
        Args:
            resource_type: Type of resource being accessed
            identifier: Unique identifier for the request
            limit_type: Type of rate limiting to apply
            user_id: User ID (for per-user limiting)
            ip_address: IP address (for per-IP limiting)
            session_id: Session ID (for per-session limiting)
            
        Returns:
            RateLimitResult with check result
        """
        try:
            # Find applicable rules
            applicable_rules = self._find_applicable_rules(resource_type, limit_type)
            
            if not applicable_rules:
                return RateLimitResult(
                    allowed=True,
                    remaining_requests=999,
                    reset_time=datetime.now() + timedelta(hours=1),
                    action_taken=RateLimitAction.BLOCK,
                    penalty_until=None,
                    warning_message=None,
                    escalation_level=0
                )
            
            # Check each rule
            for rule in applicable_rules:
                if not rule.is_active:
                    continue
                
                result = await self._check_rule(rule, identifier, user_id, ip_address, session_id)
                
                if not result.allowed:
                    return result
            
            # All rules passed
            return RateLimitResult(
                allowed=True,
                remaining_requests=999,
                reset_time=datetime.now() + timedelta(hours=1),
                action_taken=RateLimitAction.BLOCK,
                penalty_until=None,
                warning_message=None,
                escalation_level=0
            )
            
        except Exception as e:
            self.logger.error(f"❌ Failed to check rate limit: {e}")
            return RateLimitResult(
                allowed=False,
                remaining_requests=0,
                reset_time=datetime.now() + timedelta(hours=1),
                action_taken=RateLimitAction.BLOCK,
                penalty_until=datetime.now() + timedelta(minutes=5),
                warning_message="Rate limit check failed",
                escalation_level=0
            )
    
    async def _check_rule(self, rule: RateLimitRule, identifier: str,
                         user_id: Optional[str], ip_address: Optional[str],
                         session_id: Optional[str]) -> RateLimitResult:
        """Check specific rate limit rule"""
        try:
            # Get state key
            state_key = self._get_state_key(rule.limit_type, identifier, user_id, ip_address, session_id)
            
            # Get or create state
            state = self._get_or_create_state(state_key, rule.resource_type)
            
            # Check if currently blocked
            if state.blocked_until and datetime.now() < state.blocked_until:
                return RateLimitResult(
                    allowed=False,
                    remaining_requests=0,
                    reset_time=state.blocked_until,
                    action_taken=rule.action,
                    penalty_until=state.blocked_until,
                    warning_message=f"Rate limit exceeded. Try again after {state.blocked_until}",
                    escalation_level=state.escalation_level
                )
            
            # Clean old timestamps
            cutoff_time = datetime.now() - timedelta(seconds=rule.time_window_seconds)
            while state.request_timestamps and state.request_timestamps[0] < cutoff_time:
                state.request_timestamps.popleft()
            
            # Check current count
            current_count = len(state.request_timestamps)
            
            # Calculate remaining requests
            remaining_requests = max(0, rule.max_requests - current_count)
            
            # Check if limit exceeded
            if current_count >= rule.max_requests:
                return await self._handle_limit_exceeded(rule, state)
            
            # Check if near limit (warn)
            warn_threshold = int(rule.max_requests * self.limiter_config['warn_threshold'])
            if current_count >= warn_threshold and not state.is_warned:
                state.is_warned = True
                
                return RateLimitResult(
                    allowed=True,
                    remaining_requests=remaining_requests,
                    reset_time=datetime.now() + timedelta(seconds=rule.time_window_seconds),
                    action_taken=RateLimitAction.WARN,
                    penalty_until=None,
                    warning_message=f"Rate limit warning: {current_count}/{rule.max_requests} requests used",
                    escalation_level=state.escalation_level
                )
            
            # Request allowed
            state.request_timestamps.append(datetime.now())
            state.is_warned = False
            
            return RateLimitResult(
                allowed=True,
                remaining_requests=remaining_requests - 1,
                reset_time=datetime.now() + timedelta(seconds=rule.time_window_seconds),
                action_taken=RateLimitAction.BLOCK,
                penalty_until=None,
                warning_message=None,
                escalation_level=state.escalation_level
            )
            
        except Exception as e:
            self.logger.error(f"❌ Failed to check rule: {e}")
            raise
    
    async def _handle_limit_exceeded(self, rule: RateLimitRule, state: RateLimitState) -> RateLimitResult:
        """Handle rate limit exceeded"""
        try:
            # Increment violation count
            state.violation_count += 1
            state.last_violation = datetime.now()
            
            # Check escalation
            if state.violation_count >= rule.escalation_threshold:
                state.escalation_level += 1
                penalty_multiplier = self.limiter_config['penalty_multiplier']
            else:
                penalty_multiplier = 1
            
            # Calculate penalty
            penalty_seconds = rule.penalty_seconds * penalty_multiplier
            state.blocked_until = datetime.now() + timedelta(seconds=penalty_seconds)
            
            # Log violation
            if self.limiter_config['logging_enabled']:
                self.logger.warning(f"🚨 Rate limit violated: {rule.name}")
                self.logger.warning(f"📊 State: {state.key}, Violations: {state.violation_count}")
                self.logger.warning(f"⏰ Penalty: {penalty_seconds} seconds")
                self.logger.warning(f"📈 Escalation Level: {state.escalation_level}")
            
            # Take action
            if rule.action == RateLimitAction.ESCALATE:
                await self._escalate_violation(rule, state)
            
            return RateLimitResult(
                allowed=False,
                remaining_requests=0,
                reset_time=state.blocked_until,
                action_taken=rule.action,
                penalty_until=state.blocked_until,
                warning_message=f"Rate limit exceeded. Penalty: {penalty_seconds} seconds",
                escalation_level=state.escalation_level
            )
            
        except Exception as e:
            self.logger.error(f"❌ Failed to handle limit exceeded: {e}")
            raise
    
    async def _escalate_violation(self, rule: RateLimitRule, state: RateLimitState):
        """Escalate rate limit violation"""
        try:
            # Create escalation alert
            escalation_data = {
                'rule_id': rule.id,
                'rule_name': rule.name,
                'state_key': state.key,
                'violation_count': state.violation_count,
                'escalation_level': state.escalation_level,
                'blocked_until': state.blocked_until.isoformat() if state.blocked_until else None,
                'timestamp': datetime.now().isoformat()
            }
            
            # Log escalation
            self.logger.error(f"🚨 RATE LIMIT ESCALATION: {rule.name}")
            self.logger.error(f"📊 State: {state.key}")
            self.logger.error(f"📈 Escalation Level: {state.escalation_level}")
            self.logger.error(f"⏰ Blocked Until: {state.blocked_until}")
            
            # Send alert (would integrate with alert system)
            # alert_manager.send_security_alert("Rate Limit Escalation", escalation_data)
            
        except Exception as e:
            self.logger.error(f"❌ Failed to escalate violation: {e}")
    
    def check_debounce(self, key: str, delay_ms: Optional[int] = None) -> bool:
        """
        Check if action should be debounced
        
        Args:
            key: Unique key for the action
            delay_ms: Custom delay in milliseconds
            
        Returns:
            bool: True if action should be debounced
        """
        try:
            current_time = time.time()
            delay_seconds = (delay_ms or self.limiter_config['debounce_delay_ms']) / 1000
            
            if key not in self.debounce_tracking:
                self.debounce_tracking[key] = current_time
                return False
            
            last_time = self.debounce_tracking[key]
            
            if current_time - last_time >= delay_seconds:
                self.debounce_tracking[key] = current_time
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to check debounce: {e}")
            return False
    
    def _find_applicable_rules(self, resource_type: ResourceType, limit_type: RateLimitType) -> List[RateLimitRule]:
        """Find applicable rate limit rules"""
        applicable = []
        
        for rule in self.rate_limit_rules.values():
            if (rule.resource_type == resource_type and 
                rule.limit_type == limit_type and
                rule.is_active):
                applicable.append(rule)
        
        # Sort by priority (max_requests descending - stricter rules first)
        applicable.sort(key=lambda x: x.max_requests)
        
        return applicable
    
    def _get_state_key(self, limit_type: RateLimitType, identifier: str,
                       user_id: Optional[str], ip_address: Optional[str],
                       session_id: Optional[str]) -> str:
        """Get state key for rate limiting"""
        if limit_type == RateLimitType.PER_USER and user_id:
            return f"user:{user_id}:{identifier}"
        elif limit_type == RateLimitType.PER_IP and ip_address:
            return f"ip:{ip_address}:{identifier}"
        elif limit_type == RateLimitType.PER_SESSION and session_id:
            return f"session:{session_id}:{identifier}"
        elif limit_type == RateLimitType.GLOBAL:
            return f"global:{identifier}"
        else:
            return f"unknown:{identifier}"
    
    def _get_or_create_state(self, state_key: str, resource_type: ResourceType) -> RateLimitState:
        """Get or create rate limit state"""
        if state_key not in self.rate_limit_states:
            self.rate_limit_states[state_key] = RateLimitState(
                key=state_key,
                resource_type=resource_type,
                request_timestamps=deque(maxlen=1000),
                blocked_until=None,
                violation_count=0,
                last_violation=None,
                escalation_level=0,
                is_warned=False
            )
        
        return self.rate_limit_states[state_key]
    
    def _start_cleanup_task(self):
        """Start cleanup task for old states"""
        if self.cleanup_task:
            return
        
        self.cleanup_task = asyncio.create_task(self._cleanup_old_states())
    
    async def _cleanup_old_states(self):
        """Cleanup old rate limit states"""
        try:
            while True:
                await asyncio.sleep(self.limiter_config['cleanup_interval_seconds'])
                
                cutoff_time = datetime.now() - timedelta(hours=self.limiter_config['max_state_age_hours'])
                
                # Clean old states
                keys_to_remove = []
                for key, state in self.rate_limit_states.items():
                    if (state.last_violation and state.last_violation < cutoff_time and
                        len(state.request_timestamps) == 0 and
                        not state.blocked_until):
                        keys_to_remove.append(key)
                
                for key in keys_to_remove:
                    del self.rate_limit_states[key]
                
                # Clean debounce tracking
                current_time = time.time()
                debounce_keys_to_remove = []
                for key, last_time in self.debounce_tracking.items():
                    if current_time - last_time > 3600:  # 1 hour
                        debounce_keys_to_remove.append(key)
                
                for key in debounce_keys_to_remove:
                    del self.debounce_tracking[key]
                
                if keys_to_remove or debounce_keys_to_remove:
                    self.logger.info(f"🧹 Cleaned up {len(keys_to_remove)} rate limit states and {len(debounce_keys_to_remove)} debounce entries")
                
        except Exception as e:
            self.logger.error(f"❌ Cleanup task error: {e}")
    
    def get_rate_limit_statistics(self) -> Dict[str, Any]:
        """Get rate limiting statistics"""
        try:
            total_states = len(self.rate_limit_states)
            blocked_states = len([s for s in self.rate_limit_states.values() if s.blocked_until and s.blocked_until > datetime.now()])
            warned_states = len([s for s in self.rate_limit_states.values() if s.is_warned])
            
            # Violation statistics
            total_violations = sum(s.violation_count for s in self.rate_limit_states.values())
            escalation_levels = [s.escalation_level for s in self.rate_limit_states.values()]
            
            # Rule statistics
            active_rules = len([r for r in self.rate_limit_rules.values() if r.is_active])
            
            return {
                'total_states': total_states,
                'blocked_states': blocked_states,
                'warned_states': warned_states,
                'total_violations': total_violations,
                'max_escalation_level': max(escalation_levels) if escalation_levels else 0,
                'active_rules': active_rules,
                'total_rules': len(self.rate_limit_rules),
                'debounce_tracked_keys': len(self.debounce_tracking)
            }
            
        except Exception as e:
            self.logger.error(f"❌ Failed to get rate limit statistics: {e}")
            return {}
    
    def add_rate_limit_rule(self, rule_id: str, name: str, description: str,
                           resource_type: ResourceType, limit_type: RateLimitType,
                           max_requests: int, time_window_seconds: int,
                           action: RateLimitAction, penalty_seconds: int = 300) -> bool:
        """
        Add new rate limit rule
        
        Args:
            rule_id: Unique rule ID
            name: Rule name
            description: Rule description
            resource_type: Resource type to limit
            limit_type: Type of limiting
            max_requests: Maximum requests allowed
            time_window_seconds: Time window in seconds
            action: Action when limit exceeded
            penalty_seconds: Penalty duration in seconds
            
        Returns:
            bool: True if added successfully
        """
        try:
            rule = RateLimitRule(
                id=rule_id,
                name=name,
                description=description,
                resource_type=resource_type,
                limit_type=limit_type,
                max_requests=max_requests,
                time_window_seconds=time_window_seconds,
                action=action,
                penalty_seconds=penalty_seconds,
                escalation_threshold=5,
                is_active=True,
                created_at=datetime.now(),
                last_updated=datetime.now()
            )
            
            self.rate_limit_rules[rule_id] = rule
            
            self.logger.info(f"📋 Rate limit rule added: {rule_id} - {name}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to add rate limit rule: {e}")
            return False
    
    def update_rule_status(self, rule_id: str, is_active: bool) -> bool:
        """
        Update rule active status
        
        Args:
            rule_id: Rule ID
            is_active: Active status
            
        Returns:
            bool: True if updated successfully
        """
        try:
            if rule_id in self.rate_limit_rules:
                self.rate_limit_rules[rule_id].is_active = is_active
                self.rate_limit_rules[rule_id].last_updated = datetime.now()
                
                self.logger.info(f"📋 Rule status updated: {rule_id} -> {'Active' if is_active else 'Inactive'}")
                
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Failed to update rule status: {e}")
            return False
    
    def reset_user_limits(self, user_id: str) -> bool:
        """
        Reset rate limits for specific user
        
        Args:
            user_id: User ID to reset
            
        Returns:
            bool: True if reset successfully
        """
        try:
            keys_to_reset = [key for key in self.rate_limit_states.keys() if key.startswith(f"user:{user_id}:")]
            
            for key in keys_to_reset:
                state = self.rate_limit_states[key]
                state.request_timestamps.clear()
                state.blocked_until = None
                state.violation_count = 0
                state.escalation_level = 0
                state.is_warned = False
            
            self.logger.info(f"🔄 Rate limits reset for user: {user_id} ({len(keys_to_reset)} states)")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to reset user limits: {e}")
            return False

# Global internal rate limiter instance
internal_rate_limiter = InternalRateLimiter()
