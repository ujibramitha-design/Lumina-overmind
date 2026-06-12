"""
VAULT MANAGER - Centralized API Key Management
Utility for AI modules to fetch API keys from Classified Vault
"""

import os
import logging
from typing import Optional
from prisma import Client as PrismaClient
from core_modules.security.data_encryption import DataEncryption

logger = logging.getLogger(__name__)

class VaultManager:
    """Centralized manager for API key retrieval from Classified Vault"""
    
    def __init__(self):
        self.data_encryption = DataEncryption()
        self._cache = {}  # Simple in-memory cache
        self._cache_ttl = 300  # 5 minutes cache
    
    async def get_api_key(self, key_name: str, db: Optional[PrismaClient] = None) -> Optional[str]:
        """
        Get API key from Classified Vault with fallback to environment variables
        
        Args:
            key_name: Name of the API key (e.g., 'OPENAI_API_KEY')
            db: Prisma client instance (optional)
            
        Returns:
            Decrypted API key value or None if not found
        """
        try:
            # Check cache first
            if key_name in self._cache:
                cached_data = self._cache[key_name]
                import time
                if time.time() - cached_data['timestamp'] < self._cache_ttl:
                    logger.debug(f"Using cached API key for {key_name}")
                    return cached_data['value']
                else:
                    del self._cache[key_name]
            
            # Initialize database connection if not provided
            if not db:
                db = PrismaClient()
            
            # Try to get from Classified Vault first
            config_key = db.systemconfig.find_first(
                where={
                    'key_name': key_name,
                    'is_active': True
                }
            )
            
            if config_key:
                # Decrypt and cache the key
                decrypted_value = self.data_encryption.decrypt_data(config_key.key_value)
                
                # Cache the decrypted value
                import time
                self._cache[key_name] = {
                    'value': decrypted_value,
                    'timestamp': time.time()
                }
                
                logger.info(f"Retrieved API key {key_name} from Classified Vault")
                return decrypted_value
            
            # Fallback to environment variable
            env_value = os.getenv(key_name)
            if env_value:
                logger.info(f"Using fallback environment variable for {key_name}")
                # Cache the environment value
                import time
                self._cache[key_name] = {
                    'value': env_value,
                    'timestamp': time.time()
                }
                return env_value
            
            logger.warning(f"API key {key_name} not found in vault or environment")
            return None
            
        except Exception as e:
            logger.error(f"Failed to retrieve API key {key_name}: {e}")
            return None
    
    def clear_cache(self, key_name: Optional[str] = None):
        """Clear cached API keys"""
        if key_name:
            self._cache.pop(key_name, None)
            logger.info(f"Cleared cache for {key_name}")
        else:
            self._cache.clear()
            logger.info("Cleared all API key cache")
    
    async def validate_key(self, key_name: str) -> bool:
        """Validate if API key exists and is accessible"""
        try:
            key_value = await self.get_api_key(key_name)
            return key_value is not None and len(key_value) > 0
        except Exception as e:
            logger.error(f"Failed to validate key {key_name}: {e}")
            return False

# Global instance
vault_manager = VaultManager()

# Convenience functions for common API keys
async def get_openai_key() -> Optional[str]:
    """Get OpenAI API key"""
    return await vault_manager.get_api_key('OPENAI_API_KEY')

async def get_gemini_key() -> Optional[str]:
    """Get Gemini API key"""
    return await vault_manager.get_api_key('GEMINI_API_KEY')

async def get_telegram_bot_token() -> Optional[str]:
    """Get Telegram bot token"""
    return await vault_manager.get_api_key('TELEGRAM_BOT_TOKEN')

async def get_telegram_chat_id() -> Optional[str]:
    """Get Telegram chat ID"""
    return await vault_manager.get_api_key('TELEGRAM_CHAT_ID')

async def get_twilio_account_sid() -> Optional[str]:
    """Get Twilio account SID"""
    return await vault_manager.get_api_key('TWILIO_ACCOUNT_SID')

async def get_twilio_auth_token() -> Optional[str]:
    """Get Twilio auth token"""
    return await vault_manager.get_api_key('TWILIO_AUTH_TOKEN')

async def get_twilio_whatsapp_number() -> Optional[str]:
    """Get Twilio WhatsApp number"""
    return await vault_manager.get_api_key('TWILIO_WHATSAPP_NUMBER')

async def get_exa_api_key() -> Optional[str]:
    """Get Exa API key"""
    return await vault_manager.get_api_key('EXA_API_KEY')

async def get_firecrawl_api_key() -> Optional[str]:
    """Get Firecrawl API key"""
    return await vault_manager.get_api_key('FIRECRAWL_API_KEY')

async def get_encryption_key() -> Optional[str]:
    """Get encryption key"""
    return await vault_manager.get_api_key('ENCRYPTION_KEY')
