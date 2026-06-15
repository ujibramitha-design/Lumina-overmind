"""
Data Protection API
Endpoints for data encryption, masking, and classification
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
import os

router = APIRouter(prefix="/data-protection", tags=["Data Protection"])


class EncryptRequest(BaseModel):
    data: str


class DecryptRequest(BaseModel):
    encrypted_data: str


class MaskRequest(BaseModel):
    data: str
    data_type: str  # email, phone, credit_card, generic


class AnonymizeRequest(BaseModel):
    data: dict
    fields_to_mask: List[str]


class ClassifyRequest(BaseModel):
    field_name: str


@router.post("/encrypt")
async def encrypt_data(request: EncryptRequest):
    """
    Encrypt sensitive data
    """
    from core_modules.data_protection import get_data_protection
    
    encryption_key = os.getenv("DATA_PROTECTION_KEY")
    protector = get_data_protection(encryption_key)
    
    try:
        encrypted = protector.encrypt(request.data)
        return {
            "status": "success",
            "encrypted_data": encrypted
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/decrypt")
async def decrypt_data(request: DecryptRequest):
    """
    Decrypt sensitive data
    """
    from core_modules.data_protection import get_data_protection
    
    encryption_key = os.getenv("DATA_PROTECTION_KEY")
    protector = get_data_protection(encryption_key)
    
    try:
        decrypted = protector.decrypt(request.encrypted_data)
        return {
            "status": "success",
            "decrypted_data": decrypted
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/mask")
async def mask_data(request: MaskRequest):
    """
    Mask sensitive data for display
    """
    from core_modules.data_protection import get_data_protection
    
    protector = get_data_protection()
    
    try:
        if request.data_type == "email":
            masked = protector.mask_email(request.data)
        elif request.data_type == "phone":
            masked = protector.mask_phone(request.data)
        elif request.data_type == "credit_card":
            masked = protector.mask_credit_card(request.data)
        else:
            # Generic masking
            str_value = str(request.data)
            if len(str_value) > 2:
                masked = str_value[0] + '*' * (len(str_value) - 2) + str_value[-1]
            else:
                masked = '*' * len(str_value)
        
        return {
            "status": "success",
            "masked_data": masked,
            "original_length": len(str(request.data))
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/anonymize")
async def anonymize_data(request: AnonymizeRequest):
    """
    Anonymize sensitive fields in a dictionary
    """
    from core_modules.data_protection import get_data_protection
    
    protector = get_data_protection()
    
    try:
        anonymized = protector.anonymize_data(request.data, request.fields_to_mask)
        return {
            "status": "success",
            "anonymized_data": anonymized,
            "masked_fields": request.fields_to_mask
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/classify")
async def classify_field(request: ClassifyRequest):
    """
    Classify a data field by sensitivity level
    """
    from core_modules.data_protection import DataClassification
    
    try:
        classification = DataClassification.classify_field(request.field_name)
        protection = DataClassification.get_protection_level(classification)
        
        return {
            "field_name": request.field_name,
            "classification": classification,
            "protection_requirements": protection
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/classification-levels")
async def get_classification_levels():
    """
    Get all data classification levels and their requirements
    """
    from core_modules.data_protection import DataClassification
    
    levels = {
        "public": DataClassification.get_protection_level(DataClassification.PUBLIC),
        "internal": DataClassification.get_protection_level(DataClassification.INTERNAL),
        "confidential": DataClassification.get_protection_level(DataClassification.CONFIDENTIAL),
        "restricted": DataClassification.get_protection_level(DataClassification.RESTRICTED)
    }
    
    return {
        "classification_levels": levels
    }


@router.post("/hash")
async def hash_data(request: EncryptRequest):
    """
    Hash data for verification (one-way)
    """
    from core_modules.data_protection import get_data_protection
    
    protector = get_data_protection()
    
    try:
        hashed = protector.hash_data(request.data)
        return {
            "status": "success",
            "hash": hashed,
            "algorithm": "SHA-256"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-token")
async def generate_token(length: int = 32):
    """
    Generate a secure random token
    """
    from core_modules.data_protection import get_data_protection
    
    protector = get_data_protection()
    
    try:
        token = protector.generate_token(length)
        return {
            "status": "success",
            "token": token,
            "length": length
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
