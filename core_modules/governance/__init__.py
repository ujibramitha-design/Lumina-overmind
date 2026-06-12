"""
Governance Module
Handles system governance, compliance, and audit functions
"""

__version__ = "1.0.0"
__author__ = "HUNTER_AGENT_AI_MARKETING_DIGITAL"

from .compliance_manager import ComplianceManager
from .audit_logger import AuditLogger
from .policy_engine import PolicyEngine

__all__ = ['ComplianceManager', 'AuditLogger', 'PolicyEngine']
