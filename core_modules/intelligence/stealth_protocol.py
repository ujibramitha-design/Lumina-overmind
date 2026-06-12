"""
Twin-Dragon Engine - Stealth Protocol Module
Advanced rate limiting, human behavior simulation, and anti-detection measures
"""

import asyncio
import random
import time
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging
from dataclasses import dataclass
from enum import Enum
import functools

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ANSI color codes for terminal output
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
CYAN = '\033[96m'
END = '\033[0m'

class StealthMode(Enum):
    """Stealth operation modes"""
    CONSERVATIVE = "conservative"  # Slow, careful, minimal risk
    BALANCED = "balanced"         # Moderate speed, good stealth
    AGGRESSIVE = "aggressive"     # Fast, higher detection risk
    STEALTH = "stealth"           # Maximum stealth, very slow

@dataclass
class StealthConfig:
    """Stealth configuration parameters"""
    mode: StealthMode
    min_delay: float  # Minimum delay in seconds
    max_delay: float  # Maximum delay in seconds
    burst_limit: int  # Maximum requests in burst
    burst_window: int  # Time window for burst (seconds)
    session_timeout: int  # Session timeout (minutes)
    user_agent_rotation: bool = True
    proxy_rotation: bool = False
    
class StealthProtocol:
    """
    Advanced stealth protocol for anti-detection and rate limiting
    """
    
    def __init__(self, mode: StealthMode = StealthMode.BALANCED):
        self.mode = mode
        self.config = self._get_stealth_config(mode)
        
        # Rate limiting state
        self.request_count = 0
        self.session_start = datetime.now()
        self.last_request_time = datetime.now()
        self.burst_requests = []
        
        # User agents for rotation
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15'
        ]
        
        # Proxy pool (placeholder for future implementation)
        self.proxy_pool = []
        self.current_proxy_index = 0
        
        self.logger = logger
        self.logger.info(f"{CYAN}🥷 STEALTH PROTOCOL: Initialized in {mode.value} mode{END}")
        self.logger.info(f"{GREEN}✅ Rate limiting: {self.config.min_delay}s - {self.config.max_delay}s delay{END}")
        self.logger.info(f"{GREEN}✅ Burst limit: {self.config.burst_limit} requests per {self.config.burst_window}s{END}")
    
    def _get_stealth_config(self, mode: StealthMode) -> StealthConfig:
        """Get stealth configuration based on mode"""
        configs = {
            StealthMode.CONSERVATIVE: StealthConfig(
                mode=mode,
                min_delay=5.0,
                max_delay=12.0,
                burst_limit=3,
                burst_window=60,
                session_timeout=30,
                user_agent_rotation=True,
                proxy_rotation=False
            ),
            StealthMode.BALANCED: StealthConfig(
                mode=mode,
                min_delay=2.0,
                max_delay=7.0,
                burst_limit=5,
                burst_window=60,
                session_timeout=45,
                user_agent_rotation=True,
                proxy_rotation=False
            ),
            StealthMode.AGGRESSIVE: StealthConfig(
                mode=mode,
                min_delay=1.0,
                max_delay=4.0,
                burst_limit=8,
                burst_window=60,
                session_timeout=60,
                user_agent_rotation=True,
                proxy_rotation=False
            ),
            StealthMode.STEALTH: StealthConfig(
                mode=mode,
                min_delay=8.0,
                max_delay=20.0,
                burst_limit=2,
                burst_window=120,
                session_timeout=20,
                user_agent_rotation=True,
                proxy_rotation=True
            )
        }
        return configs[mode]
    
    async def human_delay(self, operation_type: str = "default") -> float:
        """
        Apply human-like delay with randomization
        
        Args:
            operation_type: Type of operation for context-aware delays
            
        Returns:
            Actual delay time applied
        """
        # Context-aware delays
        operation_multipliers = {
            "search": 1.0,        # Standard search
            "scrape": 1.5,        # Web scraping
            "login": 2.0,         # Login operations
            "form_submit": 1.8,   # Form submissions
            "navigation": 0.8,    # Page navigation
            "content_extraction": 1.2,  # Content extraction
            "platform_infiltration": 2.5,  # Platform infiltration
            "default": 1.0
        }
        
        multiplier = operation_multipliers.get(operation_type, 1.0)
        
        # Calculate base delay with randomization
        base_delay = random.uniform(self.config.min_delay, self.config.max_delay)
        adjusted_delay = base_delay * multiplier
        
        # Add small random jitter (±10%)
        jitter = random.uniform(-0.1, 0.1) * adjusted_delay
        final_delay = max(0.5, adjusted_delay + jitter)  # Minimum 0.5s delay
        
        # Log the delay
        self.logger.info(f"{YELLOW}⏱️ Human delay: {final_delay:.2f}s for {operation_type} operation{END}")
        
        # Apply the delay
        await asyncio.sleep(final_delay)
        
        # Update rate limiting state
        self.last_request_time = datetime.now()
        self.request_count += 1
        self.burst_requests.append(datetime.now())
        
        # Clean old burst requests
        cutoff_time = datetime.now() - timedelta(seconds=self.config.burst_window)
        self.burst_requests = [req_time for req_time in self.burst_requests if req_time > cutoff_time]
        
        return final_delay
    
    async def check_rate_limits(self) -> bool:
        """
        Check if current request is within rate limits
        
        Returns:
            True if request is allowed, False otherwise
        """
        # Check burst limit
        if len(self.burst_requests) >= self.config.burst_limit:
            self.logger.warning(f"{YELLOW}⚠️ Burst limit reached: {len(self.burst_requests)}/{self.config.burst_limit}{END}")
            return False
        
        # Check session timeout
        session_duration = datetime.now() - self.session_start
        if session_duration > timedelta(minutes=self.config.session_timeout):
            self.logger.info(f"{BLUE}🔄 Session timeout reached, resetting session{END}")
            self.reset_session()
            return True
        
        return True
    
    def reset_session(self):
        """Reset session state"""
        self.session_start = datetime.now()
        self.request_count = 0
        self.burst_requests = []
        self.logger.info(f"{GREEN}✅ Session reset{END}")
    
    def get_random_user_agent(self) -> str:
        """
        Get random user agent for rotation
        
        Returns:
            Random user agent string
        """
        if not self.config.user_agent_rotation:
            return self.user_agents[0]
        
        return random.choice(self.user_agents)
    
    def get_current_proxy(self) -> Optional[Dict[str, str]]:
        """
        Get current proxy for rotation (placeholder implementation)
        
        Returns:
            Proxy configuration or None
        """
        if not self.config.proxy_rotation or not self.proxy_pool:
            return None
        
        proxy = self.proxy_pool[self.current_proxy_index]
        self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxy_pool)
        
        return proxy
    
    def add_proxy(self, proxy_config: Dict[str, str]):
        """
        Add proxy to pool (placeholder implementation)
        
        Args:
            proxy_config: Proxy configuration
        """
        self.proxy_pool.append(proxy_config)
        self.logger.info(f"{GREEN}➕ Proxy added to pool: {len(self.proxy_pool)} total{END}")
    
    async def stealth_request(self, operation_type: str = "default", max_retries: int = 3):
        """
        Execute stealth request with rate limiting and retry logic
        
        Args:
            operation_type: Type of operation
            max_retries: Maximum number of retries
            
        Returns:
            Decorator function for stealth operations
        """
        def decorator(func):
            async def wrapper(*args, **kwargs):
                retry_count = 0
                
                while retry_count < max_retries:
                    try:
                        # Check rate limits
                        if not await self.check_rate_limits():
                            wait_time = random.uniform(5, 15)
                            self.logger.warning(f"{YELLOW}⏳ Rate limited, waiting {wait_time:.1f}s{END}")
                            await asyncio.sleep(wait_time)
                            continue
                        
                        # Apply human delay
                        await self.human_delay(operation_type)
                        
                        # Execute the function
                        result = await func(*args, **kwargs)
                        
                        # Success - log and return
                        self.logger.info(f"{GREEN}✅ Stealth operation completed: {operation_type}{END}")
                        return result
                        
                    except Exception as e:
                        retry_count += 1
                        if retry_count >= max_retries:
                            self.logger.error(f"{RED}❌ Stealth operation failed after {max_retries} retries: {str(e)}{END}")
                            raise e
                        
                        # Exponential backoff for retries
                        backoff_time = (2 ** retry_count) + random.uniform(0, 2)
                        self.logger.warning(f"{YELLOW}⚠️ Stealth operation failed, retry {retry_count}/{max_retries} in {backoff_time:.1f}s{END}")
                        await asyncio.sleep(backoff_time)
                
                return None
            
            return wrapper
        return decorator
    
    def get_stealth_stats(self) -> Dict[str, Any]:
        """
        Get current stealth statistics
        
        Returns:
            Dictionary with stealth statistics
        """
        session_duration = datetime.now() - self.session_start
        requests_per_minute = self.request_count / max(1, session_duration.total_seconds() / 60)
        
        return {
            "mode": self.mode.value,
            "session_duration_minutes": session_duration.total_seconds() / 60,
            "total_requests": self.request_count,
            "requests_per_minute": round(requests_per_minute, 2),
            "current_burst_count": len(self.burst_requests),
            "burst_limit": self.config.burst_limit,
            "user_agents_available": len(self.user_agents),
            "proxies_available": len(self.proxy_pool),
            "last_request_time": self.last_request_time.isoformat()
        }
    
    def change_mode(self, new_mode: StealthMode):
        """
        Change stealth mode
        
        Args:
            new_mode: New stealth mode
        """
        old_mode = self.mode
        self.mode = new_mode
        self.config = self._get_stealth_config(new_mode)
        
        self.logger.info(f"{CYAN}🔄 Stealth mode changed: {old_mode.value} → {new_mode.value}{END}")
        self.logger.info(f"{GREEN}✅ New config: {self.config.min_delay}s - {self.config.max_delay}s delay{END}")

# Global stealth protocol instance
stealth_protocol = StealthProtocol()

# Convenience functions
async def human_delay(operation_type: str = "default") -> float:
    """Apply human-like delay"""
    return await stealth_protocol.human_delay(operation_type)

def get_random_user_agent() -> str:
    """Get random user agent"""
    return stealth_protocol.get_random_user_agent()

def get_stealth_stats() -> Dict[str, Any]:
    """Get stealth statistics"""
    return stealth_protocol.get_stealth_stats()

def change_stealth_mode(mode: StealthMode):
    """Change stealth mode"""
    stealth_protocol.change_mode(mode)

# Decorator for stealth operations
def stealth_operation(operation_type: str = "default", max_retries: int = 3):
    """Decorator factory for stealth operations."""
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # This is where the stealth logic from stealth_request would wrap the function call
            # For now, we'll just log and call the original function.
            # The full implementation of stealth_request should be integrated here.
            logger.info(f"Executing stealth operation '{operation_type}' for function {func.__name__}")
            return await func(*args, **kwargs)
        return wrapper
    return decorator

# The example usage block below was causing import-time errors and has been commented out.
# async def main():
#     """Example usage of stealth protocol"""
#     print("🥷 Twin-Dragon Stealth Protocol Example")
#     print("=" * 50)
#     
#     # Test human delays
#     print("\n📊 Testing Human Delays:")
#     for i in range(3):
#         delay = await human_delay("search")
#         print(f"  Delay {i+1}: {delay:.2f}s")
#     
#     # Test stealth operation
#     print("\n🎭 Testing Stealth Operation:")
#     
#     @stealth_operation("platform_infiltration", max_retries=3)
#     async def example_infiltration():
#         """Example of stealth operation"""
#         print("Executing infiltration...")
#         return {"status": "success", "data": "infiltrated"}
#
#     result = await example_infiltration()
#     print(f"  Result: {result}")
#     
#     # Get stealth stats
#     print("\n📈 Stealth Statistics:")
#     stats = get_stealth_stats()
#     for key, value in stats.items():
#         print(f"  {key}: {value}")
#     
#     # Change mode
#     print("\n🔄 Changing to STEALTH mode:")
#     change_stealth_mode(StealthMode.STEALTH)
#     
#     # Test new mode
#     delay = await human_delay("scrape")
#     print(f"  Stealth mode delay: {delay:.2f}s")
#
# if __name__ == "__main__":
#     asyncio.run(main())
