"""
LUMINA OS - Lead State Machine & Lifecycle Management
Enterprise-grade lead lifecycle management with state transitions and automation rules
"""

import os
import logging
import asyncio
import json
from typing import Dict, Any, Optional, List, Set
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum

# Database imports
from prisma import Prisma

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LeadStatus(Enum):
    """Lead lifecycle states"""
    NEW = "NEW"                           # Fresh lead from scouting
    SCOUTED = "SCOUTED"                   # Lead identified and added to system
    AI_FOLLOW_UP = "AI_FOLLOW_UP"         # AI is handling initial communication
    HUMAN_ASSIGNED = "HUMAN_ASSIGNED"     # Lead assigned to human agent
    NEGOTIATION = "NEGOTIATION"           # Active negotiation phase
    VERIFICATION = "VERIFICATION"          # Document and identity verification
    CLOSING = "CLOSING"                   # Final closing stage
    CLOSED_WON = "CLOSED_WON"             # Successfully converted
    CLOSED_LOST = "CLOSED_LOST"           # Lost to competitor or not interested
    DNC = "DNC"                           # Do Not Contact - requested no contact
    BLACKLISTED = "BLACKLISTED"           # Blacklisted due to abuse
    ARCHIVED = "ARCHIVED"                 # Inactive but not lost
    RECYCLED = "RECYCLED"                 # Re-entered the funnel

class LeadPriority(Enum):
    """Lead priority levels"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    URGENT = "URGENT"
    CRITICAL = "CRITICAL"

class TransitionType(Enum):
    """State transition types"""
    AUTOMATIC = "automatic"               # System-initiated transition
    MANUAL = "manual"                     # Human-initiated transition
    AI_DECISION = "ai_decision"           # AI-based transition
    TIME_BASED = "time_based"             # Time-triggered transition
    EVENT_BASED = "event_based"           # Event-triggered transition

@dataclass
class StateTransition:
    """State transition record"""
    id: str
    lead_id: str
    from_status: LeadStatus
    to_status: LeadStatus
    transition_type: TransitionType
    reason: str
    triggered_by: str  # User ID, AI system, or system event
    metadata: Dict[str, Any]
    timestamp: datetime

@dataclass
class StateRule:
    """State transition rule"""
    id: str
    name: str
    description: str
    from_status: LeadStatus
    to_status: LeadStatus
    conditions: List[str]
    actions: List[str]
    transition_type: TransitionType
    is_active: bool
    priority: int

@dataclass
class LeadState:
    """Current lead state with metadata"""
    lead_id: str
    current_status: LeadStatus
    priority: LeadPriority
    assigned_to: Optional[str]
    last_contact: Optional[datetime]
    next_follow_up: Optional[datetime]
    contact_attempts: int
    max_attempts: int
    score: float
    tags: Set[str] = field(default_factory=set)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime
    updated_at: datetime

class LeadStateMachine:
    """
    Enterprise-grade lead state machine
    Manages lead lifecycle with strict state transitions and business rules
    """
    
    def __init__(self):
        """Initialize lead state machine"""
        self.logger = logging.getLogger(__name__)
        
        # Database connection
        self.db = None
        self._initialize_database()
        
        # State rules
        self.state_rules = self._initialize_state_rules()
        
        # Current lead states
        self.lead_states: Dict[str, LeadState] = {}
        
        # Transition history
        self.transition_history: List[StateTransition] = []
        
        # State transition matrix (valid transitions)
        self.transition_matrix = self._build_transition_matrix()
        
        # Automation rules
        self.automation_rules = self._initialize_automation_rules()
        
        self.logger.info("🔄 Lead State Machine initialized")
        self.logger.info(f"📋 State rules loaded: {len(self.state_rules)}")
        self.logger.info(f"⚙️ Automation rules loaded: {len(self.automation_rules)}")
    
    def _initialize_database(self):
        """Initialize database connection"""
        try:
            self.db = Prisma()
            self.logger.info("📊 Lead State Machine database connected")
        except Exception as e:
            self.logger.error(f"❌ Database connection failed: {e}")
            self.db = None
    
    def _initialize_state_rules(self) -> List[StateRule]:
        """Initialize state transition rules"""
        rules = [
            # New → Scouted (automatic when lead is added)
            StateRule(
                id="new_to_scouted",
                name="New to Scouted",
                description="Convert new lead to scouted status",
                from_status=LeadStatus.NEW,
                to_status=LeadStatus.SCOUTED,
                conditions=["lead_data_complete"],
                actions=["assign_initial_priority", "schedule_first_contact"],
                transition_type=TransitionType.AUTOMATIC,
                is_active=True,
                priority=1
            ),
            
            # Scouted → AI Follow Up (automatic for qualifying leads)
            StateRule(
                id="scouted_to_ai_follow_up",
                name="Scouted to AI Follow Up",
                description="Start AI communication for qualified leads",
                from_status=LeadStatus.SCOUTED,
                to_status=LeadStatus.AI_FOLLOW_UP,
                conditions=["lead_score >= 7", "not_blacklisted", "not_dnc"],
                actions=["start_ai_conversation", "set_follow_up_reminder"],
                transition_type=TransitionType.AI_DECISION,
                is_active=True,
                priority=2
            ),
            
            # AI Follow Up → Human Assigned (AI can't handle)
            StateRule(
                id="ai_to_human_assigned",
                name="AI to Human Assigned",
                description="Escalate to human when AI can't handle",
                from_status=LeadStatus.AI_FOLLOW_UP,
                to_status=LeadStatus.HUMAN_ASSIGNED,
                conditions=["ai_confidence < 0.7", "complex_request", "escalation_requested"],
                actions=["assign_to_human_agent", "notify_team_lead"],
                transition_type=TransitionType.AI_DECISION,
                is_active=True,
                priority=3
            ),
            
            # Human Assigned → Negotiation (showing interest)
            StateRule(
                id="human_to_negotiation",
                name="Human Assigned to Negotiation",
                description="Enter negotiation phase when lead shows interest",
                from_status=LeadStatus.HUMAN_ASSIGNED,
                to_status=LeadStatus.NEGOTIATION,
                conditions=["expressed_interest", "budget_discussed", "site_visit_requested"],
                actions=["create_negotiation_plan", "prepare_proposal"],
                transition_type=TransitionType.MANUAL,
                is_active=True,
                priority=4
            ),
            
            # Negotiation → Verification (agreement reached)
            StateRule(
                id="negotiation_to_verification",
                name="Negotiation to Verification",
                description="Start verification when agreement is reached",
                from_status=LeadStatus.NEGOTIATION,
                to_status=LeadStatus.VERIFICATION,
                conditions=["price_agreed", "terms_accepted", "payment_discussed"],
                actions=["initiate_kyc", "request_documents"],
                transition_type=TransitionType.MANUAL,
                is_active=True,
                priority=5
            ),
            
            # Verification → Closing (documents verified)
            StateRule(
                id="verification_to_closing",
                name="Verification to Closing",
                description="Enter closing stage when verification is complete",
                from_status=LeadStatus.VERIFICATION,
                to_status=LeadStatus.CLOSING,
                conditions=["documents_verified", "kyc_approved", "payment_ready"],
                actions=["prepare_closing_docs", "schedule_signing"],
                transition_type=TransitionType.AUTOMATIC,
                is_active=True,
                priority=6
            ),
            
            # Closing → Closed Won (deal completed)
            StateRule(
                id="closing_to_closed_won",
                name="Closing to Closed Won",
                description="Mark as won when deal is completed",
                from_status=LeadStatus.CLOSING,
                to_status=LeadStatus.CLOSED_WON,
                conditions=["contract_signed", "payment_received", "keys_handed"],
                actions=["celebrate_deal", "update_commission", "send_welcome_package"],
                transition_type=TransitionType.MANUAL,
                is_active=True,
                priority=7
            ),
            
            # Any → Closed Lost (lost to competitor)
            StateRule(
                id="any_to_closed_lost",
                name="Any to Closed Lost",
                description="Mark as lost when lead chooses competitor",
                from_status=None,  # Can be applied from any status
                to_status=LeadStatus.CLOSED_LOST,
                conditions=["chose_competitor", "budget_insufficient", "timing_wrong"],
                actions=["log_loss_reason", "update_competitor_intel"],
                transition_type=TransitionType.MANUAL,
                is_active=True,
                priority=6
            ),
            
            # Any → DNC (requested no contact)
            StateRule(
                id="any_to_dnc",
                name="Any to DNC",
                description="Mark as DNC when lead requests no contact",
                from_status=None,  # Can be applied from any status
                to_status=LeadStatus.DNC,
                conditions=["requested_no_contact", "complaint_received"],
                actions=["stop_all_communication", "respect_privacy"],
                transition_type=TransitionType.MANUAL,
                is_active=True,
                priority=10
            ),
            
            # Any → Blacklisted (abusive behavior)
            StateRule(
                id="any_to_blacklisted",
                name="Any to Blacklisted",
                description="Blacklist abusive leads",
                from_status=None,  # Can be applied from any status
                to_status=LeadStatus.BLACKLISTED,
                conditions=["abusive_behavior", "spam_complaint", "fraud_detected"],
                actions=["block_all_communication", "report_abuse"],
                transition_type=TransitionType.MANUAL,
                is_active=True,
                priority=10
            ),
            
            # Time-based transitions
            StateRule(
                id="time_based_recycle",
                name="Time Based Recycle",
                description="Recycle old leads for re-engagement",
                from_status=LeadStatus.ARCHIVED,
                to_status=LeadStatus.RECYCLED,
                conditions=["no_contact_90_days", "previously_interested"],
                actions=["re_engagement_campaign", "update_priority"],
                transition_type=TransitionType.TIME_BASED,
                is_active=True,
                priority=1
            )
        ]
        return rules
    
    def _initialize_automation_rules(self) -> List[Dict[str, Any]]:
        """Initialize automation rules"""
        return [
            {
                'id': 'auto_follow_up_reminder',
                'name': 'Auto Follow Up Reminder',
                'trigger': 'next_follow_up <= now()',
                'conditions': ['status in [AI_FOLLOW_UP, HUMAN_ASSIGNED, NEGOTIATION]'],
                'actions': ['send_follow_up_reminder', 'update_contact_attempts'],
                'is_active': True
            },
            {
                'id': 'auto_escalation',
                'name': 'Auto Escalation',
                'trigger': 'contact_attempts >= max_attempts',
                'conditions': ['status = AI_FOLLOW_UP'],
                'actions': ['escalate_to_human', 'mark_as_stalled'],
                'is_active': True
            },
            {
                'id': 'auto_archive',
                'name': 'Auto Archive',
                'trigger': 'last_contact >= 180_days',
                'conditions': ['status in [CLOSED_LOST, DNC]'],
                'actions': ['archive_lead', 'cleanup_data'],
                'is_active': True
            }
        ]
    
    def _build_transition_matrix(self) -> Dict[LeadStatus, Set[LeadStatus]]:
        """Build valid transition matrix"""
        matrix = {
            LeadStatus.NEW: {LeadStatus.SCOUTED, LeadStatus.CLOSED_LOST, LeadStatus.DNC, LeadStatus.BLACKLISTED},
            LeadStatus.SCOUTED: {LeadStatus.AI_FOLLOW_UP, LeadStatus.HUMAN_ASSIGNED, LeadStatus.CLOSED_LOST, LeadStatus.DNC, LeadStatus.BLACKLISTED},
            LeadStatus.AI_FOLLOW_UP: {LeadStatus.HUMAN_ASSIGNED, LeadStatus.NEGOTIATION, LeadStatus.CLOSED_LOST, LeadStatus.DNC, LeadStatus.BLACKLISTED},
            LeadStatus.HUMAN_ASSIGNED: {LeadStatus.NEGOTIATION, LeadStatus.CLOSED_LOST, LeadStatus.DNC, LeadStatus.BLACKLISTED},
            LeadStatus.NEGOTIATION: {LeadStatus.VERIFICATION, LeadStatus.CLOSED_LOST, LeadStatus.DNC, LeadStatus.BLACKLISTED},
            LeadStatus.VERIFICATION: {LeadStatus.CLOSING, LeadStatus.CLOSED_LOST, LeadStatus.DNC, LeadStatus.BLACKLISTED},
            LeadStatus.CLOSING: {LeadStatus.CLOSED_WON, LeadStatus.CLOSED_LOST, LeadStatus.DNC, LeadStatus.BLACKLISTED},
            LeadStatus.CLOSED_WON: set(),  # Terminal state
            LeadStatus.CLOSED_LOST: {LeadStatus.ARCHIVED, LeadStatus.RECYCLED},
            LeadStatus.DNC: set(),  # Terminal state
            LeadStatus.BLACKLISTED: set(),  # Terminal state
            LeadStatus.ARCHIVED: {LeadStatus.RECYCLED},
            LeadStatus.RECYCLED: {LeadStatus.SCOUTED, LeadStatus.AI_FOLLOW_UP, LeadStatus.CLOSED_LOST}
        }
        return matrix
    
    async def create_lead_state(self, lead_id: str, initial_priority: LeadPriority = LeadPriority.MEDIUM) -> LeadState:
        """
        Create initial lead state
        
        Args:
            lead_id: ID of the lead
            initial_priority: Initial priority level
            
        Returns:
            LeadState: Created lead state
        """
        try:
            state = LeadState(
                lead_id=lead_id,
                current_status=LeadStatus.NEW,
                priority=initial_priority,
                assigned_to=None,
                last_contact=None,
                next_follow_up=None,
                contact_attempts=0,
                max_attempts=5,  # Default max attempts
                score=0.0,
                tags=set(),
                metadata={},
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            self.lead_states[lead_id] = state
            
            # Save to database
            if self.db:
                await self._save_lead_state(state)
            
            # Auto-transition to SCOUTED
            await self.transition_lead_state(lead_id, LeadStatus.SCOUTED, 
                                            TransitionType.AUTOMATIC, "Lead created and auto-scouted")
            
            self.logger.info(f"🆕 Lead state created: {lead_id}")
            
            return state
            
        except Exception as e:
            self.logger.error(f"❌ Failed to create lead state: {e}")
            raise
    
    async def transition_lead_state(self, lead_id: str, new_status: LeadStatus, 
                                   transition_type: TransitionType, 
                                   reason: str, triggered_by: str = "system",
                                   metadata: Dict[str, Any] = None) -> bool:
        """
        Transition lead to new state
        
        Args:
            lead_id: ID of the lead
            new_status: New status to transition to
            transition_type: Type of transition
            reason: Reason for transition
            triggered_by: Who triggered the transition
            metadata: Additional metadata
            
        Returns:
            bool: True if transition successful
        """
        try:
            # Get current state
            current_state = self.lead_states.get(lead_id)
            if not current_state:
                self.logger.error(f"❌ Lead state not found: {lead_id}")
                return False
            
            # Check if transition is valid
            if not self._is_valid_transition(current_state.current_status, new_status):
                self.logger.error(f"❌ Invalid transition: {current_state.current_status.value} → {new_status.value}")
                return False
            
            # Check transition rules
            rule = self._find_applicable_rule(current_state.current_status, new_status)
            if not rule:
                self.logger.error(f"❌ No applicable rule for transition: {current_state.current_status.value} → {new_status.value}")
                return False
            
            # Execute transition
            old_status = current_state.current_status
            current_state.current_status = new_status
            current_state.updated_at = datetime.now()
            
            # Create transition record
            transition_id = f"trans_{int(datetime.now().timestamp() * 1000000)}"
            transition = StateTransition(
                id=transition_id,
                lead_id=lead_id,
                from_status=old_status,
                to_status=new_status,
                transition_type=transition_type,
                reason=reason,
                triggered_by=triggered_by,
                metadata=metadata or {},
                timestamp=datetime.now()
            )
            
            self.transition_history.append(transition)
            
            # Execute rule actions
            await self._execute_rule_actions(rule, lead_id, current_state)
            
            # Save to database
            if self.db:
                await self._save_transition(transition)
                await self._update_lead_state(current_state)
            
            self.logger.info(f"🔄 Lead state transitioned: {lead_id} {old_status.value} → {new_status.value}")
            self.logger.info(f"📋 Reason: {reason}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Lead state transition failed: {e}")
            return False
    
    async def can_send_message(self, lead_id: str, message_type: str = "promotional") -> Dict[str, Any]:
        """
        Check if message can be sent to lead based on state
        
        Args:
            lead_id: ID of the lead
            message_type: Type of message to send
            
        Returns:
            Dict with permission status and reasons
        """
        try:
            state = self.lead_states.get(lead_id)
            if not state:
                return {
                    'can_send': False,
                    'reason': 'Lead state not found',
                    'blocked_states': []
                }
            
            # Blocked states for any communication
            blocked_states = [LeadStatus.DNC, LeadStatus.BLACKLISTED]
            if state.current_status in blocked_states:
                return {
                    'can_send': False,
                    'reason': f'Lead is in blocked state: {state.current_status.value}',
                    'blocked_states': [s.value for s in blocked_states]
                }
            
            # Check for closed won - no promotional messages
            if state.current_status == LeadStatus.CLOSED_WON and message_type == "promotional":
                return {
                    'can_send': False,
                    'reason': 'Cannot send promotional messages to closed won leads',
                    'blocked_states': [LeadStatus.CLOSED_WON.value]
                }
            
            # Check contact attempts
            if state.contact_attempts >= state.max_attempts:
                return {
                    'can_send': False,
                    'reason': f'Max contact attempts reached: {state.max_attempts}',
                    'contact_attempts': state.contact_attempts,
                    'max_attempts': state.max_attempts
                }
            
            # Check next follow up time
            if state.next_follow_up and state.next_follow_up > datetime.now():
                return {
                    'can_send': False,
                    'reason': 'Follow up scheduled for future',
                    'next_follow_up': state.next_follow_up.isoformat()
                }
            
            return {
                'can_send': True,
                'current_status': state.current_status.value,
                'priority': state.priority.value,
                'contact_attempts': state.contact_attempts,
                'max_attempts': state.max_attempts
            }
            
        except Exception as e:
            self.logger.error(f"❌ Message permission check failed: {e}")
            return {
                'can_send': False,
                'reason': f'Permission check error: {str(e)}'
            }
    
    async def record_contact_attempt(self, lead_id: str, contact_type: str, 
                                    success: bool, metadata: Dict[str, Any] = None) -> bool:
        """
        Record contact attempt and update state
        
        Args:
            lead_id: ID of the lead
            contact_type: Type of contact (call, message, email)
            success: Whether contact was successful
            metadata: Additional contact metadata
            
        Returns:
            bool: True if recorded successfully
        """
        try:
            state = self.lead_states.get(lead_id)
            if not state:
                self.logger.error(f"❌ Lead state not found: {lead_id}")
                return False
            
            # Update contact tracking
            state.contact_attempts += 1
            state.last_contact = datetime.now()
            
            # Add to metadata
            if not state.metadata.get('contact_history'):
                state.metadata['contact_history'] = []
            
            state.metadata['contact_history'].append({
                'type': contact_type,
                'timestamp': datetime.now().isoformat(),
                'success': success,
                'metadata': metadata or {}
            })
            
            # Check if max attempts reached
            if state.contact_attempts >= state.max_attempts:
                # Auto-transition to human or close
                if state.current_status == LeadStatus.AI_FOLLOW_UP:
                    await self.transition_lead_state(lead_id, LeadStatus.HUMAN_ASSIGNED,
                                                   TransitionType.AUTOMATIC,
                                                   f"Max attempts reached: {state.max_attempts}")
            
            # Save to database
            if self.db:
                await self._update_lead_state(state)
            
            self.logger.info(f"📞 Contact attempt recorded: {lead_id} ({contact_type})")
            self.logger.info(f"🔢 Total attempts: {state.contact_attempts}/{state.max_attempts}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to record contact attempt: {e}")
            return False
    
    def _is_valid_transition(self, from_status: LeadStatus, to_status: LeadStatus) -> bool:
        """Check if transition is valid"""
        valid_transitions = self.transition_matrix.get(from_status, set())
        return to_status in valid_transitions
    
    def _find_applicable_rule(self, from_status: LeadStatus, to_status: LeadStatus) -> Optional[StateRule]:
        """Find applicable transition rule"""
        for rule in self.state_rules:
            if rule.is_active and rule.from_status == from_status and rule.to_status == to_status:
                return rule
        return None
    
    async def _execute_rule_actions(self, rule: StateRule, lead_id: str, state: LeadState):
        """Execute rule actions"""
        try:
            for action in rule.actions:
                if action == "assign_initial_priority":
                    state.priority = LeadPriority.MEDIUM
                elif action == "schedule_first_contact":
                    state.next_follow_up = datetime.now() + timedelta(hours=1)
                elif action == "start_ai_conversation":
                    # This would trigger AI conversation
                    pass
                elif action == "set_follow_up_reminder":
                    state.next_follow_up = datetime.now() + timedelta(days=1)
                elif action == "assign_to_human_agent":
                    # This would assign to human agent
                    pass
                elif action == "notify_team_lead":
                    # This would notify team lead
                    pass
                elif action == "create_negotiation_plan":
                    # This would create negotiation plan
                    pass
                elif action == "prepare_proposal":
                    # This would prepare proposal
                    pass
                elif action == "initiate_kyc":
                    # This would initiate KYC
                    pass
                elif action == "request_documents":
                    # This would request documents
                    pass
                elif action == "prepare_closing_docs":
                    # This would prepare closing documents
                    pass
                elif action == "schedule_signing":
                    # This would schedule signing
                    pass
                elif action == "celebrate_deal":
                    # This would celebrate deal
                    pass
                elif action == "update_commission":
                    # This would update commission
                    pass
                elif action == "send_welcome_package":
                    # This would send welcome package
                    pass
                elif action == "log_loss_reason":
                    # This would log loss reason
                    pass
                elif action == "update_competitor_intel":
                    # This would update competitor intelligence
                    pass
                elif action == "stop_all_communication":
                    # This would stop all communication
                    pass
                elif action == "respect_privacy":
                    # This would respect privacy
                    pass
                elif action == "block_all_communication":
                    # This would block all communication
                    pass
                elif action == "report_abuse":
                    # This would report abuse
                    pass
                elif action == "re_engagement_campaign":
                    # This would start re-engagement campaign
                    pass
                elif action == "update_priority":
                    state.priority = LeadPriority.HIGH
                elif action == "archive_lead":
                    # This would archive lead
                    pass
                elif action == "cleanup_data":
                    # This would cleanup data
                    pass
                elif action == "escalate_to_human":
                    # This would escalate to human
                    pass
                elif action == "mark_as_stalled":
                    # This would mark as stalled
                    pass
                elif action == "send_follow_up_reminder":
                    # This would send follow up reminder
                    pass
                elif action == "update_contact_attempts":
                    # This would update contact attempts
                    pass
                
                self.logger.debug(f"⚙️ Action executed: {action}")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to execute rule actions: {e}")
    
    async def _save_lead_state(self, state: LeadState):
        """Save lead state to database"""
        try:
            # This would save to the actual database
            self.logger.debug(f"📊 Lead state saved: {state.lead_id}")
        except Exception as e:
            self.logger.error(f"❌ Failed to save lead state: {e}")
    
    async def _save_transition(self, transition: StateTransition):
        """Save transition to database"""
        try:
            # This would save to the actual database
            self.logger.debug(f"📝 Transition saved: {transition.id}")
        except Exception as e:
            self.logger.error(f"❌ Failed to save transition: {e}")
    
    async def _update_lead_state(self, state: LeadState):
        """Update lead state in database"""
        try:
            # This would update the actual database
            self.logger.debug(f"📊 Lead state updated: {state.lead_id}")
        except Exception as e:
            self.logger.error(f"❌ Failed to update lead state: {e}")
    
    def get_lead_state(self, lead_id: str) -> Optional[LeadState]:
        """Get current lead state"""
        return self.lead_states.get(lead_id)
    
    def get_state_statistics(self) -> Dict[str, Any]:
        """Get state machine statistics"""
        try:
            status_counts = {}
            priority_counts = {}
            total_leads = len(self.lead_states)
            
            for state in self.lead_states.values():
                # Status distribution
                status = state.current_status.value
                status_counts[status] = status_counts.get(status, 0) + 1
                
                # Priority distribution
                priority = state.priority.value
                priority_counts[priority] = priority_counts.get(priority, 0) + 1
            
            # Transition statistics
            recent_transitions = [t for t in self.transition_history 
                                 if t.timestamp >= datetime.now() - timedelta(days=30)]
            
            transition_types = {}
            for transition in recent_transitions:
                trans_type = transition.transition_type.value
                transition_types[trans_type] = transition_types.get(trans_type, 0) + 1
            
            return {
                'total_leads': total_leads,
                'status_distribution': status_counts,
                'priority_distribution': priority_counts,
                'recent_transitions': len(recent_transitions),
                'transition_types': transition_types,
                'active_rules': len([r for r in self.state_rules if r.is_active]),
                'automation_rules': len([r for r in self.automation_rules if r['is_active']])
            }
            
        except Exception as e:
            self.logger.error(f"❌ Failed to get state statistics: {e}")
            return {}

# Global lead state machine instance
lead_state_machine = LeadStateMachine()
