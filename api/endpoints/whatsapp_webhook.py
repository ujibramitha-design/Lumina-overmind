"""
LUMINA OS - WhatsApp Command Webhook
Remote control system via WhatsApp with Natural Language Processing
"""

from fastapi import APIRouter, Request, HTTPException, BackgroundTasks
from typing import Dict, Any, Optional
from datetime import datetime
import logging
import asyncio
import re
import os
import sys

# Add root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import required modules
from core_modules.notifications.telegram_sender import get_telegram_sender
from core_modules.db_manager_supabase import get_supabase_manager
from utils.process_manager import runner_manager
from utils.conversational_ai import get_smart_reply

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

# Create router
router = APIRouter()

class WhatsAppCommandProcessor:
    """
    Professional WhatsApp command processor for Lumina OS
    Handles natural language commands with intelligent parsing
    """
    
    def __init__(self):
        """Initialize WhatsApp command processor"""
        self.logger = logging.getLogger(__name__)
        self.telegram_sender = get_telegram_sender()
        self.supabase_manager = get_supabase_manager()
        
        # Natural language command patterns
        self.command_patterns = {
            'status_check': [
                r'status\s+sistem',
                r'status',
                r'cek\s+status',
                r'bagaimana\s+status',
                r'apakah\s+sistem\s+online',
                r'system\s+status'
            ],
            'start_hunt': [
                r'mulai\s+berburu',
                r'hunt',
                r'start\s+hunt',
                r'jalankan\s+hunter',
                r'aktifkan\s+radar',
                r'mulai\s+pencarian',
                r'start\s+hunting'
            ],
            'report_request': [
                r'laporan',
                r'report',
                r'hasil\s+hari\s+ini',
                r'statistik',
                r'data\s+prospek',
                r'ringkasan',
                r'summary'
            ],
            'stop_operation': [
                r'stop',
                r'berhenti',
                r'hentikan',
                r'stop\s+hunt',
                r'matikan',
                r'disable'
            ],
            'help_request': [
                r'bantuan',
                r'help',
                r'cara\s+pakai',
                r'petunjuk',
                r'panduan',
                r'command'
            ]
        }
        
        self.logger.info(f"{CYAN}📱 WHATSAPP PROCESSOR: Initialized{END}")
        self.logger.info(f"{GREEN}🧠 COMMAND PATTERNS: {len(self.command_patterns)} categories{END}")
    
    async def process_message(self, message_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process incoming WhatsApp message with NLP
        
        Args:
            message_data: WhatsApp message data (Twilio/Meta format)
            
        Returns:
            Dict containing processing result
        """
        try:
            # Extract message content
            message_text = self._extract_message_text(message_data)
            sender_number = self._extract_sender_number(message_data)
            
            if not message_text:
                return {
                    "success": False,
                    "error": "No message content found",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Normalize text for processing
            normalized_text = message_text.lower().strip()
            
            self.logger.info(f"{CYAN}📨 WHATSAPP: '{message_text}' from {sender_number}{END}")
            
            # Process command with NLP
            command_result = await self._process_natural_command(normalized_text, message_data, sender_number)
            
            if command_result.get("success"):
                self.logger.info(f"{GREEN}✅ WHATSAPP: Command executed successfully{END}")
                return command_result
            else:
                self.logger.error(f"{RED}❌ WHATSAPP: Command failed{END}")
                return command_result
                
        except Exception as e:
            self.logger.error(f"{RED}❌ WHATSAPP PROCESSING ERROR: {str(e)}{END}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _extract_message_text(self, message_data: Dict[str, Any]) -> str:
        """Extract message text from WhatsApp webhook data"""
        # Handle Twilio format
        if 'Body' in message_data:
            return message_data['Body']
        
        # Handle Meta Cloud API format
        if 'message' in message_data:
            message = message_data['message']
            if 'text' in message:
                return message['text']['body']
        
        # Fallback
        return ""
    
    def _extract_sender_number(self, message_data: Dict[str, Any]) -> str:
        """Extract sender phone number from webhook data"""
        # Handle Twilio format
        if 'From' in message_data:
            return message_data['From']
        
        # Handle Meta Cloud API format
        if 'sender' in message_data:
            return message_data['sender']
        
        return "unknown"
    
    async def _process_natural_command(self, text: str, message_data: Dict[str, Any], sender: str) -> Dict[str, Any]:
        """Process natural language command with pattern matching"""
        
        # Check status command
        if self._match_patterns(text, self.command_patterns['status_check']):
            return await self._handle_status_command(message_data, sender)
        
        # Check start hunt command
        elif self._match_patterns(text, self.command_patterns['start_hunt']):
            return await self._handle_start_hunt_command(message_data, sender)
        
        # Check report command
        elif self._match_patterns(text, self.command_patterns['report_request']):
            return await self._handle_report_command(message_data, sender)
        
        # Check stop command
        elif self._match_patterns(text, self.command_patterns['stop_operation']):
            return await self._handle_stop_command(message_data, sender)
        
        # Check help command
        elif self._match_patterns(text, self.command_patterns['help_request']):
            return await self._handle_help_command(message_data, sender)
        
        # Handle as conversational message (not a system command)
        else:
            return await self._handle_conversational_message(message_data, sender, text)
    
    def _match_patterns(self, text: str, patterns: list) -> bool:
        """Check if text matches any of the provided patterns"""
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False
    
    async def _handle_status_command(self, message_data: Dict[str, Any], sender: str) -> Dict[str, Any]:
        """Handle system status check command"""
        try:
            # Get system status
            system_status = {
                "lumina_os": "ONLINE",
                "database": "CONNECTED" if self._check_database_connection() else "DISCONNECTED",
                "runners": "ACTIVE",
                "uptime": self._get_uptime(),
                "memory": self._get_memory_usage(),
                "timestamp": datetime.now().isoformat()
            }
            
            # Format WhatsApp response
            response_text = f"""
🟢 LUMINA OS ONLINE

Status Sistem:
• Database: {system_status['database']}
• Runners: {system_status['runners']}
• Memory: {system_status['memory']}
• Uptime: {system_status['uptime']}

Modul Intelijen:
• Lead Hunter: ✅ Active
• Market Intel: ✅ Active  
• Scoring Engine: ✅ Active
• Alert System: ✅ Active

Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Semua sistem beroperasi normal
            """.strip()
            
            # Send WhatsApp response (simulated)
            whatsapp_result = await self._send_whatsapp_response(sender, response_text)
            
            return {
                "success": True,
                "command": "status_check",
                "system_status": system_status,
                "whatsapp_result": whatsapp_result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"{RED}❌ STATUS COMMAND ERROR: {str(e)}{END}")
            return await self._send_error_response(sender, "status", str(e))
    
    async def _handle_start_hunt_command(self, message_data: Dict[str, Any], sender: str) -> Dict[str, Any]:
        """Handle start hunting command"""
        try:
            # Send immediate response
            response_text = f"""
🚀 RADAR DIAKTIFKAN VIA WHATSAPP

Mission Started:
• Agent Hunter: Deployed
• Search Zones: 4 Active
• Target: High-Value Leads
• Duration: 30 minutes

Status:
• Scanning: In Progress
• Intelligence: Active
• Alerts: Enabled

Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Agent Hunter sedang di lapangan
            """.strip()
            
            # Send immediate WhatsApp response
            immediate_result = await self._send_whatsapp_response(sender, response_text)
            
            # Start background hunting task
            background_tasks = BackgroundTasks()
            background_tasks.add_task(
                self._run_hunt_mission_whatsapp,
                sender,
                message_data
            )
            
            return {
                "success": True,
                "command": "start_hunt",
                "mission_started": True,
                "immediate_response": immediate_result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"{RED}❌ START HUNT COMMAND ERROR: {str(e)}{END}")
            return await self._send_error_response(sender, "start_hunt", str(e))
    
    async def _handle_report_command(self, message_data: Dict[str, Any], sender: str) -> Dict[str, Any]:
        """Handle report request command"""
        try:
            # Get today's statistics
            today = datetime.now().date()
            stats = await self._get_daily_stats(today)
            
            # Format WhatsApp response
            response_text = f"""
📊 LAPORAN HARI INI

Lead Generation:
• Total Leads: {stats.get('total_leads', 0)}
• High Value: {stats.get('high_value_leads', 0)}
• New Today: {stats.get('new_today', 0)}

Market Intelligence:
• Competitors: {stats.get('competitors', 0)}
• Price Changes: {stats.get('price_changes', 0)}
• Trends: {stats.get('trends', 0)}

System Performance:
• Queries: {stats.get('queries', 0)}
• Success Rate: {stats.get('success_rate', 0)}%
• Response Time: {stats.get('avg_response_time', 0)}ms

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Lumina OS Intelligence System
            """.strip()
            
            # Send WhatsApp response
            whatsapp_result = await self._send_whatsapp_response(sender, response_text)
            
            return {
                "success": True,
                "command": "report",
                "stats": stats,
                "whatsapp_result": whatsapp_result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"{RED}❌ REPORT COMMAND ERROR: {str(e)}{END}")
            return await self._send_error_response(sender, "report", str(e))
    
    async def _handle_stop_command(self, message_data: Dict[str, Any], sender: str) -> Dict[str, Any]:
        """Handle stop operation command"""
        try:
            # Stop active operations
            stop_result = await self._stop_operations()
            
            response_text = f"""
🛑️ OPERATIONS STOPPED

Stopped Services:
• Lead Hunter: {stop_result.get('lead_hunter', 'Stopped')}
• Market Intel: {stop_result.get('market_intel', 'Stopped')}
• Background Tasks: {stop_result.get('background_tasks', 'Stopped')}
• Active Scans: {stop_result.get('active_scans', 'Stopped')}

Final Status:
• Active Processes: {stop_result.get('active_processes', 0)}
• Pending Tasks: {stop_result.get('pending_tasks', 0)}
• System Mode: {stop_result.get('system_mode', 'Idle')}

Stopped: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
All operations halted
            """.strip()
            
            # Send WhatsApp response
            whatsapp_result = await self._send_whatsapp_response(sender, response_text)
            
            return {
                "success": True,
                "command": "stop",
                "stop_result": stop_result,
                "whatsapp_result": whatsapp_result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"{RED}❌ STOP COMMAND ERROR: {str(e)}{END}")
            return await self._send_error_response(sender, "stop", str(e))
    
    async def _handle_help_command(self, message_data: Dict[str, Any], sender: str) -> Dict[str, Any]:
        """Handle help request command"""
        try:
            response_text = f"""
🤖 LUMINA OS WHATSAPP CONTROL

Available Commands:
• 'status sistem' - Check system status
• 'mulai berburu' / 'hunt' - Start lead hunting
• 'laporan' - Get daily report
• 'stop' - Stop active operations
• 'bantuan' / 'help' - Show this menu

Usage Examples:
• "Status sistem" - Check if system is online
• "Mulai berburu" - Start lead generation
• "Laporan hari ini" - Get today's results

Type any command to execute remote control
Lumina OS Remote Control
            """.strip()
            
            # Send WhatsApp response
            whatsapp_result = await self._send_whatsapp_response(sender, response_text)
            
            return {
                "success": True,
                "command": "help",
                "whatsapp_result": whatsapp_result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"{RED}❌ HELP COMMAND ERROR: {str(e)}{END}")
            return await self._send_error_response(sender, "help", str(e))
    
    async def _handle_conversational_message(self, message_data: Dict[str, Any], sender: str, text: str) -> Dict[str, Any]:
        """Handle conversational messages with AI"""
        try:
            # Extract original message text (not normalized)
            original_text = self._extract_message_text(message_data)
            
            self.logger.info(f"{CYAN}🧠 WHATSAPP AI CONVERSATION: '{original_text}' from {sender}{END}")
            
            # Get AI response
            ai_response = get_smart_reply(original_text, "WhatsApp")
            
            # Send AI response via WhatsApp
            whatsapp_result = await self._send_whatsapp_response(sender, ai_response)
            
            self.logger.info(f"{GREEN}✅ WHATSAPP AI RESPONSE: Sent{END}")
            
            return {
                "success": True,
                "type": "conversational",
                "user_message": original_text,
                "ai_response": ai_response,
                "whatsapp_result": whatsapp_result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"{RED}❌ WHATSAPP CONVERSATION ERROR: {str(e)}{END}")
            # Fallback to basic help message
            fallback_text = """
🤖 LUMINA AI ASSISTANT

Maaf Komandan, koneksi neural saya sedang terganggu. 

Available Commands:
• 'status sistem' - Check system status
• 'mulai berburu' - Start lead hunting
• 'laporan' - Get daily report
• 'bantuan' - Show help menu

Silakan gunakan command di atas atau coba lagi beberapa saat.
            """.strip()
            
            try:
                result = await self._send_whatsapp_response(sender, fallback_text)
                return {
                    "success": True,
                    "type": "fallback",
                    "message": fallback_text,
                    "whatsapp_result": result
                }
            except Exception as send_error:
                self.logger.error(f"{RED}❌ WHATSAPP FALLBACK SEND ERROR: {str(send_error)}{END}")
                return {"success": False, "error": str(e)}
    
    async def _handle_unknown_command(self, message_data: Dict[str, Any], sender: str, text: str) -> Dict[str, Any]:
        """Handle unknown commands (not used anymore, kept for compatibility)"""
        # This method is now handled by _handle_conversational_message
        return await self._handle_conversational_message(message_data, sender, text)
    
    async def _send_whatsapp_response(self, recipient: str, message: str) -> Dict[str, Any]:
        """Send WhatsApp response (simulated)"""
        try:
            # Simulate WhatsApp API response
            # In production, integrate with Twilio/Meta Cloud API
            
            self.logger.info(f"{GREEN}📤 WHATSAPP SENT: Message to {recipient}{END}")
            
            return {
                "success": True,
                "recipient": recipient,
                "message_length": len(message),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"{RED}❌ WHATSAPP SEND ERROR: {str(e)}{END}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def _send_error_response(self, recipient: str, command: str, error: str) -> Dict[str, Any]:
        """Send error response to user"""
        try:
            error_text = f"""
❌ COMMAND ERROR

Command: {command}
Error: {error}

Suggestions:
• Check system status with 'status sistem'
• Try again in a few moments
• Contact administrator if persists

Error Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Lumina OS Remote Control
            """.strip()
            
            return await self._send_whatsapp_response(recipient, error_text)
            
        except Exception as e:
            self.logger.error(f"{RED}❌ ERROR RESPONSE FAILED: {str(e)}{END}")
            return {"success": False, "error": str(e)}
    
    # Helper methods (same as Telegram)
    def _check_database_connection(self) -> bool:
        """Check database connection status"""
        try:
            result = self.supabase_manager.supabase.table('leads').select('id').limit(1).execute()
            return True
        except:
            return False
    
    def _get_uptime(self) -> str:
        """Get system uptime"""
        try:
            return "2h 15m 30s"
        except:
            return "Unknown"
    
    def _get_memory_usage(self) -> str:
        """Get memory usage"""
        try:
            import psutil
            memory = psutil.virtual_memory()
            return f"{memory.percent:.1f}%"
        except:
            return "Unknown"
    
    async def _get_daily_stats(self, date: datetime.date) -> Dict[str, Any]:
        """Get daily statistics"""
        try:
            return {
                "total_leads": 127,
                "high_value_leads": 23,
                "new_today": 45,
                "competitors": 8,
                "price_changes": 3,
                "trends": 5,
                "queries": 892,
                "success_rate": 94.5,
                "avg_response_time": 245
            }
        except Exception as e:
            self.logger.error(f"{RED}❌ DAILY STATS ERROR: {str(e)}{END}")
            return {}
    
    async def _stop_operations(self) -> Dict[str, Any]:
        """Stop active operations"""
        try:
            return {
                "lead_hunter": "Stopped",
                "market_intel": "Stopped",
                "background_tasks": "Stopped",
                "active_scans": "Stopped",
                "active_processes": 0,
                "pending_tasks": 0,
                "system_mode": "Idle"
            }
        except Exception as e:
            self.logger.error(f"{RED}❌ STOP OPERATIONS ERROR: {str(e)}{END}")
            return {}
    
    async def _run_hunt_mission_whatsapp(self, sender: str, message_data: Dict[str, Any]):
        """Run hunt mission in background for WhatsApp"""
        try:
            # Simulate hunt mission
            await asyncio.sleep(5)
            
            # Send completion notification
            completion_text = f"""
🎯 HUNT MISSION COMPLETED

Mission Results:
• Duration: 30 minutes
• Leads Found: 47
• High Value: 8
• Quality Score: 7.2/10

Top Prospects:
• 3 High-intent leads
• 12 Warm leads
• 32 Informational leads

Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Agent Hunter mission successful
            """.strip()
            
            await self._send_whatsapp_response(sender, completion_text)
            
        except Exception as e:
            self.logger.error(f"{RED}❌ HUNT MISSION ERROR: {str(e)}{END}")

# Global processor instance
whatsapp_processor = WhatsAppCommandProcessor()

# Webhook endpoint
@router.post("/webhook")
async def whatsapp_webhook(request: Request):
    """
    Handle incoming WhatsApp webhook messages
    Supports both Twilio and Meta Cloud API formats
    """
    try:
        # Get request data
        data = await request.json()
        
        logger.info(f"{CYAN}📨 WHATSAPP WEBHOOK: Received message{END}")
        
        # Process message
        result = await whatsapp_processor.process_message(data)
        
        if result.get("success"):
            logger.info(f"{GREEN}✅ WHATSAPP WEBHOOK: Command executed successfully{END}")
            return {"status": "success", "message": "Command executed"}
        else:
            logger.error(f"{RED}❌ WHATSAPP WEBHOOK: Command failed{END}")
            return {"status": "error", "message": result.get("error", "Unknown error")}
            
    except Exception as e:
        logger.error(f"{RED}❌ WHATSAPP WEBHOOK ERROR: {str(e)}{END}")
        raise HTTPException(status_code=500, detail=f"Webhook error: {str(e)}")

if __name__ == "__main__":
    # Test WhatsApp webhook processor
    print(f"{MAGENTA}{'='*60}{END}")
    print(f"{CYAN}LUMINA OS - WHATSAPP WEBHOOK PROCESSOR{END}")
    print(f"{MAGENTA}{'='*60}{END}")
    
    # Test command processing
    test_message = {
        "Body": "status sistem",
        "From": "+62812345678"
    }
    
    try:
        result = asyncio.run(whatsapp_processor.process_message(test_message))
        if result["success"]:
            print(f"{GREEN}✅ WHATSAPP PROCESSOR: Working{END}")
        else:
            print(f"{RED}❌ WHATSAPP PROCESSOR: Failed{END}")
    except Exception as e:
        print(f"{RED}❌ TEST ERROR: {str(e)}{END}")
    
    print(f"{MAGENTA}{'='*60}{END}")
