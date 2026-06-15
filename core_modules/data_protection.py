"""
Data Protection Module
Provides encryption, masking, and data protection utilities
"""

import hashlib
import secrets
import json
from typing import Any, Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import re


class DataProtection:
    """Data protection utilities for encryption and masking"""
    
    def __init__(self, encryption_key: Optional[str] = None):
        """
        Initialize data protection
        
        Args:
            encryption_key: Optional encryption key. If not provided, generates one.
        """
        if encryption_key:
            self.key = self._derive_key(encryption_key)
        else:
            self.key = Fernet.generate_key()
        
        self.cipher = Fernet(self.key)
    
    def _derive_key(self, password: str, salt: bytes = b'lumina_salt') -> bytes:
        """Derive encryption key from password"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def encrypt(self, data: str) -> str:
        """
        Encrypt sensitive data
        
        Args:
            data: Plain text data to encrypt
            
        Returns:
            Encrypted data as base64 string
        """
        encrypted = self.cipher.encrypt(data.encode())
        return base64.urlsafe_b64encode(encrypted).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """
        Decrypt sensitive data
        
        Args:
            encrypted_data: Encrypted data as base64 string
            
        Returns:
            Decrypted plain text
        """
        encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode())
        decrypted = self.cipher.decrypt(encrypted_bytes)
        return decrypted.decode()
    
    def hash_data(self, data: str) -> str:
        """
        Hash data for verification (one-way)
        
        Args:
            data: Data to hash
            
        Returns:
            SHA-256 hash
        """
        return hashlib.sha256(data.encode()).hexdigest()
    
    def mask_email(self, email: str) -> str:
        """
        Mask email address for privacy
        
        Args:
            email: Email address to mask
            
        Returns:
            Masked email (e.g., j***@example.com)
        """
        if '@' not in email:
            return email
        
        local, domain = email.split('@', 1)
        masked_local = local[0] + '*' * (len(local) - 1) if len(local) > 1 else '*'
        return f"{masked_local}@{domain}"
    
    def mask_phone(self, phone: str) -> str:
        """
        Mask phone number for privacy
        
        Args:
            phone: Phone number to mask
            
        Returns:
            Masked phone (e.g., +62***1234)
        """
        # Remove non-numeric characters
        cleaned = re.sub(r'[^\d+]', '', phone)
        
        if len(cleaned) <= 4:
            return '*' * len(cleaned)
        
        # Show first 2 and last 2 digits
        return cleaned[:2] + '*' * (len(cleaned) - 4) + cleaned[-2:]
    
    def mask_credit_card(self, card: str) -> str:
        """
        Mask credit card number
        
        Args:
            card: Credit card number to mask
            
        Returns:
            Masked card (e.g., ****1234)
        """
        cleaned = re.sub(r'[^\d]', '', card)
        
        if len(cleaned) <= 4:
            return '*' * len(cleaned)
        
        return '*' * (len(cleaned) - 4) + cleaned[-4:]
    
    def anonymize_data(self, data: dict, fields_to_mask: list[str]) -> dict:
        """
        Anonymize sensitive fields in a dictionary
        
        Args:
            data: Dictionary containing data
            fields_to_mask: List of field names to mask
            
        Returns:
            Dictionary with masked fields
        """
        result = data.copy()
        
        for field in fields_to_mask:
            if field in result:
                value = result[field]
                
                # Apply appropriate masking based on field name
                if 'email' in field.lower():
                    result[field] = self.mask_email(str(value))
                elif 'phone' in field.lower() or 'mobile' in field.lower():
                    result[field] = self.mask_phone(str(value))
                elif 'card' in field.lower() or 'credit' in field.lower():
                    result[field] = self.mask_credit_card(str(value))
                else:
                    # Generic masking
                    str_value = str(value)
                    if len(str_value) > 2:
                        result[field] = str_value[0] + '*' * (len(str_value) - 2) + str_value[-1]
                    else:
                        result[field] = '*' * len(str_value)
        
        return result
    
    def generate_token(self, length: int = 32) -> str:
        """
        Generate secure random token
        
        Args:
            length: Token length in bytes
            
        Returns:
            Hex-encoded token
        """
        return secrets.token_hex(length)
    
    def verify_hash(self, data: str, hash_value: str) -> bool:
        """
        Verify data against hash
        
        Args:
            data: Original data
            hash_value: Hash to verify against
            
        Returns:
            True if hash matches
        """
        return self.hash_data(data) == hash_value


class DataClassification:
    """Data classification for sensitivity levels"""
    
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"
    
    @staticmethod
    def classify_field(field_name: str) -> str:
        """
        Classify a field based on its name
        
        Args:
            field_name: Name of the field
            
        Returns:
            Classification level
        """
        field_lower = field_name.lower()
        
        # Restricted data
        if any(keyword in field_lower for keyword in ['password', 'secret', 'token', 'key', 'api_key']):
            return DataClassification.RESTRICTED
        
        # Confidential data
        if any(keyword in field_lower for keyword in ['email', 'phone', 'mobile', 'address', 'ssn', 'nik']):
            return DataClassification.CONFIDENTIAL
        
        # Internal data
        if any(keyword in field_lower for keyword in ['notes', 'comments', 'internal', 'admin']):
            return DataClassification.INTERNAL
        
        # Public data
        return DataClassification.PUBLIC
    
    @staticmethod
    def get_protection_level(classification: str) -> dict:
        """
        Get protection requirements for classification level
        
        Args:
            classification: Classification level
            
        Returns:
            Dictionary with protection requirements
        """
        protections = {
            DataClassification.PUBLIC: {
                'encryption': False,
                'access_control': False,
                'audit_logging': False,
                'retention_days': 365 * 10
            },
            DataClassification.INTERNAL: {
                'encryption': False,
                'access_control': True,
                'audit_logging': True,
                'retention_days': 365 * 7
            },
            DataClassification.CONFIDENTIAL: {
                'encryption': True,
                'access_control': True,
                'audit_logging': True,
                'retention_days': 365 * 5
            },
            DataClassification.RESTRICTED: {
                'encryption': True,
                'access_control': True,
                'audit_logging': True,
                'retention_days': 365 * 2
            }
        }
        
        return protections.get(classification, protections[DataClassification.PUBLIC])


# Singleton instance
_data_protection_instance: Optional[DataProtection] = None


def get_data_protection(encryption_key: Optional[str] = None) -> DataProtection:
    """Get or create data protection instance"""
    global _data_protection_instance
    
    if _data_protection_instance is None:
        _data_protection_instance = DataProtection(encryption_key)
    
    return _data_protection_instance
