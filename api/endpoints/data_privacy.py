"""
Data Privacy API Endpoints
Data masking, anonymization, retention policies, access logging, and breach detection
"""

import os
import sys
import logging
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime, timedelta
import hashlib
import json

# Add root directory to Python path
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(root_dir)

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/privacy", tags=["Data Privacy"])

# Pydantic models
class DataMaskingRequest(BaseModel):
    data: Dict[str, Any]
    fields_to_mask: List[str]
    masking_method: str = "partial"  # 'partial', 'full', 'hash', 'tokenize'

class DataMaskingResponse(BaseModel):
    masked_data: Dict[str, Any]
    masked_fields: List[str]
    masking_method: str
    timestamp: str

class DataRetentionRequest(BaseModel):
    data_type: str
    retention_days: int
    action: str  # 'set', 'check', 'purge'

class DataRetentionResponse(BaseModel):
    data_type: str
    retention_days: int
    action: str
    records_affected: int
    status: str
    timestamp: str

class DataAccessLog(BaseModel):
    id: str
    user_id: str
    resource_type: str
    resource_id: str
    action: str  # 'read', 'write', 'delete'
    timestamp: str
    ip_address: str
    user_agent: str
    success: bool

class DataBreachAlert(BaseModel):
    id: str
    severity: str  # 'low', 'medium', 'high', 'critical'
    description: str
    affected_records: int
    detected_at: str
    status: str  # 'open', 'investigating', 'resolved'
    remediation: str

# Mock data access logs
DATA_ACCESS_LOGS = []

# Mock data breach alerts
DATA_BREACH_ALERTS = []

# Data retention policies (in days)
RETENTION_POLICIES = {
    'leads': 365,  # 1 year
    'projects': 1825,  # 5 years
    'assets': 3650,  # 10 years
    'logs': 90,  # 3 months
    'analytics': 365,  # 1 year
    'communications': 730,  # 2 years
    'financial': 2555  # 7 years
}

@router.post("/mask", response_model=DataMaskingResponse)
async def mask_data(request: DataMaskingRequest):
    """
    Mask sensitive data fields
    """
    try:
        masked_data = request.data.copy()
        masked_fields = []
        
        for field in request.fields_to_mask:
            if field in masked_data:
                original_value = masked_data[field]
                
                if request.masking_method == 'full':
                    # Full masking: replace with asterisks
                    if isinstance(original_value, str):
                        masked_data[field] = '*' * len(original_value)
                    else:
                        masked_data[field] = '******'
                
                elif request.masking_method == 'partial':
                    # Partial masking: show first and last characters
                    if isinstance(original_value, str) and len(original_value) > 4:
                        masked_data[field] = original_value[0] + '*' * (len(original_value) - 2) + original_value[-1]
                    else:
                        masked_data[field] = '****'
                
                elif request.masking_method == 'hash':
                    # Hash the value
                    if isinstance(original_value, str):
                        masked_data[field] = hashlib.sha256(original_value.encode()).hexdigest()[:16]
                    else:
                        masked_data[field] = hashlib.sha256(str(original_value).encode()).hexdigest()[:16]
                
                elif request.masking_method == 'tokenize':
                    # Tokenize: replace with random token
                    import uuid
                    masked_data[field] = str(uuid.uuid4())[:8]
                
                masked_fields.append(field)
        
        return DataMaskingResponse(
            masked_data=masked_data,
            masked_fields=masked_fields,
            masking_method=request.masking_method,
            timestamp=datetime.utcnow().isoformat()
        )
    
    except Exception as e:
        logger.error(f"Error masking data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Data masking failed: {str(e)}")

@router.post("/retention", response_model=DataRetentionResponse)
async def manage_data_retention(request: DataRetentionRequest):
    """
    Manage data retention policies
    """
    try:
        records_affected = 0
        status = "success"
        
        if request.action == 'set':
            # Set retention policy
            RETENTION_POLICIES[request.data_type] = request.retention_days
            records_affected = 1
        
        elif request.action == 'check':
            # Check retention policy
            retention_days = RETENTION_POLICIES.get(request.data_type, 365)
            records_affected = 0
        
        elif request.action == 'purge':
            # Purge old data (mock implementation)
            retention_days = RETENTION_POLICIES.get(request.data_type, 365)
            cutoff_date = datetime.utcnow() - timedelta(days=retention_days)
            # Mock: assume 10 records would be purged
            records_affected = 10
        
        return DataRetentionResponse(
            data_type=request.data_type,
            retention_days=RETENTION_POLICIES.get(request.data_type, request.retention_days),
            action=request.action,
            records_affected=records_affected,
            status=status,
            timestamp=datetime.utcnow().isoformat()
        )
    
    except Exception as e:
        logger.error(f"Error managing data retention: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Data retention management failed: {str(e)}")

@router.post("/access-log")
async def log_data_access(
    user_id: str,
    resource_type: str,
    resource_id: str,
    action: str,
    ip_address: str,
    user_agent: str,
    success: bool = True
):
    """
    Log data access for audit trail
    """
    try:
        log_entry = DataAccessLog(
            id=f"LOG-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            user_id=user_id,
            resource_type=resource_type,
            resource_id=resource_id,
            action=action,
            timestamp=datetime.utcnow().isoformat(),
            ip_address=ip_address,
            user_agent=user_agent,
            success=success
        )
        
        DATA_ACCESS_LOGS.append(log_entry)
        
        # Check for suspicious activity
        if not success:
            # Create breach alert for failed access attempts
            alert = DataBreachAlert(
                id=f"ALERT-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
                severity="medium",
                description=f"Failed access attempt by user {user_id} on {resource_type}/{resource_id}",
                affected_records=1,
                detected_at=datetime.utcnow().isoformat(),
                status="open",
                remediation="Review user access permissions and investigate suspicious activity"
            )
            DATA_BREACH_ALERTS.append(alert)
        
        return {
            "log_id": log_entry.id,
            "status": "logged",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Error logging data access: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Data access logging failed: {str(e)}")

@router.get("/access-logs")
async def get_access_logs(
    user_id: Optional[str] = None,
    resource_type: Optional[str] = None,
    limit: int = 50
):
    """
    Get data access logs with optional filters
    """
    try:
        logs = DATA_ACCESS_LOGS
        
        if user_id:
            logs = [log for log in logs if log.user_id == user_id]
        if resource_type:
            logs = [log for log in logs if log.resource_type == resource_type]
        
        return {
            "logs": logs[-limit:],
            "total": len(logs),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Error getting access logs: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get access logs: {str(e)}")

@router.get("/breach-alerts")
async def get_breach_alerts(
    severity: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 50
):
    """
    Get data breach alerts with optional filters
    """
    try:
        alerts = DATA_BREACH_ALERTS
        
        if severity:
            alerts = [alert for alert in alerts if alert.severity == severity]
        if status:
            alerts = [alert for alert in alerts if alert.status == status]
        
        return {
            "alerts": alerts[-limit:],
            "total": len(alerts),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Error getting breach alerts: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get breach alerts: {str(e)}")

@router.put("/breach-alerts/{alert_id}")
async def update_breach_alert(
    alert_id: str,
    status: str,
    remediation: Optional[str] = None
):
    """
    Update breach alert status
    """
    try:
        alert = next((a for a in DATA_BREACH_ALERTS if a.id == alert_id), None)
        
        if not alert:
            raise HTTPException(status_code=404, detail=f"Alert {alert_id} not found")
        
        alert.status = status
        if remediation:
            alert.remediation = remediation
        
        return {
            "alert_id": alert_id,
            "status": status,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating breach alert: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update breach alert: {str(e)}")

@router.get("/retention-policies")
async def get_retention_policies():
    """
    Get all data retention policies
    """
    try:
        return {
            "policies": RETENTION_POLICIES,
            "total": len(RETENTION_POLICIES),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Error getting retention policies: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get retention policies: {str(e)}")

@router.post("/anonymize")
async def anonymize_data(
    data: Dict[str, Any],
    fields_to_anonymize: List[str]
):
    """
    Anonymize data by removing or hashing sensitive fields
    """
    try:
        anonymized_data = data.copy()
        
        for field in fields_to_anonymize:
            if field in anonymized_data:
                # Remove the field completely
                del anonymized_data[field]
        
        return {
            "anonymized_data": anonymized_data,
            "removed_fields": fields_to_anonymize,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Error anonymizing data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Data anonymization failed: {str(e)}")

@router.get("/summary")
async def get_privacy_summary():
    """
    Get data privacy summary
    """
    try:
        total_logs = len(DATA_ACCESS_LOGS)
        open_alerts = len([a for a in DATA_BREACH_ALERTS if a.status == 'open'])
        critical_alerts = len([a for a in DATA_BREACH_ALERTS if a.severity == 'critical'])
        
        return {
            "total_access_logs": total_logs,
            "open_breach_alerts": open_alerts,
            "critical_breach_alerts": critical_alerts,
            "retention_policies_count": len(RETENTION_POLICIES),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Error getting privacy summary: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get privacy summary: {str(e)}")
