"""
LUMINA OS - Webhook Security & Advanced Authentication
Enterprise-grade webhook security with HMAC validation and rate limiting
"""

import os
import logging
import asyncio
import json
import hashlib
import hmac
import time
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import ipaddress
from functools import wraps

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecurityLevel(Enum):
    """Security levels for webhook validation"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ValidationStatus(Enum):
    """Webhook validation status"""
    VALID = "valid"
    INVALID = "invalid"
    EXPIRED = "expired"
    RATE_LIMITED = "rate_limited"
    BLOCKED = "blocked"
    SUSPICIOUS = "suspicious"

@dataclass
class WebhookConfig:
    """Webhook security configuration"""
    endpoint_path: str
    secret_key: str
    security_level: SecurityLevel
    rate_limit_per_minute: int
    rate_limit_per_hour: int
    max_payload_size: int
    allowed_ips: List[str]
    blocked_ips: List[str]
    require_hmac: bool
    hmac_algorithm: str
    max_age_seconds: int

@dataclass
class WebhookRequest:
    """Webhook request information"""
    headers: Dict[str, str]
    body: bytes
    ip_address: str
    user_agent: str
    timestamp: datetime
    endpoint: str

@dataclass
class ValidationResult:
    """Webhook validation result"""
    status: ValidationStatus
    is_valid: bool
    error_message: Optional[str]
    security_score: float
    risk_factors: List[str]
    processing_time: float

class WebhookSecurity:
    """
    Enterprise-grade webhook security system
    Provides HMAC validation, rate limiting, IP filtering, and comprehensive security
    """
    
    def __init__(self):
        """Initialize webhook security system"""
        self.logger = logging.getLogger(__name__)
        
        # Webhook configurations
        self.webhook_configs: Dict[str, WebhookConfig] = {}
        self._initialize_webhook_configs()
        
        # Rate limiting storage
        self.rate_limits: Dict[str, Dict[str, Any]] = {}
        
        # IP reputation
        self.ip_reputation: Dict[str, Dict[str, Any]] = {}
        self._initialize_ip_reputation()
        
        # Security metrics
        self.security_metrics = {
            'total_requests': 0,
            'valid_requests': 0,
            'invalid_requests': 0,
            'blocked_requests': 0,
            'rate_limited_requests': 0,
            'suspicious_requests': 0
        }
        
        # Threat detection
        self.threat_patterns = self._initialize_threat_patterns()
        
        self.logger.info("🔐 Webhook Security initialized")
        self.logger.info(f"🛡️ Webhook endpoints configured: {len(self.webhook_configs)}")
    
    def _initialize_webhook_configs(self):
        """Initialize webhook configurations"""
        self.webhook_configs['incoming-lead'] = WebhookConfig(
            endpoint_path='/api/webhook/incoming-lead',
            secret_key=os.getenv('WEBHOOK_SECRET_KEY', 'your-secret-key-here'),
            security_level=SecurityLevel.HIGH,
            rate_limit_per_minute=60,
            rate_limit_per_hour=1000,
            max_payload_size=1024 * 1024,  # 1MB
            allowed_ips=[],  # Empty means allow all
            blocked_ips=[
                '192.168.1.100',  # Example blocked IP
                '10.0.0.50'       # Example blocked IP
            ],
            require_hmac=True,
            hmac_algorithm='sha256',
            max_age_seconds=300  # 5 minutes
        )
        
        self.webhook_configs['meta-webhook'] = WebhookConfig(
            endpoint_path='/api/webhook/meta',
            secret_key=os.getenv('META_WEBHOOK_SECRET', 'meta-secret-key'),
            security_level=SecurityLevel.CRITICAL,
            rate_limit_per_minute=30,
            rate_limit_per_hour=500,
            max_payload_size=512 * 1024,  # 512KB
            allowed_ips=[
                '31.13.66.0/24',    # Meta IP range
                '66.220.144.0/20',   # Meta IP range
                '69.63.176.0/20',    # Meta IP range
                '69.63.184.0/20',    # Meta IP range
                '74.119.76.0/22',    # Meta IP range
                '103.4.96.0/22',     # Meta IP range
                '157.240.0.0/16',    # Meta IP range
                '173.252.64.0/18',   # Meta IP range
                '173.252.96.0/19',   # Meta IP range
                '179.60.192.0/22',   # Meta IP range
                '185.60.216.0/22',   # Meta IP range
                '204.15.20.0/22',    # Meta IP range
            ],
            blocked_ips=[],
            require_hmac=True,
            hmac_algorithm='sha256',
            max_age_seconds=60  # 1 minute
        )
        
        self.webhook_configs['payment-webhook'] = WebhookConfig(
            endpoint_path='/api/webhook/payment',
            secret_key=os.getenv('PAYMENT_WEBHOOK_SECRET', 'payment-secret-key'),
            security_level=SecurityLevel.CRITICAL,
            rate_limit_per_minute=10,
            rate_limit_per_hour=100,
            max_payload_size=256 * 1024,  # 256KB
            allowed_ips=[
                '127.0.0.1',  # Localhost
                '10.0.0.0/8',  # Private network
                '172.16.0.0/12',  # Private network
                '192.168.0.0/16'  # Private network
            ],
            blocked_ips=[],
            require_hmac=True,
            hmac_algorithm='sha256',
            max_age_seconds=300  # 5 minutes
        )
    
    def _initialize_ip_reputation(self):
        """Initialize IP reputation system"""
        # Known malicious IPs (example)
        self.ip_reputation = {
            '192.168.1.100': {'reputation': -10, 'reason': 'test_blocked'},
            '10.0.0.50': {'reputation': -10, 'reason': 'test_blocked'},
        }
    
    def _initialize_threat_patterns(self) -> List[str]:
        """Initialize threat detection patterns"""
        return [
            r'<script.*?>.*?</script>',  # XSS attempts
            r'union.*select.*from',     # SQL injection attempts
            r'drop.*table',            # SQL injection attempts
            r'exec.*\(',               # Command injection attempts
            r'eval.*\(',               # Code injection attempts
            r'base64_decode',          # Obfuscation attempts
            r'shell_exec',             # Command execution attempts
            r'system.*\(',             # System command attempts
        ]
    
    def validate_webhook_request(self, request: WebhookRequest, endpoint_name: str) -> ValidationResult:
        """
        Validate webhook request with comprehensive security checks
        
        Args:
            request: Webhook request information
            endpoint_name: Name of the webhook endpoint
            
        Returns:
            ValidationResult: Validation result with detailed information
        """
        start_time = time.time()
        
        try:
            config = self.webhook_configs.get(endpoint_name)
            if not config:
                return ValidationResult(
                    status=ValidationStatus.INVALID,
                    is_valid=False,
                    error_message=f"Unknown endpoint: {endpoint_name}",
                    security_score=0.0,
                    risk_factors=["Unknown endpoint"],
                    processing_time=time.time() - start_time
                )
            
            # Update metrics
            self.security_metrics['total_requests'] += 1
            
            # Perform security checks
            risk_factors = []
            security_score = 100.0
            
            # 1. IP validation
            ip_result = self._validate_ip_address(request.ip_address, config)
            if not ip_result['valid']:
                risk_factors.extend(ip_result['risk_factors'])
                security_score -= ip_result['score_penalty']
            
            # 2. Rate limiting
            rate_result = self._check_rate_limit(request.ip_address, config)
            if not rate_result['allowed']:
                self.security_metrics['rate_limited_requests'] += 1
                return ValidationResult(
                    status=ValidationStatus.RATE_LIMITED,
                    is_valid=False,
                    error_message="Rate limit exceeded",
                    security_score=security_score,
                    risk_factors=risk_factors + ["Rate limit exceeded"],
                    processing_time=time.time() - start_time
                )
            
            # 3. Payload size validation
            if len(request.body) > config.max_payload_size:
                risk_factors.append("Payload too large")
                security_score -= 20.0
            
            # 4. HMAC validation (if required)
            if config.require_hmac:
                hmac_result = self._validate_hmac_signature(request, config)
                if not hmac_result['valid']:
                    risk_factors.extend(hmac_result['risk_factors'])
                    security_score -= hmac_result['score_penalty']
            
            # 5. Timestamp validation
            if config.max_age_seconds > 0:
                timestamp_result = self._validate_timestamp(request, config)
                if not timestamp_result['valid']:
                    risk_factors.extend(timestamp_result['risk_factors'])
                    security_score -= timestamp_result['score_penalty']
            
            # 6. Content validation
            content_result = self._validate_content(request.body.decode('utf-8', errors='ignore'))
            if not content_result['valid']:
                risk_factors.extend(content_result['risk_factors'])
                security_score -= content_result['score_penalty']
            
            # 7. User agent validation
            ua_result = self._validate_user_agent(request.user_agent)
            if not ua_result['valid']:
                risk_factors.extend(ua_result['risk_factors'])
                security_score -= ua_result['score_penalty']
            
            # Determine final status
            is_valid = len(risk_factors) == 0 and security_score >= 70.0
            
            if is_valid:
                status = ValidationStatus.VALID
                self.security_metrics['valid_requests'] += 1
            elif security_score < 30.0:
                status = ValidationStatus.BLOCKED
                self.security_metrics['blocked_requests'] += 1
            elif security_score < 50.0:
                status = ValidationStatus.SUSPICIOUS
                self.security_metrics['suspicious_requests'] += 1
            else:
                status = ValidationStatus.INVALID
                self.security_metrics['invalid_requests'] += 1
            
            return ValidationResult(
                status=status,
                is_valid=is_valid,
                error_message=None if is_valid else f"Security validation failed: {', '.join(risk_factors)}",
                security_score=max(0.0, security_score),
                risk_factors=risk_factors,
                processing_time=time.time() - start_time
            )
            
        except Exception as e:
            self.logger.error(f"❌ Webhook validation error: {e}")
            return ValidationResult(
                status=ValidationStatus.INVALID,
                is_valid=False,
                error_message=f"Validation error: {str(e)}",
                security_score=0.0,
                risk_factors=["Validation error"],
                processing_time=time.time() - start_time
            )
    
    def _validate_ip_address(self, ip_address: str, config: WebhookConfig) -> Dict[str, Any]:
        """Validate IP address against allowed/blocked lists"""
        try:
            # Check blocked IPs first
            for blocked_ip in config.blocked_ips:
                if self._ip_matches(ip_address, blocked_ip):
                    return {
                        'valid': False,
                        'risk_factors': [f"IP address blocked: {ip_address}"],
                        'score_penalty': 50.0
                    }
            
            # Check allowed IPs (if specified)
            if config.allowed_ips:
                allowed = False
                for allowed_ip in config.allowed_ips:
                    if self._ip_matches(ip_address, allowed_ip):
                        allowed = True
                        break
                
                if not allowed:
                    return {
                        'valid': False,
                        'risk_factors': [f"IP address not allowed: {ip_address}"],
                        'score_penalty': 30.0
                    }
            
            # Check IP reputation
            reputation = self.ip_reputation.get(ip_address, {'reputation': 0})
            if reputation['reputation'] < -5:
                return {
                    'valid': False,
                    'risk_factors': [f"Low IP reputation: {reputation['reason']}"],
                    'score_penalty': 25.0
                }
            
            return {'valid': True, 'risk_factors': [], 'score_penalty': 0.0}
            
        except Exception as e:
            self.logger.error(f"❌ IP validation error: {e}")
            return {'valid': False, 'risk_factors': ['IP validation error'], 'score_penalty': 10.0}
    
    def _ip_matches(self, ip_address: str, ip_pattern: str) -> bool:
        """Check if IP address matches pattern (supports CIDR)"""
        try:
            if '/' in ip_pattern:
                # CIDR notation
                network = ipaddress.ip_network(ip_pattern, strict=False)
                return ipaddress.ip_address(ip_address) in network
            else:
                # Exact match
                return ip_address == ip_pattern
        except Exception:
            return False
    
    def _check_rate_limit(self, ip_address: str, config: WebhookConfig) -> Dict[str, Any]:
        """Check rate limiting for IP address"""
        try:
            current_time = time.time()
            
            # Initialize rate limit tracking for IP
            if ip_address not in self.rate_limits:
                self.rate_limits[ip_address] = {
                    'requests_per_minute': [],
                    'requests_per_hour': []
                }
            
            ip_limits = self.rate_limits[ip_address]
            
            # Clean old requests
            ip_limits['requests_per_minute'] = [
                req_time for req_time in ip_limits['requests_per_minute']
                if current_time - req_time < 60
            ]
            
            ip_limits['requests_per_hour'] = [
                req_time for req_time in ip_limits['requests_per_hour']
                if current_time - req_time < 3600
            ]
            
            # Check limits
            minute_count = len(ip_limits['requests_per_minute'])
            hour_count = len(ip_limits['requests_per_hour'])
            
            if minute_count >= config.rate_limit_per_minute:
                return {'allowed': False, 'reason': 'Minute rate limit exceeded'}
            
            if hour_count >= config.rate_limit_per_hour:
                return {'allowed': False, 'reason': 'Hour rate limit exceeded'}
            
            # Add current request
            ip_limits['requests_per_minute'].append(current_time)
            ip_limits['requests_per_hour'].append(current_time)
            
            return {'allowed': True, 'reason': None}
            
        except Exception as e:
            self.logger.error(f"❌ Rate limit check error: {e}")
            return {'allowed': True, 'reason': 'Rate limit check error'}
    
    def _validate_hmac_signature(self, request: WebhookRequest, config: WebhookConfig) -> Dict[str, Any]:
        """Validate HMAC signature"""
        try:
            # Get signature from headers
            signature_header = request.headers.get('X-Hub-Signature-256') or request.headers.get('X-Signature')
            
            if not signature_header:
                return {
                    'valid': False,
                    'risk_factors': ['Missing HMAC signature'],
                    'score_penalty': 40.0
                }
            
            # Parse signature
            if '=' in signature_header:
                algorithm, signature = signature_header.split('=', 1)
            else:
                return {
                    'valid': False,
                    'risk_factors': ['Invalid signature format'],
                    'score_penalty': 30.0
                }
            
            # Calculate expected signature
            expected_signature = self._calculate_hmac_signature(
                request.body, 
                config.secret_key, 
                config.hmac_algorithm
            )
            
            # Compare signatures
            if not hmac.compare_digest(signature, expected_signature):
                return {
                    'valid': False,
                    'risk_factors': ['HMAC signature mismatch'],
                    'score_penalty': 50.0
                }
            
            return {'valid': True, 'risk_factors': [], 'score_penalty': 0.0}
            
        except Exception as e:
            self.logger.error(f"❌ HMAC validation error: {e}")
            return {'valid': False, 'risk_factors': ['HMAC validation error'], 'score_penalty': 20.0}
    
    def _calculate_hmac_signature(self, body: bytes, secret_key: str, algorithm: str) -> str:
        """Calculate HMAC signature"""
        try:
            if algorithm.lower() == 'sha256':
                return hmac.new(
                    secret_key.encode('utf-8'),
                    body,
                    hashlib.sha256
                ).hexdigest()
            elif algorithm.lower() == 'sha1':
                return hmac.new(
                    secret_key.encode('utf-8'),
                    body,
                    hashlib.sha1
                ).hexdigest()
            else:
                raise ValueError(f"Unsupported algorithm: {algorithm}")
                
        except Exception as e:
            self.logger.error(f"❌ HMAC calculation error: {e}")
            raise
    
    def _validate_timestamp(self, request: WebhookRequest, config: WebhookConfig) -> Dict[str, Any]:
        """Validate request timestamp"""
        try:
            # Get timestamp from headers
            timestamp_header = request.headers.get('X-Timestamp') or request.headers.get('timestamp')
            
            if not timestamp_header:
                return {'valid': True, 'risk_factors': [], 'score_penalty': 0.0}
            
            # Parse timestamp
            try:
                timestamp = float(timestamp_header)
                request_time = datetime.fromtimestamp(timestamp)
            except ValueError:
                return {
                    'valid': False,
                    'risk_factors': ['Invalid timestamp format'],
                    'score_penalty': 20.0
                }
            
            # Check age
            age_seconds = (datetime.now() - request_time).total_seconds()
            if age_seconds > config.max_age_seconds:
                return {
                    'valid': False,
                    'risk_factors': [f'Request too old: {age_seconds}s'],
                    'score_penalty': 30.0
                }
            
            return {'valid': True, 'risk_factors': [], 'score_penalty': 0.0}
            
        except Exception as e:
            self.logger.error(f"❌ Timestamp validation error: {e}")
            return {'valid': False, 'risk_factors': ['Timestamp validation error'], 'score_penalty': 10.0}
    
    def _validate_content(self, content: str) -> Dict[str, Any]:
        """Validate content for threats"""
        try:
            content_lower = content.lower()
            risk_factors = []
            score_penalty = 0.0
            
            # Check for threat patterns
            for pattern in self.threat_patterns:
                import re
                if re.search(pattern, content_lower, re.IGNORECASE):
                    risk_factors.append(f"Suspicious content pattern: {pattern}")
                    score_penalty += 15.0
            
            # Check for JSON structure (if expected)
            try:
                json.loads(content)
            except json.JSONDecodeError:
                # Not necessarily a threat, but worth noting
                pass
            
            return {'valid': len(risk_factors) == 0, 'risk_factors': risk_factors, 'score_penalty': score_penalty}
            
        except Exception as e:
            self.logger.error(f"❌ Content validation error: {e}")
            return {'valid': False, 'risk_factors': ['Content validation error'], 'score_penalty': 10.0}
    
    def _validate_user_agent(self, user_agent: str) -> Dict[str, Any]:
        """Validate user agent"""
        try:
            if not user_agent:
                return {
                    'valid': False,
                    'risk_factors': ['Missing user agent'],
                    'score_penalty': 10.0
                }
            
            # Check for suspicious user agents
            suspicious_patterns = [
                'bot', 'crawler', 'spider', 'scraper', 'curl', 'wget',
                'python', 'java', 'perl', 'php', 'ruby'
            ]
            
            user_agent_lower = user_agent.lower()
            risk_factors = []
            score_penalty = 0.0
            
            for pattern in suspicious_patterns:
                if pattern in user_agent_lower:
                    risk_factors.append(f"Suspicious user agent: {pattern}")
                    score_penalty += 5.0
            
            return {'valid': len(risk_factors) == 0, 'risk_factors': risk_factors, 'score_penalty': score_penalty}
            
        except Exception as e:
            self.logger.error(f"❌ User agent validation error: {e}")
            return {'valid': False, 'risk_factors': ['User agent validation error'], 'score_penalty': 5.0}
    
    def generate_hmac_signature(self, payload: Dict[str, Any], secret_key: str, algorithm: str = 'sha256') -> Tuple[str, str]:
        """
        Generate HMAC signature for webhook payload
        
        Args:
            payload: Payload to sign
            secret_key: Secret key for signing
            algorithm: HMAC algorithm
            
        Returns:
            Tuple[str, str]: (signature, algorithm)
        """
        try:
            body = json.dumps(payload, separators=(',', ':')).encode('utf-8')
            signature = self._calculate_hmac_signature(body, secret_key, algorithm)
            return signature, algorithm
            
        except Exception as e:
            self.logger.error(f"❌ HMAC generation error: {e}")
            raise
    
    def get_security_metrics(self) -> Dict[str, Any]:
        """Get security metrics and statistics"""
        try:
            metrics = self.security_metrics.copy()
            
            # Calculate rates
            total_requests = metrics['total_requests']
            if total_requests > 0:
                metrics['valid_rate'] = (metrics['valid_requests'] / total_requests) * 100
                metrics['invalid_rate'] = (metrics['invalid_requests'] / total_requests) * 100
                metrics['blocked_rate'] = (metrics['blocked_requests'] / total_requests) * 100
                metrics['rate_limited_rate'] = (metrics['rate_limited_requests'] / total_requests) * 100
                metrics['suspicious_rate'] = (metrics['suspicious_requests'] / total_requests) * 100
            else:
                metrics['valid_rate'] = 0.0
                metrics['invalid_rate'] = 0.0
                metrics['blocked_rate'] = 0.0
                metrics['rate_limited_rate'] = 0.0
                metrics['suspicious_rate'] = 0.0
            
            # Add rate limit info
            metrics['active_rate_limits'] = len(self.rate_limits)
            
            # Add IP reputation info
            metrics['ip_reputation_entries'] = len(self.ip_reputation)
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"❌ Security metrics error: {e}")
            return {}
    
    def update_ip_reputation(self, ip_address: str, reputation_change: int, reason: str):
        """Update IP reputation"""
        try:
            if ip_address not in self.ip_reputation:
                self.ip_reputation[ip_address] = {'reputation': 0}
            
            self.ip_reputation[ip_address]['reputation'] += reputation_change
            self.ip_reputation[ip_address]['reason'] = reason
            
            self.logger.info(f"📊 IP reputation updated: {ip_address} -> {self.ip_reputation[ip_address]['reputation']}")
            
        except Exception as e:
            self.logger.error(f"❌ IP reputation update error: {e}")
    
    def cleanup_old_data(self):
        """Clean up old rate limit data"""
        try:
            current_time = time.time()
            
            # Clean old rate limit data
            for ip_address in list(self.rate_limits.keys()):
                ip_limits = self.rate_limits[ip_address]
                
                # Clean minute limits
                ip_limits['requests_per_minute'] = [
                    req_time for req_time in ip_limits['requests_per_minute']
                    if current_time - req_time < 60
                ]
                
                # Clean hour limits
                ip_limits['requests_per_hour'] = [
                    req_time for req_time in ip_limits['requests_per_hour']
                    if current_time - req_time < 3600
                ]
                
                # Remove empty entries
                if not ip_limits['requests_per_minute'] and not ip_limits['requests_per_hour']:
                    del self.rate_limits[ip_address]
            
            self.logger.info("🧹 Rate limit data cleaned up")
            
        except Exception as e:
            self.logger.error(f"❌ Cleanup error: {e}")

# Decorator for webhook validation
def webhook_security(endpoint_name: str):
    """Decorator for automatic webhook security validation"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            from flask import request
            
            # Create webhook request object
            webhook_request = WebhookRequest(
                headers=dict(request.headers),
                body=request.get_data(),
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent', ''),
                timestamp=datetime.now(),
                endpoint=endpoint_name
            )
            
            # Validate request
            validation_result = webhook_security.validate_webhook_request(webhook_request, endpoint_name)
            
            if not validation_result.is_valid:
                return {
                    'success': False,
                    'error': 'Webhook validation failed',
                    'details': validation_result.error_message,
                    'security_score': validation_result.security_score
                }, 401
            
            # Call original function
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator

# Global webhook security instance
webhook_security = WebhookSecurity()
