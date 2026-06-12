"""
LUMINA OS - The Invisible Net
====================================

Meta Conversions API Retargeting Engine
Server-side tracking and prospect data injection for digital shadow campaigns

Features:
- Meta Pixel integration with SHA256 hashing
- Asynchronous event sending
- Lead data hashing and injection
- Shadow network monitoring
- Anti-crash error handling
- Compliance-ready data processing
"""

import os
import sys
import requests
import hashlib
import json
import time
import logging
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path

# Add root directory to Python path
root_dir = Path(__file__).parent.parent.parent.parent
sys.path.append(str(root_dir))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ANSI color codes for terminal output
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
BOLD = '\033[1m'
END = '\033[0m'

class MetaConversionAPI:
    """
    Meta Conversions API integration for server-side retargeting
    Handles data hashing, event sending, and shadow network operations
    """
    
    def __init__(self):
        """Initialize Meta Conversion API client"""
        self.logger = logging.getLogger(__name__)
        
        # Load configuration from environment
        self.pixel_id = os.getenv('META_PIXEL_ID', '1234567890123456')
        self.access_token = os.getenv('META_ACCESS_TOKEN', 'EAAGtest_token_1234567890')
        self.api_endpoint = f"https://graph.facebook.com/v19.0/{self.pixel_id}/events"
        
        # Request headers
        self.headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'LuminaOS-ShadowNetwork/1.0'
        }
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 0.1  # 100ms between requests
        
        # Statistics
        self.stats = {
            'total_events_sent': 0,
            'successful_events': 0,
            'failed_events': 0,
            'hashed_leads': 0,
            'last_reset': datetime.now().isoformat()
        }
        
        self.logger.info(f"{CYAN}🕸️ SHADOW NETWORK: Meta Conversion API initialized{END}")
        self.logger.info(f"{GREEN}✅ PIXEL_ID: {self.pixel_id}{END}")
        self.logger.info(f"{GREEN}✅ API Endpoint: {self.api_endpoint}{END}")
    
    def hash_data(self, data: str) -> str:
        """
        Hash data using SHA256 for Meta compliance
        Meta requires PII to be hashed before sending to Pixel
        
        Args:
            data: Raw data string (email, phone, etc.)
            
        Returns:
            SHA256 hashed string
        """
        try:
            # Clean and normalize data
            clean_data = str(data).strip().lower()
            
            # Remove special characters and spaces
            clean_data = ''.join(c for c in clean_data if c.isalnum())
            
            # Create SHA256 hash
            hash_object = hashlib.sha256(clean_data.encode('utf-8'))
            hashed_data = hash_object.hexdigest()
            
            self.logger.debug(f"🔒 Data hashed: {data[:10]}... -> {hashed_data[:8]}...")
            return hashed_data
            
        except Exception as e:
            self.logger.error(f"❌ Hashing error: {str(e)}")
            return ""
    
    def send_lead_event(self, email: str = None, phone: str = None, event_name: str = 'Lead', custom_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Send lead event to Meta Pixel for retargeting
        
        Args:
            email: Lead email address (will be hashed)
            phone: Lead phone number (will be hashed)
            event_name: Event name for tracking
            custom_data: Additional custom data
            
        Returns:
            Dict with event status and details
        """
        try:
            # Rate limiting
            current_time = time.time()
            if current_time - self.last_request_time < self.min_request_interval:
                wait_time = self.min_request_interval - (current_time - self.last_request_time)
                self.logger.warning(f"⏱️ Rate limiting: Waiting {wait_time:.2f}s")
                time.sleep(wait_time)
            
            # Prepare event data
            event_data = {
                "event_name": event_name,
                "event_time": datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
                "action_source": "lumina_os_shadow_network",
                "custom_data": custom_data or {}
            }
            
            # Add hashed PII data
            if email:
                hashed_email = self.hash_data(email)
                event_data["custom_data"]["hashed_email"] = hashed_email
                event_data["custom_data"]["original_email_length"] = len(email)
                self.stats['hashed_leads'] += 1
            
            if phone:
                hashed_phone = self.hash_data(phone)
                event_data["custom_data"]["hashed_phone"] = hashed_phone
                event_data["custom_data"]["original_phone_length"] = len(phone)
                self.stats['hashed_leads'] += 1
            
            # Add system metadata
            event_data["custom_data"]["system"] = "lumina_os"
            event_data["custom_data"]["version"] = "1.0"
            event_data["custom_data"]["timestamp"] = datetime.now().isoformat()
            event_data["custom_data"]["environment"] = os.getenv('ENVIRONMENT', 'development')
            
            # Prepare full request payload
            payload = {
                "data": [event_data]
            }
            
            # Send request to Meta API
            response = requests.post(
                self.api_endpoint,
                headers=self.headers,
                json=payload,
                params={'access_token': self.access_token},
                timeout=30
            )
            
            # Update statistics
            self.stats['total_events_sent'] += 1
            self.last_request_time = time.time()
            
            if response.status_code == 200:
                self.stats['successful_events'] += 1
                self.logger.info(f"{GREEN}✅ SHADOW INJECTION: Event '{event_name}' sent successfully{END}")
                self.logger.info(f"{CYAN}🕸️ SHADOW NETWORK: Prospect data hashed and injected to Meta Pixel. Tracking initiated.{END}")
                
                return {
                    "status": "success",
                    "event_name": event_name,
                    "hashed_email": hashed_email if email else None,
                    "hashed_phone": hashed_phone if phone else None,
                    "response_status": response.status_code,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                self.stats['failed_events'] += 1
                error_data = response.text if response.text else "Unknown error"
                self.logger.error(f"{RED}❌ SHADOW INJECTION FAILED: Status {response.status_code}{END}")
                self.logger.error(f"{RED}❌ Error: {error_data}{END}")
                
                return {
                    "status": "failed",
                    "event_name": event_name,
                    "error": error_data,
                    "response_status": response.status_code,
                    "timestamp": datetime.now().isoformat()
                }
                
        except requests.exceptions.RequestException as e:
            self.stats['failed_events'] += 1
            self.logger.error(f"{RED}❌ NETWORK ERROR: {str(e)}{END}")
            return {
                "status": "network_error",
                "event_name": event_name,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            self.stats['failed_events'] += 1
            self.logger.error(f"{RED}❌ SHADOW INJECTION ERROR: {str(e)}{END}")
            return {
                "status": "error",
                "event_name": event_name,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def send_custom_event(self, event_name: str, custom_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send custom event to Meta Pixel
        
        Args:
            event_name: Custom event name
            custom_data: Custom event data
            
        Returns:
            Dict with event status
        """
        return self.send_lead_event(event_name=event_name, custom_data=custom_data)
    
    def batch_send_events(self, events: list) -> Dict[str, Any]:
        """
        Send multiple events in batch
        
        Args:
            events: List of event dictionaries
            
        Returns:
            Dict with batch status
        """
        try:
            results = []
            successful = 0
            failed = 0
            
            for event in events:
                result = self.send_lead_event(
                    email=event.get('email'),
                    phone=event.get('phone'),
                    event_name=event.get('event_name', 'Lead'),
                    custom_data=event.get('custom_data')
                )
                
                results.append(result)
                
                if result['status'] == 'success':
                    successful += 1
                else:
                    failed += 1
                
                # Small delay between events
                time.sleep(0.2)
            
            self.logger.info(f"{GREEN}✅ BATCH COMPLETE: {successful}/{len(events)} events sent successfully{END}")
            
            return {
                "status": "completed",
                "total_events": len(events),
                "successful": successful,
                "failed": failed,
                "results": results,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"{RED}❌ BATCH ERROR: {str(e)}{END}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get retargeting engine statistics"""
        return {
            **self.stats,
            "success_rate": (self.stats['successful_events'] / max(self.stats['total_events_sent'], 1)) * 100,
            "hash_rate": (self.stats['hashed_leads'] / max(self.stats['total_events_sent'], 1)) * 100,
            "timestamp": datetime.now().isoformat()
        }
    
    def test_connection(self) -> Dict[str, Any]:
        """Test connection to Meta API"""
        try:
            # Send test event
            test_result = self.send_custom_event(
                event_name="ShadowNetworkTest",
                custom_data={
                    "test": True,
                    "system": "lumina_os",
                    "timestamp": datetime.now().isoformat()
                }
            )
            
            if test_result['status'] == 'success':
                self.logger.info(f"{GREEN}✅ CONNECTION TEST: Meta API working correctly{END}")
                return {
                    "status": "connected",
                    "test_result": test_result,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                self.logger.error(f"{RED}❌ CONNECTION TEST FAILED: {test_result.get('error', 'Unknown')}{END}")
                return {
                    "status": "failed",
                    "test_result": test_result,
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            self.logger.error(f"{RED}❌ CONNECTION TEST ERROR: {str(e)}{END}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def reset_statistics(self) -> None:
        """Reset statistics counters"""
        self.stats = {
            'total_events_sent': 0,
            'successful_events': 0,
            'failed_events': 0,
            'hashed_leads': 0,
            'last_reset': datetime.now().isoformat()
        }
        self.logger.info(f"{YELLOW}🔄 STATISTICS RESET: All counters cleared{END}")

# Global retargeting engine instance
retargeting_engine = MetaConversionAPI()

# Convenience functions
def send_lead_to_shadow_network(email: str = None, phone: str = None, event_name: str = 'Lead') -> Dict[str, Any]:
    """
    Convenience function to send lead to shadow network
    
    Args:
        email: Lead email
        phone: Lead phone
        event_name: Event name
        
    Returns:
        Dict with result status
    """
    return retargeting_engine.send_lead_event(email, phone, event_name)

def hash_prospect_data(data: str) -> str:
    """
    Convenience function to hash prospect data
    
    Args:
        data: Data to hash
        
    Returns:
        Hashed string
    """
    return retargeting_engine.hash_data(data)

def get_shadow_network_status() -> Dict[str, Any]:
    """
    Get shadow network status and statistics
    
    Returns:
        Dict with status information
    """
    return retargeting_engine.get_statistics()

# Test function
if __name__ == "__main__":
    print(f"{MAGENTA}{'='*80}{END}")
    print(f"{CYAN}LUMINA OS - THE INVISIBLE NET{END}")
    print(f"{MAGENTA}{'='*80}{END}")
    
    # Test connection
    print(f"{BLUE}🔌 Testing Meta API connection...{END}")
    test_result = retargeting_engine.test_connection()
    
    if test_result['status'] == 'connected':
        print(f"{GREEN}✅ Connection test passed{END}")
        
        # Test lead injection
        print(f"{BLUE}🕸️ Testing lead injection...{END}")
        lead_result = send_lead_to_shadow_network(
            email="test@example.com",
            phone="+62812345678",
            event_name="TestLead"
        )
        
        print(f"{GREEN}✅ Lead injection test completed{END}")
        print(f"Status: {lead_result['status']}")
        
        # Show statistics
        stats = get_shadow_network_status()
        print(f"{CYAN}📊 SHADOW NETWORK STATISTICS:{END}")
        print(f"Total Events: {stats['total_events_sent']}")
        print(f"Successful: {stats['successful_events']}")
        print(f"Failed: {stats['failed_events']}")
        print(f"Success Rate: {stats['success_rate']:.1f}%")
        print(f"Hash Rate: {stats['hash_rate']:.1f}%")
        
    else:
        print(f"{RED}❌ Connection test failed{END}")
        print(f"Error: {test_result.get('error', 'Unknown')}")
    
    print(f"{MAGENTA}{'='*80}{END}")
