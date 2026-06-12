"""
Alert Manager Module - Telegram Bot Integration
Mengirim notifikasi high-intent leads ke Telegram untuk immediate action
"""

import os
import json
import requests
import logging
from datetime import datetime
from typing import Dict, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AlertManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Telegram configuration from environment
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        # Validate configuration
        self.is_configured = bool(self.bot_token and self.chat_id)
        
        if not self.is_configured:
            self.logger.warning("Telegram Bot not configured. Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env file")
        else:
            self.logger.info("Telegram Bot Alert Manager initialized successfully")
        
        # API endpoint
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
    
    def send_telegram_alert(self, lead_data: Dict) -> bool:
        """
        Mengirim alert ke Telegram untuk high-intent lead
        
        Args:
            lead_data: Dict containing lead information
            
        Returns:
            bool: True if alert sent successfully, False otherwise
        """
        if not self.is_configured:
            self.logger.error("Telegram Bot not configured. Cannot send alert.")
            return False
        
        try:
            # Prepare alert message
            message = self._format_alert_message(lead_data)
            
            # Prepare API payload
            payload = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': 'HTML',
                'disable_web_page_preview': False
            }
            
            # Send request to Telegram API
            response = requests.post(self.api_url, json=payload, timeout=30)
            
            # Check response
            if response.status_code == 200:
                result = response.json()
                if result.get('ok'):
                    self.logger.info(f"Telegram alert sent successfully for lead: {lead_data.get('title', 'Unknown')}")
                    return True
                else:
                    error_msg = result.get('description', 'Unknown error')
                    self.logger.error(f"Telegram API error: {error_msg}")
                    return False
            else:
                self.logger.error(f"HTTP error sending Telegram alert: {response.status_code} - {response.text}")
                return False
                
        except requests.exceptions.Timeout:
            self.logger.error("Timeout sending Telegram alert")
            return False
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request error sending Telegram alert: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error sending Telegram alert: {e}")
            return False
    
    def _format_alert_message(self, lead_data: Dict) -> str:
        """
        Format alert message untuk Telegram
        """
        try:
            # Extract lead information
            title = lead_data.get('title', 'Unknown Title')
            source = lead_data.get('source', 'Unknown Source')
            score = lead_data.get('elite_score', lead_data.get('score', 0))
            url = lead_data.get('url', '')
            lead_type = lead_data.get('lead_type', 'unknown')
            location = lead_data.get('location', 'Unknown')
            timestamp = lead_data.get('timestamp', lead_data.get('date_found', datetime.now().isoformat()))
            
            # Format timestamp
            try:
                if isinstance(timestamp, str):
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    formatted_time = str(timestamp)
            except:
                formatted_time = str(timestamp)
            
            # Build message
            message_parts = [
                "🎯 <b>HIGH INTENT LEAD ALERT</b>",
                "",
                f"<b>Title:</b> {title}",
                f"<b>Score:</b> {score}/10",
                f"<b>Type:</b> {lead_type.title()}",
                f"<b>Location:</b> {location}",
                f"<b>Source:</b> {source}",
                f"<b>Time:</b> {formatted_time}",
            ]
            
            # Add URL if available
            if url:
                message_parts.extend([
                    "",
                    f"<b>🔗 Link:</b> <a href='{url}'>View Lead</a>"
                ])
            
            # Add contact info if available
            contact_info = lead_data.get('contact_info', {})
            if contact_info:
                phone_numbers = contact_info.get('phone_numbers', [])
                emails = contact_info.get('emails', [])
                
                if phone_numbers:
                    message_parts.append(f"<b>📱 Phone:</b> {phone_numbers[0]}")
                
                if emails:
                    message_parts.append(f"<b>📧 Email:</b> {emails[0]}")
            
            # Add urgency indicator
            if score >= 9:
                urgency = "🔥 URGENT - Immediate Action Required!"
            elif score >= 8:
                urgency = "⚡ HIGH PRIORITY - Contact ASAP!"
            else:
                urgency = "📋 Follow Up Recommended"
            
            message_parts.extend([
                "",
                f"<b>{urgency}</b>",
                "",
                "——",
                f"<i>Professional Elite Hunter System</i>",
                f"<i>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>"
            ])
            
            return '\n'.join(message_parts)
            
        except Exception as e:
            self.logger.error(f"Error formatting alert message: {e}")
            return f"🎯 HIGH INTENT LEAD ALERT\n\nTitle: {lead_data.get('title', 'Unknown')}\nScore: {lead_data.get('score', 0)}/10\n\nError formatting message: {e}"
    
    def send_test_alert(self) -> bool:
        """
        Mengirim test alert untuk verifikasi konfigurasi
        """
        test_lead = {
            'title': 'Test Lead - Professional Elite Hunter',
            'source': 'Test System',
            'score': 10,
            'elite_score': 10,
            'lead_type': 'test',
            'location': 'Test Location',
            'url': 'https://example.com/test',
            'timestamp': datetime.now().isoformat(),
            'contact_info': {
                'phone_numbers': ['+62812345678'],
                'emails': ['test@example.com']
            }
        }
        
        return self.send_telegram_alert(test_lead)
    
    def check_telegram_connection(self) -> Dict:
        """
        Check koneksi ke Telegram Bot
        """
        if not self.is_configured:
            return {
                'status': 'error',
                'message': 'Telegram Bot not configured. Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env file'
            }
        
        try:
            # Check bot info
            info_url = f"https://api.telegram.org/bot{self.bot_token}/getMe"
            response = requests.get(info_url, timeout=10)
            
            if response.status_code == 200:
                bot_info = response.json()
                if bot_info.get('ok'):
                    bot_name = bot_info.get('result', {}).get('first_name', 'Unknown')
                    return {
                        'status': 'success',
                        'message': f'Connected to Telegram Bot: {bot_name}',
                        'bot_info': bot_info.get('result', {})
                    }
                else:
                    return {
                        'status': 'error',
                        'message': f"Telegram Bot API error: {bot_info.get('description', 'Unknown error')}"
                    }
            else:
                return {
                    'status': 'error',
                    'message': f"HTTP error: {response.status_code} - {response.text}"
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'message': f"Connection error: {str(e)}"
            }
    
    def get_alert_statistics(self) -> Dict:
        """
        Get alert statistics (placeholder for future enhancement)
        """
        return {
            'total_alerts_sent': 0,  # This could be tracked in database
            'alerts_today': 0,
            'alerts_this_week': 0,
            'last_alert_time': None,
            'telegram_status': 'connected' if self.is_configured else 'not_configured'
        }

# Global alert manager instance
alert_manager = AlertManager()

# Convenience functions
def send_high_intent_alert(lead_data: Dict) -> bool:
    """
    Convenience function to send alert for high-intent lead (score >= 8)
    """
    score = lead_data.get('elite_score', lead_data.get('score', 0))
    
    if score >= 8:
        return alert_manager.send_telegram_alert(lead_data)
    else:
        # Log low score leads for debugging
        logging.getLogger(__name__).debug(f"Lead score {score} < 8, not sending alert")
        return True

def send_test_alert() -> bool:
    """Convenience function to send test alert"""
    return alert_manager.send_test_alert()

def check_telegram_status() -> Dict:
    """Convenience function to check Telegram status"""
    return alert_manager.check_telegram_connection()

if __name__ == "__main__":
    # Test the alert manager
    logging.basicConfig(level=logging.INFO)
    
    print("=== Telegram Alert Manager Test ===")
    
    # Check configuration
    status = alert_manager.check_telegram_connection()
    print(f"Telegram Status: {status}")
    
    # Send test alert if configured
    if status.get('status') == 'success':
        print("\nSending test alert...")
        test_result = alert_manager.send_test_alert()
        print(f"Test alert result: {'Success' if test_result else 'Failed'}")
    else:
        print("\nPlease configure TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env file")
        print("Get your bot token from @BotFather on Telegram")
