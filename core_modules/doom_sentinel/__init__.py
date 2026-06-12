"""
DOOM SENTINEL - Digital Overwatch & Operations Machine
Multi-channel AI assistant with military-grade security and proactive monitoring
"""

from .telegram_gateway import TelegramGateway
from .whatsapp_gateway import WhatsAppGateway
from .security_middleware import SecurityMiddleware
from .alert_system import AlertSystem
from .rbac_manager import RBACManager

__version__ = "1.0.0"
__author__ = "LUMINA OS - Lead System Architect"

__all__ = [
    "TelegramGateway",
    "WhatsAppGateway", 
    "SecurityMiddleware",
    "AlertSystem",
    "RBACManager"
]
