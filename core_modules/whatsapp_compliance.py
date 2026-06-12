"""
LUMINA OS - WhatsApp Compliance & 24-Hour Rule Manager
Enterprise-grade WhatsApp API compliance and message quality management
"""

import os
import logging
import asyncio
import json
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

# Database imports
from prisma import Prisma

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MessageType(Enum):
    """WhatsApp message types with compliance rules"""
    SERVICE = "service"  # Always allowed (customer service)
    TRANSACTIONAL = "transactional"  # Always allowed (order confirmations)
    PROMOTIONAL = "promotional"  # 24-hour rule applies
    MARKETING = "marketing"  # 24-hour rule applies

class MessageStatus(Enum):
    """WhatsApp message delivery status"""
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"
    BOUNCED = "bounced"

class QualityRating(Enum):
    """WhatsApp number quality rating"""
    HIGH = "high"      # Green - Excellent
    MEDIUM = "medium"  # Yellow - Good
    LOW = "low"        # Orange - Warning
    BLOCKED = "blocked" # Red - Blocked

@dataclass
class MessageRecord:
    """WhatsApp message record for compliance tracking"""
    id: str
    phone_number: str
    message_type: MessageType
    content: str
    template_name: Optional[str]
    sent_at: datetime
    last_customer_interaction: datetime
    delivery_status: MessageStatus
    quality_rating: QualityRating
    is_compliant: bool
    violation_reason: Optional[str]
    retry_count: int
    created_at: datetime

@dataclass
class ComplianceRule:
    """WhatsApp compliance rule"""
    id: str
    name: str
    description: str
    message_type: MessageType
    time_window_hours: int
    max_messages_per_window: int
    cooldown_hours: int
    is_active: bool

class WhatsAppCompliance:
    """
    Enterprise-grade WhatsApp compliance manager
    Ensures 24-hour rule compliance and maintains message quality
    """
    
    def __init__(self):
        """Initialize WhatsApp compliance manager"""
        self.logger = logging.getLogger(__name__)
        
        # Database connection
        self.db = None
        self._initialize_database()
        
        # Compliance rules
        self.compliance_rules = self._initialize_compliance_rules()
        
        # Message tracking
        self.message_history: Dict[str, List[MessageRecord]] = {}
        
        # Number quality tracking
        self.number_quality: Dict[str, QualityRating] = {}
        
        # Bounced number tracking
        self.bounced_numbers: Dict[str, datetime] = {}
        
        # Rate limiting
        self.rate_limits: Dict[str, List[datetime]] = {}
        
        self.logger.info("📱 WhatsApp Compliance Manager initialized")
        self.logger.info(f"📋 Compliance rules loaded: {len(self.compliance_rules)}")
    
    def _initialize_database(self):
        """Initialize database connection"""
        try:
            self.db = Prisma()
            self.logger.info("📊 WhatsApp Compliance database connected")
        except Exception as e:
            self.logger.error(f"❌ Database connection failed: {e}")
            self.db = None
    
    def _initialize_compliance_rules(self) -> List[ComplianceRule]:
        """Initialize WhatsApp compliance rules"""
        rules = [
            ComplianceRule(
                id="service_24x7",
                name="Service Messages 24/7",
                description="Customer service messages always allowed",
                message_type=MessageType.SERVICE,
                time_window_hours=24,
                max_messages_per_window=999,  # Unlimited
                cooldown_hours=0,
                is_active=True
            ),
            ComplianceRule(
                id="transactional_24x7",
                name="Transactional Messages 24/7",
                description="Order confirmations and updates always allowed",
                message_type=MessageType.TRANSACTIONAL,
                time_window_hours=24,
                max_messages_per_window=999,  # Unlimited
                cooldown_hours=0,
                is_active=True
            ),
            ComplianceRule(
                id="promotional_24hr",
                name="Promotional 24-Hour Rule",
                description="Promotional messages within 24-hour window",
                message_type=MessageType.PROMOTIONAL,
                time_window_hours=24,
                max_messages_per_window=5,
                cooldown_hours=1,
                is_active=True
            ),
            ComplianceRule(
                id="marketing_24hr",
                name="Marketing 24-Hour Rule",
                description="Marketing messages within 24-hour window",
                message_type=MessageType.MARKETING,
                time_window_hours=24,
                max_messages_per_window=3,
                cooldown_hours=2,
                is_active=True
            )
        ]
        return rules
    
    async def check_compliance(self, phone_number: str, message_type: MessageType, 
                              content: str, template_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Check if message complies with WhatsApp rules
        
        Args:
            phone_number: Target phone number
            message_type: Type of message to send
            content: Message content
            template_name: WhatsApp template name (if applicable)
            
        Returns:
            Dict with compliance result
        """
        try:
            # Check if number is blocked
            if phone_number in self.bounced_numbers:
                bounce_time = self.bounced_numbers[phone_number]
                if datetime.now() - bounce_time < timedelta(days=7):
                    return {
                        'compliant': False,
                        'reason': 'Number temporarily blocked due to previous bounce',
                        'quality_rating': QualityRating.BLOCKED.value,
                        'can_send': False
                    }
                else:
                    # Remove from blocked list after 7 days
                    del self.bounced_numbers[phone_number]
            
            # Get compliance rule for message type
            rule = self._get_compliance_rule(message_type)
            if not rule or not rule.is_active:
                return {
                    'compliant': False,
                    'reason': f'No active compliance rule for {message_type.value}',
                    'can_send': False
                }
            
            # Check 24-hour rule for promotional/marketing messages
            if message_type in [MessageType.PROMOTIONAL, MessageType.MARKETING]:
                last_interaction = await self._get_last_customer_interaction(phone_number)
                if last_interaction:
                    time_since_interaction = datetime.now() - last_interaction
                    if time_since_interaction > timedelta(hours=rule.time_window_hours):
                        return {
                            'compliant': False,
                            'reason': f'24-hour rule violated. Last interaction: {last_interaction}',
                            'hours_since_interaction': time_since_interaction.total_seconds() / 3600,
                            'can_send': False,
                            'requires_customer_reply': True
                        }
            
            # Check rate limiting
            rate_limit_ok = await self._check_rate_limit(phone_number, rule)
            if not rate_limit_ok:
                return {
                    'compliant': False,
                    'reason': 'Rate limit exceeded',
                    'can_send': False,
                    'cooldown_hours': rule.cooldown_hours
                }
            
            # Check number quality
            quality = self._get_number_quality(phone_number)
            if quality == QualityRating.BLOCKED:
                return {
                    'compliant': False,
                    'reason': 'Number quality rating is BLOCKED',
                    'quality_rating': quality.value,
                    'can_send': False
                }
            
            # Check cooldown period
            cooldown_ok = await self._check_cooldown_period(phone_number, rule)
            if not cooldown_ok:
                return {
                    'compliant': False,
                    'reason': 'Message in cooldown period',
                    'can_send': False,
                    'cooldown_hours': rule.cooldown_hours
                }
            
            return {
                'compliant': True,
                'can_send': True,
                'quality_rating': quality.value,
                'message_type': message_type.value,
                'rule_applied': rule.name
            }
            
        except Exception as e:
            self.logger.error(f"❌ Compliance check failed: {e}")
            return {
                'compliant': False,
                'reason': f'Compliance check error: {str(e)}',
                'can_send': False
            }
    
    async def record_message(self, phone_number: str, message_type: MessageType, 
                           content: str, delivery_status: MessageStatus,
                           template_name: Optional[str] = None) -> str:
        """
        Record message for compliance tracking
        
        Args:
            phone_number: Target phone number
            message_type: Type of message sent
            content: Message content
            delivery_status: Delivery status
            template_name: WhatsApp template name
            
        Returns:
            str: Message record ID
        """
        try:
            message_id = f"msg_{int(datetime.now().timestamp() * 1000000)}"
            
            # Get last customer interaction
            last_interaction = await self._get_last_customer_interaction(phone_number)
            
            # Create message record
            record = MessageRecord(
                id=message_id,
                phone_number=phone_number,
                message_type=message_type,
                content=content,
                template_name=template_name,
                sent_at=datetime.now(),
                last_customer_interaction=last_interaction or datetime.now(),
                delivery_status=delivery_status,
                quality_rating=self._get_number_quality(phone_number),
                is_compliant=True,
                violation_reason=None,
                retry_count=0,
                created_at=datetime.now()
            )
            
            # Add to message history
            if phone_number not in self.message_history:
                self.message_history[phone_number] = []
            self.message_history[phone_number].append(record)
            
            # Save to database
            if self.db:
                await self._save_message_record(record)
            
            self.logger.info(f"📝 Message recorded: {message_id} to {phone_number}")
            
            return message_id
            
        except Exception as e:
            self.logger.error(f"❌ Failed to record message: {e}")
            return ""
    
    async def handle_bounced_message(self, phone_number: str, message_id: str, 
                                   bounce_reason: str) -> bool:
        """
        Handle bounced message and update number quality
        
        Args:
            phone_number: Phone number that bounced
            message_id: ID of the bounced message
            bounce_reason: Reason for bounce
            
        Returns:
            bool: True if handled successfully
        """
        try:
            # Update message record
            if phone_number in self.message_history:
                for record in self.message_history[phone_number]:
                    if record.id == message_id:
                        record.delivery_status = MessageStatus.BOUNCED
                        record.violation_reason = bounce_reason
                        break
            
            # Add to bounced numbers list
            self.bounced_numbers[phone_number] = datetime.now()
            
            # Update number quality rating
            current_quality = self._get_number_quality(phone_number)
            new_quality = self._degrade_quality_rating(current_quality)
            self.number_quality[phone_number] = new_quality
            
            # Save to database
            if self.db:
                await self._update_number_quality(phone_number, new_quality)
            
            self.logger.warning(f"🚫 Message bounced: {message_id} to {phone_number}")
            self.logger.warning(f"📉 Quality degraded: {current_quality.value} → {new_quality.value}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to handle bounced message: {e}")
            return False
    
    async def update_customer_interaction(self, phone_number: str, 
                                         interaction_type: str = "message") -> bool:
        """
        Update last customer interaction time
        
        Args:
            phone_number: Customer phone number
            interaction_type: Type of interaction (message, call, etc.)
            
        Returns:
            bool: True if updated successfully
        """
        try:
            # Update message history
            if phone_number in self.message_history:
                for record in self.message_history[phone_number]:
                    record.last_customer_interaction = datetime.now()
            
            # Save to database
            if self.db:
                await self._update_customer_interaction(phone_number, datetime.now())
            
            self.logger.info(f"🔄 Customer interaction updated: {phone_number}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to update customer interaction: {e}")
            return False
    
    async def get_compliance_report(self, days: int = 30) -> Dict[str, Any]:
        """
        Generate compliance report
        
        Args:
            days: Number of days to analyze
            
        Returns:
            Dict with compliance metrics
        """
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            # Analyze message history
            total_messages = 0
            compliant_messages = 0
            bounced_messages = 0
            blocked_numbers = 0
            
            message_type_stats = {}
            quality_stats = {}
            
            for phone_number, records in self.message_history.items():
                for record in records:
                    if record.created_at >= cutoff_date:
                        total_messages += 1
                        
                        if record.is_compliant:
                            compliant_messages += 1
                        
                        if record.delivery_status == MessageStatus.BOUNCED:
                            bounced_messages += 1
                        
                        # Message type stats
                        msg_type = record.message_type.value
                        message_type_stats[msg_type] = message_type_stats.get(msg_type, 0) + 1
                        
                        # Quality stats
                        quality = record.quality_rating.value
                        quality_stats[quality] = quality_stats.get(quality, 0) + 1
            
            # Calculate compliance rate
            compliance_rate = (compliant_messages / total_messages * 100) if total_messages > 0 else 0
            bounce_rate = (bounced_messages / total_messages * 100) if total_messages > 0 else 0
            
            # Count blocked numbers
            blocked_numbers = len([num for num, quality in self.number_quality.items() 
                                 if quality == QualityRating.BLOCKED])
            
            return {
                'period_days': days,
                'total_messages': total_messages,
                'compliant_messages': compliant_messages,
                'bounced_messages': bounced_messages,
                'blocked_numbers': blocked_numbers,
                'compliance_rate': compliance_rate,
                'bounce_rate': bounce_rate,
                'message_type_stats': message_type_stats,
                'quality_stats': quality_stats,
                'active_rules': len([r for r in self.compliance_rules if r.is_active])
            }
            
        except Exception as e:
            self.logger.error(f"❌ Failed to generate compliance report: {e}")
            return {}
    
    def _get_compliance_rule(self, message_type: MessageType) -> Optional[ComplianceRule]:
        """Get compliance rule for message type"""
        for rule in self.compliance_rules:
            if rule.message_type == message_type and rule.is_active:
                return rule
        return None
    
    async def _get_last_customer_interaction(self, phone_number: str) -> Optional[datetime]:
        """Get last customer interaction time"""
        if phone_number in self.message_history:
            records = self.message_history[phone_number]
            if records:
                # Return the most recent interaction
                return max(record.last_customer_interaction for record in records)
        return None
    
    async def _check_rate_limit(self, phone_number: str, rule: ComplianceRule) -> bool:
        """Check rate limiting for phone number"""
        try:
            now = datetime.now()
            window_start = now - timedelta(hours=rule.time_window_hours)
            
            # Get recent messages
            if phone_number not in self.message_history:
                return True
            
            recent_messages = [
                record for record in self.message_history[phone_number]
                if record.sent_at >= window_start and record.message_type == rule.message_type
            ]
            
            return len(recent_messages) < rule.max_messages_per_window
            
        except Exception as e:
            self.logger.error(f"❌ Rate limit check failed: {e}")
            return False
    
    async def _check_cooldown_period(self, phone_number: str, rule: ComplianceRule) -> bool:
        """Check cooldown period for phone number"""
        try:
            if rule.cooldown_hours == 0:
                return True
            
            if phone_number not in self.message_history:
                return True
            
            # Get last message of this type
            last_message = None
            for record in reversed(self.message_history[phone_number]):
                if record.message_type == rule.message_type:
                    last_message = record
                    break
            
            if not last_message:
                return True
            
            cooldown_end = last_message.sent_at + timedelta(hours=rule.cooldown_hours)
            return datetime.now() >= cooldown_end
            
        except Exception as e:
            self.logger.error(f"❌ Cooldown check failed: {e}")
            return False
    
    def _get_number_quality(self, phone_number: str) -> QualityRating:
        """Get number quality rating"""
        return self.number_quality.get(phone_number, QualityRating.HIGH)
    
    def _degrade_quality_rating(self, current: QualityRating) -> QualityRating:
        """Degrade quality rating by one level"""
        if current == QualityRating.HIGH:
            return QualityRating.MEDIUM
        elif current == QualityRating.MEDIUM:
            return QualityRating.LOW
        elif current == QualityRating.LOW:
            return QualityRating.BLOCKED
        else:
            return QualityRating.BLOCKED
    
    async def _save_message_record(self, record: MessageRecord):
        """Save message record to database"""
        try:
            # This would save to the actual database
            self.logger.debug(f"📝 Message record saved: {record.id}")
        except Exception as e:
            self.logger.error(f"❌ Failed to save message record: {e}")
    
    async def _update_number_quality(self, phone_number: str, quality: QualityRating):
        """Update number quality in database"""
        try:
            # This would update the actual database
            self.logger.debug(f"📊 Number quality updated: {phone_number} → {quality.value}")
        except Exception as e:
            self.logger.error(f"❌ Failed to update number quality: {e}")
    
    async def _update_customer_interaction(self, phone_number: str, interaction_time: datetime):
        """Update customer interaction in database"""
        try:
            # This would update the actual database
            self.logger.debug(f"🔄 Customer interaction updated: {phone_number}")
        except Exception as e:
            self.logger.error(f"❌ Failed to update customer interaction: {e}")

# Global WhatsApp compliance instance
whatsapp_compliance = WhatsAppCompliance()
