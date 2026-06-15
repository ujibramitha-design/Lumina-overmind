"""
Cross-Border Data Compliance API
Endpoints for cross-border data transfer compliance for Asia markets
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime

router = APIRouter(prefix="/cross-border", tags=["Cross-Border Compliance"])


class DataTransferRequest(BaseModel):
    data_type: str  # personal_data, financial_data, health_data
    source_country: str
    destination_country: str
    data_volume: int  # in bytes
    purpose: str  # business_transfer, analytics, backup


class ComplianceCheckRequest(BaseModel):
    data_type: str
    source_country: str
    destination_country: str
    transfer_purpose: str


class DataTransferLog(BaseModel):
    transfer_id: str
    data_type: str
    source_country: str
    destination_country: str
    data_volume: int
    purpose: str
    consent_obtained: bool
    encryption_used: bool
    timestamp: datetime


# Asia market data transfer regulations
ASIA_DATA_TRANSFER_RULES = {
    "Indonesia": {
        "requires_consent": True,
        "data_localization": True,
        "allowed_destinations": ["Indonesia", "Singapore", "Malaysia"],
        "sensitive_data_types": ["personal_data", "financial_data", "health_data"],
        "regulation": "UU PDP (Personal Data Protection Law)"
    },
    "Singapore": {
        "requires_consent": True,
        "data_localization": False,
        "allowed_destinations": ["Singapore", "Malaysia", "Indonesia", "Thailand"],
        "sensitive_data_types": ["personal_data", "financial_data"],
        "regulation": "PDPA (Personal Data Protection Act)"
    },
    "Malaysia": {
        "requires_consent": True,
        "data_localization": False,
        "allowed_destinations": ["Malaysia", "Singapore", "Indonesia"],
        "sensitive_data_types": ["personal_data", "financial_data"],
        "regulation": "PDPA (Personal Data Protection Act)"
    },
    "Thailand": {
        "requires_consent": True,
        "data_localization": False,
        "allowed_destinations": ["Thailand", "Singapore", "Malaysia"],
        "sensitive_data_types": ["personal_data", "financial_data", "health_data"],
        "regulation": "PDPA (Personal Data Protection Act)"
    },
    "Vietnam": {
        "requires_consent": True,
        "data_localization": True,
        "allowed_destinations": ["Vietnam"],
        "sensitive_data_types": ["personal_data", "financial_data"],
        "regulation": "Decree on Personal Data Protection"
    },
    "Philippines": {
        "requires_consent": True,
        "data_localization": False,
        "allowed_destinations": ["Philippines", "Singapore", "Malaysia"],
        "sensitive_data_types": ["personal_data", "financial_data", "health_data"],
        "regulation": "Data Privacy Act"
    }
}


@router.get("/regulations")
async def get_data_transfer_regulations():
    """
    Get data transfer regulations for Asia markets
    """
    return {
        "regulations": ASIA_DATA_TRANSFER_RULES,
        "count": len(ASIA_DATA_TRANSFER_RULES)
    }


@router.get("/regulations/{country}")
async def get_country_regulations(country: str):
    """
    Get data transfer regulations for a specific country
    """
    country_key = country.capitalize()
    
    if country_key not in ASIA_DATA_TRANSFER_RULES:
        raise HTTPException(status_code=404, detail=f"Regulations not found for {country}")
    
    return {
        "country": country,
        "regulations": ASIA_DATA_TRANSFER_RULES[country_key]
    }


@router.post("/check-compliance")
async def check_transfer_compliance(request: ComplianceCheckRequest):
    """
    Check if data transfer is compliant with regulations
    """
    source_rules = ASIA_DATA_TRANSFER_RULES.get(request.source_country.capitalize())
    dest_rules = ASIA_DATA_TRANSFER_RULES.get(request.destination_country.capitalize())
    
    if not source_rules:
        raise HTTPException(status_code=400, detail=f"Unknown source country: {request.source_country}")
    
    if not dest_rules:
        raise HTTPException(status_code=400, detail=f"Unknown destination country: {request.destination_country}")
    
    compliance_issues = []
    is_compliant = True
    
    # Check if destination is allowed
    if request.destination_country.capitalize() not in source_rules["allowed_destinations"]:
        is_compliant = False
        compliance_issues.append({
            "issue": "Destination not in allowed list",
            "allowed_destinations": source_rules["allowed_destinations"]
        })
    
    # Check if consent is required
    if source_rules["requires_consent"]:
        compliance_issues.append({
            "issue": "Consent required",
            "action": "Obtain explicit consent from data subject"
        })
    
    # Check data localization
    if source_rules["data_localization"] and request.destination_country != request.source_country:
        is_compliant = False
        compliance_issues.append({
            "issue": "Data localization requirement",
            "action": "Data must remain within country borders"
        })
    
    # Check if data type is sensitive
    if request.data_type in source_rules["sensitive_data_types"]:
        compliance_issues.append({
            "issue": "Sensitive data type",
            "action": "Apply additional security measures"
        })
    
    return {
        "is_compliant": is_compliant,
        "compliance_issues": compliance_issues,
        "source_regulation": source_rules["regulation"],
        "destination_regulation": dest_rules["regulation"]
    }


@router.post("/log-transfer")
async def log_data_transfer(request: DataTransferRequest):
    """
    Log a cross-border data transfer for audit purposes
    """
    transfer_id = f"transfer-{datetime.utcnow().timestamp()}"
    
    # TODO: Store in database
    transfer_log = {
        "transfer_id": transfer_id,
        "data_type": request.data_type,
        "source_country": request.source_country,
        "destination_country": request.destination_country,
        "data_volume": request.data_volume,
        "purpose": request.purpose,
        "consent_obtained": False,  # Would be verified
        "encryption_used": True,  # Assume encryption is used
        "timestamp": datetime.utcnow().isoformat()
    }
    
    return {
        "status": "success",
        "transfer_id": transfer_id,
        "log": transfer_log
    }


@router.get("/transfer-logs")
async def get_transfer_logs(
    source_country: Optional[str] = None,
    destination_country: Optional[str] = None,
    limit: int = 100
):
    """
    Get cross-border data transfer logs
    """
    # TODO: Retrieve from database
    return {
        "logs": [],
        "filters": {
            "source_country": source_country,
            "destination_country": destination_country,
            "limit": limit
        }
    }


@router.get("/transfer-logs/{transfer_id}")
async def get_transfer_log(transfer_id: str):
    """
    Get specific transfer log
    """
    # TODO: Retrieve from database
    return {
        "transfer_id": transfer_id,
        "status": "not_found"
    }


@router.post("/data-localization-check")
async def check_data_localization(country: str, data_type: str):
    """
    Check if data must be localized within country
    """
    rules = ASIA_DATA_TRANSFER_RULES.get(country.capitalize())
    
    if not rules:
        raise HTTPException(status_code=400, detail=f"Unknown country: {country}")
    
    is_sensitive = data_type in rules["sensitive_data_types"]
    requires_localization = rules["data_localization"] and is_sensitive
    
    return {
        "country": country,
        "data_type": data_type,
        "is_sensitive": is_sensitive,
        "requires_localization": requires_localization,
        "regulation": rules["regulation"]
    }


@router.get("/allowed-destinations/{source_country}")
async def get_allowed_destinations(source_country: str):
    """
    Get allowed destination countries for data transfer
    """
    rules = ASIA_DATA_TRANSFER_RULES.get(source_country.capitalize())
    
    if not rules:
        raise HTTPException(status_code=400, detail=f"Unknown source country: {source_country}")
    
    return {
        "source_country": source_country,
        "allowed_destinations": rules["allowed_destinations"],
        "regulation": rules["regulation"]
    }


@router.post("/consent-template")
async def get_consent_template(
    data_type: str,
    source_country: str,
    destination_country: str
):
    """
    Get consent template for cross-border data transfer
    """
    template = f"""
CROSS-BORDER DATA TRANSFER CONSENT

I hereby consent to the transfer of my {data_type} from {source_country} to {destination_country}.

Purpose of Transfer: Business operations and analytics

Rights:
- I have the right to withdraw this consent at any time
- I have the right to access my data
- I have the right to request deletion of my data

Data Protection:
- Data will be encrypted during transfer
- Data will be stored securely in the destination country
- Data will only be used for the stated purpose

By signing below, I acknowledge that I have read and understood this consent form.

Date: _______________
Signature: _______________
"""
    
    return {
        "template": template,
        "data_type": data_type,
        "source_country": source_country,
        "destination_country": destination_country
    }
