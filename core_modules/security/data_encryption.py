"""
LUMINA OS - Data Encryption & Privacy Protection
Enterprise-grade encryption for sensitive data (phone numbers, PII)
"""

import os
import logging
import base64
from typing import Optional, Dict, Any
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataEncryption:
    """
    Enterprise-grade data encryption system
    Implements symmetric encryption for sensitive data storage
    """
    
    def __init__(self):
        """Initialize data encryption system"""
        self.logger = logging.getLogger(__name__)
        
        # Load encryption key from environment
        self.encryption_key = self._load_encryption_key()
        
        # Initialize cipher
        self.cipher = Fernet(self.encryption_key)
        
        self.logger.info("🔐 Data Encryption initialized")
        self.logger.info("🔑 Encryption key loaded from environment")
    
    def _load_encryption_key(self) -> bytes:
        """
        Load or generate encryption key
        
        Returns:
            Encryption key bytes
        """
        try:
            # Try to load from environment
            key_env = os.getenv("ENCRYPTION_KEY")
            if key_env:
                # Decode base64 key from environment
                return base64.urlsafe_b64decode(key_env.encode())
            
            # Generate new key if not exists
            self.logger.warning("⚠️ ENCRYPTION_KEY not found in environment, generating new key")
            key = Fernet.generate_key()
            
            # Save key to environment (for development only)
            key_b64 = base64.urlsafe_b64encode(key).decode()
            self.logger.info(f"🔑 Generated new encryption key: {key_b64}")
            self.logger.info("⚠️ Add this to your .env file: ENCRYPTION_KEY=" + key_b64)
            
            return key
            
        except Exception as e:
            self.logger.error(f"❌ Failed to load encryption key: {e}")
            # Fallback to generated key
            return Fernet.generate_key()
    
    def encrypt_sensitive_data(self, data: str) -> str:
        """
        Encrypt sensitive data
        
        Args:
            data: Plain text data to encrypt
            
        Returns:
            Encrypted data (base64 encoded)
        """
        try:
            if not data:
                return ""
            
            # Convert to bytes
            data_bytes = data.encode('utf-8')
            
            # Encrypt
            encrypted_data = self.cipher.encrypt(data_bytes)
            
            # Return base64 encoded string
            return base64.urlsafe_b64encode(encrypted_data).decode('utf-8')
            
        except Exception as e:
            self.logger.error(f"❌ Data encryption failed: {e}")
            return ""
    
    def decrypt_sensitive_data(self, encrypted_data: str) -> str:
        """
        Decrypt sensitive data
        
        Args:
            encrypted_data: Base64 encoded encrypted data
            
        Returns:
            Decrypted plain text data
        """
        try:
            if not encrypted_data:
                return ""
            
            # Decode from base64
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode('utf-8'))
            
            # Decrypt
            decrypted_data = self.cipher.decrypt(encrypted_bytes)
            
            # Return as string
            return decrypted_data.decode('utf-8')
            
        except Exception as e:
            self.logger.error(f"❌ Data decryption failed: {e}")
            return ""
    
    def encrypt_phone_number(self, phone: str) -> str:
        """
        Encrypt phone number with additional validation
        
        Args:
            phone: Phone number to encrypt
            
        Returns:
            Encrypted phone number
        """
        try:
            # Normalize phone number first
            normalized_phone = self._normalize_phone_number(phone)
            
            if not normalized_phone:
                return ""
            
            # Encrypt
            return self.encrypt_sensitive_data(normalized_phone)
            
        except Exception as e:
            self.logger.error(f"❌ Phone encryption failed: {e}")
            return ""
    
    def decrypt_phone_number(self, encrypted_phone: str) -> str:
        """
        Decrypt phone number
        
        Args:
            encrypted_phone: Encrypted phone number
            
        Returns:
            Decrypted phone number
        """
        try:
            # Decrypt
            decrypted = self.decrypt_sensitive_data(encrypted_phone)
            
            # Validate decrypted phone
            return self._validate_phone_number(decrypted)
            
        except Exception as e:
            self.logger.error(f"❌ Phone decryption failed: {e}")
            return ""
    
    def encrypt_email(self, email: str) -> str:
        """
        Encrypt email address
        
        Args:
            email: Email address to encrypt
            
        Returns:
            Encrypted email address
        """
        try:
            # Validate and normalize email
            normalized_email = self._normalize_email(email)
            
            if not normalized_email:
                return ""
            
            # Encrypt
            return self.encrypt_sensitive_data(normalized_email)
            
        except Exception as e:
            self.logger.error(f"❌ Email encryption failed: {e}")
            return ""
    
    def decrypt_email(self, encrypted_email: str) -> str:
        """
        Decrypt email address
        
        Args:
            encrypted_email: Encrypted email address
            
        Returns:
            Decrypted email address
        """
        try:
            # Decrypt
            decrypted = self.decrypt_sensitive_data(encrypted_email)
            
            # Validate decrypted email
            return self._validate_email(decrypted)
            
        except Exception as e:
            self.logger.error(f"❌ Email decryption failed: {e}")
            return ""
    
    def encrypt_pii_data(self, pii_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Encrypt PII data dictionary
        
        Args:
            pii_data: Dictionary with PII data
            
        Returns:
            Dictionary with encrypted PII data
        """
        try:
            encrypted_data = {}
            
            for key, value in pii_data.items():
                if isinstance(value, str) and value.strip():
                    # Encrypt string values
                    if key in ['phone', 'whatsapp', 'contact_phone']:
                        encrypted_data[key] = self.encrypt_phone_number(value)
                    elif key in ['email', 'email_address']:
                        encrypted_data[key] = self.encrypt_email(value)
                    else:
                        encrypted_data[key] = self.encrypt_sensitive_data(value)
                else:
                    encrypted_data[key] = value
            
            return encrypted_data
            
        except Exception as e:
            self.logger.error(f"❌ PII encryption failed: {e}")
            return pii_data
    
    def decrypt_pii_data(self, encrypted_pii_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Decrypt PII data dictionary
        
        Args:
            encrypted_pii_data: Dictionary with encrypted PII data
            
        Returns:
            Dictionary with decrypted PII data
        """
        try:
            decrypted_data = {}
            
            for key, value in encrypted_pii_data.items():
                if isinstance(value, str) and value.strip():
                    # Decrypt string values
                    if key in ['phone', 'whatsapp', 'contact_phone']:
                        decrypted_data[key] = self.decrypt_phone_number(value)
                    elif key in ['email', 'email_address']:
                        decrypted_data[key] = self.decrypt_email(value)
                    else:
                        decrypted_data[key] = self.decrypt_sensitive_data(value)
                else:
                    decrypted_data[key] = value
            
            return decrypted_data
            
        except Exception as e:
            self.logger.error(f"❌ PII decryption failed: {e}")
            return encrypted_pii_data
    
    def _normalize_phone_number(self, phone: str) -> str:
        """Normalize phone number to international format"""
        try:
            if not phone:
                return ""
            
            # Remove all non-digit characters
            digits_only = ''.join(filter(str.isdigit, phone))
            
            # Handle Indonesian phone numbers
            if digits_only.startswith('62'):
                # Already has country code
                if len(digits_only) >= 10 and len(digits_only) <= 13:
                    return '+' + digits_only
            elif digits_only.startswith('0'):
                # Remove leading zero and add country code
                if len(digits_only) >= 9 and len(digits_only) <= 12:
                    return '+62' + digits_only[1:]
            
            return ""
            
        except Exception:
            return ""
    
    def _validate_phone_number(self, phone: str) -> str:
        """Validate decrypted phone number"""
        try:
            if not phone:
                return ""
            
            # Basic validation
            if phone.startswith('+62') and len(phone) >= 12 and len(phone) <= 15:
                return phone
            
            return ""
            
        except Exception:
            return ""
    
    def _normalize_email(self, email: str) -> str:
        """Normalize email address"""
        try:
            if not email:
                return ""
            
            # Basic normalization
            email = email.strip().lower()
            
            # Basic validation
            if '@' in email and '.' in email.split('@')[-1]:
                return email
            
            return ""
            
        except Exception:
            return ""
    
    def _validate_email(self, email: str) -> str:
        """Validate decrypted email"""
        try:
            if not email:
                return ""
            
            # Basic validation
            if '@' in email and '.' in email.split('@')[-1]:
                return email
            
            return ""
            
        except Exception:
            return ""
    
    def generate_encryption_key(self) -> str:
        """
        Generate new encryption key
        
        Returns:
            Base64 encoded encryption key
        """
        try:
            key = Fernet.generate_key()
            key_b64 = base64.urlsafe_b64encode(key).decode()
            
            self.logger.info(f"🔑 Generated new encryption key: {key_b64}")
            self.logger.info("⚠️ Update your .env file with: ENCRYPTION_KEY=" + key_b64)
            
            return key_b64
            
        except Exception as e:
            self.logger.error(f"❌ Failed to generate encryption key: {e}")
            return ""
    
    def rotate_encryption_key(self) -> bool:
        """
        Rotate encryption key (for maintenance)
        
        Returns:
            True if successful
        """
        try:
            # Generate new key
            new_key_b64 = self.generate_encryption_key()
            
            # Update cipher
            new_key = base64.urlsafe_b64decode(new_key_b64.encode())
            self.cipher = Fernet(new_key)
            self.encryption_key = new_key
            
            self.logger.info("🔄 Encryption key rotated successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Key rotation failed: {e}")
            return False
    
    def get_encryption_stats(self) -> Dict[str, Any]:
        """Get encryption system statistics"""
        try:
            return {
                "cipher_algorithm": "Fernet (AES-128-CBC)",
                "key_length": len(self.encryption_key) * 8,  # bytes to bits
                "supports_rotation": True,
                "encryption_method": "symmetric",
                "key_storage": "environment_variable"
            }
            
        except Exception as e:
            self.logger.error(f"❌ Failed to get encryption stats: {e}")
            return {}

# Global data encryption instance
data_encryption = DataEncryption()
