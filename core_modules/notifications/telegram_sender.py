"""
LUMINA OS - Telegram Message Sender Helper
Remote control system for two-way communication via Telegram
"""

import os
import requests
import logging
from typing import Optional, Dict, Any
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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

class TelegramSender:
    """
    Professional Telegram message sender for Lumina OS remote control
    Handles two-way communication with proper error handling and logging
    """
    
    def __init__(self):
        """Initialize Telegram sender with configuration"""
        self.logger = logging.getLogger(__name__)
        
        # Get Telegram configuration
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.default_chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        if not self.bot_token:
            self.logger.error(f"{RED}❌ TELEGRAM CONFIG: BOT TOKEN not found{END}")
            raise ValueError("TELEGRAM_BOT_TOKEN not found in environment variables")
        
        if not self.default_chat_id:
            self.logger.error(f"{RED}❌ TELEGRAM CONFIG: CHAT ID not found{END}")
            raise ValueError("TELEGRAM_CHAT_ID not found in environment variables")
        
        # Telegram API endpoint
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        
        self.logger.info(f"{CYAN}📱 TELEGRAM SENDER: Initialized{END}")
        self.logger.info(f"{GREEN}🔗 API ENDPOINT: {self.api_url}{END}")
        self.logger.info(f"{BLUE}💬 DEFAULT CHAT: {self.default_chat_id}{END}")
    
    def send_message(self, text: str, chat_id: Optional[str] = None, parse_mode: str = "HTML") -> Dict[str, Any]:
        """
        Send message to Telegram chat
        
        Args:
            text: Message text to send (supports HTML formatting)
            chat_id: Target chat ID (uses default if None)
            parse_mode: Message parsing mode (HTML or Markdown)
            
        Returns:
            Dict containing operation result
        """
        try:
            # Use default chat ID if not provided
            target_chat_id = chat_id or self.default_chat_id
            
            # Prepare payload
            payload = {
                'chat_id': target_chat_id,
                'text': text,
                'parse_mode': parse_mode,
                'disable_web_page_preview': False
            }
            
            # Send request to Telegram API
            self.logger.info(f"{CYAN}📤 SENDING: Message to chat {target_chat_id}{END}")
            
            response = requests.post(
                self.api_url,
                json=payload,
                timeout=30,
                headers={'Content-Type': 'application/json'}
            )
            
            # Check response
            if response.status_code == 200:
                result = response.json()
                message_id = result.get('result', {}).get('message_id')
                
                self.logger.info(f"{GREEN}✅ SENT: Message ID {message_id}{END}")
                self.logger.info(f"{CYAN}📊 RESPONSE: {response.status_code} - OK{END}")
                
                return {
                    "success": True,
                    "message_id": message_id,
                    "chat_id": target_chat_id,
                    "status_code": response.status_code,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                error_detail = response.json().get('description', 'Unknown error')
                self.logger.error(f"{RED}❌ FAILED: {response.status_code} - {error_detail}{END}")
                
                return {
                    "success": False,
                    "error": error_detail,
                    "status_code": response.status_code,
                    "timestamp": datetime.now().isoformat()
                }
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"{RED}❌ NETWORK ERROR: {str(e)}{END}")
            return {
                "success": False,
                "error": f"Network error: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"{RED}❌ UNEXPECTED ERROR: {str(e)}{END}")
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def send_status_message(self, status: str, details: str = "") -> Dict[str, Any]:
        """
        Send formatted status message
        
        Args:
            status: Status text (e.g., "ONLINE", "OFFLINE")
            details: Additional status details
            
        Returns:
            Dict containing operation result
        """
        emoji = "🟢" if "ONLINE" in status.upper() else "🔴"
        
        message = f"""
{emoji} <b>LUMINA OS {status}</b>

{details}

<b>Timestamp:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
<i>Remote Control System</i>
        """.strip()
        
        return self.send_message(message)
    
    def send_report_message(self, title: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send formatted report message
        
        Args:
            title: Report title
            data: Report data dictionary
            
        Returns:
            Dict containing operation result
        """
        message = f"""
📊 <b>{title}</b>

{self._format_data(data)}

<b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
<i>Lumina OS Intelligence System</i>
        """.strip()
        
        return self.send_message(message)
    
    def send_command_response(self, command: str, response: str, success: bool = True) -> Dict[str, Any]:
        """
        Send command response message
        
        Args:
            command: Command that was executed
            response: Response message
            success: Whether command was successful
            
        Returns:
            Dict containing operation result
        """
        emoji = "✅" if success else "❌"
        status = "SUCCESS" if success else "FAILED"
        
        message = f"""
{emoji} <b>COMMAND: {command}</b>

<b>Status:</b> {status}
<b>Response:</b> {response}

<b>Executed:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
<i>Lumina OS Remote Control</i>
        """.strip()
        
        return self.send_message(message)
    
    def send_help_message(self) -> Dict[str, Any]:
        """
        Send help menu message
        
        Returns:
            Dict containing operation result
        """
        help_message = """
🤖 <b>LUMINA OS REMOTE CONTROL</b>

<b>Available Commands:</b>

🟢 <b>/status</b> - Check system status
📊 <b>/report</b> - Get daily intelligence report
🚀 <b>/hunt</b> - Start lead hunting mission
🔍 <b>/scan</b> - Quick market scan
⚙️ <b>/config</b> - System configuration
📈 <b>/stats</b> - Performance statistics
🗄️ <b>/backup</b> - Database backup
🔄 <b>/restart</b> - Restart system services
🛑️ <b>/stop</b> - Stop active operations
❓ <b>/help</b> - Show this help menu

<b>Examples:</b>
<code>/status</code> - Check if system is online
<code>/hunt</code> - Start lead generation
<code>/report</code> - Get today's results

<i>Type any command to execute remotely</i>
        """.strip()
        
        return self.send_message(help_message)
    
    def _format_data(self, data: Dict[str, Any]) -> str:
        """
        Format data dictionary for Telegram message
        
        Args:
            data: Data dictionary to format
            
        Returns:
            Formatted string
        """
        formatted_lines = []
        
        for key, value in data.items():
            if isinstance(value, (int, float)):
                formatted_lines.append(f"<b>{key}:</b> {value:,}")
            elif isinstance(value, str):
                formatted_lines.append(f"<b>{key}:</b> {value}")
            elif isinstance(value, bool):
                formatted_lines.append(f"<b>{key}:</b> {'✅ Yes' if value else '❌ No'}")
            elif isinstance(value, list):
                formatted_lines.append(f"<b>{key}:</b> {len(value)} items")
            elif isinstance(value, dict):
                formatted_lines.append(f"<b>{key}:</b> {len(value)} entries")
            else:
                formatted_lines.append(f"<b>{key}:</b> {str(value)}")
        
        return "\n".join(formatted_lines)
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test Telegram connection
        
        Returns:
            Dict containing test result
        """
        try:
            test_message = f"""
🧪 <b>CONNECTION TEST</b>

Lumina OS Remote Control System is <b>ONLINE</b>

<b>Bot Token:</b> {self.bot_token[:10]}...
<b>Chat ID:</b> {self.default_chat_id}
<b>API Endpoint:</b> Working

<b>Test Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
<i>System Ready for Remote Control</i>
            """.strip()
            
            result = self.send_message(test_message)
            
            if result['success']:
                self.logger.info(f"{GREEN}✅ CONNECTION TEST: SUCCESS{END}")
                return {
                    "success": True,
                    "message": "Telegram connection working",
                    "details": result
                }
            else:
                self.logger.error(f"{RED}❌ CONNECTION TEST: FAILED{END}")
                return {
                    "success": False,
                    "message": "Telegram connection failed",
                    "error": result.get('error')
                }
                
        except Exception as e:
            self.logger.error(f"{RED}❌ CONNECTION TEST ERROR: {str(e)}{END}")
            return {
                "success": False,
                "message": "Connection test failed",
                "error": str(e)
            }

# Global telegram sender instance
telegram_sender = None

def get_telegram_sender() -> TelegramSender:
    """Get or create telegram sender instance"""
    global telegram_sender
    if telegram_sender is None:
        try:
            telegram_sender = TelegramSender()
        except Exception as e:
            logger.error(f"Failed to initialize Telegram sender: {e}")
            raise
    return telegram_sender

# Convenience functions
def send_message(text: str, chat_id: Optional[str] = None) -> Dict[str, Any]:
    """Send message using global telegram sender"""
    sender = get_telegram_sender()
    return sender.send_message(text, chat_id)

def send_status_message(status: str, details: str = "") -> Dict[str, Any]:
    """Send status message using global telegram sender"""
    sender = get_telegram_sender()
    return sender.send_status_message(status, details)

def send_report_message(title: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Send report message using global telegram sender"""
    sender = get_telegram_sender()
    return sender.send_report_message(title, data)

def send_help_message() -> Dict[str, Any]:
    """Send help message using global telegram sender"""
    sender = get_telegram_sender()
    return sender.send_help_message()

def test_telegram_connection() -> Dict[str, Any]:
    """Test telegram connection using global telegram sender"""
    sender = get_telegram_sender()
    return sender.test_connection()

if __name__ == "__main__":
    # Test telegram sender
    print(f"{MAGENTA}{'='*60}{END}")
    print(f"{CYAN}LUMINA OS - TELEGRAM MESSAGE SENDER{END}")
    print(f"{MAGENTA}{'='*60}{END}")
    
    try:
        sender = get_telegram_sender()
        test_result = sender.test_connection()
        
        if test_result["success"]:
            print(f"{GREEN}✅ TELEGRAM CONNECTION: SUCCESS{END}")
            print(f"{CYAN}📱 BOT READY: Remote control system online{END}")
        else:
            print(f"{RED}❌ TELEGRAM CONNECTION: FAILED{END}")
            print(f"{RED}🔥 ERROR: {test_result.get('error')}{END}")
            
    except Exception as e:
        print(f"{RED}❌ INITIALIZATION FAILED: {str(e)}{END}")
    
    print(f"{MAGENTA}{'='*60}{END}")
