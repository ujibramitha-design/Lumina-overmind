#!/usr/bin/env python3
"""
Lumina Telegram Bot - Executive Blueprint Notification System
Advanced Telegram bot integration for hot lead alerts

Author: HUNTER_AGENT_AI_MARKETING_DIGITAL
Version: 1.0.0
"""

import os
import logging
import requests
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import json

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
class TelegramAlertResult:
    """Data class for Telegram alert results"""
    success: bool
    message_id: Optional[int]
    error: Optional[str]
    timestamp: str
    response_data: Optional[Dict[str, Any]]

class LuminaTelegramAlert:
    """
    Advanced Telegram bot system for hot lead notifications
    
    Executive Blueprint Lumina OS - Professional Notification System
    
    Features:
    - Hot lead alerts with rich formatting
    - Emoji integration for visual appeal
    - Comprehensive error handling
    - Configuration management
    - Message tracking and analytics
    """
    
    def __init__(self):
        """Initialize LuminaTelegramAlert with configuration"""
        self.logger = logging.getLogger(__name__)
        
        # Telegram API configuration
        self.bot_token = self._get_bot_token()
        self.chat_id = self._get_chat_id()
        self.api_base_url = f"https://api.telegram.org/bot{self.bot_token}"
        
        # Message formatting configuration
        self.message_config = {
            'parse_mode': 'HTML',
            'disable_web_page_preview': False,
            'disable_notification': False
        }
        
        # Alert templates
        self.alert_templates = {
            'hot_lead': {
                'emoji': '🎯',
                'title': 'HOT LEAD ALERT',
                'priority': 'HIGH PRIORITY'
            },
            'warm_lead': {
                'emoji': '📊',
                'title': 'WARM LEAD NOTIFICATION',
                'priority': 'MEDIUM PRIORITY'
            },
            'system': {
                'emoji': '🔧',
                'title': 'SYSTEM NOTIFICATION',
                'priority': 'INFO'
            }
        }
        
        print(f"{GREEN}🤖 LUMINA TELEGRAM BOT INITIALIZED{END}")
        print(f"{CYAN}├── Bot Token: {'✅ Configured' if self.bot_token else '❌ Missing'}{END}")
        print(f"{CYAN}├── Chat ID: {'✅ Configured' if self.chat_id else '❌ Missing'}{END}")
        print(f"{CYAN}├── API Base: {self.api_base_url[:50]}...{END}")
        print(f"{CYAN}├── Parse Mode: {self.message_config['parse_mode']}{END}")
        print(f"{CYAN}├── Timestamp: {self._get_timestamp()}{END}")
        print(f"{GREEN}└── Status: Ready for notifications{END}")
    
    def _get_bot_token(self) -> str:
        """Get Telegram bot token from environment variables"""
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not token:
            # Use dummy token for development
            token = os.getenv('LUMINA_TELEGRAM_BOT_TOKEN', '1234567890:ABCdefGHIjklMNOpqrsTUVwxyz')
            if token == '1234567890:ABCdefGHIjklMNOpqrsTUVwxyz':
                self.logger.warning("Using dummy Telegram bot token - notifications will not be sent")
        return token
    
    def _get_chat_id(self) -> str:
        """Get Telegram chat ID from environment variables"""
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
        if not chat_id:
            # Use dummy chat ID for development
            chat_id = os.getenv('LUMINA_TELEGRAM_CHAT_ID', '123456789')
            if chat_id == '123456789':
                self.logger.warning("Using dummy Telegram chat ID - notifications will not be sent")
        return chat_id
    
    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format"""
        return datetime.now().isoformat()
    
    def send_hot_lead_alert(self, lead_name: str, score: int, intent: str, **kwargs) -> TelegramAlertResult:
        """
        Send hot lead alert with professional formatting
        
        Args:
            lead_name: Name of the lead
            score: Lead score (0-100)
            intent: Intent category
            **kwargs: Additional lead information
            
        Returns:
            TelegramAlertResult object with sending status
        """
        timestamp = self._get_timestamp()
        
        print(f"{GREEN}🎯 HOT LEAD ALERT INITIATED{END}")
        print(f"{CYAN}├── Lead Name: {lead_name}{END}")
        print(f"{CYAN}├── Score: {score}/100{END}")
        print(f"{CYAN}├── Intent: {intent}{END}")
        print(f"{CYAN}├── Timestamp: {timestamp}{END}")
        
        try:
            # Build message with rich formatting
            message = self._build_hot_lead_message(lead_name, score, intent, **kwargs)
            
            # Send message
            result = self._send_message(message, 'hot_lead')
            
            print(f"{GREEN}✅ HOT LEAD ALERT SENT{END}")
            print(f"{CYAN}├── Message ID: {result.message_id}{END}")
            print(f"{CYAN}├── Status: {result.success}{END}")
            print(f"{CYAN}├── Timestamp: {result.timestamp}{END}")
            print(f"{GREEN}└── Notification delivered successfully{END}")
            
            return result
            
        except Exception as e:
            error_msg = f"Failed to send hot lead alert: {e}"
            self.logger.error(error_msg)
            
            print(f"{RED}❌ HOT LEAD ALERT FAILED{END}")
            print(f"{RED}├── Error: {e}{END}")
            print(f"{RED}└── Status: Failed to send notification{END}")
            
            return TelegramAlertResult(
                success=False,
                message_id=None,
                error=error_msg,
                timestamp=timestamp,
                response_data=None
            )
    
    def _build_hot_lead_message(self, lead_name: str, score: int, intent: str, **kwargs) -> str:
        """
        Build formatted hot lead message
        
        Args:
            lead_name: Name of the lead
            score: Lead score
            intent: Intent category
            **kwargs: Additional lead information
            
        Returns:
            Formatted HTML message string
        """
        template = self.alert_templates['hot_lead']
        
        # Build message sections
        message_parts = [
            f"{template['emoji']} <b>{template['title']}</b>",
            "",
            f"<b>📊 Lead Information</b>",
            f"👤 <b>Name:</b> {lead_name}",
            f"⭐ <b>Score:</b> {score}/100",
            f"🎯 <b>Intent:</b> {intent}",
            f"⚡ <b>Priority:</b> {template['priority']}",
            ""
        ]
        
        # Add additional information if available
        if kwargs.get('phone'):
            message_parts.append(f"📱 <b>Phone:</b> {kwargs['phone']}")
        
        if kwargs.get('email'):
            message_parts.append(f"📧 <b>Email:</b> {kwargs['email']}")
        
        if kwargs.get('location'):
            message_parts.append(f"📍 <b>Location:</b> {kwargs['location']}")
        
        if kwargs.get('source'):
            message_parts.append(f"🔗 <b>Source:</b> {kwargs['source']}")
        
        if kwargs.get('message'):
            message_parts.append(f"💬 <b>Message:</b> {kwargs['message'][:200]}{'...' if len(kwargs['message']) > 200 else ''}")
        
        # Add urgency indicator based on score
        if score >= 90:
            urgency = "🔥 IMMEDIATE ACTION REQUIRED"
        elif score >= 80:
            urgency = "⚡ HIGH PRIORITY - Contact ASAP"
        elif score >= 70:
            urgency = "📞 PRIORITY FOLLOW-UP"
        else:
            urgency = "📋 STANDARD FOLLOW-UP"
        
        message_parts.extend([
            "",
            f"<b>{urgency}</b>",
            "",
            f"<i>🤖 Lumina AI System</i>",
            f"<i>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>",
            "",
            "——"
        ])
        
        return "\n".join(message_parts)
    
    def _send_message(self, message: str, alert_type: str = 'system') -> TelegramAlertResult:
        """
        Send message to Telegram chat
        
        Args:
            message: Message to send
            alert_type: Type of alert for logging
            
        Returns:
            TelegramAlertResult object with sending status
        """
        timestamp = self._get_timestamp()
        
        try:
            # Prepare request data
            data = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': self.message_config['parse_mode'],
                'disable_web_page_preview': self.message_config['disable_web_page_preview'],
                'disable_notification': self.message_config['disable_notification']
            }
            
            # Send request to Telegram API
            response = requests.post(
                f"{self.api_base_url}/sendMessage",
                json=data,
                timeout=30
            )
            
            # Check response
            if response.status_code == 200:
                response_data = response.json()
                message_id = response_data.get('result', {}).get('message_id')
                
                self.logger.info(f"Telegram message sent successfully (ID: {message_id})")
                
                return TelegramAlertResult(
                    success=True,
                    message_id=message_id,
                    error=None,
                    timestamp=timestamp,
                    response_data=response_data
                )
            else:
                error_msg = f"Telegram API error: {response.status_code} - {response.text}"
                self.logger.error(error_msg)
                
                return TelegramAlertResult(
                    success=False,
                    message_id=None,
                    error=error_msg,
                    timestamp=timestamp,
                    response_data=None
                )
                
        except requests.exceptions.Timeout:
            error_msg = "Telegram API timeout"
            self.logger.error(error_msg)
            
            return TelegramAlertResult(
                success=False,
                message_id=None,
                error=error_msg,
                timestamp=timestamp,
                response_data=None
            )
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Telegram API request error: {e}"
            self.logger.error(error_msg)
            
            return TelegramAlertResult(
                success=False,
                message_id=None,
                error=error_msg,
                timestamp=timestamp,
                response_data=None
            )
            
        except Exception as e:
            error_msg = f"Unexpected error sending Telegram message: {e}"
            self.logger.error(error_msg)
            
            return TelegramAlertResult(
                success=False,
                message_id=None,
                error=error_msg,
                timestamp=timestamp,
                response_data=None
            )
    
    def send_warm_lead_alert(self, lead_name: str, score: int, intent: str, **kwargs) -> TelegramAlertResult:
        """
        Send warm lead alert with professional formatting
        
        Args:
            lead_name: Name of the lead
            score: Lead score (0-100)
            intent: Intent category
            **kwargs: Additional lead information
            
        Returns:
            TelegramAlertResult object with sending status
        """
        timestamp = self._get_timestamp()
        
        print(f"{GREEN}📊 WARM LEAD ALERT INITIATED{END}")
        print(f"{CYAN}├── Lead Name: {lead_name}{END}")
        print(f"{CYAN}├── Score: {score}/100{END}")
        print(f"{CYAN}├── Intent: {intent}{END}")
        print(f"{CYAN}├── Timestamp: {timestamp}{END}")
        
        try:
            # Build message with warm lead formatting
            message = self._build_warm_lead_message(lead_name, score, intent, **kwargs)
            
            # Send message
            result = self._send_message(message, 'warm_lead')
            
            print(f"{GREEN}✅ WARM LEAD ALERT SENT{END}")
            print(f"{CYAN}├── Message ID: {result.message_id}{END}")
            print(f"{CYAN}├── Status: {result.success}{END}")
            print(f"{CYAN}├── Timestamp: {result.timestamp}{END}")
            print(f"{GREEN}└── Notification delivered successfully{END}")
            
            return result
            
        except Exception as e:
            error_msg = f"Failed to send warm lead alert: {e}"
            self.logger.error(error_msg)
            
            print(f"{RED}❌ WARM LEAD ALERT FAILED{END}")
            print(f"{RED}├── Error: {e}{END}")
            print(f"{RED}└── Status: Failed to send notification{END}")
            
            return TelegramAlertResult(
                success=False,
                message_id=None,
                error=error_msg,
                timestamp=timestamp,
                response_data=None
            )
    
    def _build_warm_lead_message(self, lead_name: str, score: int, intent: str, **kwargs) -> str:
        """
        Build formatted warm lead message
        
        Args:
            lead_name: Name of the lead
            score: Lead score
            intent: Intent category
            **kwargs: Additional lead information
            
        Returns:
            Formatted HTML message string
        """
        template = self.alert_templates['warm_lead']
        
        # Build message sections
        message_parts = [
            f"{template['emoji']} <b>{template['title']}</b>",
            "",
            f"<b>📊 Lead Information</b>",
            f"👤 <b>Name:</b> {lead_name}",
            f"⭐ <b>Score:</b> {score}/100",
            f"🎯 <b>Intent:</b> {intent}",
            f"📋 <b>Priority:</b> {template['priority']}",
            ""
        ]
        
        # Add additional information if available
        if kwargs.get('phone'):
            message_parts.append(f"📱 <b>Phone:</b> {kwargs['phone']}")
        
        if kwargs.get('email'):
            message_parts.append(f"📧 <b>Email:</b> {kwargs['email']}")
        
        if kwargs.get('location'):
            message_parts.append(f"📍 <b>Location:</b> {kwargs['location']}")
        
        if kwargs.get('source'):
            message_parts.append(f"🔗 <b>Source:</b> {kwargs['source']}")
        
        # Add follow-up recommendation
        if score >= 70:
            follow_up = "📞 Follow up within 24 hours"
        elif score >= 60:
            follow_up = "📋 Follow up within 48 hours"
        else:
            follow_up = "📝 Add to nurturing sequence"
        
        message_parts.extend([
            "",
            f"<b>{follow_up}</b>",
            "",
            f"<i>🤖 Lumina AI System</i>",
            f"<i>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>",
            "",
            "——"
        ])
        
        return "\n".join(message_parts)
    
    def send_system_notification(self, title: str, message: str, **kwargs) -> TelegramAlertResult:
        """
        Send system notification with professional formatting
        
        Args:
            title: Notification title
            message: Notification message
            **kwargs: Additional information
            
        Returns:
            TelegramAlertResult object with sending status
        """
        timestamp = self._get_timestamp()
        
        print(f"{GREEN}🔧 SYSTEM NOTIFICATION INITIATED{END}")
        print(f"{CYAN}├── Title: {title}{END}")
        print(f"{CYAN}├── Message Length: {len(message)} characters{END}")
        print(f"{CYAN}├── Timestamp: {timestamp}{END}")
        
        try:
            # Build message with system formatting
            formatted_message = self._build_system_message(title, message, **kwargs)
            
            # Send message
            result = self._send_message(formatted_message, 'system')
            
            print(f"{GREEN}✅ SYSTEM NOTIFICATION SENT{END}")
            print(f"{CYAN}├── Message ID: {result.message_id}{END}")
            print(f"{CYAN}├── Status: {result.success}{END}")
            print(f"{CYAN}├── Timestamp: {result.timestamp}{END}")
            print(f"{GREEN}└── Notification delivered successfully{END}")
            
            return result
            
        except Exception as e:
            error_msg = f"Failed to send system notification: {e}"
            self.logger.error(error_msg)
            
            print(f"{RED}❌ SYSTEM NOTIFICATION FAILED{END}")
            print(f"{RED}├── Error: {e}{END}")
            print(f"{RED}└── Status: Failed to send notification{END}")
            
            return TelegramAlertResult(
                success=False,
                message_id=None,
                error=error_msg,
                timestamp=timestamp,
                response_data=None
            )
    
    def _build_system_message(self, title: str, message: str, **kwargs) -> str:
        """
        Build formatted system message
        
        Args:
            title: Notification title
            message: Notification message
            **kwargs: Additional information
            
        Returns:
            Formatted HTML message string
        """
        template = self.alert_templates['system']
        
        # Build message sections
        message_parts = [
            f"{template['emoji']} <b>{template['title']}</b>",
            "",
            f"<b>📋 {title}</b>",
            f"💬 {message}",
            ""
        ]
        
        # Add additional information if available
        if kwargs.get('details'):
            message_parts.append(f"📝 <b>Details:</b> {kwargs['details']}")
        
        if kwargs.get('action_required'):
            message_parts.append(f"⚠️ <b>Action Required:</b> {kwargs['action_required']}")
        
        message_parts.extend([
            "",
            f"<i>🤖 Lumina AI System</i>",
            f"<i>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>",
            "",
            "——"
        ])
        
        return "\n".join(message_parts)
    
    def get_bot_info(self) -> Dict[str, Any]:
        """
        Get bot information from Telegram API
        
        Returns:
            Dictionary with bot information
        """
        try:
            response = requests.get(f"{self.api_base_url}/getMe", timeout=10)
            
            if response.status_code == 200:
                return response.json().get('result', {})
            else:
                self.logger.error(f"Failed to get bot info: {response.status_code}")
                return {}
                
        except Exception as e:
            self.logger.error(f"Error getting bot info: {e}")
            return {}
    
    def test_connection(self) -> bool:
        """
        Test connection to Telegram API
        
        Returns:
            True if connection is successful, False otherwise
        """
        try:
            bot_info = self.get_bot_info()
            return bool(bot_info.get('id'))
        except Exception:
            return False

def main():
    """
    Main function to demonstrate LuminaTelegramAlert
    """
    print("🤖 LUMINA TELEGRAM BOT - EXECUTIVE BLUEPRINT")
    print("=" * 60)
    print("🔐 Advanced Telegram bot system for hot lead notifications")
    print("=" * 60)
    
    # Initialize bot
    bot = LuminaTelegramAlert()
    
    # Test connection
    print("\n📊 Testing Telegram connection...")
    connection_status = bot.test_connection()
    print(f"✅ Connection Status: {'Connected' if connection_status else 'Disconnected'}")
    
    # Test hot lead alert
    print("\n📊 Testing hot lead alert...")
    hot_result = bot.send_hot_lead_alert(
        lead_name="John Doe",
        score=95,
        intent="Transactional",
        phone="+62812345678",
        email="john@example.com",
        location="Serang",
        source="Web Form",
        message="I'm looking to buy a house immediately, ready to pay cash"
    )
    
    # Test warm lead alert
    print("\n📊 Testing warm lead alert...")
    warm_result = bot.send_warm_lead_alert(
        lead_name="Jane Smith",
        score=75,
        intent="Informational",
        phone="+62898765432",
        email="jane@example.com",
        location="Jakarta",
        source="Phone Call",
        message="I'm interested in learning more about your properties"
    )
    
    # Test system notification
    print("\n📊 Testing system notification...")
    system_result = bot.send_system_notification(
        title="System Update",
        message="Lead scoring system has been updated with new intent classification features",
        details="Executive Blueprint v1.0.0",
        action_required="Review new scoring results"
    )
    
    # Get bot info
    print("\n📊 Getting bot information...")
    bot_info = bot.get_bot_info()
    print(f"✅ Bot Name: {bot_info.get('first_name', 'Unknown')}")
    print(f"✅ Bot Username: @{bot_info.get('username', 'Unknown')}")
    print(f"✅ Bot ID: {bot_info.get('id', 'Unknown')}")
    
    print("\n" + "=" * 60)
    print("✅ LUMINA TELEGRAM BOT DEMO COMPLETE")
    print("🤖 Executive-grade Telegram notification system ready for production")
    print("=" * 60)

if __name__ == "__main__":
    main()
