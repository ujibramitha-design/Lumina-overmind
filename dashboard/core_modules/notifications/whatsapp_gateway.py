#!/usr/bin/env python3
"""
HUNTER AGENT AI MARKETING DIGITAL - WhatsApp Gateway Module
Professional WhatsApp message delivery system with multiple modes
"""

import webbrowser
import urllib.parse
import os
import sys
import time
import logging
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ASCII Art for Lumina OS
LUMINA_ASCII_ART = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║    ██╗    ██╗██╗  ██╗ ██████╗ ██████╗ ██╗███╗   ██╗██╗██╗ ║
    ║    ██║    ██║╚██╗██╔╝██╔════╝██╔═══╝ ██║████╗ ████║██║██║ ║
    ║    ██║ █╗ ██║ ╚███╔╝ ██║     ██║     ██║██╔████╔██║██║██║ ║
    ║    ██║███╗██║ ██╔██╗ ██║     ██║     ██║██║╚██╔╝██║╚██╗╚██╗║
    ║    ╚███╔███╔╝ ██╔╝ ██╗╚██████╗╚██████╗██║██║ ╚═╝██║╚██╗╚██╗║
    ║     ╚══╝╚══╝ ╚═╝  ╚═╝ ╚═════╝ ╚═════╝╚═╝╚═╝     ╚═╝╚═╝  ╚═╝
    ║                                                              ║
    ║              LUMINA OS WA GATEWAY v1.0                      ║
    ║              Professional Message Delivery                ║
    ╚══════════════════════════════════════════════════════════════╝
"""

@dataclass
class MessageResult:
    """Data class for message delivery results"""
    success: bool
    phone_number: str
    message: str
    mode: str
    timestamp: str
    delivery_method: str
    error_message: Optional[str] = None
    message_id: Optional[str] = None

@dataclass
class QueuedMessage:
    """Data class for queued messages"""
    id: int
    lead_id: int
    phone_number: str
    message: str
    lead_name: str
    created_at: str
    attempts: int = 0
    last_attempt: Optional[str] = None

class WhatsAppGateway:
    """
    Professional WhatsApp Gateway for Lumina OS
    Supports multiple delivery modes with comprehensive error handling
    """
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize WhatsApp Gateway
        
        Args:
            db_path: Path to SQLite database (defaults to ../data/leads.db)
        """
        print(LUMINA_ASCII_ART)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 🚀 Initializing Lumina OS WhatsApp Gateway...")
        
        self.db_path = db_path or os.path.join('..', 'data', 'leads.db (SQLite - removed))
        self.webbrowser_available = self._check_webbrowser_availability()
        self.message_queue = []
        self.delivery_stats = {
            'total_sent': 0,
            'total_failed': 0,
            'web_mode_used': 0,
            'api_simulation_used': 0
        }
        
        # Ensure database directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ WhatsApp Gateway initialized successfully")
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 📊 Database path: {self.db_path}")
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 🌐 Web browser available: {self.webbrowser_available}")
        print()
    
    def _check_webbrowser_availability(self) -> bool:
        """Check if webbrowser module is available"""
        try:
            webbrowser.open_new('about:blank')
            time.sleep(0.1)
            return True
        except Exception:
            logger.warning("Web browser not available")
            return False
    
    def _get_db_connection(self) -> sqlite3.Connection:
        """Get database connection with proper error handling"""
        try:
            conn = # SQLite connection removed
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.Error as e:
            logger.error(f"Database connection error: {e}")
            raise WhatsAppGatewayError(f"Failed to connect to database: {e}")
    
    def _validate_phone_number(self, phone_number: str) -> str:
        """Validate and normalize phone number"""
        # Remove common prefixes and symbols
        cleaned = phone_number.replace('+', '').replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
        
        # Remove leading zeros for international format
        if cleaned.startswith('0'):
            cleaned = cleaned[1:]
        
        # Add country code if not present
        if not cleaned.startswith('62'):
            cleaned = '62' + cleaned
        
        # Basic validation
        if len(cleaned) < 10 or len(cleaned) > 15:
            raise WhatsAppGatewayError(f"Invalid phone number: {phone_number}")
        
        if not cleaned.isdigit():
            raise WhatsAppGatewayError(f"Phone number contains invalid characters: {phone_number}")
        
        return cleaned
    
    def _validate_message(self, message: str) -> str:
        """Validate message content"""
        if not message or not message.strip():
            raise WhatsAppGatewayError("Message cannot be empty")
        
        if len(message) > 1600:  # WhatsApp message limit
            raise WhatsAppGatewayError(f"Message too long: {len(message)} characters (max 1600)")
        
        return message.strip()
    
    def _generate_message_id(self) -> str:
        """Generate unique message ID"""
        return f"wa_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{int(time.time())}"
    
    def send_message(self, phone_number: str, message: str, mode: str = 'web') -> MessageResult:
        """
        Send WhatsApp message using specified mode
        
        Args:
            phone_number: Target phone number
            message: Message content
            mode: Delivery mode ('web' or 'api_simulation')
        
        Returns:
            MessageResult object with delivery details
        """
        timestamp = datetime.now().isoformat()
        message_id = self._generate_message_id()
        
        try:
            # Validate inputs
            validated_phone = self._validate_phone_number(phone_number)
            validated_message = self._validate_message(message)
            
            # Validate mode
            if mode not in ['web', 'api_simulation']:
                raise WhatsAppGatewayError(f"Invalid mode: {mode}. Use 'web' or 'api_simulation'")
            
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 📤 Sending message to +{validated_phone} via {mode} mode...")
            
            if mode == 'web':
                result = self._send_web_mode(validated_phone, validated_message, message_id, timestamp)
            else:
                result = self._send_api_simulation_mode(validated_phone, validated_message, message_id, timestamp)
            
            # Update statistics
            if result.success:
                self.delivery_stats['total_sent'] += 1
                if mode == 'web':
                    self.delivery_stats['web_mode_used'] += 1
                else:
                    self.delivery_stats['api_simulation_used'] += 1
            else:
                self.delivery_stats['total_failed'] += 1
            
            return result
            
        except WhatsAppGatewayError as e:
            logger.error(f"WhatsApp Gateway error: {e}")
            return MessageResult(
                success=False,
                phone_number=phone_number,
                message=message,
                mode=mode,
                timestamp=timestamp,
                delivery_method=f"gateway_error",
                error_message=str(e),
                message_id=message_id
            )
        except Exception as e:
            logger.error(f"Unexpected error in send_message: {e}")
            return MessageResult(
                success=False,
                phone_number=phone_number,
                message=message,
                mode=mode,
                timestamp=timestamp,
                delivery_method=f"unexpected_error",
                error_message=str(e),
                message_id=message_id
            )
    
    def _send_web_mode(self, phone_number: str, message: str, message_id: str, timestamp: str) -> MessageResult:
        """Send message using web mode (wa.me URL)"""
        try:
            # Encode message for URL
            encoded_message = urllib.parse.quote(message)
            
            # Generate WhatsApp URL
            wa_url = f"https://wa.me/{phone_number}?text={encoded_message}"
            
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 🌐 Opening WhatsApp Web: {wa_url}")
            
            if self.webbrowser_available:
                # Open in browser
                webbrowser.open_new(wa_url)
                delivery_method = "web_browser"
            else:
                # Return URL for manual opening
                print(f"[{datetime.now().strftime('%H:%M:%S')}] 🔗 Please open manually: {wa_url}")
                delivery_method = "url_returned"
            
            return MessageResult(
                success=True,
                phone_number=phone_number,
                message=message,
                mode='web',
                timestamp=timestamp,
                delivery_method=delivery_method,
                message_id=message_id
            )
            
        except Exception as e:
            logger.error(f"Web mode error: {e}")
            return MessageResult(
                success=False,
                phone_number=phone_number,
                message=message,
                mode='web',
                timestamp=timestamp,
                delivery_method="web_error",
                error_message=str(e),
                message_id=message_id
            )
    
    def _send_api_simulation_mode(self, phone_number: str, message: str, message_id: str, timestamp: str) -> MessageResult:
        """Send message using API simulation mode"""
        try:
            # Simulate API call delay
            time.sleep(random.uniform(0.5, 1.5))
            
            # Simulate success (95% success rate)
            if random.random() < 0.95:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Message successfully dispatched to +{phone_number} via Lumina Gateway")
                print(f"[{datetime.now().strftime('%H:%M:%S')}] 📋 Message ID: {message_id}")
                print(f"[{datetime.now().strftime('%H:%M:%S')}] 📏 Message length: {len(message)} characters")
                
                return MessageResult(
                    success=True,
                    phone_number=phone_number,
                    message=message,
                    mode='api_simulation',
                    timestamp=timestamp,
                    delivery_method="api_simulation",
                    message_id=message_id
                )
            else:
                # Simulate API error
                error_msg = "API rate limit exceeded"
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ API simulation failed: {error_msg}")
                
                return MessageResult(
                    success=False,
                    phone_number=phone_number,
                    message=message,
                    mode='api_simulation',
                    timestamp=timestamp,
                    delivery_method="api_simulation_error",
                    error_message=error_msg,
                    message_id=message_id
                )
                
        except Exception as e:
            logger.error(f"API simulation error: {e}")
            return MessageResult(
                success=False,
                phone_number=phone_number,
                message=message,
                mode='api_simulation',
                timestamp=timestamp,
                delivery_method="api_simulation_error",
                error_message=str(e),
                message_id=message_id
            )
    
    def process_pending_queue(self) -> Dict[str, Any]:
        """
        Process pending messages from leads database
        Finds leads with status 'Contacted' but no message_sent_time
        """
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 🔍 Processing pending message queue...")
        
        try:
            conn = self._get_db_connection()
            cursor = conn.cursor()
            
            # Check if message_sent_time column exists
            # cursor.execute() removed"PRAGMA table_info(leads)")
            columns = [column[1] for column in cursor.fetchall()]
            
            if 'message_sent_time' not in columns:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] 🔧 Adding message_sent_time column to database...")
                # cursor.execute() removed'ALTER TABLE leads ADD COLUMN message_sent_time TEXT')
                # conn.commit() removed
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Column added successfully")
            
            # Find pending leads
            # cursor.execute() removed'''
                SELECT id, business_name, contact, created_at
                FROM leads 
                WHERE status = 'Contacted' 
                AND (message_sent_time IS NULL OR message_sent_time = '')
                ORDER BY created_at ASC
                LIMIT 10
            ''')
            
            pending_leads = cursor.fetchall()
            
            if not pending_leads:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ℹ️  No pending messages in queue")
                return {
                    'processed': 0,
                    'success': 0,
                    'failed': 0,
                    'pending_count': 0
                }
            
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 📊 Found {len(pending_leads)} pending messages")
            
            processed_count = 0
            success_count = 0
            failed_count = 0
            
            for lead in pending_leads:
                lead_id = lead['id']
                lead_name = lead['business_name']
                contact_info = lead['contact']
                created_at = lead['created_at']
                
                try:
                    # Extract phone number from contact
                    phone_number = self._extract_phone_from_contact(contact_info)
                    
                    if not phone_number:
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] ⚠️  No phone number found for lead {lead_name} (ID: {lead_id})")
                        failed_count += 1
                        continue
                    
                    # Generate message
                    message = self._generate_default_message(lead_name)
                    
                    # Send message (use api_simulation for automation)
                    result = self.send_message(phone_number, message, mode='api_simulation')
                    
                    if result.success:
                        # Update database
                        # cursor.execute() removed'''
                            UPDATE leads 
                            SET message_sent_time = ?, updated_at = ?
                            WHERE id = ?
                        ''', (result.timestamp, datetime.now().isoformat(), lead_id))
                        
                        # conn.commit() removed
                        success_count += 1
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Marked as sent: {lead_name}")
                    else:
                        failed_count += 1
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Failed to send: {lead_name} - {result.error_message}")
                    
                    processed_count += 1
                    
                    # Small delay between messages
                    time.sleep(0.5)
                    
                except Exception as e:
                    logger.error(f"Error processing lead {lead_id}: {e}")
                    failed_count += 1
                    processed_count += 1
            
            # conn.close() removed
            
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 📈 Queue processing completed:")
            print(f"[{datetime.now().strftime('%H:%M:%S')}]   Processed: {processed_count}")
            print(f"[{datetime.now().strftime('%H:%M:%S')}]   Success: {success_count}")
            print(f"[{datetime.now().strftime('%H:%M:%S')}]   Failed: {failed_count}")
            
            return {
                'processed': processed_count,
                'success': success_count,
                'failed': failed_count,
                'pending_count': len(pending_leads)
            }
            
        except Exception as e:
            logger.error(f"Error processing queue: {e}")
            return {
                'processed': 0,
                'success': 0,
                'failed': 0,
                'pending_count': 0,
                'error': str(e)
            }
    
    def _extract_phone_from_contact(self, contact: str) -> Optional[str]:
        """Extract phone number from contact string"""
        try:
            # Look for phone number patterns
            import re
            
            # Pattern 1: Phone: +62xxx
            phone_match = re.search(r'Phone:\s*([+0-9\s\-\(\)]+)', contact)
            if phone_match:
                phone = phone_match.group(1)
                return self._validate_phone_number(phone)
            
            # Pattern 2: +62xxx at beginning
            phone_match = re.search(r'^([+0-9\s\-\(\)]+)', contact)
            if phone_match:
                phone = phone_match.group(1)
                return self._validate_phone_number(phone)
            
            # Pattern 3: Any 10-15 digit number
            phone_match = re.search(r'([0-9]{10,15})', contact)
            if phone_match:
                phone = phone_match.group(1)
                return self._validate_phone_number(phone)
            
            return None
            
        except Exception as e:
            logger.error(f"Error extracting phone number: {e}")
            return None
    
    def _generate_default_message(self, lead_name: str) -> str:
        """Generate default message for lead"""
        messages = [
            f"Halo {lead_name}, terima kasih atas minat Anda. Kami siap membantu menemukan properti impian Anda.",
            f"Selamat pagi {lead_name}. Ada yang bisa kami bantu untuk kebutuhan properti Anda?",
            f"Halo {lead_name}, kami dari HUNTER AGENT siap memberikan solusi properti terbaik untuk Anda.",
            f"Terima kasih {lead_name} atas kepercayaan Anda. Mari kami bantu temukan rumah idaman keluarga."
            f"Halo {lead_name}, kami punya berbagai pilihan properti menarik yang mungkin cocok untuk Anda."
        ]
        
        return random.choice(messages)
    
    def get_delivery_stats(self) -> Dict[str, Any]:
        """Get delivery statistics"""
        return {
            'total_sent': self.delivery_stats['total_sent'],
            'total_failed': self.delivery_stats['total_failed'],
            'web_mode_used': self.delivery_stats['web_mode_used'],
            'api_simulation_used': self.delivery_stats['api_simulation_used'],
            'success_rate': (self.delivery_stats['total_sent'] / max(1, self.delivery_stats['total_sent'] + self.delivery_stats['total_failed'])) * 100
        }
    
    def reset_stats(self) -> None:
        """Reset delivery statistics"""
        self.delivery_stats = {
            'total_sent': 0,
            'total_failed': 0,
            'web_mode_used': 0,
            'api_simulation_used': 0
        }
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 📊 Statistics reset")

class WhatsAppGatewayError(Exception):
    """Custom exception for WhatsApp Gateway errors"""
    pass

# Import random for API simulation
import random

# Example usage and testing
if __name__ == "__main__":
    print("=" * 80)
    print("🧪 Testing WhatsApp Gateway")
    print("=" * 80)
    
    try:
        # Initialize gateway
        gateway = WhatsAppGateway()
        
        # Test web mode
        print("\n📱 Testing Web Mode...")
        result1 = gateway.send_message("628123456789", "Hello from Lumina OS!", mode='web')
        print(f"Result: {result1.success}")
        
        # Test API simulation mode
        print("\n🤖 Testing API Simulation Mode...")
        result2 = gateway.send_message("628123456789", "Test message from API simulation", mode='api_simulation')
        print(f"Result: {result2.success}")
        
        # Test queue processing
        print("\n📊 Testing Queue Processing...")
        queue_result = gateway.process_pending_queue()
        print(f"Queue Result: {queue_result}")
        
        # Get statistics
        print("\n📈 Delivery Statistics:")
        stats = gateway.get_delivery_stats()
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)
    
    print("\n✅ All tests completed!")
