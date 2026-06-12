#!/usr/bin/env python3
"""
Data Vault - Advanced Encryption System
Executive Blueprint Lumina OS Security Module

Author: HUNTER_AGENT_AI_MARKETING_DIGITAL
Version: 1.0.0
"""

import os
import logging
from cryptography.fernet import Fernet
from dotenv import load_dotenv, set_key
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
import json
import base64

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ANSI Color Codes for hacker-style logging
GREEN = '\033[92m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
RED = '\033[91m'
MAGENTA = '\033[95m'
BOLD = '\033[1m'
END = '\033[0m'

@dataclass
class EncryptionResult:
    """Data class for encryption/decryption results"""
    success: bool
    data: Optional[str]
    error: Optional[str]
    operation: str
    timestamp: str
    metadata: Dict[str, Any]

class DataVault:
    """
    Advanced data encryption vault for sensitive information protection
    
    This class provides enterprise-grade encryption capabilities for protecting
    sensitive data such as phone numbers, emails, and personal information
    in compliance with Indonesia's Personal Data Protection (PDP) regulations.
    """
    
    def __init__(self):
        """Initialize DataVault with self-healing encryption key management"""
        self.logger = logging.getLogger(__name__)
        
        # Initialize encryption system
        self.fernet = None
        self.encryption_key = None
        self.key_file_path = '.env'
        
        # Encryption metadata
        self.encryption_metadata = {
            'algorithm': 'Fernet (AES-128-CBC)',
            'key_length': 256,  # bits
            'compliance': 'Indonesia PDP Regulation',
            'version': '1.0.0',
            'self_healing': True
        }
        
        print(f"{GREEN}🔐 DATA VAULT INITIALIZATION{END}")
        print(f"{CYAN}├── Security System: Executive Blueprint Lumina OS{END}")
        print(f"{CYAN}├── Compliance: Indonesia PDP Regulation{END}")
        print(f"{CYAN}├── Algorithm: Fernet (AES-128-CBC){END}")
        print(f"{CYAN}├── Self-Healing: Enabled{END}")
        print(f"{CYAN}├── Timestamp: {self._get_timestamp()}{END}")
        
        # Initialize with self-healing capability
        self._initialize_with_self_healing()
        
        print(f"{GREEN}✅ DATA VAULT READY{END}")
        print(f"{CYAN}├── Encryption Key: {'✅ Valid' if self.fernet else '❌ Invalid'}{END}")
        print(f"{CYAN}├── Key Source: {self._get_key_source()}{END}")
        print(f"{CYAN}├── Protection Level: Enterprise{END}")
        print(f"{GREEN}└── Status: Active and Ready{END}")
    
    def _initialize_with_self_healing(self) -> None:
        """
        Self-healing initialization process
        Automatically generates and manages encryption keys
        """
        try:
            # Load existing environment variables
            load_dotenv(self.key_file_path)
            
            # Check for existing encryption key
            encryption_key = os.getenv('ENCRYPTION_KEY')
            
            if encryption_key:
                # Validate existing key
                if self._validate_encryption_key(encryption_key):
                    self.encryption_key = encryption_key.encode()
                    self.fernet = Fernet(self.encryption_key)
                    self.logger.info("🔐 Existing encryption key loaded successfully")
                    print(f"{GREEN}├── Encryption Key: Loaded from existing .env{END}")
                else:
                    # Invalid key detected, regenerate
                    self.logger.warning("⚠️ Invalid encryption key detected, regenerating...")
                    self._regenerate_encryption_key()
            else:
                # No key found, generate new one
                self.logger.info("🔑 No encryption key found, generating new key...")
                self._generate_and_save_encryption_key()
                
        except Exception as e:
            self.logger.error(f"❌ Self-healing initialization failed: {e}")
            print(f"{RED}├── Self-Healing Error: {e}{END}")
            raise RuntimeError(f"DataVault initialization failed: {e}")
    
    def _validate_encryption_key(self, key: str) -> bool:
        """
        Validate encryption key format and functionality
        
        Args:
            key: Encryption key string to validate
            
        Returns:
            True if key is valid, False otherwise
        """
        try:
            # Check key format (should be base64 encoded)
            key_bytes = key.encode()
            
            # Try to decode base64
            try:
                decoded_key = base64.b64decode(key_bytes)
            except Exception:
                return False
            
            # Check key length (should be 32 bytes for Fernet)
            if len(decoded_key) != 32:
                return False
            
            # Test key functionality
            test_fernet = Fernet(key_bytes)
            test_data = b"test_validation"
            encrypted = test_fernet.encrypt(test_data)
            decrypted = test_fernet.decrypt(encrypted)
            
            return decrypted == test_data
            
        except Exception:
            return False
    
    def _generate_and_save_encryption_key(self) -> None:
        """Generate new encryption key and save to .env file"""
        try:
            # Generate new encryption key
            new_key = Fernet.generate_key()
            key_string = new_key.decode()
            
            # Save to .env file
            self._save_key_to_env(key_string)
            
            # Initialize Fernet with new key
            self.encryption_key = new_key
            self.fernet = Fernet(new_key)
            
            self.logger.info("🔑 New encryption key generated and saved successfully")
            print(f"{GREEN}├── Encryption Key: Generated and saved to .env{END}")
            print(f"{YELLOW}├── Security Note: Key backup recommended{END}")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to generate encryption key: {e}")
            raise RuntimeError(f"Encryption key generation failed: {e}")
    
    def _regenerate_encryption_key(self) -> None:
        """Regenerate encryption key (emergency recovery)"""
        try:
            print(f"{YELLOW}⚠️ REGENERATING ENCRYPTION KEY{END}")
            print(f"{CYAN}├── Reason: Invalid key detected{END}")
            print(f"{CYAN}├── Action: Emergency key regeneration{END}")
            
            # Generate new key
            self._generate_and_save_encryption_key()
            
            print(f"{GREEN}├── Key Regeneration: Complete{END}")
            print(f"{YELLOW}├── Warning: Old encrypted data may become inaccessible{END}")
            
        except Exception as e:
            self.logger.error(f"❌ Key regeneration failed: {e}")
            raise RuntimeError(f"Key regeneration failed: {e}")
    
    def _save_key_to_env(self, key: str) -> None:
        """
        Save encryption key to .env file
        
        Args:
            key: Encryption key string to save
        """
        try:
            # Create .env file if it doesn't exist
            env_file_path = self.key_file_path
            
            # Read existing .env content
            env_content = ""
            if os.path.exists(env_file_path):
                with open(env_file_path, 'r') as f:
                    env_content = f.read()
            
            # Update or add ENCRYPTION_KEY
            lines = env_content.split('\n')
            key_found = False
            
            for i, line in enumerate(lines):
                if line.startswith('ENCRYPTION_KEY='):
                    lines[i] = f'ENCRYPTION_KEY={key}'
                    key_found = True
                    break
            
            if not key_found:
                lines.append(f'ENCRYPTION_KEY={key}')
            
            # Write back to .env file
            with open(env_file_path, 'w') as f:
                f.write('\n'.join(lines))
            
            self.logger.info(f"Encryption key saved to {env_file_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to save encryption key to .env: {e}")
            raise
    
    def _get_key_source(self) -> str:
        """Get the source of the encryption key"""
        if self.encryption_key:
            return "Self-Generated"
        else:
            return "Not Available"
    
    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def encrypt_data(self, text: Union[str, bytes]) -> EncryptionResult:
        """
        Encrypt sensitive data using Fernet encryption
        
        Args:
            text: Data to encrypt (string or bytes)
            
        Returns:
            EncryptionResult object with encrypted data or error
        """
        timestamp = self._get_timestamp()
        
        print(f"{GREEN}🔒 DATA ENCRYPTION INITIATED{END}")
        print(f"{CYAN}├── Data Length: {len(text) if text else 0} characters{END}")
        print(f"{CYAN}├── Algorithm: Fernet (AES-128-CBC){END}")
        print(f"{CYAN}├── Compliance: Indonesia PDP Regulation{END}")
        print(f"{CYAN}├── Timestamp: {timestamp}{END}")
        
        try:
            # Validate encryption system
            if not self.fernet:
                raise RuntimeError("Encryption system not initialized")
            
            # Convert to bytes if necessary
            if isinstance(text, str):
                data_bytes = text.encode('utf-8')
            else:
                data_bytes = text
            
            # Encrypt data
            encrypted_data = self.fernet.encrypt(data_bytes)
            encrypted_string = encrypted_data.decode('utf-8')
            
            result = EncryptionResult(
                success=True,
                data=encrypted_string,
                error=None,
                operation='encrypt',
                timestamp=timestamp,
                metadata={
                    'algorithm': self.encryption_metadata['algorithm'],
                    'compliance': self.encryption_metadata['compliance'],
                    'original_length': len(text),
                    'encrypted_length': len(encrypted_string)
                }
            )
            
            print(f"{GREEN}✅ ENCRYPTION SUCCESSFUL{END}")
            print(f"{CYAN}├── Original Length: {result.metadata['original_length']} characters{END}")
            print(f"{CYAN}├── Encrypted Length: {result.metadata['encrypted_length']} characters{END}")
            print(f"{CYAN}├── Algorithm: {result.metadata['algorithm']}{END}")
            print(f"{CYAN}├── Compliance: {result.metadata['compliance']}{END}")
            print(f"{GREEN}└── Status: Data encrypted and protected{END}")
            
            self.logger.info(f"Data encrypted successfully (length: {len(text)})")
            
            return result
            
        except Exception as e:
            error_msg = f"Encryption failed: {e}"
            self.logger.error(error_msg)
            
            print(f"{RED}❌ ENCRYPTION ERROR{END}")
            print(f"{RED}├── Error: {e}{END}")
            print(f"{RED}└── Status: Encryption failed{END}")
            
            return EncryptionResult(
                success=False,
                data=None,
                error=error_msg,
                operation='encrypt',
                timestamp=timestamp,
                metadata={'error': True}
            )
    
    def decrypt_data(self, encrypted_text: Union[str, bytes]) -> EncryptionResult:
        """
        Decrypt encrypted data using Fernet decryption
        
        Args:
            encrypted_text: Encrypted data to decrypt (string or bytes)
            
        Returns:
            EncryptionResult object with decrypted data or error
        """
        timestamp = self._get_timestamp()
        
        print(f"{GREEN}🔓 DATA DECRYPTION INITIATED{END}")
        print(f"{CYAN}├── Data Length: {len(encrypted_text) if encrypted_text else 0} characters{END}")
        print(f"{CYAN}├── Algorithm: Fernet (AES-128-CBC){END}")
        print(f"{CYAN}├── Compliance: Indonesia PDP Regulation{END}")
        print(f"{CYAN}├── Timestamp: {timestamp}{END}")
        
        try:
            # Validate encryption system
            if not self.fernet:
                raise RuntimeError("Encryption system not initialized")
            
            # Convert to bytes if necessary
            if isinstance(encrypted_text, str):
                encrypted_bytes = encrypted_text.encode('utf-8')
            else:
                encrypted_bytes = encrypted_text
            
            # Decrypt data
            decrypted_data = self.fernet.decrypt(encrypted_bytes)
            decrypted_string = decrypted_data.decode('utf-8')
            
            result = EncryptionResult(
                success=True,
                data=decrypted_string,
                error=None,
                operation='decrypt',
                timestamp=timestamp,
                metadata={
                    'algorithm': self.encryption_metadata['algorithm'],
                    'compliance': self.encryption_metadata['compliance'],
                    'encrypted_length': len(encrypted_text),
                    'decrypted_length': len(decrypted_string)
                }
            )
            
            print(f"{GREEN}✅ DECRYPTION SUCCESSFUL{END}")
            print(f"{CYAN}├── Encrypted Length: {result.metadata['encrypted_length']} characters{END}")
            print(f"{CYAN}├── Decrypted Length: {result.metadata['decrypted_length']} characters{END}")
            print(f"{CYAN}├── Algorithm: {result.metadata['algorithm']}{END}")
            print(f"{CYAN}├── Compliance: {result.metadata['compliance']}{END}")
            print(f"{GREEN}└── Status: Data decrypted and accessible{END}")
            
            self.logger.info(f"Data decrypted successfully (length: {len(decrypted_string)})")
            
            return result
            
        except Exception as e:
            error_msg = f"Decryption failed: {e}"
            self.logger.error(error_msg)
            
            print(f"{RED}❌ DECRYPTION ERROR{END}")
            print(f"{RED}├── Error: {e}{END}")
            print(f"{RED}└── Status: Decryption failed{END}")
            
            return EncryptionResult(
                success=False,
                data=None,
                error=error_msg,
                operation='decrypt',
                timestamp=timestamp,
                metadata={'error': True}
            )
    
    def encrypt_sensitive_fields(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Encrypt sensitive fields in a data dictionary
        
        Args:
            data: Dictionary containing potentially sensitive fields
            
        Returns:
            Dictionary with sensitive fields encrypted
        """
        sensitive_fields = ['phone', 'email', 'contact_info', 'personal_data', 'ssn', 'id_number']
        
        print(f"{GREEN}🔒 BATCH ENCRYPTION INITIATED{END}")
        print(f"{CYAN}├── Fields to Check: {len(data)}{END}")
        print(f"{CYAN}├── Sensitive Fields: {len(sensitive_fields)}{END}")
        print(f"{CYAN}├── Timestamp: {self._get_timestamp()}{END}")
        
        encrypted_data = data.copy()
        encrypted_count = 0
        
        for field_name, field_value in data.items():
            if field_name.lower() in sensitive_fields and field_value:
                # Encrypt the field
                result = self.encrypt_data(str(field_value))
                if result.success:
                    encrypted_data[field_name] = result.data
                    encrypted_count += 1
                    print(f"{CYAN}├── Encrypted: {field_name}{END}")
                else:
                    print(f"{RED}├── Failed to encrypt: {field_name} - {result.error}{END}")
        
        print(f"{GREEN}✅ BATCH ENCRYPTION COMPLETE{END}")
        print(f"{CYAN}├── Fields Encrypted: {encrypted_count}/{len(data)}{END}")
        print(f"{GREEN}└── Status: Sensitive data protected{END}")
        
        return encrypted_data
    
    def decrypt_sensitive_fields(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Decrypt sensitive fields in a data dictionary
        
        Args:
            data: Dictionary containing encrypted sensitive fields
            
        Returns:
            Dictionary with sensitive fields decrypted
        """
        sensitive_fields = ['phone', 'email', 'contact_info', 'personal_data', 'ssn', 'id_number']
        
        print(f"{GREEN}🔓 BATCH DECRYPTION INITIATED{END}")
        print(f"{CYAN}├── Fields to Check: {len(data)}{END}")
        print(f"{CYAN}├── Sensitive Fields: {len(sensitive_fields)}{END}")
        print(f"{CYAN}├── Timestamp: {self._get_timestamp()}{END}")
        
        decrypted_data = data.copy()
        decrypted_count = 0
        
        for field_name, field_value in data.items():
            if field_name.lower() in sensitive_fields and field_value:
                # Decrypt the field
                result = self.decrypt_data(str(field_value))
                if result.success:
                    decrypted_data[field_name] = result.data
                    decrypted_count += 1
                    print(f"{CYAN}├── Decrypted: {field_name}{END}")
                else:
                    print(f"{RED}├── Failed to decrypt: {field_name} - {result.error}{END}")
        
        print(f"{GREEN}✅ BATCH DECRYPTION COMPLETE{END}")
        print(f"{CYAN}├── Fields Decrypted: {decrypted_count}/{len(data)}{END}")
        print(f"{GREEN}└── Status: Sensitive data accessible{END}")
        
        return decrypted_data
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        Get comprehensive system status and security information
        
        Returns:
            Dictionary containing system status
        """
        return {
            'system': 'DataVault',
            'version': self.encryption_metadata['version'],
            'algorithm': self.encryption_metadata['algorithm'],
            'key_length': self.encryption_metadata['key_length'],
            'compliance': self.encryption_metadata['compliance'],
            'self_healing': self.encryption_metadata['self_healing'],
            'encryption_status': 'Active' if self.fernet else 'Inactive',
            'key_source': self._get_key_source(),
            'key_file': self.key_file_path,
            'timestamp': self._get_timestamp(),
            'security_level': 'Enterprise'
        }

def main():
    """
    Main function to demonstrate DataVault functionality
    """
    print("🔐 DATA VAULT - EXECUTIVE BLUEPRINT LUMINA OS")
    print("=" * 60)
    print("🛡️ Advanced encryption system for sensitive data protection")
    print("=" * 60)
    
    # Initialize DataVault
    vault = DataVault()
    
    # Test encryption
    print("\n📊 Testing data encryption...")
    test_data = "08123456789"
    encrypt_result = vault.encrypt_data(test_data)
    
    if encrypt_result.success:
        print(f"✅ Original: {test_data}")
        print(f"✅ Encrypted: {encrypt_result.data[:50]}...")
    
    # Test decryption
    print("\n📊 Testing data decryption...")
    if encrypt_result.success:
        decrypt_result = vault.decrypt_data(encrypt_result.data)
        
        if decrypt_result.success:
            print(f"✅ Decrypted: {decrypt_result.data}")
            print(f"✅ Match: {decrypt_result.data == test_data}")
    
    # Test batch encryption
    print("\n📊 Testing batch encryption...")
    sample_lead = {
        'name': 'John Doe',
        'phone': '08123456789',
        'email': 'john.doe@example.com',
        'contact_info': 'Phone: 08123456789, Email: john.doe@example.com',
        'message': 'I am interested in your property'
    }
    
    encrypted_lead = vault.encrypt_sensitive_fields(sample_lead)
    
    # Test batch decryption
    print("\n📊 Testing batch decryption...")
    decrypted_lead = vault.decrypt_sensitive_fields(encrypted_lead)
    
    # Show system status
    print("\n📊 System Status:")
    status = vault.get_system_status()
    for key, value in status.items():
        print(f"✅ {key}: {value}")
    
    print("\n" + "=" * 60)
    print("✅ DATA VAULT DEMO COMPLETE")
    print("🛡️ Executive-grade encryption system ready for production")
    print("=" * 60)

if __name__ == "__main__":
    main()
