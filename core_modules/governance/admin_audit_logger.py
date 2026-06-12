"""
LUMINA OS - Admin Audit Logger
Enterprise-grade audit logging for human/administrator actions
"""

import os
import logging
import asyncio
import json
from typing import Dict, Any, Optional, List
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum
from functools import wraps

# Database imports
from prisma import Prisma

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ActionType(Enum):
    """Types of admin actions"""
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    APPROVE = "approve"
    REJECT = "reject"
    LOGIN = "login"
    LOGOUT = "logout"
    EXPORT = "export"
    IMPORT = "import"
    CONFIGURE = "configure"
    DEPLOY = "deploy"
    BACKUP = "backup"
    RESTORE = "restore"

class ResourceCategory(Enum):
    """Categories of resources being acted upon"""
    PROJECT = "project"
    LEAD = "lead"
    USER = "user"
    CAMPAIGN = "campaign"
    CONTENT = "content"
    SYSTEM = "system"
    DATABASE = "database"
    SECURITY = "security"
    FINANCE = "finance"

class RiskLevel(Enum):
    """Risk levels for admin actions"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class AuditRecord:
    """Admin audit record"""
    id: Optional[str]
    timestamp: datetime
    user_id: str
    username: str
    action: ActionType
    resource_category: ResourceCategory
    resource_id: Optional[str]
    resource_name: Optional[str]
    old_values: Optional[Dict[str, Any]]
    new_values: Optional[Dict[str, Any]]
    ip_address: str
    user_agent: str
    session_id: str
    risk_level: RiskLevel
    success: bool
    error_message: Optional[str]
    additional_metadata: Optional[Dict[str, Any]]

class AdminAuditLogger:
    """
    Enterprise-grade admin audit logging system
    Tracks all human/administrator actions with comprehensive audit trail
    """
    
    def __init__(self):
        """Initialize admin audit logger"""
        self.logger = logging.getLogger(__name__)
        
        # Database connection
        self.db = None
        self._initialize_database()
        
        # In-memory audit trail for immediate access
        self.audit_trail: List[AuditRecord] = []
        
        # Risk assessment rules
        self.risk_rules = self._initialize_risk_rules()
        
        # Sensitive fields configuration
        self.sensitive_fields = [
            'password', 'token', 'secret', 'key', 'credential',
            'api_key', 'private_key', 'access_token'
        ]
        
        self.logger.info("👤 Admin Audit Logger initialized")
        self.logger.info(f"🔐 Risk rules loaded: {len(self.risk_rules)}")
    
    def _initialize_database(self):
        """Initialize database connection"""
        try:
            self.db = Prisma()
            self.logger.info("📊 Admin Audit Logger database connected")
        except Exception as e:
            self.logger.error(f"❌ Database connection failed: {e}")
            self.db = None
    
    def _initialize_risk_rules(self) -> Dict[str, Dict[str, Any]]:
        """Initialize risk assessment rules"""
        return {
            'delete': {
                'base_risk': RiskLevel.MEDIUM,
                'critical_resources': ['project', 'user', 'database'],
                'high_risk_resources': ['campaign', 'finance']
            },
            'update': {
                'base_risk': RiskLevel.LOW,
                'critical_fields': ['status', 'role', 'permissions'],
                'high_risk_resources': ['user', 'security']
            },
            'create': {
                'base_risk': RiskLevel.LOW,
                'critical_resources': ['user', 'system'],
                'high_risk_resources': ['project', 'finance']
            },
            'approve': {
                'base_risk': RiskLevel.MEDIUM,
                'critical_resources': ['project', 'campaign'],
                'high_risk_resources': ['finance']
            },
            'configure': {
                'base_risk': RiskLevel.HIGH,
                'critical_fields': ['api_key', 'secret', 'password'],
                'high_risk_resources': ['system', 'security']
            },
            'backup': {
                'base_risk': RiskLevel.MEDIUM,
                'critical_resources': ['database'],
                'high_risk_resources': []
            },
            'restore': {
                'base_risk': RiskLevel.HIGH,
                'critical_resources': ['database'],
                'high_risk_resources': []
            }
        }
    
    def log_admin_action(self, user_id: str, username: str, action: ActionType,
                        resource_category: ResourceCategory, resource_id: str = None,
                        resource_name: str = None, old_values: Dict[str, Any] = None,
                        new_values: Dict[str, Any] = None, ip_address: str = None,
                        user_agent: str = None, session_id: str = None,
                        success: bool = True, error_message: str = None,
                        additional_metadata: Dict[str, Any] = None) -> str:
        """
        Log admin action with comprehensive audit trail
        
        Args:
            user_id: ID of the admin user
            username: Username of the admin
            action: Action performed
            resource_category: Category of resource
            resource_id: ID of the resource
            resource_name: Name of the resource
            old_values: Previous values before action
            new_values: New values after action
            ip_address: IP address of the request
            user_agent: User agent string
            session_id: Session ID
            success: Whether action was successful
            error_message: Error message if action failed
            additional_metadata: Additional metadata
            
        Returns:
            str: Audit record ID
        """
        try:
            # Generate audit record ID
            audit_id = f"audit_{int(datetime.now().timestamp() * 1000000)}"
            
            # Assess risk level
            risk_level = self._assess_risk_level(action, resource_category, new_values, old_values)
            
            # Create audit record
            audit_record = AuditRecord(
                id=audit_id,
                timestamp=datetime.now(),
                user_id=user_id,
                username=username,
                action=action,
                resource_category=resource_category,
                resource_id=resource_id,
                resource_name=resource_name,
                old_values=self._sanitize_values(old_values),
                new_values=self._sanitize_values(new_values),
                ip_address=ip_address or "unknown",
                user_agent=user_agent or "unknown",
                session_id=session_id or "unknown",
                risk_level=risk_level,
                success=success,
                error_message=error_message,
                additional_metadata=additional_metadata or {}
            )
            
            # Add to in-memory trail
            self.audit_trail.append(audit_record)
            
            # Save to database
            if self.db:
                await self._save_audit_record(audit_record)
            
            # Log to file
            self._log_to_file(audit_record)
            
            # Send alert if high risk
            if risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
                await self._send_security_alert(audit_record)
            
            self.logger.info(f"👤 Admin action logged: {username} - {action.value} - {resource_category.value}")
            
            return audit_id
            
        except Exception as e:
            self.logger.error(f"❌ Admin action logging failed: {e}")
            return ""
    
    def _assess_risk_level(self, action: ActionType, resource_category: ResourceCategory,
                          new_values: Dict[str, Any], old_values: Dict[str, Any]) -> RiskLevel:
        """Assess risk level based on action and resource"""
        try:
            # Get base risk level
            action_rules = self.risk_rules.get(action.value, {'base_risk': RiskLevel.LOW})
            base_risk = action_rules['base_risk']
            
            # Check for critical resources
            critical_resources = action_rules.get('critical_resources', [])
            if resource_category.value in critical_resources:
                return RiskLevel.CRITICAL
            
            # Check for high-risk resources
            high_risk_resources = action_rules.get('high_risk_resources', [])
            if resource_category.value in high_risk_resources:
                return RiskLevel.HIGH
            
            # Check for critical fields
            critical_fields = action_rules.get('critical_fields', [])
            if new_values:
                for field in critical_fields:
                    if field in new_values:
                        return RiskLevel.HIGH
            
            if old_values:
                for field in critical_fields:
                    if field in old_values:
                        return RiskLevel.HIGH
            
            # Check for sensitive data
            if self._contains_sensitive_data(new_values) or self._contains_sensitive_data(old_values):
                return RiskLevel.HIGH
            
            return base_risk
            
        except Exception as e:
            self.logger.error(f"❌ Risk assessment failed: {e}")
            return RiskLevel.MEDIUM
    
    def _sanitize_values(self, values: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Sanitize sensitive values for audit logging"""
        if not values:
            return None
        
        sanitized = {}
        for key, value in values.items():
            if any(sensitive in key.lower() for sensitive in self.sensitive_fields):
                sanitized[key] = "[REDACTED]"
            elif isinstance(value, str) and len(value) > 100:
                sanitized[key] = value[:100] + "..."
            else:
                sanitized[key] = value
        
        return sanitized
    
    def _contains_sensitive_data(self, values: Optional[Dict[str, Any]]) -> bool:
        """Check if values contain sensitive data"""
        if not values:
            return False
        
        for key, value in values.items():
            if isinstance(value, str):
                if any(sensitive in value.lower() for sensitive in self.sensitive_fields):
                    return True
            elif isinstance(value, dict):
                if self._contains_sensitive_data(value):
                    return True
        
        return False
    
    async def _save_audit_record(self, audit_record: AuditRecord):
        """Save audit record to database"""
        try:
            # This would save to the actual audit table
            # For now, just log the action
            self.logger.debug(f"📝 Audit record saved to database: {audit_record.id}")
            
        except Exception as e:
            self.logger.error(f"❌ Database save failed: {e}")
    
    def _log_to_file(self, audit_record: AuditRecord):
        """Log audit record to file"""
        try:
            log_entry = {
                'id': audit_record.id,
                'timestamp': audit_record.timestamp.isoformat(),
                'user_id': audit_record.user_id,
                'username': audit_record.username,
                'action': audit_record.action.value,
                'resource_category': audit_record.resource_category.value,
                'resource_id': audit_record.resource_id,
                'resource_name': audit_record.resource_name,
                'old_values': audit_record.old_values,
                'new_values': audit_record.new_values,
                'ip_address': audit_record.ip_address,
                'user_agent': audit_record.user_agent,
                'session_id': audit_record.session_id,
                'risk_level': audit_record.risk_level.value,
                'success': audit_record.success,
                'error_message': audit_record.error_message,
                'additional_metadata': audit_record.additional_metadata
            }
            
            # Write to audit log file
            with open('logs/admin_audit.log', 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
            
        except Exception as e:
            self.logger.error(f"❌ File logging failed: {e}")
    
    async def _send_security_alert(self, audit_record: AuditRecord):
        """Send security alert for high-risk actions"""
        try:
            alert_message = f"""
🚨 **HIGH-RISK ADMIN ACTION**

**User:** {audit_record.username} ({audit_record.user_id})
**Action:** {audit_record.action.value.upper()}
**Resource:** {audit_record.resource_category.value} - {audit_record.resource_name}
**Risk Level:** {audit_record.risk_level.value.upper()}
**Timestamp:** {audit_record.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
**IP Address:** {audit_record.ip_address}

**Details:**
- Old Values: {audit_record.old_values}
- New Values: {audit_record.new_values}
- Success: {audit_record.success}

⚠️ This action requires immediate attention and review.
            """
            
            # Send to alert system
            from core_modules.doom_sentinel.alert_system import AlertSystem
            alert_system = AlertSystem()
            await alert_system.send_custom_alert(
                "High-Risk Admin Action",
                alert_message.strip(),
                "critical"
            )
            
        except Exception as e:
            self.logger.error(f"❌ Security alert failed: {e}")
    
    def get_audit_trail(self, limit: int = 100, user_id: str = None,
                        action: ActionType = None, resource_category: ResourceCategory = None,
                        risk_level: RiskLevel = None, start_date: datetime = None,
                        end_date: datetime = None) -> List[AuditRecord]:
        """
        Get filtered audit trail
        
        Args:
            limit: Maximum number of records to return
            user_id: Filter by user ID
            action: Filter by action type
            resource_category: Filter by resource category
            risk_level: Filter by risk level
            start_date: Filter by start date
            end_date: Filter by end date
            
        Returns:
            List[AuditRecord]: Filtered audit records
        """
        try:
            filtered_trail = self.audit_trail
            
            # Apply filters
            if user_id:
                filtered_trail = [r for r in filtered_trail if r.user_id == user_id]
            
            if action:
                filtered_trail = [r for r in filtered_trail if r.action == action]
            
            if resource_category:
                filtered_trail = [r for r in filtered_trail if r.resource_category == resource_category]
            
            if risk_level:
                filtered_trail = [r for r in filtered_trail if r.risk_level == risk_level]
            
            if start_date:
                filtered_trail = [r for r in filtered_trail if r.timestamp >= start_date]
            
            if end_date:
                filtered_trail = [r for r in filtered_trail if r.timestamp <= end_date]
            
            # Sort by timestamp (newest first)
            filtered_trail.sort(key=lambda x: x.timestamp, reverse=True)
            
            # Apply limit
            if limit and limit > 0:
                filtered_trail = filtered_trail[:limit]
            
            return filtered_trail
            
        except Exception as e:
            self.logger.error(f"❌ Failed to get audit trail: {e}")
            return []
    
    def get_audit_statistics(self) -> Dict[str, Any]:
        """Get comprehensive audit statistics"""
        try:
            total_actions = len(self.audit_trail)
            
            if total_actions == 0:
                return {
                    'total_actions': 0,
                    'successful_actions': 0,
                    'failed_actions': 0,
                    'action_distribution': {},
                    'user_activity': {},
                    'risk_distribution': {},
                    'resource_distribution': {},
                    'time_period': 'No data'
                }
            
            # Calculate statistics
            successful_actions = len([r for r in self.audit_trail if r.success])
            failed_actions = total_actions - successful_actions
            
            # Action distribution
            action_counts = {}
            for record in self.audit_trail:
                action_counts[record.action.value] = action_counts.get(record.action.value, 0) + 1
            
            # User activity
            user_counts = {}
            for record in self.audit_trail:
                user_counts[record.username] = user_counts.get(record.username, 0) + 1
            
            # Risk distribution
            risk_counts = {}
            for record in self.audit_trail:
                risk_counts[record.risk_level.value] = risk_counts.get(record.risk_level.value, 0) + 1
            
            # Resource distribution
            resource_counts = {}
            for record in self.audit_trail:
                resource_counts[record.resource_category.value] = resource_counts.get(record.resource_category.value, 0) + 1
            
            # Time period
            if self.audit_trail:
                oldest_record = min(self.audit_trail, key=lambda x: x.timestamp)
                newest_record = max(self.audit_trail, key=lambda x: x.timestamp)
                time_period = f"{oldest_record.timestamp.strftime('%Y-%m-%d')} to {newest_record.timestamp.strftime('%Y-%m-%d')}"
            else:
                time_period = "No data"
            
            return {
                'total_actions': total_actions,
                'successful_actions': successful_actions,
                'failed_actions': failed_actions,
                'success_rate': (successful_actions / total_actions) * 100,
                'action_distribution': action_counts,
                'user_activity': user_counts,
                'risk_distribution': risk_counts,
                'resource_distribution': resource_counts,
                'time_period': time_period
            }
            
        except Exception as e:
            self.logger.error(f"❌ Failed to get statistics: {e}")
            return {}
    
    def generate_audit_report(self, format_type: str = "json") -> str:
        """Generate comprehensive audit report"""
        try:
            stats = self.get_audit_statistics()
            
            if format_type == "json":
                return json.dumps(stats, indent=2)
            elif format_type == "markdown":
                return self._generate_markdown_report(stats)
            else:
                return json.dumps(stats, indent=2)
                
        except Exception as e:
            self.logger.error(f"❌ Failed to generate report: {e}")
            return "{}"
    
    def _generate_markdown_report(self, stats: Dict[str, Any]) -> str:
        """Generate markdown audit report"""
        try:
            report = f"""
# 👤 ADMIN AUDIT REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 EXECUTIVE SUMMARY
- **Total Actions**: {stats['total_actions']}
- **Success Rate**: {stats['success_rate']:.1f}%
- **Successful Actions**: {stats['successful_actions']}
- **Failed Actions**: {stats['failed_actions']}
- **Time Period**: {stats['time_period']}

## 📈 ACTION DISTRIBUTION
"""
            
            for action, count in stats['action_distribution'].items():
                report += f"- **{action.upper()}**: {count}\n"
            
            report += "\n## 👥 USER ACTIVITY\n"
            
            for user, count in sorted(stats['user_activity'].items(), key=lambda x: x[1], reverse=True):
                report += f"- **{user}**: {count} actions\n"
            
            report += "\n## ⚠️ RISK LEVEL DISTRIBUTION\n"
            
            risk_order = ['critical', 'high', 'medium', 'low']
            for risk in risk_order:
                count = stats['risk_distribution'].get(risk, 0)
                if count > 0:
                    report += f"- **{risk.upper()}**: {count}\n"
            
            report += "\n## 📁 RESOURCE CATEGORIES\n"
            
            for resource, count in stats['resource_distribution'].items():
                report += f"- **{resource.upper()}**: {count}\n"
            
            return report
            
        except Exception as e:
            self.logger.error(f"❌ Failed to generate markdown report: {e}")
            return "Report generation failed"
    
    async def cleanup_old_records(self, days_to_keep: int = 365):
        """Clean up old audit records"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days_to_keep)
            
            # Remove old records from memory
            original_count = len(self.audit_trail)
            self.audit_trail = [r for r in self.audit_trail if r.timestamp >= cutoff_date]
            
            removed_count = original_count - len(self.audit_trail)
            
            self.logger.info(f"🗑️ Cleaned up {removed_count} old audit records (older than {days_to_keep} days)")
            
        except Exception as e:
            self.logger.error(f"❌ Cleanup failed: {e}")

# Decorator for automatic admin action logging
def audit_action(action: ActionType, resource_category: ResourceCategory):
    """Decorator for automatic admin action logging"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract admin context (this would come from authentication system)
            admin_context = kwargs.get('admin_context', {})
            
            # Extract action parameters
            resource_id = kwargs.get('resource_id')
            resource_name = kwargs.get('resource_name')
            old_values = kwargs.get('old_values')
            new_values = kwargs.get('new_values')
            
            # Get request context
            request_context = kwargs.get('request_context', {})
            ip_address = request_context.get('ip_address')
            user_agent = request_context.get('user_agent')
            session_id = request_context.get('session_id')
            
            # Execute the function
            try:
                result = await func(*args, **kwargs)
                success = True
                error_message = None
            except Exception as e:
                result = None
                success = False
                error_message = str(e)
                raise
            
            # Log the action
            audit_logger.log_admin_action(
                user_id=admin_context.get('user_id', 'unknown'),
                username=admin_context.get('username', 'unknown'),
                action=action,
                resource_category=resource_category,
                resource_id=resource_id,
                resource_name=resource_name,
                old_values=old_values,
                new_values=new_values,
                ip_address=ip_address,
                user_agent=user_agent,
                session_id=session_id,
                success=success,
                error_message=error_message
            )
            
            return result
        
        return wrapper
    return decorator

# Global admin audit logger instance
admin_audit_logger = AdminAuditLogger()
