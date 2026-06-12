"""
LUMINA OVERMIND SYSTEM - Sentry Integration
=========================================

Application Performance Monitoring and Error Tracking
"""

import os
import logging
from typing import Optional, Dict, Any
from datetime import datetime

# Try to import Sentry, but don't fail if not available
try:
    import sentry_sdk
    from sentry_sdk.integrations.fastapi import FastApiIntegration
    from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
    from sentry_sdk.integrations.redis import RedisIntegration
    from sentry_sdk.integrations.celery import CeleryIntegration
    SENTRY_AVAILABLE = True
except ImportError:
    SENTRY_AVAILABLE = False

logger = logging.getLogger(__name__)

class SentryManager:
    """
    Sentry APM and error tracking manager
    """
    
    def __init__(self):
        self.enabled = False
        self.dsn = None
        self.environment = None
        self.release = None
        
    def initialize(self, dsn: Optional[str] = None) -> bool:
        """
        Initialize Sentry SDK
        
        Args:
            dsn: Sentry DSN (defaults to environment variable)
            
        Returns:
            True if initialization successful, False otherwise
        """
        if not SENTRY_AVAILABLE:
            logger.warning("⚠️ Sentry SDK not available, skipping initialization")
            return False
            
        self.dsn = dsn or os.getenv("SENTRY_DSN")
        self.environment = os.getenv("ENVIRONMENT", "development")
        self.release = os.getenv("APP_VERSION", "2.0.0")
        
        if not self.dsn or self.dsn == "dummy-sentry-dsn-replace-in-production":
            logger.info("ℹ️ Sentry DSN not configured, monitoring disabled")
            return False
            
        try:
            sentry_sdk.init(
                dsn=self.dsn,
                environment=self.environment,
                release=self.release,
                integrations=[
                    FastApiIntegration(auto_enabling_integrations=False),
                    SqlalchemyIntegration(),
                    RedisIntegration(),
                    CeleryIntegration(),
                ],
                traces_sample_rate=float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", "0.1")),
                sample_rate=float(os.getenv("SENTRY_SAMPLE_RATE", "0.1")),
                send_default_pii=False,
                debug=self.environment == "development",
                before_send=self._before_send,
                before_breadcrumb=self._before_breadcrumb,
            )
            
            self.enabled = True
            logger.info(f"✅ Sentry initialized for environment: {self.environment}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize Sentry: {e}")
            return False
    
    def _before_send(self, event: Dict[str, Any], hint: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Filter and modify events before sending to Sentry
        
        Args:
            event: Sentry event
            hint: Sentry hint
            
        Returns:
            Modified event or None to drop
        """
        # Filter out sensitive data
        if "exception" in event:
            exception = event["exception"]
            if "values" in exception:
                for value in exception["values"]:
                    # Remove sensitive information from stack traces
                    if "stacktrace" in value:
                        stacktrace = value["stacktrace"]
                        if "frames" in stacktrace:
                            for frame in stacktrace["frames"]:
                                # Remove passwords and API keys from frame vars
                                if "vars" in frame:
                                    vars_dict = frame["vars"]
                                    for key, val in vars_dict.items():
                                        if any(sensitive in key.lower() for sensitive in ["password", "secret", "key", "token"]):
                                            vars_dict[key] = "[FILTERED]"
        
        # Add custom context
        event["tags"] = {
            **event.get("tags", {}),
            "service": "lumina-overmind-api",
            "version": self.release,
        }
        
        event["extra"] = {
            **event.get("extra", {}),
            "timestamp": datetime.utcnow().isoformat(),
        }
        
        return event
    
    def _before_breadcrumb(self, breadcrumb: Dict[str, Any], hint: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Filter breadcrumbs before sending to Sentry
        
        Args:
            breadcrumb: Sentry breadcrumb
            hint: Sentry hint
            
        Returns:
            Modified breadcrumb or None to drop
        """
        # Filter out health check breadcrumbs
        if breadcrumb.get("category") == "http" and "/health" in breadcrumb.get("data", {}).get("url", ""):
            return None
            
        return breadcrumb
    
    def capture_exception(self, exception: Exception, extra: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """
        Capture exception and send to Sentry
        
        Args:
            exception: Exception to capture
            extra: Additional context data
            
        Returns:
            Event ID if captured, None otherwise
        """
        if not self.enabled:
            return None
            
        try:
            event_id = sentry_sdk.capture_exception(exception, extra=extra)
            logger.info(f"🔍 Exception captured: {event_id}")
            return event_id
        except Exception as e:
            logger.error(f"❌ Failed to capture exception: {e}")
            return None
    
    def capture_message(self, message: str, level: str = "info", extra: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """
        Capture message and send to Sentry
        
        Args:
            message: Message to capture
            level: Message level
            extra: Additional context data
            
        Returns:
            Event ID if captured, None otherwise
        """
        if not self.enabled:
            return None
            
        try:
            event_id = sentry_sdk.capture_message(message, level=level, extra=extra)
            logger.info(f"📝 Message captured: {event_id}")
            return event_id
        except Exception as e:
            logger.error(f"❌ Failed to capture message: {e}")
            return None
    
    def set_user(self, user: Dict[str, Any]) -> None:
        """
        Set user context for Sentry
        
        Args:
            user: User information
        """
        if not self.enabled:
            return
            
        try:
            sentry_sdk.set_user({
                "id": user.get("id"),
                "email": user.get("email"),
                "username": user.get("username"),
                "role": user.get("role")
            })
        except Exception as e:
            logger.error(f"❌ Failed to set user context: {e}")
    
    def set_tag(self, key: str, value: str) -> None:
        """
        Set tag for Sentry context
        
        Args:
            key: Tag key
            value: Tag value
        """
        if not self.enabled:
            return
            
        try:
            sentry_sdk.set_tag(key, value)
        except Exception as e:
            logger.error(f"❌ Failed to set tag: {e}")
    
    def set_extra(self, key: str, value: Any) -> None:
        """
        Set extra context for Sentry
        
        Args:
            key: Context key
            value: Context value
        """
        if not self.enabled:
            return
            
        try:
            sentry_sdk.set_extra(key, value)
        except Exception as e:
            logger.error(f"❌ Failed to set extra context: {e}")
    
    def add_breadcrumb(self, category: str, message: str, level: str = "info", data: Optional[Dict[str, Any]] = None) -> None:
        """
        Add breadcrumb to Sentry context
        
        Args:
            category: Breadcrumb category
            message: Breadcrumb message
            level: Breadcrumb level
            data: Additional data
        """
        if not self.enabled:
            return
            
        try:
            sentry_sdk.add_breadcrumb(
                category=category,
                message=message,
                level=level,
                data=data
            )
        except Exception as e:
            logger.error(f"❌ Failed to add breadcrumb: {e}")
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get Sentry status and configuration
        
        Returns:
            Dict with status information
        """
        return {
            "enabled": self.enabled,
            "dsn": "***configured***" if self.dsn else None,
            "environment": self.environment,
            "release": self.release,
            "sdk_available": SENTRY_AVAILABLE,
            "timestamp": datetime.utcnow().isoformat()
        }

# Global Sentry manager instance
sentry_manager = SentryManager()

# Initialize Sentry if configured
def initialize_sentry() -> bool:
    """Initialize Sentry with environment configuration"""
    return sentry_manager.initialize()

# Decorator for automatic exception capture
def capture_exceptions(extra: Optional[Dict[str, Any]] = None):
    """
    Decorator to automatically capture exceptions
    
    Args:
        extra: Additional context data
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                sentry_manager.capture_exception(e, extra)
                raise
        return wrapper
    return decorator

# Context manager for performance monitoring
class PerformanceMonitor:
    """
    Context manager for monitoring performance
    """
    
    def __init__(self, operation: str, extra: Optional[Dict[str, Any]] = None):
        self.operation = operation
        self.extra = extra or {}
        self.start_time = None
        
    def __enter__(self):
        if sentry_manager.enabled:
            self.start_time = datetime.utcnow()
            sentry_manager.add_breadcrumb(
                category="performance",
                message=f"Starting {self.operation}",
                level="info",
                data=self.extra
            )
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if sentry_manager.enabled and self.start_time:
            duration = (datetime.utcnow() - self.start_time).total_seconds()
            
            sentry_manager.add_breadcrumb(
                category="performance",
                message=f"Completed {self.operation}",
                level="info",
                data={
                    **self.extra,
                    "duration_seconds": duration,
                    "success": exc_type is None
                }
            )

# FastAPI middleware for Sentry
def setup_sentry_middleware(app):
    """
    Setup Sentry middleware for FastAPI
    
    Args:
        app: FastAPI application instance
    """
    if sentry_manager.enabled:
        @app.middleware("http")
        async def sentry_middleware(request, call_next):
            sentry_manager.add_breadcrumb(
                category="http",
                message=f"{request.method} {request.url.path}",
                level="info",
                data={
                    "method": request.method,
                    "url": str(request.url),
                    "user_agent": request.headers.get("user-agent")
                }
            )
            
            response = await call_next(request)
            return response
        
        logger.info("✅ Sentry middleware configured")
    else:
        logger.info("ℹ️ Sentry middleware not configured")

# Celery task monitoring
def setup_celery_monitoring():
    """
    Setup monitoring for Celery tasks
    """
    if sentry_manager.enabled:
        # This would be integrated with Celery signals
        sentry_manager.add_breadcrumb(
            category="celery",
            message="Celery monitoring enabled",
            level="info"
        )
        
        logger.info("✅ Celery monitoring configured")
    else:
        logger.info("ℹ️ Celery monitoring not configured")

# Export main functions
__all__ = [
    "sentry_manager",
    "initialize_sentry", 
    "capture_exceptions",
    "PerformanceMonitor",
    "setup_sentry_middleware",
    "setup_celery_monitoring"
]
