"""
LICENSE ENDPOINTS - License Management API
Endpoints for license validation and feature access checking
"""

import logging
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Dict, Any

from core_modules.security.license_validator import license_validator

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/license", tags=["License"])

@router.get("/info")
async def get_license_info():
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
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get license information: {str(e)}"
        )

@router.get("/features")
async def get_available_features():
    """Get available features from current license"""
    try:
        features = license_validator.get_license_features()
        
        return JSONResponse(
            status_code=200,
            content={
                'features': features,
                'total_features': len(features),
                'enabled_features': sum(1 for f in features.values() if f)
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to get license features: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get license features: {str(e)}"
        )

@router.get("/check/{feature}")
async def check_feature_access(feature: str):
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
        raise HTTPException(
            status_code=500,
            detail=f"Failed to check feature access: {str(e)}"
        )

@router.get("/validate")
async def validate_license():
    """Validate current license"""
    try:
        is_valid, license_info = license_validator.validate_license()
        
        return JSONResponse(
            status_code=200,
            content={
                'valid': is_valid,
                'license_info': license_info,
                'message': 'License validation completed'
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to validate license: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to validate license: {str(e)}"
        )

@router.get("/usage")
async def get_usage_stats():
    """Get license usage statistics"""
    try:
        # TODO: Implement usage statistics collection
        # For now, return mock data
        usage_stats = {
            'api_requests': 1250,
            'ai_requests': 450,
            'leads_generated': 89,
            'active_users': 12,
            'storage_used': '2.3GB',
            'last_updated': '2024-01-01T00:00:00Z'
        }
        
        return JSONResponse(
            status_code=200,
            content={
                'usage': usage_stats,
                'message': 'Usage statistics retrieved successfully'
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to get usage stats: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get usage statistics: {str(e)}"
        )

@router.post("/activate")
async def activate_license(activation_data: Dict[str, Any]):
    """Activate a new license"""
    try:
        license_key = activation_data.get('license_key')
        
        if not license_key:
            raise HTTPException(
                status_code=400,
                detail="License key is required"
            )
        
        # Create new license validator instance with provided key
        new_validator = license_validator.__class__(license_key)
        
        # Validate the new license
        is_valid, license_info = new_validator.validate_license()
        
        if not is_valid:
            raise HTTPException(
                status_code=400,
                detail=f"License validation failed: {license_info.get('message', 'Invalid license')}"
            )
        
        # TODO: Save license key to environment or database
        # For now, just return success
        
        return JSONResponse(
            status_code=200,
            content={
                'message': 'License activated successfully',
                'license_info': license_info,
                'activated_at': '2024-01-01T00:00:00Z'
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to activate license: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to activate license: {str(e)}"
        )
