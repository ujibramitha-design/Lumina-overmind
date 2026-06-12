"""
LUMINA OS - PROXY ROTATOR & STEALTH SYSTEM
============================================

Advanced proxy rotation and User-Agent manipulation system
for OSINT activities without triggering anti-bot systems.

Features:
- Rotating proxy pool with health checking
- User-Agent randomization across browsers/devices
- Request throttling and rate limiting
- Anti-detection headers and cookies management
- Session management and fingerprint rotation
- IP reputation scoring and blacklisting
"""

import os
import sys
import json
import time
import random
import asyncio
import logging
import hashlib
import requests
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from urllib.parse import urlparse
import aiohttp
from fake_useragent import UserAgent

# Add root directory to Python path
root_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root_dir)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class ProxyConfig:
    """Proxy configuration dataclass"""
    ip: str
    port: int
    username: Optional[str] = None
    password: Optional[str] = None
    protocol: str = 'http'
    country: Optional[str] = None
    last_checked: Optional[datetime] = None
    success_rate: float = 0.0
    response_time: float = 0.0
    is_active: bool = True
    blacklist_until: Optional[datetime] = None

@dataclass
class UserAgentProfile:
    """User-Agent profile for fingerprint rotation"""
    user_agent: str
    platform: str
    browser: str
    version: str
    screen_resolution: str
    timezone: str
    language: str
    accept_language: str
    accept_encoding: str
    dnt: str
    upgrade_insecure_requests: str

class ProxyRotator:
    """Advanced proxy rotation system with anti-detection capabilities"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or os.path.join(root_dir, 'config', 'proxy_config.json')
        self.proxies: List[ProxyConfig] = []
        self.current_proxy_index = 0
        self.user_agent_generator = UserAgent()
        self.user_agent_profiles: List[UserAgentProfile] = []
        self.session_cookies: Dict[str, Dict] = {}
        self.request_history: List[Dict] = []
        self.blacklisted_ips: set = set()
        
        # Load configuration
        self.load_config()
        self.generate_user_agent_profiles()
        
    def load_config(self):
        """Load proxy configuration from file"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    
                # Load proxy list
                for proxy_data in config.get('proxies', []):
                    proxy = ProxyConfig(**proxy_data)
                    self.proxies.append(proxy)
                    
                logger.info(f"Loaded {len(self.proxies)} proxies from config")
            else:
                # Create default configuration
                self.create_default_config()
                
        except Exception as e:
            logger.error(f"Error loading proxy config: {e}")
            self.create_default_config()
    
    def create_default_config(self):
        """Create default proxy configuration"""
        default_config = {
            'proxies': [
                {
                    'ip': '127.0.0.1',
                    'port': 8080,
                    'protocol': 'http',
                    'country': 'Local',
                    'is_active': True
                }
            ],
            'rotation_settings': {
                'rotation_interval': 300,  # 5 minutes
                'max_failures': 3,
                'health_check_interval': 60,
                'request_delay': (1, 3),  # Random delay between requests
                'max_concurrent_requests': 5
            },
            'anti_detection': {
                'random_user_agent': True,
                'random_headers': True,
                'cookie_management': True,
                'request_throttling': True,
                'fingerprint_rotation': True
            }
        }
        
        # Create config directory if it doesn't exist
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        
        with open(self.config_path, 'w') as f:
            json.dump(default_config, f, indent=2, default=str)
            
        logger.info("Created default proxy configuration")
    
    def generate_user_agent_profiles(self):
        """Generate diverse user-agent profiles for fingerprint rotation"""
        platforms = ['Win32', 'Win64', 'MacIntel', 'Linux x86_64']
        browsers = ['Chrome', 'Firefox', 'Safari', 'Edge']
        languages = ['en-US,en;q=0.9', 'id-ID,id;q=0.9,en;q=0.8', 'en-GB,en;q=0.9']
        timezones = ['America/New_York', 'Europe/London', 'Asia/Jakarta', 'Asia/Tokyo']
        resolutions = ['1920x1080', '1366x768', '1440x900', '1536x864']
        
        for _ in range(20):  # Generate 20 different profiles
            try:
                ua = self.user_agent_generator.random
                profile = UserAgentProfile(
                    user_agent=ua,
                    platform=random.choice(platforms),
                    browser=random.choice(browsers),
                    version=self._extract_browser_version(ua),
                    screen_resolution=random.choice(resolutions),
                    timezone=random.choice(timezones),
                    language=random.choice(languages),
                    accept_language=random.choice(languages),
                    accept_encoding='gzip, deflate, br',
                    dnt=random.choice(['0', '1']),
                    upgrade_insecure_requests='1'
                )
                self.user_agent_profiles.append(profile)
            except Exception as e:
                logger.warning(f"Error generating user agent profile: {e}")
                continue
                
        logger.info(f"Generated {len(self.user_agent_profiles)} user-agent profiles")
    
    def _extract_browser_version(self, user_agent: str) -> str:
        """Extract browser version from user agent string"""
        try:
            if 'Chrome' in user_agent:
                import re
                match = re.search(r'Chrome/(\d+\.\d+)', user_agent)
                return match.group(1) if match else '90.0'
            elif 'Firefox' in user_agent:
                import re
                match = re.search(r'Firefox/(\d+\.\d+)', user_agent)
                return match.group(1) if match else '88.0'
            else:
                return '90.0'
        except:
            return '90.0'
    
    def get_next_proxy(self) -> Optional[ProxyConfig]:
        """Get next available proxy from rotation pool"""
        if not self.proxies:
            logger.warning("No proxies available")
            return None
            
        # Find active proxy
        attempts = 0
        while attempts < len(self.proxies):
            proxy = self.proxies[self.current_proxy_index]
            
            # Check if proxy is active and not blacklisted
            if (proxy.is_active and 
                (proxy.blacklist_until is None or proxy.blacklist_until < datetime.now())):
                
                self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxies)
                return proxy
                
            self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxies)
            attempts += 1
            
        logger.warning("No active proxies available")
        return None
    
    def get_random_user_agent_profile(self) -> UserAgentProfile:
        """Get random user-agent profile for fingerprint rotation"""
        return random.choice(self.user_agent_profiles)
    
    def build_stealth_headers(self, profile: UserAgentProfile, target_url: str) -> Dict[str, str]:
        """Build stealth headers to avoid detection"""
        parsed_url = urlparse(target_url)
        domain = parsed_url.netloc
        
        headers = {
            'User-Agent': profile.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': profile.accept_language,
            'Accept-Encoding': profile.accept_encoding,
            'DNT': profile.dnt,
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': profile.upgrade_insecure_requests,
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'Sec-Ch-Ua': f'"Chromium";v="{profile.version}", "{profile.browser}";v="{profile.version}", "Not_A Brand";v="99"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': f'"{profile.platform}"',
        }
        
        # Add domain-specific headers
        if 'google.com' in domain:
            headers.update({
                'Referer': 'https://www.google.com/',
                'Origin': 'https://www.google.com'
            })
        elif 'duckduckgo.com' in domain:
            headers.update({
                'Referer': 'https://duckduckgo.com/',
                'Origin': 'https://duckduckgo.com'
            })
            
        return headers
    
    async def make_stealth_request(
        self, 
        url: str, 
        method: str = 'GET',
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        timeout: int = 30,
        max_retries: int = 3
    ) -> Tuple[Optional[requests.Response], Optional[str]]:
        """Make stealth request with proxy rotation and anti-detection"""
        
        for attempt in range(max_retries):
            try:
                # Get proxy and user agent profile
                proxy = self.get_next_proxy()
                profile = self.get_random_user_agent_profile()
                
                if not proxy:
                    raise Exception("No available proxies")
                
                # Build proxy URL
                if proxy.username and proxy.password:
                    proxy_url = f"{proxy.protocol}://{proxy.username}:{proxy.password}@{proxy.ip}:{proxy.port}"
                else:
                    proxy_url = f"{proxy.protocol}://{proxy.ip}:{proxy.port}"
                
                # Build stealth headers
                headers = self.build_stealth_headers(profile, url)
                
                # Add random delay to avoid rate limiting
                delay = random.uniform(1, 3)
                await asyncio.sleep(delay)
                
                # Make request
                proxies = {
                    'http': proxy_url,
                    'https': proxy_url
                }
                
                session = requests.Session()
                response = session.request(
                    method=method,
                    url=url,
                    params=params,
                    data=data,
                    headers=headers,
                    proxies=proxies,
                    timeout=timeout,
                    allow_redirects=True
                )
                
                # Log successful request
                self.log_request(proxy, profile, url, response.status_code, True)
                
                # Update proxy statistics
                self.update_proxy_stats(proxy, True, response.elapsed.total_seconds())
                
                return response, None
                
            except Exception as e:
                error_msg = str(e)
                logger.warning(f"Request failed (attempt {attempt + 1}/{max_retries}): {error_msg}")
                
                # Log failed request
                self.log_request(proxy, profile, url, 0, False)
                
                # Update proxy statistics and potentially blacklist
                if proxy:
                    self.update_proxy_stats(proxy, False, 0)
                    if attempt >= max_retries - 1:
                        self.blacklist_proxy(proxy, duration=timedelta(hours=1))
                
                if attempt == max_retries - 1:
                    return None, error_msg
                    
                # Wait before retry
                await asyncio.sleep(random.uniform(2, 5))
        
        return None, "Max retries exceeded"
    
    def log_request(self, proxy: ProxyConfig, profile: UserAgentProfile, url: str, status_code: int, success: bool):
        """Log request for monitoring and analytics"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'proxy_ip': proxy.ip,
            'proxy_port': proxy.port,
            'user_agent': profile.user_agent,
            'browser': profile.browser,
            'platform': profile.platform,
            'url': url,
            'status_code': status_code,
            'success': success,
            'response_time': getattr(proxy, 'last_response_time', 0)
        }
        
        self.request_history.append(log_entry)
        
        # Keep only last 1000 entries
        if len(self.request_history) > 1000:
            self.request_history = self.request_history[-1000:]
    
    def update_proxy_stats(self, proxy: ProxyConfig, success: bool, response_time: float):
        """Update proxy statistics"""
        proxy.last_response_time = response_time
        
        if success:
            # Update success rate (exponential moving average)
            if proxy.success_rate == 0:
                proxy.success_rate = 1.0
            else:
                proxy.success_rate = (proxy.success_rate * 0.9) + (1.0 * 0.1)
        else:
            # Decrease success rate
            proxy.success_rate = (proxy.success_rate * 0.9) + (0.0 * 0.1)
    
    def blacklist_proxy(self, proxy: ProxyConfig, duration: timedelta):
        """Blacklist proxy for specified duration"""
        proxy.blacklist_until = datetime.now() + duration
        proxy.is_active = False
        logger.warning(f"Blacklisted proxy {proxy.ip}:{proxy.port} until {proxy.blacklist_until}")
    
    async def health_check_proxies(self):
        """Health check all proxies in the pool"""
        logger.info("Starting proxy health check")
        
        test_url = "http://httpbin.org/ip"
        
        tasks = []
        for proxy in self.proxies:
            task = asyncio.create_task(self.check_single_proxy(proxy, test_url))
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        active_count = 0
        for i, result in enumerate(results):
            proxy = self.proxies[i]
            if isinstance(result, bool):
                proxy.is_active = result
                if result:
                    active_count += 1
            else:
                proxy.is_active = False
                logger.error(f"Health check error for proxy {proxy.ip}:{proxy.port}: {result}")
        
        logger.info(f"Health check completed: {active_count}/{len(self.proxies)} proxies active")
    
    async def check_single_proxy(self, proxy: ProxyConfig, test_url: str) -> bool:
        """Check single proxy health"""
        try:
            if proxy.username and proxy.password:
                proxy_url = f"{proxy.protocol}://{proxy.username}:{proxy.password}@{proxy.ip}:{proxy.port}"
            else:
                proxy_url = f"{proxy.protocol}://{proxy.ip}:{proxy.port}"
            
            proxies = {
                'http': proxy_url,
                'https': proxy_url
            }
            
            profile = self.get_random_user_agent_profile()
            headers = self.build_stealth_headers(profile, test_url)
            
            response = requests.get(
                test_url,
                headers=headers,
                proxies=proxies,
                timeout=10
            )
            
            return response.status_code == 200
            
        except Exception as e:
            logger.debug(f"Proxy {proxy.ip}:{proxy.port} health check failed: {e}")
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get proxy rotation statistics"""
        total_proxies = len(self.proxies)
        active_proxies = sum(1 for p in self.proxies if p.is_active)
        blacklisted_proxies = sum(1 for p in self.proxies if p.blacklist_until and p.blacklist_until > datetime.now())
        
        avg_success_rate = sum(p.success_rate for p in self.proxies) / total_proxies if total_proxies > 0 else 0
        avg_response_time = sum(p.last_response_time for p in self.proxies) / total_proxies if total_proxies > 0 else 0
        
        recent_requests = [r for r in self.request_history if datetime.fromisoformat(r['timestamp']) > datetime.now() - timedelta(hours=1)]
        success_rate_recent = sum(1 for r in recent_requests if r['success']) / len(recent_requests) if recent_requests else 0
        
        return {
            'total_proxies': total_proxies,
            'active_proxies': active_proxies,
            'blacklisted_proxies': blacklisted_proxies,
            'avg_success_rate': avg_success_rate,
            'avg_response_time': avg_response_time,
            'recent_requests': len(recent_requests),
            'recent_success_rate': success_rate_recent,
            'user_agent_profiles': len(self.user_agent_profiles)
        }
    
    def save_config(self):
        """Save current proxy configuration to file"""
        try:
            config = {
                'proxies': [asdict(proxy) for proxy in self.proxies],
                'rotation_settings': {
                    'rotation_interval': 300,
                    'max_failures': 3,
                    'health_check_interval': 60,
                    'request_delay': (1, 3),
                    'max_concurrent_requests': 5
                },
                'anti_detection': {
                    'random_user_agent': True,
                    'random_headers': True,
                    'cookie_management': True,
                    'request_throttling': True,
                    'fingerprint_rotation': True
                }
            }
            
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=2, default=str)
                
            logger.info("Proxy configuration saved")
            
        except Exception as e:
            logger.error(f"Error saving proxy config: {e}")

# Global proxy rotator instance
proxy_rotator = ProxyRotator()

# Convenience functions for external use
async def stealth_request(url: str, **kwargs) -> Tuple[Optional[requests.Response], Optional[str]]:
    """Make stealth request using global proxy rotator"""
    return await proxy_rotator.make_stealth_request(url, **kwargs)

def get_proxy_stats() -> Dict[str, Any]:
    """Get proxy rotation statistics"""
    return proxy_rotator.get_statistics()

async def health_check_all_proxies():
    """Health check all proxies"""
    await proxy_rotator.health_check_proxies()
