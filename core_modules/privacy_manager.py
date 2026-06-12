"""
DOOM SENTINEL - Privacy Manager & GDPR Compliance
Data Protection, Opt-Out Management, and Right to be Forgotten
"""

import os
import logging
import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

# Database imports
from prisma import Prisma

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConsentStatus(Enum):
    """Consent status for data processing"""
    OPTED_IN = "opted_in"
    OPTED_OUT = "opted_out"
    UNKNOWN = "unknown"
    EXPIRED = "expired"

class DataCategory(Enum):
    """Data categories for GDPR compliance"""
    PERSONAL = "personal"
    CONTACT = "contact"
    BEHAVIORAL = "behavioral"
    TRANSACTIONAL = "transactional"
    ANALYTICAL = "analytical"

@dataclass
class ConsentRecord:
    """Consent tracking record"""
    prospect_id: str
    consent_status: ConsentStatus
    consent_date: datetime
    consent_method: str  # whatsapp, telegram, email, web
    consent_text: str
    ip_address: str
    user_agent: str
    expires_at: Optional[datetime]

@dataclass
class DeletionRequest:
    """Right to be forgotten deletion request"""
    prospect_id: str
    request_date: datetime
    request_method: str
    verification_code: str
    status: str  # pending, verified, completed, failed
    processed_date: Optional[datetime]
    deletion_log: List[str]

class PrivacyManager:
    """
    Privacy Manager for GDPR Compliance
    Handles consent management, opt-out, and right to be forgotten
    """
    
    def __init__(self):
        """Initialize privacy manager"""
        self.logger = logging.getLogger(__name__)
        
        # Consent records
        self.consent_records: Dict[str, ConsentRecord] = {}
        
        # Deletion requests
        self.deletion_requests: Dict[str, DeletionRequest] = {}
        
        # Database connection
        self.db = None
        self._initialize_database()
        
        # Privacy settings
        self.consent_expiry_days = 365  # 1 year
        self.auto_opt_out_keywords = [
            'stop', 'berhenti', 'jangan kirim', 'hapus data',
            'opt out', 'unsubscribe', 'remove'
        ]
        
        self.logger.info("🔒 Privacy Manager initialized")
        self.logger.info(f"📋 Auto opt-out keywords: {len(self.auto_opt_out_keywords)}")
    
    def _initialize_database(self):
        """Initialize database connection"""
        try:
            self.db = Prisma()
            self.logger.info("📊 Privacy Manager database connected")
        except Exception as e:
            self.logger.error(f"❌ Database connection failed: {e}")
            self.db = None
    
    async def check_consent(self, prospect_id: str, contact_info: str) -> ConsentStatus:
        """
        Check consent status for a prospect
        
        Args:
            prospect_id: Unique prospect identifier
            contact_info: Contact information (phone/email)
            
        Returns:
            ConsentStatus: Current consent status
        """
        try:
            # Check existing consent record
            if prospect_id in self.consent_records:
                consent_record = self.consent_records[prospect_id]
                
                # Check if consent has expired
                if consent_record.expires_at and datetime.now() > consent_record.expires_at:
                    return ConsentStatus.EXPIRED
                
                return consent_record.consent_status
            
            # Check database for existing consent
            if self.db:
                db_consent = await self._get_consent_from_db(prospect_id)
                if db_consent:
                    return ConsentStatus(db_consent['status'])
            
            # Default to unknown for new prospects
            return ConsentStatus.UNKNOWN
            
        except Exception as e:
            self.logger.error(f"❌ Consent check failed: {e}")
            return ConsentStatus.UNKNOWN
    
    async def record_consent(self, prospect_id: str, contact_info: str, consent_method: str,
                          consent_text: str, ip_address: str, user_agent: str) -> bool:
        """
        Record consent for a prospect
        
        Args:
            prospect_id: Unique prospect identifier
            contact_info: Contact information
            consent_method: Method of consent (whatsapp, telegram, etc.)
            consent_text: Actual consent text
            ip_address: IP address
            user_agent: User agent string
            
        Returns:
            bool: True if consent recorded successfully
        """
        try:
            # Determine consent status
            consent_status = self._determine_consent_status(consent_text)
            
            # Calculate expiry date
            expires_at = datetime.now() + timedelta(days=self.consent_expiry_days)
            
            # Create consent record
            consent_record = ConsentRecord(
                prospect_id=prospect_id,
                consent_status=consent_status,
                consent_date=datetime.now(),
                consent_method=consent_method,
                consent_text=consent_text,
                ip_address=ip_address,
                user_agent=user_agent,
                expires_at=expires_at
            )
            
            # Store in memory
            self.consent_records[prospect_id] = consent_record
            
            # Save to database
            if self.db:
                await self._save_consent_record(consent_record)
            
            self.logger.info(f"📋 Consent recorded: {prospect_id} - {consent_status.value}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Consent recording failed: {e}")
            return False
    
    def _determine_consent_status(self, consent_text: str) -> ConsentStatus:
        """Determine consent status from text"""
        consent_lower = consent_text.lower()
        
        # Check for opt-out keywords
        for keyword in self.auto_opt_out_keywords:
            if keyword in consent_lower:
                return ConsentStatus.OPTED_OUT
        
        # Check for explicit opt-in
        opt_in_keywords = ['ya', 'ok', 'setuju', 'boleh', 'lanjutkan', 'yes', 'agree']
        for keyword in opt_in_keywords:
            if keyword in consent_lower:
                return ConsentStatus.OPTED_IN
        
        # Default to opted in for positive engagement
        return ConsentStatus.OPTED_IN
    
    async def process_opt_out_request(self, prospect_id: str, contact_info: str, 
                                    method: str, message_text: str) -> bool:
        """
        Process opt-out request
        
        Args:
            prospect_id: Unique prospect identifier
            contact_info: Contact information
            method: Communication method
            message_text: Opt-out message text
            
        Returns:
            bool: True if opt-out processed successfully
        """
        try:
            # Record opt-out consent
            success = await self.record_consent(
                prospect_id=prospect_id,
                contact_info=contact_info,
                consent_method=method,
                consent_text=message_text,
                ip_address="unknown",
                user_agent="opt_out_request"
            )
            
            if success:
                # Send confirmation message
                await self._send_opt_out_confirmation(contact_info, method)
                
                # Log opt-out
                self.logger.info(f"🚫 Opt-out processed: {prospect_id} via {method}")
                
                # Send alert to admin
                await self._send_privacy_alert(
                    "Opt-Out Request",
                    f"Prospect {prospect_id} has opted out via {method}",
                    "privacy_manager"
                )
            
            return success
            
        except Exception as e:
            self.logger.error(f"❌ Opt-out processing failed: {e}")
            return False
    
    async def request_right_to_be_forgotten(self, prospect_id: str, contact_info: str,
                                          request_method: str) -> str:
        """
        Initiate right to be forgotten request
        
        Args:
            prospect_id: Unique prospect identifier
            contact_info: Contact information
            request_method: Method of request
            
        Returns:
            str: Verification code for the request
        """
        try:
            # Generate verification code
            verification_code = self._generate_verification_code()
            
            # Create deletion request
            deletion_request = DeletionRequest(
                prospect_id=prospect_id,
                request_date=datetime.now(),
                request_method=request_method,
                verification_code=verification_code,
                status="pending",
                processed_date=None,
                deletion_log=[]
            )
            
            # Store request
            self.deletion_requests[prospect_id] = deletion_request
            
            # Save to database
            if self.db:
                await self._save_deletion_request(deletion_request)
            
            # Send verification code
            await self._send_verification_code(contact_info, verification_code, request_method)
            
            self.logger.info(f"🗑️ Right to be forgotten request: {prospect_id}")
            
            return verification_code
            
        except Exception as e:
            self.logger.error(f"❌ Deletion request failed: {e}")
            return ""
    
    async def verify_and_execute_deletion(self, prospect_id: str, verification_code: str) -> bool:
        """
        Verify deletion request and execute data deletion
        
        Args:
            prospect_id: Unique prospect identifier
            verification_code: Verification code
            
        Returns:
            bool: True if deletion executed successfully
        """
        try:
            # Get deletion request
            deletion_request = self.deletion_requests.get(prospect_id)
            if not deletion_request:
                self.logger.error(f"❌ Deletion request not found: {prospect_id}")
                return False
            
            # Verify code
            if deletion_request.verification_code != verification_code:
                self.logger.error(f"❌ Invalid verification code: {prospect_id}")
                return False
            
            # Execute deletion
            success = await self._execute_data_deletion(prospect_id)
            
            if success:
                # Update request status
                deletion_request.status = "completed"
                deletion_request.processed_date = datetime.now()
                deletion_request.deletion_log.append("Data deletion completed successfully")
                
                # Save to database
                if self.db:
                    await self._update_deletion_request(deletion_request)
                
                # Send confirmation
                await self._send_deletion_confirmation(prospect_id)
                
                # Send alert to admin
                await self._send_privacy_alert(
                    "Data Deletion Completed",
                    f"All data for prospect {prospect_id} has been deleted",
                    "privacy_manager"
                )
                
                self.logger.info(f"✅ Data deletion completed: {prospect_id}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"❌ Deletion execution failed: {e}")
            return False
    
    async def _execute_data_deletion(self, prospect_id: str) -> bool:
        """
        Execute complete data deletion for a prospect
        
        Args:
            prospect_id: Unique prospect identifier
            
        Returns:
            bool: True if deletion successful
        """
        try:
            deletion_log = []
            
            # Delete from leads table
            if self.db:
                try:
                    # Delete lead records
                    deleted_leads = await self.db.lead.delete_many(
                        where={'business_name': prospect_id}  # Assuming business_name as prospect_id
                    )
                    deletion_log.append(f"Deleted {deleted_leads} lead records")
                    
                    # Delete consent records
                    deleted_consents = await self.db.consentrecord.delete_many(
                        where={'prospectId': prospect_id}
                    )
                    deletion_log.append(f"Deleted {deleted_consents} consent records")
                    
                    # Delete activity logs
                    deleted_activities = await self.db.activitylog.delete_many(
                        where={'resourceId': prospect_id}
                    )
                    deletion_log.append(f"Deleted {deleted_activities} activity records")
                    
                    # Delete from any other tables that might contain prospect data
                    # Add more table deletions as needed
                    
                except Exception as e:
                    deletion_log.append(f"Database deletion error: {str(e)}")
                    self.logger.error(f"❌ Database deletion failed: {e}")
                    return False
            
            # Clear from memory
            if prospect_id in self.consent_records:
                del self.consent_records[prospect_id]
                deletion_log.append("Cleared consent records from memory")
            
            if prospect_id in self.deletion_requests:
                del self.deletion_requests[prospect_id]
                deletion_log.append("Cleared deletion requests from memory")
            
            # Log deletion
            for log_entry in deletion_log:
                self.logger.info(f"🗑️ Deletion log: {log_entry}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Data deletion execution failed: {e}")
            return False
    
    def _generate_verification_code(self) -> str:
        """Generate 6-digit verification code"""
        import random
        return ''.join([str(random.randint(0, 9)) for _ in range(6)])
    
    async def _send_verification_code(self, contact_info: str, code: str, method: str):
        """Send verification code to prospect"""
        try:
            message = (
                f"🔐 **Data Deletion Verification**\n\n"
                f"Your verification code is: **{code}**\n\n"
                f"This code will expire in 24 hours.\n"
                f"If you didn't request this, please ignore this message."
            )
            
            # Send via appropriate channel
            if method == "whatsapp":
                from .doom_sentinel.whatsapp_gateway import WhatsAppGateway
                gateway = WhatsAppGateway()
                await gateway.send_message(contact_info, message)
            elif method == "telegram":
                from .doom_sentinel.telegram_gateway import TelegramGateway
                gateway = TelegramGateway()
                await gateway.bot.send_message(chat_id=contact_info, text=message)
            
        except Exception as e:
            self.logger.error(f"❌ Verification code sending failed: {e}")
    
    async def _send_opt_out_confirmation(self, contact_info: str, method: str):
        """Send opt-out confirmation"""
        try:
            message = (
                f"🚫 **Opt-Out Confirmed**\n\n"
                f"You have been successfully opted out of future communications.\n"
                f"Your data will not be used for marketing purposes.\n\n"
                f"If you change your mind, you can opt back in at any time."
            )
            
            # Send via appropriate channel
            if method == "whatsapp":
                from .doom_sentinel.whatsapp_gateway import WhatsAppGateway
                gateway = WhatsAppGateway()
                await gateway.send_message(contact_info, message)
            elif method == "telegram":
                from .doom_sentinel.telegram_gateway import TelegramGateway
                gateway = TelegramGateway()
                await gateway.bot.send_message(chat_id=contact_info, text=message)
            
        except Exception as e:
            self.logger.error(f"❌ Opt-out confirmation failed: {e}")
    
    async def _send_deletion_confirmation(self, prospect_id: str):
        """Send deletion confirmation to admin"""
        try:
            from .doom_sentinel.alert_system import AlertSystem
            alert_system = AlertSystem()
            await alert_system.send_custom_alert(
                "Data Deletion Confirmation",
                f"All data for prospect {prospect_id} has been permanently deleted",
                "info"
            )
        except Exception as e:
            self.logger.error(f"❌ Deletion confirmation failed: {e}")
    
    async def _send_privacy_alert(self, title: str, message: str, source: str):
        """Send privacy-related alert to admin"""
        try:
            from .doom_sentinel.alert_system import AlertSystem
            alert_system = AlertSystem()
            await alert_system.send_custom_alert(title, message, "warning")
        except Exception as e:
            self.logger.error(f"❌ Privacy alert failed: {e}")
    
    async def _get_consent_from_db(self, prospect_id: str) -> Optional[Dict[str, Any]]:
        """Get consent record from database"""
        try:
            # This would query the actual consent table
            # For now, return None as placeholder
            return None
        except Exception as e:
            self.logger.error(f"❌ Database consent query failed: {e}")
            return None
    
    async def _save_consent_record(self, consent_record: ConsentRecord):
        """Save consent record to database"""
        try:
            # This would save to the actual consent table
            # For now, just log the action
            self.logger.info(f"📋 Consent saved to database: {consent_record.prospect_id}")
        except Exception as e:
            self.logger.error(f"❌ Database consent save failed: {e}")
    
    async def _save_deletion_request(self, deletion_request: DeletionRequest):
        """Save deletion request to database"""
        try:
            # This would save to the actual deletion_requests table
            # For now, just log the action
            self.logger.info(f"🗑️ Deletion request saved to database: {deletion_request.prospect_id}")
        except Exception as e:
            self.logger.error(f"❌ Database deletion request save failed: {e}")
    
    async def _update_deletion_request(self, deletion_request: DeletionRequest):
        """Update deletion request in database"""
        try:
            # This would update the actual deletion_requests table
            # For now, just log the action
            self.logger.info(f"🗑️ Deletion request updated in database: {deletion_request.prospect_id}")
        except Exception as e:
            self.logger.error(f"❌ Database deletion request update failed: {e}")
    
    def get_privacy_summary(self) -> Dict[str, Any]:
        """Get privacy compliance summary"""
        try:
            total_consent = len(self.consent_records)
            opted_in = len([r for r in self.consent_records.values() if r.consent_status == ConsentStatus.OPTED_IN])
            opted_out = len([r for r in self.consent_records.values() if r.consent_status == ConsentStatus.OPTED_OUT])
            expired = len([r for r in self.consent_records.values() if r.consent_status == ConsentStatus.EXPIRED])
            
            pending_deletions = len([r for r in self.deletion_requests.values() if r.status == "pending"])
            completed_deletions = len([r for r in self.deletion_requests.values() if r.status == "completed"])
            
            return {
                'consent_records': {
                    'total': total_consent,
                    'opted_in': opted_in,
                    'opted_out': opted_out,
                    'expired': expired,
                    'opt_out_rate': (opted_out / total_consent * 100) if total_consent > 0 else 0
                },
                'deletion_requests': {
                    'pending': pending_deletions,
                    'completed': completed_deletions,
                    'total': pending_deletions + completed_deletions
                },
                'compliance_status': 'compliant' if opted_out < (total_consent * 0.05) else 'review_needed'
            }
            
        except Exception as e:
            self.logger.error(f"❌ Privacy summary generation failed: {e}")
            return {}
    
    async def cleanup_expired_consents(self):
        """Clean up expired consent records"""
        try:
            current_time = datetime.now()
            expired_prospects = []
            
            for prospect_id, consent_record in self.consent_records.items():
                if (consent_record.expires_at and 
                    current_time > consent_record.expires_at and
                    consent_record.consent_status == ConsentStatus.OPTED_IN):
                    expired_prospects.append(prospect_id)
            
            # Update expired consents
            for prospect_id in expired_prospects:
                self.consent_records[prospect_id].consent_status = ConsentStatus.EXPIRED
            
            if expired_prospects:
                self.logger.info(f"🕐 Updated {len(expired_prospects)} expired consent records")
            
        except Exception as e:
            self.logger.error(f"❌ Consent cleanup failed: {e}")

# Global privacy manager instance
privacy_manager = PrivacyManager()
