"""
LICENSE VALIDATOR - DRM Framework for LUMINA OS
Commercial license validation and compliance checking
"""

import os
import logging
import hashlib
import hmac
import json
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
from cryptography.fernet import Fernet

logger = logging.getLogger(__name__)

class LicenseValidator:
    """
    License validation and DRM compliance system
    Validates commercial licenses and enforces usage restrictions
    """
    
    def __init__(self, license_key: Optional[str] = None):
        self.license_key = license_key or os.getenv('LUMINA_LICENSE_KEY', '')
        self.master_secret = os.getenv('LUMINA_MASTER_SECRET', 'lumina-master-2024-secret-key')
        self.validation_cache = {}
        self.cache_ttl = 300  # 5 minutes cache
        
    def validate_license(self) -> Tuple[bool, Dict[str, any]]:
        """
        Validate the license and return validation result
        
        Returns:
            Tuple[bool, Dict]: (is_valid, license_info)
        """
        try:
            # Check cache first
            cache_key = self._generate_cache_key()
            if cache_key in self.validation_cache:
                cache_entry = self.validation_cache[cache_key]
                if datetime.now().timestamp() - cache_entry['timestamp'] < self.cache_ttl:
                    return cache_entry['result']
            
            # Perform validation
            result = self._perform_validation()
            
            # Cache result
            self.validation_cache[cache_key] = {
                'result': result,
                'timestamp': datetime.now().timestamp()
            }
            
            return result
            
        except Exception as e:
            logger.error(f"License validation failed: {e}")
            return False, {'error': str(e), 'valid': False}
    
    def _perform_validation(self) -> Tuple[bool, Dict[str, any]]:
        """Perform actual license validation"""
        
        # Check if license key exists
        if not self.license_key:
            return False, {
                'valid': False,
                'error': 'No license key provided',
                'message': 'Please provide a valid LUMINA_LICENSE_KEY'
            }
        
        # Parse license key
        try:
            parts = self.license_key.split('-')
            if len(parts) != 4 or parts[0] != 'LUMINA':
                return False, {
                    'valid': False,
                    'error': 'Invalid license format',
                    'message': 'License key must follow format: LUMINA-{CLIENT_ID}-{VERSION}-{HASH}'
                }
            
            client_id, version, signature = parts[1], parts[2], parts[3]
            
        except Exception as e:
            return False, {
                'valid': False,
                'error': 'License parsing failed',
                'message': str(e)
            }
        
        # Validate license signature
        expected_signature = self._generate_signature(client_id, version)
        if not hmac.compare_digest(signature, expected_signature):
            return False, {
                'valid': False,
                'error': 'Invalid license signature',
                'message': 'License key is corrupted or tampered'
            }
        
        # Check version compatibility
        if not self._is_version_compatible(version):
            return False, {
                'valid': False,
                'error': 'Incompatible version',
                'message': f'License version {version} is not compatible with current version'
            }
        
        # Check license expiration (if applicable)
        expiration_info = self._check_expiration(client_id)
        if not expiration_info['valid']:
            return False, expiration_info
        
        # Get license features
        features = self._get_license_features(client_id, version)
        
        return True, {
            'valid': True,
            'client_id': client_id,
            'version': version,
            'features': features,
            'expiration': expiration_info.get('expiration'),
            'message': 'License is valid'
        }
    
    def _generate_signature(self, client_id: str, version: str) -> str:
        """Generate HMAC signature for license validation"""
        message = f"{client_id}-{version}".encode('utf-8')
        signature = hmac.new(
            self.master_secret.encode('utf-8'),
            message,
            hashlib.sha256
        ).hexdigest()
        return signature[:16]  # Use first 16 characters
    
    def _generate_cache_key(self) -> str:
        """Generate cache key for validation results"""
        return hashlib.md5(self.license_key.encode()).hexdigest()
    
    def _is_version_compatible(self, version: str) -> bool:
        """Check if license version is compatible"""
        try:
            # Parse semantic version
            major, minor, patch = map(int, version.split('.'))
            current_major, current_minor, current_patch = 1, 0, 0  # Current version
            
            # Major version must match
            if major != current_major:
                return False
            
            # Minor version can be higher or equal
            if minor > current_minor:
                return False
            
            return True
            
        except Exception:
            return False
    
    def _check_expiration(self, client_id: str) -> Dict[str, any]:
        """Check if license has expiration"""
        # For demo licenses, no expiration
        if client_id.startswith('DEMO'):
            return {'valid': True}
        
        # For commercial licenses, check expiration
        # TODO: Implement expiration check based on client_id and master server
        return {'valid': True}
    
    def _get_license_features(self, client_id: str, version: str) -> Dict[str, bool]:
        """Get available features based on license"""
        
        # Demo license features
        if client_id.startswith('DEMO'):
            return {
                'ai_intelligence': True,
                'lead_generation': True,
                'basic_analytics': True,
                'white_label': False,
                'advanced_ai': False,
                'api_access': False,
                'unlimited_users': False,
                'priority_support': False
            }
        
        # Commercial license features
        return {
            'ai_intelligence': True,
            'lead_generation': True,
            'basic_analytics': True,
            'white_label': True,
            'advanced_ai': True,
            'api_access': True,
            'unlimited_users': True,
            'priority_support': True
        }
    
    def check_feature_access(self, feature: str) -> bool:
        """Check if current license allows access to a feature"""
        is_valid, license_info = self.validate_license()
        
        if not is_valid:
            return False
        
        features = license_info.get('features', {})
        return features.get(feature, False)
    
    def get_license_info(self) -> Dict[str, any]:
        """Get license information"""
        is_valid, license_info = self.validate_license()
        
        if not is_valid:
            return {
                'valid': False,
                'error': license_info.get('error', 'Unknown error')
            }
        
        return {
            'valid': True,
            'client_id': license_info.get('client_id'),
            'version': license_info.get('version'),
            'features': license_info.get('features', {}),
            'expiration': license_info.get('expiration')
        }
    
    def validate_api_request(self, endpoint: str, method: str) -> bool:
        """Validate if API request is allowed under current license"""
        # Check if license is valid
        is_valid, license_info = self.validate_license()
        if not is_valid:
            return False
        
        # Check API access feature
        if not license_info.get('features', {}).get('api_access', False):
            return False
        
        # Check specific endpoint restrictions
        restricted_endpoints = [
            '/api/config-vault',
            '/api/admin',
            '/api/system'
        ]
        
        if endpoint in restricted_endpoints:
            # Require admin license for restricted endpoints
            return license_info.get('client_id', '').startswith('COMMERCIAL')
        
        return True
    
    def log_usage(self, action: str, resource: str, metadata: Dict = None):
        """Log usage for license compliance monitoring"""
        try:
            usage_data = {
                'timestamp': datetime.now().isoformat(),
                'action': action,
                'resource': resource,
                'client_id': self.license_key.split('-')[1] if '-' in self.license_key else 'UNKNOWN',
                'metadata': metadata or {}
            }
            
            # TODO: Send usage data to master license server
            logger.info(f"License usage logged: {usage_data}")
            
        except Exception as e:
            logger.error(f"Failed to log usage: {e}")
    
    def generate_license_request(self, client_info: Dict[str, any]) -> Dict[str, any]:
        """Generate license request for new client"""
        try:
            client_id = client_info.get('client_id', '').upper().replace(' ', '_')
            version = client_info.get('version', '1.0.0')
            
            # Generate signature
            signature = self._generate_signature(client_id, version)
            
            # Create license key
            license_key = f"LUMINA-{client_id}-{version}-{signature}"
            
            return {
                'license_key': license_key,
                'client_id': client_id,
                'version': version,
                'signature': signature,
                'generated_at': datetime.now().isoformat(),
                'expires_at': None  # TODO: Implement expiration logic
            }
            
        except Exception as e:
            logger.error(f"Failed to generate license request: {e}")
            return {'error': str(e)}

# Global license validator instance
license_validator = LicenseValidator()

# Middleware decorator for API endpoints
def require_license(feature: str = None):
    """Decorator to require valid license for API endpoints"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Check license validity
            is_valid, license_info = license_validator.validate_license()
            
            if not is_valid:
                raise PermissionError(f"License validation failed: {license_info.get('message', 'Unknown error')}")
            
            # Check feature access if specified
            if feature:
                if not license_info.get('features', {}).get(feature, False):
                    raise PermissionError(f"Feature '{feature}' not available in current license")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Convenience functions
def is_license_valid() -> bool:
    """Check if current license is valid"""
    is_valid, _ = license_validator.validate_license()
    return is_valid

def get_license_features() -> Dict[str, bool]:
    """Get available features from current license"""
    _, license_info = license_validator.validate_license()
    return license_info.get('features', {})

def has_feature_access(feature: str) -> bool:
    """Check if current license allows access to a feature"""
    return license_validator.check_feature_access(feature)

# TODO: Connect to Master License Server
# This function should be implemented to connect to the central license server
# for real-time license validation, usage tracking, and compliance monitoring
async def validate_with_master_server(license_key: str, client_id: str) -> Dict[str, any]:
    """
    TODO: Connect to Master License Server
    
    This function should:
    1. Send license key and client ID to master server
    2. Receive validation result from master server
    3. Log validation and usage data
    4. Return validation result
    
    Master server endpoint: https://license.lumina.tech/api/validate
    """
    pass
