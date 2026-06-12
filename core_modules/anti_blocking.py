"""
Anti-Blocking & Stability Module
Menyedi fake-useragent dan rate limiting untuk menghindari blocking
"""

import random
import time
from typing import List, Dict
import logging
from fake_useragent import UserAgent

class AntiBlockingManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # User-Agent pools untuk rotasi
        self.ua = UserAgent()
        self.user_agents = [
            # Chrome Desktop
            self.ua.chrome,
            self.ua.firefox,
            self.ua.safari,
            self.ua.edge,
            
            # Mobile
            self.ua.chrome,
            self.ua.safari,
        ]
        
        # Rate limiting configuration
        self.min_delay = 5  # seconds
        self.max_delay = 10  # seconds
        self.last_request_time = {}
        
        # Request tracking
        self.request_count = 0
        self.blocked_requests = 0
        
    def get_random_user_agent(self) -> str:
        """
        Get random user-agent from pool
        """
        return self.ua.random
    
    def get_headers(self, additional_headers: Dict = None) -> Dict:
        """
        Get headers dengan random user-agent untuk menghindari blocking
        """
        headers = {
            'User-Agent': self.get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'none',
            'Sec-Fetch-Mode': 'navigate',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
        }
        
        # Add any additional headers
        if additional_headers:
            headers.update(additional_headers)
        
        return headers
    
    def rate_limit(self, domain: str = "default") -> None:
        """
        Implement rate limiting dengan random delay
        """
        current_time = time.time()
        
        # Get last request time for this domain
        if domain not in self.last_request_time:
            self.last_request_time[domain] = 0
        
        # Calculate time since last request
        time_since_last = current_time - self.last_request_time[domain]
        
        # If not enough time has passed, wait
        if time_since_last < self.min_delay:
            wait_time = random.uniform(self.min_delay, self.max_delay)
            self.logger.info(f"Rate limiting for {domain}: waiting {wait_time:.2f} seconds")
            time.sleep(wait_time)
        
        # Update last request time
        self.last_request_time[domain] = current_time
        self.request_count += 1
    
    def handle_request_error(self, error: Exception, domain: str = "default") -> bool:
        """
        Handle request error dan implement backoff strategy
        """
        self.blocked_requests += 1
        
        # Log error
        self.logger.error(f"Request error for {domain}: {str(error)}")
        
        # Implement exponential backoff
        backoff_time = min(300, (2 ** self.blocked_requests) * 5)  # Max 5 minutes
        self.logger.info(f"Backing off for {domain}: waiting {backoff_time} seconds")
        
        time.sleep(backoff_time)
        
        # Reset after successful request
        if self.blocked_requests > 10:
            self.blocked_requests = 0
        
        return self.blocked_requests < 10  # Continue if not too many failures
    
    def get_proxy_rotation(self) -> List[Dict]:
        """
        Get proxy configuration for rotation (placeholder for future use)
        """
        # This can be expanded with actual proxy configurations
        return []
    
    def create_session_with_anti_blocking(self, proxy_list: List[Dict] = None) -> object:
        """
        Create session dengan anti-blocking measures
        """
        import requests
        
        session = requests.Session()
        
        # Set headers
        headers = self.get_headers()
        session.headers.update(headers)
        
        # Configure proxy if provided
        if proxy_list:
            proxy = random.choice(proxy_list)
            session.proxies.update({
                'http': proxy.get('http'),
                'https': proxy.get('https')
            })
        
        # Configure retry strategy
        retry_strategy = requests.adapters.HTTPAdapter(
            max_retries=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        
        session.mount('https://', retry_strategy)
        session.mount('http://', retry_strategy)
        
        return session
    
    def validate_response(self, response: object) -> bool:
        """
        Validate response untuk memastikan tidak ada blocking indicators
        """
        # Check for common blocking indicators
        blocking_indicators = [
            'captcha',
            'blocked',
            'forbidden',
            'access denied',
            'rate limited',
            'too many requests',
            'temporarily unavailable'
        ]
        
        content = response.text.lower() if hasattr(response, 'text') else ''
        
        for indicator in blocking_indicators:
            if indicator in content:
                self.logger.warning(f"Blocking indicator detected: {indicator}")
                return False
        
        return True
    
    def log_request_stats(self):
        """
        Log request statistics untuk monitoring
        """
        self.logger.info(f"Request Statistics:")
        self.logger.info(f"  Total Requests: {self.request_count}")
        self.logger.info(f"  Blocked Requests: {self.blocked_requests}")
        self.logger.info(f"  Success Rate: {((self.request_count - self.blocked_requests) / max(1, self.request_count)) * 100:.1f}%")

# Global instance
anti_blocking = AntiBlockingManager()

# Convenience functions
def get_safe_headers(additional_headers: Dict = None) -> Dict:
    """Get headers dengan anti-blocking measures"""
    return anti_blocking.get_headers(additional_headers)

def apply_rate_limit(domain: str = "default") -> None:
    """Apply rate limiting untuk domain tertentu"""
    return anti_blocking.rate_limit(domain)

def create_safe_session(proxy_list: List[Dict] = None) -> object:
    """Create session dengan anti-blocking measures"""
    return anti_blocking.create_session_with_anti_blocking(proxy_list)
