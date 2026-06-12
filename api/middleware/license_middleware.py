"""
LICENSE MIDDLEWARE - API License Validation
Validates licenses for all API requests
"""

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import logging
import json
from typing import Dict, Any

from core_modules.security.license_validator import license_validator

logger = logging.getLogger(__name__)

class LicenseMiddleware(BaseHTTPMiddleware):
    """
    Middleware to validate licenses for API requests
    """
    
    def __init__(self, app, excluded_paths: list = None):
        super().__init__(app)
        self.excluded_paths = excluded_paths or [
            '/health',
            '/api/auth/login',
            '/api/auth/verify',
            '/docs',
            '/openapi.json',
            '/favicon.ico'
        ]
    
    async def dispatch(self, request: Request, call_next):
        # Get request path
        path = request.url.path
        
        # Skip license validation for excluded paths
        if any(path.startswith(excluded_path) for excluded_path in self.excluded_paths):
            return await call_next(request)
        
        # Skip license validation for OPTIONS requests (CORS preflight)
        if request.method == 'OPTIONS':
            return await call_next(request)
        
        # Validate license
        try:
            # Check if license is valid
            is_valid, license_info = license_validator.validate_license()
            
            if not is_valid:
                logger.warning(f"License validation failed for {path}: {license_info.get('message', 'Unknown error')}")
                
                return JSONResponse(
                    status_code=403,
                    content={
                        'error': 'License validation failed',
                        'message': license_info.get('message', 'Invalid license'),
                        'code': 'LICENSE_INVALID'
                    }
                )
            
            # Validate API access
            if not license_validator.validate_api_request(path, request.method):
                logger.warning(f"API access denied for {path} - insufficient license")
                
                return JSONResponse(
                    status_code=403,
                    content={
                        'error': 'API access denied',
                        'message': 'Current license does not allow access to this API endpoint',
                        'code': 'INSUFFICIENT_LICENSE'
                    }
                )
            
            # Add license info to request headers for downstream use
            request.state.license_info = license_info
            
            # Log usage
            license_validator.log_usage(
                action='api_request',
                resource=f"{request.method} {path}",
                metadata={
                    'user_agent': request.headers.get('user-agent'),
                    'ip': request.client.host
                }
            )
            
            # Continue with request
            return await call_next(request)
            
        except Exception as e:
            logger.error(f"License middleware error: {e}")
            
            return JSONResponse(
                status_code=500,
                content={
                    'error': 'License validation error',
                    'message': 'An error occurred during license validation',
                    'code': 'LICENSE_ERROR'
                }
            )

# License endpoint for license information
async def get_license_info(request: Request):
    """Get current license information"""
    try:
        license_info = license_validator.get_license_info()
        
        return JSONResponse(
            status_code=200,
            content={
                'license': license_info,
                'timestamp': '2024-01-01T00:00:00Z'
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to get license info: {e}")
        
        return JSONResponse(
            status_code=500,
            content={
                'error': 'Failed to get license information',
                'message': str(e)
            }
        )

# Feature access check endpoint
async def check_feature_access(request: Request, feature: str):
    """Check if current license allows access to a specific feature"""
    try:
        has_access = license_validator.check_feature_access(feature)
        
        return JSONResponse(
            status_code=200,
            content={
                'feature': feature,
                'has_access': has_access,
                'message': f"Access {'granted' if has_access else 'denied'} for feature '{feature}'"
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to check feature access: {e}")
        
        return JSONResponse(
            status_code=500,
            content={
                'error': 'Failed to check feature access',
                'message': str(e)
            }
        )
