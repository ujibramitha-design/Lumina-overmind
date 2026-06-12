"""
DOOM SENTINEL - Security Middleware
Military-grade access control and authentication system
"""

import os
import logging
from typing import Dict, Any, Optional, List
from enum import Enum
from dataclasses import dataclass
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AccessLevel(Enum):
    """Access levels for DOOM system"""
    ADMIN = "admin"      # Jenderal/Lead System Architect
    GUEST = "guest"      # Customer Service mode
    BLOCKED = "blocked"  # Denied access

@dataclass
class UserSession:
    """User session data"""
    sender_id: str
    platform: str  # 'telegram' or 'whatsapp'
    access_level: AccessLevel
    last_activity: datetime
    command_count: int = 0
    is_verified: bool = False

class SecurityMiddleware:
    """
    Military-grade security middleware for DOOM system
    Handles authentication, authorization, and access control
    """
    
    def __init__(self):
        """Initialize security middleware"""
        self.logger = logging.getLogger(__name__)
        
        # Load admin credentials from environment
        self.admin_whatsapp_numbers = self._load_admin_whatsapp_numbers()
        self.admin_telegram_ids = self._load_admin_telegram_ids()
        
        # Active sessions storage
        self.active_sessions: Dict[str, UserSession] = {}
        
        # Security settings
        self.max_commands_per_hour = 100
        self.session_timeout_minutes = 60
        
        self.logger.info("🛡️ DOOM Security Middleware initialized")
        self.logger.info(f"📋 Admin WhatsApp numbers: {len(self.admin_whatsapp_numbers)}")
        self.logger.info(f"📋 Admin Telegram IDs: {len(self.admin_telegram_ids)}")
    
    def _load_admin_whatsapp_numbers(self) -> List[str]:
        """Load admin WhatsApp numbers from environment"""
        admin_numbers_str = os.getenv('ADMIN_WA_NUMBER', '')
        return [num.strip() for num in admin_numbers_str.split(',') if num.strip()]
    
    def _load_admin_telegram_ids(self) -> List[str]:
        """Load admin Telegram IDs from environment"""
        admin_ids_str = os.getenv('ADMIN_TELE_ID', '')
        return [id_.strip() for id_ in admin_ids_str.split(',') if id_.strip()]
    
    def verify_admin_access(self, sender_id: str, platform: str) -> AccessLevel:
        """
        Verify admin access based on sender ID and platform
        
        Args:
            sender_id: User ID (phone number for WA, chat ID for Telegram)
            platform: Platform identifier ('telegram' or 'whatsapp')
            
        Returns:
            AccessLevel: ADMIN, GUEST, or BLOCKED
        """
        try:
            # Check if sender is admin
            is_admin = False
            
            if platform == 'whatsapp':
                # Normalize WhatsApp number (remove +, spaces, etc.)
                normalized_number = self._normalize_whatsapp_number(sender_id)
                is_admin = normalized_number in self.admin_whatsapp_numbers
                
            elif platform == 'telegram':
                # Telegram ID comparison
                is_admin = sender_id in self.admin_telegram_ids
            
            # Determine access level
            if is_admin:
                access_level = AccessLevel.ADMIN
                self.logger.info(f"🎖️ Admin access granted: {sender_id} ({platform})")
            else:
                access_level = AccessLevel.GUEST
                self.logger.info(f"👤 Guest access: {sender_id} ({platform})")
            
            # Update or create session
            self._update_session(sender_id, platform, access_level)
            
            return access_level
            
        except Exception as e:
            self.logger.error(f"❌ Security verification error: {e}")
            return AccessLevel.BLOCKED
    
    def _normalize_whatsapp_number(self, number: str) -> str:
        """Normalize WhatsApp number for comparison"""
        # Remove +, spaces, dashes, etc.
        normalized = number.replace('+', '').replace(' ', '').replace('-', '')
        
        # Remove country code if present (assuming Indonesia +62)
        if normalized.startswith('62'):
            normalized = normalized[2:]
        elif normalized.startswith('0'):
            normalized = normalized[1:]
        
        return normalized
    
    def _update_session(self, sender_id: str, platform: str, access_level: AccessLevel):
        """Update or create user session"""
        session_key = f"{platform}:{sender_id}"
        
        if session_key in self.active_sessions:
            # Update existing session
            session = self.active_sessions[session_key]
            session.last_activity = datetime.now()
            session.command_count += 1
        else:
            # Create new session
            session = UserSession(
                sender_id=sender_id,
                platform=platform,
                access_level=access_level,
                last_activity=datetime.now(),
                is_verified=True
            )
            self.active_sessions[session_key] = session
        
        # Check for session timeout
        self._cleanup_expired_sessions()
    
    def _cleanup_expired_sessions(self):
        """Remove expired sessions"""
        current_time = datetime.now()
        expired_sessions = []
        
        for session_key, session in self.active_sessions.items():
            time_diff = (current_time - session.last_activity).total_seconds()
            if time_diff > (self.session_timeout_minutes * 60):
                expired_sessions.append(session_key)
        
        for session_key in expired_sessions:
            del self.active_sessions[session_key]
            self.logger.info(f"🗑️ Session expired: {session_key}")
    
    def check_command_permission(self, sender_id: str, platform: str, command: str) -> Dict[str, Any]:
        """
        Check if user has permission to execute specific command
        
        Args:
            sender_id: User ID
            platform: Platform identifier
            command: Command string
            
        Returns:
            Dict with permission status and response
        """
        access_level = self.verify_admin_access(sender_id, platform)
        
        # Define admin-only commands
        admin_commands = [
            '/status',
            '/deploy_scout',
            '/approve_ads',
            '/system_control',
            '/database_query',
            '/user_management',
            '/api_keys',
            '/logs'
        ]
        
        # Check if command requires admin access
        is_admin_command = any(cmd in command.lower() for cmd in admin_commands)
        
        if is_admin_command and access_level != AccessLevel.ADMIN:
            return {
                'allowed': False,
                'access_level': access_level,
                'response': "🚫 Akses ditolak. Otorisasi keamanan DOOM tidak valid.",
                'error_code': 'UNAUTHORIZED_ACCESS'
            }
        
        return {
            'allowed': True,
            'access_level': access_level,
            'response': None,
            'error_code': None
        }
    
    def get_session_info(self, sender_id: str, platform: str) -> Optional[UserSession]:
        """Get session information for user"""
        session_key = f"{platform}:{sender_id}"
        return self.active_sessions.get(session_key)
    
    def get_active_sessions_count(self) -> Dict[str, int]:
        """Get count of active sessions by access level"""
        count = {
            'admin': 0,
            'guest': 0,
            'total': len(self.active_sessions)
        }
        
        for session in self.active_sessions.values():
            if session.access_level == AccessLevel.ADMIN:
                count['admin'] += 1
            elif session.access_level == AccessLevel.GUEST:
                count['guest'] += 1
        
        return count
    
    def revoke_access(self, sender_id: str, platform: str) -> bool:
        """Revoke access for specific user"""
        session_key = f"{platform}:{sender_id}"
        if session_key in self.active_sessions:
            del self.active_sessions[session_key]
            self.logger.info(f"🔒 Access revoked: {sender_id} ({platform})")
            return True
        return False
