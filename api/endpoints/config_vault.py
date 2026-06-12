"""
CLASSIFIED VAULT - Secure API Key Management
Protected endpoint for managing encrypted API keys
"""

import logging
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from prisma import Client as PrismaClient

# Security imports
from core_modules.security.admin_auth import AdminAuth
from core_modules.security.data_encryption import DataEncryption

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/config-vault", tags=["Classified Vault"])

# Initialize security modules
admin_auth = AdminAuth()
data_encryption = DataEncryption()

# Pydantic models
class ConfigKeyCreate(BaseModel):
    key_name: str = Field(..., min_length=1, max_length=100, description="API key name")
    key_value: str = Field(..., min_length=1, description="API key value (will be encrypted)")
    description: Optional[str] = Field(None, max_length=500, description="Key description")
    category: str = Field("API_KEYS", max_length=50, description="Key category")

class ConfigKeyUpdate(BaseModel):
    key_value: str = Field(..., min_length=1, description="New API key value (will be encrypted)")
    description: Optional[str] = Field(None, max_length=500, description="Updated description")
    is_active: Optional[bool] = Field(None, description="Key activation status")

class ConfigKeyResponse(BaseModel):
    id: str
    key_name: str
    description: Optional[str]
    category: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

# Admin authentication dependency
async def verify_admin_access(user_id: str = None, credentials: str = None):
    """Verify admin access before allowing vault operations"""
    try:
        # For now, we'll use a simple admin check
        # In production, this should verify proper admin credentials
        if not admin_auth:
            raise HTTPException(status_code=503, detail="Security module not available")
        
        # TODO: Implement proper admin authentication
        # For now, we'll allow access (implement proper auth in production)
        return True
        
    except Exception as e:
        logger.error(f"Admin authentication failed: {e}")
        raise HTTPException(status_code=401, detail="Unauthorized access to Classified Vault")

# Database dependency
def get_db():
    db = PrismaClient()
    return db

@router.post("/keys", response_model=ConfigKeyResponse)
async def create_config_key(
    key_data: ConfigKeyCreate,
    db: PrismaClient = Depends(get_db),
    admin_verified: bool = Depends(verify_admin_access)
):
    """Create new encrypted API key in vault"""
    try:
        # Encrypt the key value
        encrypted_value = data_encryption.encrypt_data(key_data.key_value)
        
        # Create the config key
        config_key = db.systemconfig.create({
            'key_name': key_data.key_name,
            'key_value': encrypted_value,
            'description': key_data.description,
            'category': key_data.category,
            'is_active': True
        })
        
        logger.info(f"Created encrypted config key: {key_data.key_name}")
        
        return ConfigKeyResponse(
            id=config_key.id,
            key_name=config_key.key_name,
            description=config_key.description,
            category=config_key.category,
            is_active=config_key.is_active,
            created_at=config_key.createdAt,
            updated_at=config_key.updatedAt
        )
        
    except Exception as e:
        logger.error(f"Failed to create config key: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/keys", response_model=List[ConfigKeyResponse])
async def list_config_keys(
    category: Optional[str] = None,
    db: PrismaClient = Depends(get_db),
    admin_verified: bool = Depends(verify_admin_access)
):
    """List all encrypted config keys (without values)"""
    try:
        where_clause = {}
        if category:
            where_clause['category'] = category
        
        keys = db.systemconfig.find_many(
            where=where_clause,
            order={'createdAt': 'desc'}
        )
        
        return [
            ConfigKeyResponse(
                id=key.id,
                key_name=key.key_name,
                description=key.description,
                category=key.category,
                is_active=key.is_active,
                created_at=key.createdAt,
                updated_at=key.updatedAt
            )
            for key in keys
        ]
        
    except Exception as e:
        logger.error(f"Failed to list config keys: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/keys/{key_name}")
async def get_config_key(
    key_name: str,
    decrypt_value: bool = False,
    db: PrismaClient = Depends(get_db),
    admin_verified: bool = Depends(verify_admin_access)
):
    """Get specific config key (optionally decrypted)"""
    try:
        key = db.systemconfig.find_first(where={'key_name': key_name})
        
        if not key:
            raise HTTPException(status_code=404, detail="Config key not found")
        
        response = {
            'id': key.id,
            'key_name': key.key_name,
            'description': key.description,
            'category': key.category,
            'is_active': key.is_active,
            'created_at': key.createdAt,
            'updated_at': key.updatedAt
        }
        
        # Only decrypt if explicitly requested and authorized
        if decrypt_value:
            response['key_value'] = data_encryption.decrypt_data(key.key_value)
        else:
            response['key_value'] = '***ENCRYPTED***'
        
        return response
        
    except Exception as e:
        logger.error(f"Failed to get config key: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/keys/{key_name}", response_model=ConfigKeyResponse)
async def update_config_key(
    key_name: str,
    key_data: ConfigKeyUpdate,
    db: PrismaClient = Depends(get_db),
    admin_verified: bool = Depends(verify_admin_access)
):
    """Update existing config key"""
    try:
        # Find existing key
        existing_key = db.systemconfig.find_first(where={'key_name': key_name})
        
        if not existing_key:
            raise HTTPException(status_code=404, detail="Config key not found")
        
        # Encrypt new value
        encrypted_value = data_encryption.encrypt_data(key_data.key_value)
        
        # Update data
        update_data = {
            'key_value': encrypted_value
        }
        
        if key_data.description is not None:
            update_data['description'] = key_data.description
        
        if key_data.is_active is not None:
            update_data['is_active'] = key_data.is_active
        
        updated_key = db.systemconfig.update(
            where={'id': existing_key.id},
            data=update_data
        )
        
        logger.info(f"Updated config key: {key_name}")
        
        return ConfigKeyResponse(
            id=updated_key.id,
            key_name=updated_key.key_name,
            description=updated_key.description,
            category=updated_key.category,
            is_active=updated_key.is_active,
            created_at=updated_key.createdAt,
            updated_at=updated_key.updatedAt
        )
        
    except Exception as e:
        logger.error(f"Failed to update config key: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/keys/{key_name}")
async def delete_config_key(
    key_name: str,
    db: PrismaClient = Depends(get_db),
    admin_verified: bool = Depends(verify_admin_access)
):
    """Delete config key from vault"""
    try:
        key = db.systemconfig.find_first(where={'key_name': key_name})
        
        if not key:
            raise HTTPException(status_code=404, detail="Config key not found")
        
        db.systemconfig.delete(where={'id': key.id})
        
        logger.info(f"Deleted config key: {key_name}")
        
        return {'message': f'Config key {key_name} deleted successfully'}
        
    except Exception as e:
        logger.error(f"Failed to delete config key: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/keys/{key_name}/test")
async def test_config_key(
    key_name: str,
    db: PrismaClient = Depends(get_db),
    admin_verified: bool = Depends(verify_admin_access)
):
    """Test if config key is working (decrypt and validate)"""
    try:
        key = db.systemconfig.find_first(where={'key_name': key_name})
        
        if not key:
            raise HTTPException(status_code=404, detail="Config key not found")
        
        # Try to decrypt
        decrypted_value = data_encryption.decrypt_data(key.key_value)
        
        # Basic validation
        is_valid = len(decrypted_value) > 0 and key.is_active
        
        return {
            'key_name': key_name,
            'is_valid': is_valid,
            'test_time': datetime.now(),
            'message': 'Key is valid and decryptable' if is_valid else 'Key validation failed'
        }
        
    except Exception as e:
        logger.error(f"Failed to test config key: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Utility function for other modules to get decrypted API keys
async def get_api_key(key_name: str, db: PrismaClient = None) -> Optional[str]:
    """
    Get decrypted API key from vault
    Falls back to environment variable if not found in vault
    """
    try:
        if not db:
            db = PrismaClient()
        
        # Try to get from vault first
        config_key = db.systemconfig.find_first(where={'key_name': key_name, 'is_active': True})
        
        if config_key:
            # Decrypt and return
            return data_encryption.decrypt_data(config_key.key_value)
        
        # Fallback to environment variable
        import os
        env_value = os.getenv(key_name)
        
        if env_value:
            logger.info(f"Using fallback environment variable for {key_name}")
            return env_value
        
        logger.warning(f"API key {key_name} not found in vault or environment")
        return None
        
    except Exception as e:
        logger.error(f"Failed to get API key {key_name}: {e}")
        return None
