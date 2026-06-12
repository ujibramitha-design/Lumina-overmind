"""
LUMINA OS - Admin Authentication & Security
Enterprise-grade admin access control with encrypted credentials
"""

import os
import logging
import hashlib
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserRole(Enum):
    """User roles for RBAC"""
    ADMIN = "admin"
    OPERATOR = "operator"
    VIEWER = "viewer"
    AI_AGENT = "ai_agent"

@dataclass
class AdminCredentials:
    """Admin credentials with security metadata"""
    user_id: str
    role: UserRole
    hashed_identifier: str
    last_access: Optional[datetime]
    access_count: int
    is_active: bool
    created_at: datetime

class AdminAuth:
    """
    Enterprise-grade admin authentication system
    Secure credential management with environment-based storage
    """
    
    def __init__(self):
        """Initialize admin authentication"""
        self.logger = logging.getLogger(__name__)
        
        # Load admin credentials from environment
        self._load_admin_credentials()
        
        # Session management
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
        
        # Security settings
        self.max_sessions = 5
        self.session_timeout_hours = 24
        self.max_failed_attempts = 3
        self.lockout_duration_minutes = 30
        
        self.logger.info("🔐 Admin Authentication initialized")
        self.logger.info(f"👥 Admin users loaded: {len(self.admin_credentials)}")
    
    def _load_admin_credentials(self):
        """Load admin credentials from secure environment variables"""
        try:
            self.admin_credentials = {}
            
            # Load WhatsApp admin numbers
            wa_admins = os.getenv("ADMIN_WA_NUMBERS", "").split(",")
            for wa_number in wa_admins:
                if wa_number.strip():
                    admin_id = self._hash_identifier(f"wa:{wa_number.strip()}")
                    self.admin_credentials[admin_id] = AdminCredentials(
                        user_id=wa_number.strip(),
                        role=UserRole.ADMIN,
                        hashed_identifier=admin_id,
                        last_access=None,
                        access_count=0,
                        is_active=True,
                        created_at=datetime.now()
                    )
            
            # Load Telegram admin IDs
            tg_admins = os.getenv("ADMIN_TELE_IDS", "").split(",")
            for tg_id in tg_admins:
                if tg_id.strip():
                    admin_id = self._hash_identifier(f"tg:{tg_id.strip()}")
                    self.admin_credentials[admin_id] = AdminCredentials(
                        user_id=tg_id.strip(),
                        role=UserRole.ADMIN,
                        hashed_identifier=admin_id,
                        last_access=None,
                        access_count=0,
                        is_active=True,
                        created_at=datetime.now()
                    )
            
            # Load operators (optional)
            operators = os.getenv("OPERATOR_WA_NUMBERS", "").split(",")
            for op_number in operators:
                if op_number.strip():
                    admin_id = self._hash_identifier(f"wa:{op_number.strip()}")
                    self.admin_credentials[admin_id] = AdminCredentials(
                        user_id=op_number.strip(),
                        role=UserRole.OPERATOR,
                        hashed_identifier=admin_id,
                        last_access=None,
                        access_count=0,
                        is_active=True,
                        created_at=datetime.now()
                    )
            
            self.logger.info(f"📋 Loaded {len(self.admin_credentials)} admin credentials from environment")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to load admin credentials: {e}")
            self.admin_credentials = {}
    
    def _hash_identifier(self, identifier: str) -> str:
        """Hash identifier for secure storage"""
        return hashlib.sha256(identifier.encode()).hexdigest()
    
    def verify_admin_access(self, sender_id: str, platform: str = "whatsapp") -> Optional[AdminCredentials]:
        """
        Verify admin access with security checks
        
        Args:
            sender_id: Sender ID (phone number or Telegram ID)
            platform: Platform type (whatsapp, telegram)
            
        Returns:
            AdminCredentials if valid, None otherwise
        """
        try:
            # Create platform-specific identifier
            platform_prefix = f"{platform}:"
            full_identifier = platform_prefix + sender_id
            hashed_id = self._hash_identifier(full_identifier)
            
            # Check if admin exists
            admin = self.admin_credentials.get(hashed_id)
            if not admin:
                self.logger.warning(f"🚫 Access denied: Unknown admin {platform}:{sender_id}")
                return None
            
            # Check if admin is active
            if not admin.is_active:
                self.logger.warning(f"🚫 Access denied: Inactive admin {platform}:{sender_id}")
                return None
            
            # Update access tracking
            admin.last_access = datetime.now()
            admin.access_count += 1
            
            self.logger.info(f"✅ Admin access verified: {platform}:{sender_id} (Role: {admin.role.value})")
            
            return admin
            
        except Exception as e:
            self.logger.error(f"❌ Admin verification failed: {e}")
            return None
    
    def create_session(self, admin_id: str, session_data: Dict[str, Any]) -> str:
        """
        Create secure admin session
        
        Args:
            admin_id: Admin identifier
            session_data: Session metadata
            
        Returns:
            Session token
        """
        try:
            # Generate session token
            session_token = self._generate_session_token()
            
            # Create session
            session = {
                "token": session_token,
                "admin_id": admin_id,
                "created_at": datetime.now(),
                "last_activity": datetime.now(),
                "platform": session_data.get("platform", "unknown"),
                "ip_address": session_data.get("ip_address", "unknown"),
                "user_agent": session_data.get("user_agent", "unknown"),
                "metadata": session_data
            }
            
            # Store session
            self.active_sessions[session_token] = session
            
            # Clean old sessions
            self._cleanup_old_sessions()
            
            self.logger.info(f"🔑 Session created: {session_token[:8]}... for admin {admin_id}")
            
            return session_token
            
        except Exception as e:
            self.logger.error(f"❌ Session creation failed: {e}")
            return ""
    
    def verify_session(self, session_token: str) -> Optional[Dict[str, Any]]:
        """
        Verify admin session
        
        Args:
            session_token: Session token
            
        Returns:
            Session data if valid, None otherwise
        """
        try:
            session = self.active_sessions.get(session_token)
            if not session:
                return None
            
            # Check session timeout
            if datetime.now() - session["last_activity"] > timedelta(hours=self.session_timeout_hours):
                # Remove expired session
                del self.active_sessions[session_token]
                return None
            
            # Update last activity
            session["last_activity"] = datetime.now()
            
            return session
            
        except Exception as e:
            self.logger.error(f"❌ Session verification failed: {e}")
            return None
    
    def revoke_session(self, session_token: str) -> bool:
        """
        Revoke admin session
        
        Args:
            session_token: Session token
            
        Returns:
            True if revoked successfully
        """
        try:
            if session_token in self.active_sessions:
                del self.active_sessions[session_token]
                self.logger.info(f"🔒 Session revoked: {session_token[:8]}...")
                return True
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Session revocation failed: {e}")
            return False
    
    def get_admin_by_role(self, role: UserRole) -> List[AdminCredentials]:
        """
        Get admins by role
        
        Args:
            role: User role
            
        Returns:
            List of admin credentials
        """
        return [admin for admin in self.admin_credentials.values() if admin.role == role]
    
    def deactivate_admin(self, sender_id: str, platform: str = "whatsapp") -> bool:
        """
        Deactivate admin access
        
        Args:
            sender_id: Sender ID
            platform: Platform type
            
        Returns:
            True if deactivated successfully
        """
        try:
            platform_prefix = f"{platform}:"
            full_identifier = platform_prefix + sender_id
            hashed_id = self._hash_identifier(full_identifier)
            
            admin = self.admin_credentials.get(hashed_id)
            if admin:
                admin.is_active = False
                self.logger.info(f"🚫 Admin deactivated: {platform}:{sender_id}")
                
                # Revoke all sessions for this admin
                sessions_to_revoke = [
                    token for token, session in self.active_sessions.items()
                    if session["admin_id"] == hashed_id
                ]
                for token in sessions_to_revoke:
                    self.revoke_session(token)
                
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Admin deactivation failed: {e}")
            return False
    
    def _generate_session_token(self) -> str:
        """Generate secure session token"""
        import secrets
        return secrets.token_urlsafe(32)
    
    def _cleanup_old_sessions(self):
        """Clean up old and inactive sessions"""
        try:
            current_time = datetime.now()
            sessions_to_remove = []
            
            for token, session in self.active_sessions.items():
                # Remove expired sessions
                if current_time - session["last_activity"] > timedelta(hours=self.session_timeout_hours):
                    sessions_to_remove.append(token)
                
                # Remove if too many sessions
                if len(self.active_sessions) > self.max_sessions:
                    # Sort by last activity and remove oldest
                    sorted_sessions = sorted(
                        self.active_sessions.items(),
                        key=lambda x: x[1]["last_activity"]
                    )
                    excess_count = len(self.active_sessions) - self.max_sessions
                    for i in range(excess_count):
                        sessions_to_remove.append(sorted_sessions[i][0])
            
            # Remove sessions
            for token in sessions_to_remove:
                if token in self.active_sessions:
                    del self.active_sessions[token]
            
            if sessions_to_remove:
                self.logger.info(f"🧹 Cleaned up {len(sessions_to_remove)} old sessions")
            
        except Exception as e:
            self.logger.error(f"❌ Session cleanup failed: {e}")
    
    def get_security_stats(self) -> Dict[str, Any]:
        """Get security statistics"""
        try:
            return {
                "total_admins": len(self.admin_credentials),
                "active_admins": len([a for a in self.admin_credentials.values() if a.is_active]),
                "role_distribution": {
                    role.value: len([a for a in self.admin_credentials.values() if a.role == role])
                    for role in UserRole
                },
                "active_sessions": len(self.active_sessions),
                "max_sessions": self.max_sessions,
                "session_timeout_hours": self.session_timeout_hours
            }
            
        except Exception as e:
            self.logger.error(f"❌ Failed to get security stats: {e}")
            return {}

# Global admin authentication instance
admin_auth = AdminAuth()
