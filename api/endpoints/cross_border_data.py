"""
Cross-Border Data Transfer API Endpoints
Data residency compliance, cross-border encryption, and regional data centers
"""

import os
import sys
import logging
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime

# Add root directory to Python path
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(root_dir)

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/cross-border", tags=["Cross-Border Data"])

# Pydantic models
class DataTransferRequest(BaseModel):
    source_region: str  # 'indonesia', 'singapore', 'japan', etc.
    target_region: str
    data_type: str  # 'leads', 'projects', 'users', 'analytics'
    data_volume: int  # in MB
    encryption_required: bool = True
    compliance_check: bool = True

class DataTransferResponse(BaseModel):
    transfer_id: str
    status: str  # 'approved', 'pending', 'rejected'
    source_region: str
    target_region: str
    data_type: str
    data_volume: int
    encryption_status: str
    compliance_status: str
    estimated_time: str
    restrictions: List[str]
    timestamp: str

class DataResidencyCheckRequest(BaseModel):
    region: str
    data_type: str

class DataResidencyCheckResponse(BaseModel):
    region: str
    data_type: str
    residency_compliant: bool
    data_location: str
    restrictions: List[str]
    recommendations: List[str]
    timestamp: str

class RegionalDataCenterInfo(BaseModel):
    region: str
    data_center: str
    location: str
    compliance_standards: List[str]
    available: bool
    latency: str  # in ms

# Regional data centers configuration
REGIONAL_DATA_CENTERS = {
    'indonesia': {
        'data_center': 'AWS Jakarta',
        'location': 'Jakarta, Indonesia',
        'compliance_standards': ['PDPA', 'GDPR', 'ISO 27001'],
        'available': True,
        'latency': '5-10ms'
    },
    'singapore': {
        'data_center': 'AWS Singapore',
        'location': 'Singapore',
        'compliance_standards': ['PDPA', 'GDPR', 'ISO 27001'],
        'available': True,
        'latency': '10-15ms'
    },
    'japan': {
        'data_center': 'AWS Tokyo',
        'location': 'Tokyo, Japan',
        'compliance_standards': ['APPI', 'GDPR', 'ISO 27001'],
        'available': True,
        'latency': '20-30ms'
    },
    'hong_kong': {
        'data_center': 'AWS Hong Kong',
        'location': 'Hong Kong',
        'compliance_standards': ['PDPO', 'GDPR', 'ISO 27001'],
        'available': True,
        'latency': '15-25ms'
    },
    'uae': {
        'data_center': 'AWS Dubai',
        'location': 'Dubai, UAE',
        'compliance_standards': ['UAE Data Protection Law', 'GDPR', 'ISO 27001'],
        'available': True,
        'latency': '30-40ms'
    }
}

# Cross-border data transfer restrictions
CROSS_BORDER_RESTRICTIONS = {
    'indonesia': {
        'allowed_to': ['singapore', 'japan', 'hong_kong'],
        'restricted_to': ['uae'],
        'requires_approval': ['uae']
    },
    'singapore': {
        'allowed_to': ['indonesia', 'japan', 'hong_kong', 'uae'],
        'restricted_to': [],
        'requires_approval': []
    },
    'japan': {
        'allowed_to': ['indonesia', 'singapore', 'hong_kong'],
        'restricted_to': ['uae'],
        'requires_approval': ['uae']
    },
    'hong_kong': {
        'allowed_to': ['indonesia', 'singapore', 'japan', 'uae'],
        'restricted_to': [],
        'requires_approval': []
    },
    'uae': {
        'allowed_to': ['singapore', 'hong_kong'],
        'restricted_to': ['indonesia', 'japan'],
        'requires_approval': ['indonesia', 'japan']
    }
}

@router.post("/transfer", response_model=DataTransferResponse)
async def initiate_data_transfer(request: DataTransferRequest):
    """
    Initiate cross-border data transfer with compliance check
    """
    try:
        transfer_id = f"TRF-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        
        # Check if transfer is allowed
        restrictions = CROSS_BORDER_RESTRICTIONS.get(request.source_region, {})
        
        if request.target_region in restrictions.get('restricted_to', []):
            return DataTransferResponse(
                transfer_id=transfer_id,
                status='rejected',
                source_region=request.source_region,
                target_region=request.target_region,
                data_type=request.data_type,
                data_volume=request.data_volume,
                encryption_status='N/A',
                compliance_status='non_compliant',
                estimated_time='N/A',
                restrictions=[f'Transfer from {request.source_region} to {request.target_region} is restricted'],
                timestamp=datetime.utcnow().isoformat()
            )
        
        # Check if approval is required
        if request.target_region in restrictions.get('requires_approval', []):
            return DataTransferResponse(
                transfer_id=transfer_id,
                status='pending',
                source_region=request.source_region,
                target_region=request.target_region,
                data_type=request.data_type,
                data_volume=request.data_volume,
                encryption_status='pending',
                compliance_status='approval_required',
                estimated_time='2-3 business days',
                restrictions=[f'Transfer from {request.source_region} to {request.target_region} requires approval'],
                timestamp=datetime.utcnow().isoformat()
            )
        
        # Check compliance if required
        compliance_status = 'compliant'
        if request.compliance_check:
            # Mock compliance check
            compliance_status = 'compliant'
        
        # Check encryption
        encryption_status = 'encrypted' if request.encryption_required else 'unencrypted'
        
        # Calculate estimated time
        estimated_time = f"{request.data_volume // 10 + 1} minutes"
        
        return DataTransferResponse(
            transfer_id=transfer_id,
            status='approved',
            source_region=request.source_region,
            target_region=request.target_region,
            data_type=request.data_type,
            data_volume=request.data_volume,
            encryption_status=encryption_status,
            compliance_status=compliance_status,
            estimated_time=estimated_time,
            restrictions=[],
            timestamp=datetime.utcnow().isoformat()
        )
    
    except Exception as e:
        logger.error(f"Error initiating data transfer: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Data transfer initiation failed: {str(e)}")

@router.post("/residency-check", response_model=DataResidencyCheckResponse)
async def check_data_residency(request: DataResidencyCheckRequest):
    """
    Check data residency compliance for specified region
    """
    try:
        region_info = REGIONAL_DATA_CENTERS.get(request.region)
        
        if not region_info:
            raise HTTPException(status_code=400, detail=f"Invalid region: {request.region}")
        
        # Check residency compliance
        residency_compliant = True
        restrictions = []
        recommendations = []
        
        # Add region-specific recommendations
        if request.region == 'indonesia':
            recommendations.append('Ensure PDPA compliance for Indonesian data')
            recommendations.append('Data must be stored in Indonesia for Indonesian citizens')
        elif request.region == 'uae':
            recommendations.append('Ensure UAE Data Protection Law compliance')
            recommendations.append('Data encryption is mandatory')
        
        return DataResidencyCheckResponse(
            region=request.region,
            data_type=request.data_type,
            residency_compliant=residency_compliant,
            data_location=region_info['location'],
            restrictions=restrictions,
            recommendations=recommendations,
            timestamp=datetime.utcnow().isoformat()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error checking data residency: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Data residency check failed: {str(e)}")

@router.get("/data-centers")
async def get_regional_data_centers():
    """
    Get information about regional data centers
    """
    try:
        data_centers = []
        
        for region, info in REGIONAL_DATA_CENTERS.items():
            data_centers.append(RegionalDataCenterInfo(
                region=region,
                data_center=info['data_center'],
                location=info['location'],
                compliance_standards=info['compliance_standards'],
                available=info['available'],
                latency=info['latency']
            ))
        
        return {
            'data_centers': data_centers,
            'total': len(data_centers),
            'timestamp': datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Error getting data centers: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get data centers: {str(e)}")

@router.get("/restrictions")
async def get_cross_border_restrictions():
    """
    Get cross-border data transfer restrictions
    """
    try:
        return {
            'restrictions': CROSS_BORDER_RESTRICTIONS,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Error getting restrictions: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get restrictions: {str(e)}")

@router.post("/encrypt")
async def encrypt_data_for_transfer(
    data: Dict[str, Any],
    target_region: str
):
    """
    Encrypt data for cross-border transfer
    """
    try:
        # Mock encryption (in production, use actual encryption)
        encryption_method = 'AES-256'
        
        return {
            'status': 'encrypted',
            'encryption_method': encryption_method,
            'target_region': target_region,
            'data_size': len(str(data)),
            'timestamp': datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Error encrypting data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Data encryption failed: {str(e)}")
