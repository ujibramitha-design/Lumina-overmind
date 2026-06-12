"""
Twin-Dragon Engine - Proxy Rotation Framework (Structure)
Advanced IP rotation for anti-detection and load distribution
"""

import asyncio
import random
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import aiohttp

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

class ProxyType(Enum):
    """Proxy types"""
    HTTP = "http"
    HTTPS = "https"
    SOCKS4 = "socks4"
    SOCKS5 = "socks5"

class ProxyStatus(Enum):
    """Proxy status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    BANNED = "banned"
    TESTING = "testing"

@dataclass
class ProxyConfig:
    """Proxy configuration"""
    id: str
    host: str
    port: int
    username: Optional[str] = None
    password: Optional[str] = None
    proxy_type: ProxyType = ProxyType.HTTP
    country: Optional[str] = None
    city: Optional[str] = None
    provider: Optional[str] = None
    max_concurrent_requests: int = 10
    timeout: int = 30
    status: ProxyStatus = ProxyStatus.INACTIVE
    success_count: int = 0
    failure_count: int = 0
    last_used: Optional[datetime] = None
    last_success: Optional[datetime] = None
    last_failure: Optional[datetime] = None
    response_time_avg: float = 0.0

class ProxyRotationStrategy(Enum):
    """Proxy rotation strategies"""
    ROUND_ROBIN = "round_robin"
    RANDOM = "random"
    WEIGHTED = "weighted"
    GEOGRAPHIC = "geographic"
    LEAST_USED = "least_used"
    FASTEST = "fastest"

class ProxyRotator:
    """
    Advanced proxy rotation system with health monitoring
    """
    
    def __init__(self, strategy: ProxyRotationStrategy = ProxyRotationStrategy.ROUND_ROBIN):
        self.strategy = strategy
        self.proxies: Dict[str, ProxyConfig] = {}
        self.active_proxies: List[str] = []
        self.current_index = 0
        self.session_stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'proxy_rotations': 0,
            'session_start': datetime.now()
        }
        
        # Health check settings
        self.health_check_interval = 300  # 5 minutes
        self.health_check_timeout = 10
        self.max_failure_rate = 0.3  # 30% failure rate threshold
        
        self.logger = logger
        self.logger.info(f"{CYAN}🌐 PROXY ROTATOR: Initialized with {strategy.value} strategy{END}")
    
    def add_proxy(self, proxy_config: ProxyConfig) -> bool:
        """
        Add proxy to rotation pool
        
        Args:
            proxy_config: Proxy configuration
            
        Returns:
            True if proxy added successfully
        """
        try:
            # Validate proxy configuration
            if not self._validate_proxy_config(proxy_config):
                self.logger.error(f"{RED}❌ Invalid proxy configuration: {proxy_config.id}{END}")
                return False
            
            # Add proxy to pool
            self.proxies[proxy_config.id] = proxy_config
            
            # Add to active list if not banned
            if proxy_config.status != ProxyStatus.BANNED:
                self.active_proxies.append(proxy_config.id)
            
            self.logger.info(f"{GREEN}✅ Proxy added: {proxy_config.id} ({proxy_config.host}:{proxy_config.port}){END}")
            self.logger.info(f"{CYAN}📊 Total proxies: {len(self.proxies)} | Active: {len(self.active_proxies)}{END}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"{RED}❌ Error adding proxy: {str(e)}{END}")
            return False
    
    def _validate_proxy_config(self, proxy_config: ProxyConfig) -> bool:
        """Validate proxy configuration"""
        if not proxy_config.host or not proxy_config.port:
            return False
        
        if proxy_config.port < 1 or proxy_config.port > 65535:
            return False
        
        return True
    
    def get_next_proxy(self) -> Optional[ProxyConfig]:
        """
        Get next proxy based on rotation strategy
        
        Returns:
            Next proxy configuration or None
        """
        if not self.active_proxies:
            self.logger.warning(f"{YELLOW}⚠️ No active proxies available{END}")
            return None
        
        try:
            proxy_id = None
            
            if self.strategy == ProxyRotationStrategy.ROUND_ROBIN:
                proxy_id = self._get_round_robin_proxy()
            elif self.strategy == ProxyRotationStrategy.RANDOM:
                proxy_id = self._get_random_proxy()
            elif self.strategy == ProxyRotationStrategy.LEAST_USED:
                proxy_id = self._get_least_used_proxy()
            elif self.strategy == ProxyRotationStrategy.FASTEST:
                proxy_id = self._get_fastest_proxy()
            elif self.strategy == ProxyRotationStrategy.GEOGRAPHIC:
                proxy_id = self._get_geographic_proxy()
            else:
                proxy_id = self._get_round_robin_proxy()
            
            if proxy_id and proxy_id in self.proxies:
                proxy = self.proxies[proxy_id]
                proxy.last_used = datetime.now()
                self.session_stats['proxy_rotations'] += 1
                
                self.logger.debug(f"{BLUE}🔄 Selected proxy: {proxy_id} ({self.strategy.value}){END}")
                return proxy
            
            return None
            
        except Exception as e:
            self.logger.error(f"{RED}❌ Error getting next proxy: {str(e)}{END}")
            return None
    
    def _get_round_robin_proxy(self) -> Optional[str]:
        """Get proxy using round-robin strategy"""
        if not self.active_proxies:
            return None
        
        proxy_id = self.active_proxies[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.active_proxies)
        return proxy_id
    
    def _get_random_proxy(self) -> Optional[str]:
        """Get proxy using random strategy"""
        if not self.active_proxies:
            return None
        
        return random.choice(self.active_proxies)
    
    def _get_least_used_proxy(self) -> Optional[str]:
        """Get proxy with least usage"""
        if not self.active_proxies:
            return None
        
        least_used_proxy = None
        min_usage = float('inf')
        
        for proxy_id in self.active_proxies:
            proxy = self.proxies[proxy_id]
            total_usage = proxy.success_count + proxy.failure_count
            
            if total_usage < min_usage:
                min_usage = total_usage
                least_used_proxy = proxy_id
        
        return least_used_proxy
    
    def _get_fastest_proxy(self) -> Optional[str]:
        """Get proxy with fastest response time"""
        if not self.active_proxies:
            return None
        
        fastest_proxy = None
        min_response_time = float('inf')
        
        for proxy_id in self.active_proxies:
            proxy = self.proxies[proxy_id]
            if proxy.response_time_avg < min_response_time and proxy.response_time_avg > 0:
                min_response_time = proxy.response_time_avg
                fastest_proxy = proxy_id
        
        return fastest_proxy or self._get_random_proxy()
    
    def _get_geographic_proxy(self) -> Optional[str]:
        """Get proxy based on geographic distribution (placeholder)"""
        # This would implement geographic load balancing
        # For now, fall back to random selection
        return self._get_random_proxy()
    
    def mark_proxy_success(self, proxy_id: str, response_time: float = 0.0):
        """
        Mark proxy request as successful
        
        Args:
            proxy_id: Proxy identifier
            response_time: Response time in seconds
        """
        if proxy_id in self.proxies:
            proxy = self.proxies[proxy_id]
            proxy.success_count += 1
            proxy.last_success = datetime.now()
            
            # Update average response time
            if response_time > 0:
                total_requests = proxy.success_count + proxy.failure_count
                proxy.response_time_avg = ((proxy.response_time_avg * (total_requests - 1)) + response_time) / total_requests
            
            self.session_stats['successful_requests'] += 1
            self.session_stats['total_requests'] += 1
            
            self.logger.debug(f"{GREEN}✅ Proxy success: {proxy_id} ({response_time:.2f}s){END}")
    
    def mark_proxy_failure(self, proxy_id: str, error_message: str = ""):
        """
        Mark proxy request as failed
        
        Args:
            proxy_id: Proxy identifier
            error_message: Error message for logging
        """
        if proxy_id in self.proxies:
            proxy = self.proxies[proxy_id]
            proxy.failure_count += 1
            proxy.last_failure = datetime.now()
            
            # Check if proxy should be banned
            failure_rate = proxy.failure_count / (proxy.success_count + proxy.failure_count)
            if failure_rate > self.max_failure_rate and (proxy.success_count + proxy.failure_count) >= 10:
                proxy.status = ProxyStatus.BANNED
                if proxy_id in self.active_proxies:
                    self.active_proxies.remove(proxy_id)
                self.logger.warning(f"{YELLOW}⚠️ Proxy banned due to high failure rate: {proxy_id} ({failure_rate:.2%}){END}")
            
            self.session_stats['failed_requests'] += 1
            self.session_stats['total_requests'] += 1
            
            self.logger.debug(f"{RED}❌ Proxy failure: {proxy_id} ({error_message}){END}")
    
    def get_proxy_url(self, proxy_config: ProxyConfig) -> str:
        """
        Get proxy URL for HTTP requests
        
        Args:
            proxy_config: Proxy configuration
            
        Returns:
            Proxy URL string
        """
        if proxy_config.username and proxy_config.password:
            return f"{proxy_config.proxy_type.value}://{proxy_config.username}:{proxy_config.password}@{proxy_config.host}:{proxy_config.port}"
        else:
            return f"{proxy_config.proxy_type.value}://{proxy_config.host}:{proxy_config.port}"
    
    async def test_proxy_health(self, proxy_config: ProxyConfig) -> bool:
        """
        Test proxy health and connectivity
        
        Args:
            proxy_config: Proxy configuration to test
            
        Returns:
            True if proxy is healthy
        """
        try:
            proxy_url = self.get_proxy_url(proxy_config)
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "http://httpbin.org/ip",
                    proxy=proxy_url,
                    timeout=aiohttp.ClientTimeout(total=self.health_check_timeout)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        self.logger.info(f"{GREEN}✅ Proxy health check passed: {proxy_config.id} (IP: {data.get('origin', 'unknown')}){END}")
                        return True
                    else:
                        self.logger.warning(f"{YELLOW}⚠️ Proxy health check failed: {proxy_config.id} (Status: {response.status}){END}")
                        return False
                        
        except Exception as e:
            self.logger.error(f"{RED}❌ Proxy health check error: {proxy_config.id} ({str(e)}){END}")
            return False
    
    async def health_check_all_proxies(self):
        """Perform health check on all proxies"""
        self.logger.info(f"{CYAN}🔍 Starting health check for {len(self.proxies)} proxies{END}")
        
        tasks = []
        for proxy_config in self.proxies.values():
            if proxy_config.status != ProxyStatus.BANNED:
                tasks.append(self.test_proxy_health(proxy_config))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        healthy_count = 0
        for i, result in enumerate(results):
            proxy_id = list(self.proxies.keys())[i]
            if isinstance(result, bool) and result:
                healthy_count += 1
                if self.proxies[proxy_id].status == ProxyStatus.INACTIVE:
                    self.proxies[proxy_id].status = ProxyStatus.ACTIVE
                    if proxy_id not in self.active_proxies:
                        self.active_proxies.append(proxy_id)
            else:
                if proxy_id in self.active_proxies:
                    self.active_proxies.remove(proxy_id)
                self.proxies[proxy_id].status = ProxyStatus.INACTIVE
        
        self.logger.info(f"{GREEN}✅ Health check completed: {healthy_count}/{len(self.proxies)} proxies healthy{END}")
    
    def get_rotation_stats(self) -> Dict[str, Any]:
        """
        Get proxy rotation statistics
        
        Returns:
            Dictionary with rotation statistics
        """
        session_duration = datetime.now() - self.session_stats['session_start']
        
        return {
            "strategy": self.strategy.value,
            "total_proxies": len(self.proxies),
            "active_proxies": len(self.active_proxies),
            "banned_proxies": len([p for p in self.proxies.values() if p.status == ProxyStatus.BANNED]),
            "session_duration_minutes": session_duration.total_seconds() / 60,
            "total_requests": self.session_stats['total_requests'],
            "successful_requests": self.session_stats['successful_requests'],
            "failed_requests": self.session_stats['failed_requests'],
            "success_rate": self.session_stats['successful_requests'] / max(1, self.session_stats['total_requests']),
            "proxy_rotations": self.session_stats['proxy_rotations'],
            "avg_requests_per_proxy": self.session_stats['total_requests'] / max(1, len(self.active_proxies))
        }
    
    def change_strategy(self, new_strategy: ProxyRotationStrategy):
        """
        Change proxy rotation strategy
        
        Args:
            new_strategy: New rotation strategy
        """
        old_strategy = self.strategy
        self.strategy = new_strategy
        self.current_index = 0  # Reset index for round-robin
        
        self.logger.info(f"{CYAN}🔄 Proxy rotation strategy changed: {old_strategy.value} → {new_strategy.value}{END}")
    
    def reset_stats(self):
        """Reset session statistics"""
        self.session_stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'proxy_rotations': 0,
            'session_start': datetime.now()
        }
        
        # Reset proxy stats
        for proxy in self.proxies.values():
            proxy.success_count = 0
            proxy.failure_count = 0
            proxy.response_time_avg = 0.0
        
        self.logger.info(f"{GREEN}✅ Proxy rotation stats reset{END}")

# Global proxy rotator instance
proxy_rotator = ProxyRotator()

# Convenience functions
def add_proxy(host: str, port: int, username: str = None, password: str = None, 
              proxy_type: ProxyType = ProxyType.HTTP, country: str = None) -> bool:
    """Add proxy to rotation pool"""
    proxy_id = f"{host}:{port}"
    proxy_config = ProxyConfig(
        id=proxy_id,
        host=host,
        port=port,
        username=username,
        password=password,
        proxy_type=proxy_type,
        country=country
    )
    return proxy_rotator.add_proxy(proxy_config)

def get_next_proxy() -> Optional[ProxyConfig]:
    """Get next proxy for rotation"""
    return proxy_rotator.get_next_proxy()

def mark_proxy_success(proxy_id: str, response_time: float = 0.0):
    """Mark proxy request as successful"""
    proxy_rotator.mark_proxy_success(proxy_id, response_time)

def mark_proxy_failure(proxy_id: str, error_message: str = ""):
    """Mark proxy request as failed"""
    proxy_rotator.mark_proxy_failure(proxy_id, error_message)

def get_rotation_stats() -> Dict[str, Any]:
    """Get proxy rotation statistics"""
    return proxy_rotator.get_rotation_stats()

# Example usage
async def main():
    """Example usage of proxy rotation"""
    print("🌐 Twin-Dragon Proxy Rotation Example")
    print("=" * 50)
    
    # Add some example proxies
    print("\n➕ Adding example proxies:")
    add_proxy("proxy1.example.com", 8080, "user1", "pass1")
    add_proxy("proxy2.example.com", 8080, "user2", "pass2")
    add_proxy("proxy3.example.com", 8080, "user3", "pass3")
    
    # Test proxy selection
    print("\n🔄 Testing proxy selection:")
    for i in range(5):
        proxy = get_next_proxy()
        if proxy:
            print(f"  Request {i+1}: {proxy.id} ({proxy.host}:{proxy.port})")
            mark_proxy_success(proxy.id, random.uniform(0.5, 2.0))
        else:
            print(f"  Request {i+1}: No proxy available")
    
    # Get rotation stats
    print("\n📊 Proxy Rotation Statistics:")
    stats = get_rotation_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Change strategy
    print("\n🔄 Changing to RANDOM strategy:")
    proxy_rotator.change_strategy(ProxyRotationStrategy.RANDOM)
    
    # Test with new strategy
    print("\n🔄 Testing with RANDOM strategy:")
    for i in range(3):
        proxy = get_next_proxy()
        if proxy:
            print(f"  Request {i+1}: {proxy.id} ({proxy.host}:{proxy.port})")
            mark_proxy_success(proxy.id, random.uniform(0.5, 2.0))

if __name__ == "__main__":
    asyncio.run(main())
