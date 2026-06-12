"""
DOOM SENTINEL - WhatsApp Gateway
Military-grade WhatsApp integration with RBAC and proactive monitoring
"""

import os
import logging
import asyncio
import json
from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum

# WhatsApp Business API (using twilio as example)
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

# Internal modules
from .security_middleware import SecurityMiddleware, AccessLevel
from .rbac_manager import RBACManager
from .alert_system import AlertSystem

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WhatsAppGateway:
    """
    DOOM WhatsApp Gateway - Military-grade WhatsApp integration
    Handles dual personality responses based on user access level
    """
    
    def __init__(self):
        """Initialize WhatsApp gateway"""
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.security = SecurityMiddleware()
        self.rbac = RBACManager()
        self.alert_system = AlertSystem()
        
        # WhatsApp configuration
        self.twilio_account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.whatsapp_number = os.getenv('TWILIO_WHATSAPP_NUMBER')
        
        if not all([self.twilio_account_sid, self.twilio_auth_token, self.whatsapp_number]):
            raise ValueError("Twilio WhatsApp credentials not configured")
        
        # Initialize Twilio client
        self.client = Client(self.twilio_account_sid, self.twilio_auth_token)
        
        # Message queue for bulk operations
        self.message_queue = asyncio.Queue()
        self.processing_messages = False
        
        self.logger.info("📱 DOOM WhatsApp Gateway initialized")
        self.logger.info(f"📞 WhatsApp number: {self.whatsapp_number}")
    
    async def process_incoming_message(self, from_number: str, message_body: str, message_id: str = None):
        """
        Process incoming WhatsApp message
        
        Args:
            from_number: Sender's WhatsApp number
            message_body: Message content
            message_id: WhatsApp message ID
        """
        try:
            self.logger.info(f"📨 Incoming message from {from_number}: {message_body[:50]}...")
            
            # Verify access
            access_level = self.security.verify_admin_access(from_number, 'whatsapp')
            
            # Check if it's a command
            if message_body.startswith('/'):
                await self._handle_command(from_number, message_body, access_level)
            else:
                await self._handle_regular_message(from_number, message_body, access_level)
                
        except Exception as e:
            self.logger.error(f"❌ Error processing message: {e}")
            await self.send_error_message(from_number, "Sorry, I encountered an error processing your message.")
    
    async def _handle_command(self, from_number: str, command: str, access_level: AccessLevel):
        """Handle command messages"""
        # Check permission
        permission = self.security.check_command_permission(from_number, 'whatsapp', command)
        
        if not permission['allowed']:
            await self.send_message(from_number, permission['response'])
            return
        
        # Process command based on access level
        if access_level == AccessLevel.ADMIN:
            await self._handle_admin_command(from_number, command)
        else:
            await self._handle_guest_command(from_number, command)
    
    async def _handle_admin_command(self, from_number: str, command: str):
        """Handle admin commands"""
        command_parts = command.split()
        cmd = command_parts[0].lower()
        
        if cmd == '/status':
            status_report = await self.rbac.generate_status_report()
            response = (
                "🎖️ *DOOM SYSTEM STATUS*\n\n"
                f"📊 Server Health: {status_report['server_health']}\n"
                f"💾 Database: {status_report['database_status']}\n"
                f"👥 Leads Today: {status_report['leads_today']}\n"
                f"💰 Budget: {status_report['budget_remaining']}\n"
                f"🤖 AI Agents: {status_report['active_agents']}/{status_report['total_agents']}\n"
                f"⚡ Uptime: {status_report['uptime']}\n\n"
                f"🕐 Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
            
        elif cmd == '/deploy_scout':
            location = ' '.join(command_parts[1:]) if len(command_parts) > 1 else 'default'
            deployment_result = await self.rbac.deploy_scout(location)
            response = (
                "🎖️ *DOOM SCOUT DEPLOYMENT*\n\n"
                f"📍 Location: {location}\n"
                f"🤖 Agent: {deployment_result['agent_name']}\n"
                f"📊 Status: {deployment_result['status']}\n"
                f"⏱️ ETA: {deployment_result['eta']}\n\n"
                f"🔍 Mission: {deployment_result['mission_description']}"
            )
            
        elif cmd == '/approve_ads':
            campaign_id = command_parts[1] if len(command_parts) > 1 else None
            if not campaign_id:
                response = "🎖️ *DOOM ADS APPROVAL*\n\n❌ Please provide campaign ID: /approve_ads <campaign_id>"
            else:
                approval_result = await self.rbac.approve_ads(campaign_id)
                response = (
                    "🎖️ *DOOM ADS APPROVAL*\n\n"
                    f"📢 Campaign ID: {campaign_id}\n"
                    f"✅ Status: {approval_result['status']}\n"
                    f"💰 Budget: {approval_result['budget']}\n"
                    f"🎯 Target: {approval_result['target_audience']}\n\n"
                    f"🚀 Launch Time: {approval_result['launch_time']}"
                )
                
        elif cmd == '/system_control':
            response = (
                "🎖️ *DOOM SYSTEM CONTROL*\n\n"
                "Available actions:\n"
                "• restart_services - Restart all services\n"
                "• view_logs - View system logs\n"
                "• db_maintenance - Database maintenance\n"
                "• emergency_stop - Emergency system stop\n"
                "• performance - Performance metrics\n"
                "• diagnostics - System diagnostics\n\n"
                "Reply with action name to execute."
            )
            
        elif cmd == '/help':
            response = (
                "🎖️ *DOOM COMMAND HELP*\n\n"
                "*Admin Commands:*\n"
                "• /status - Server health, leads today, budget status\n"
                "• /deploy_scout <location> - Deploy Hunter to location\n"
                "• /approve_ads <campaign_id> - Approve ad campaign\n"
                "• /system_control - Advanced system controls\n\n"
                "*Monitoring:*\n"
                "• Proactive alerts enabled\n"
                "• Real-time server monitoring\n"
                "• Automatic error notifications\n\n"
                "🔒 Access restricted to authorized personnel only."
            )
            
        else:
            # Process as natural command
            response = await self.rbac.process_natural_command(command)
            response = f"🎖️ *DOOM RESPONSE*\n\n{response}"
        
        await self.send_message(from_number, response)
    
    async def _handle_guest_command(self, from_number: str, command: str):
        """Handle guest commands - Customer service mode"""
        # Guests don't get access to commands, redirect to customer service
        response = (
            "👋 *Virtual Assistant*\n\n"
            "I'm here to help you with information about our property projects.\n"
            "How can I assist you today?\n\n"
            "You can ask me about:\n"
            "• Available properties\n"
            "• Project information\n"
            "• General inquiries"
        )
        
        await self.send_message(from_number, response)
    
    async def _handle_regular_message(self, from_number: str, message: str, access_level: AccessLevel):
        """Handle regular messages"""
        if access_level == AccessLevel.ADMIN:
            # Admin gets natural command processing
            response = await self.rbac.process_natural_command(message)
            response = f"🎖️ *DOOM RESPONSE*\n\n{response}"
        else:
            # Guest gets customer service response
            response = await self.rbac.process_customer_service_inquiry(message)
            response = f"👋 *Virtual Assistant*\n\n{response}"
        
        await self.send_message(from_number, response)
    
    async def send_message(self, to_number: str, message: str):
        """
        Send WhatsApp message
        
        Args:
            to_number: Recipient's WhatsApp number
            message: Message content
        """
        try:
            # Normalize phone number
            normalized_number = self._normalize_phone_number(to_number)
            
            # Send message via Twilio
            message_obj = self.client.messages.create(
                body=message,
                from_=f'whatsapp:{self.whatsapp_number}',
                to=f'whatsapp:{normalized_number}'
            )
            
            self.logger.info(f"📤 Message sent to {normalized_number}: {message_obj.sid}")
            return message_obj.sid
            
        except TwilioRestException as e:
            self.logger.error(f"❌ Twilio error sending message: {e}")
            raise
        except Exception as e:
            self.logger.error(f"❌ Error sending message: {e}")
            raise
    
    async def send_bulk_messages(self, messages: List[Dict[str, str]]):
        """
        Send bulk messages with queue management
        
        Args:
            messages: List of message dictionaries with 'to' and 'body' keys
        """
        # Add messages to queue
        for message in messages:
            await self.message_queue.put(message)
        
        # Start processing if not already running
        if not self.processing_messages:
            asyncio.create_task(self._process_message_queue())
    
    async def _process_message_queue(self):
        """Process message queue with rate limiting"""
        self.processing_messages = True
        self.logger.info("📋 Starting message queue processing...")
        
        while not self.message_queue.empty():
            try:
                # Get message from queue
                message = await self.message_queue.get()
                
                # Send message with rate limiting
                await self.send_message(message['to'], message['body'])
                
                # Rate limiting: 1 message per second to avoid being blocked
                await asyncio.sleep(1)
                
                # Mark task as done
                self.message_queue.task_done()
                
            except Exception as e:
                self.logger.error(f"❌ Error processing queued message: {e}")
        
        self.processing_messages = False
        self.logger.info("✅ Message queue processing completed")
    
    async def send_alert_to_admin(self, message: str):
        """Send proactive alert to admin"""
        admin_numbers = self.security.admin_whatsapp_numbers
        
        for admin_number in admin_numbers:
            try:
                await self.send_message(admin_number, f"🚨 *DOOM ALERT*\n\n{message}")
                self.logger.info(f"📨 Alert sent to admin {admin_number}")
            except Exception as e:
                self.logger.error(f"❌ Failed to send alert to admin {admin_number}: {e}")
    
    async def send_error_message(self, to_number: str, error_message: str):
        """Send error message to user"""
        response = (
            "❌ *Error*\n\n"
            f"{error_message}\n\n"
            "Please try again later or contact support."
        )
        
        await self.send_message(to_number, response)
    
    def _normalize_phone_number(self, phone_number: str) -> str:
        """Normalize phone number for WhatsApp"""
        # Remove +, spaces, dashes, etc.
        normalized = phone_number.replace('+', '').replace(' ', '').replace('-', '')
        
        # Add country code if missing (assuming Indonesia)
        if not normalized.startswith('62'):
            if normalized.startswith('0'):
                normalized = '62' + normalized[1:]
            else:
                normalized = '62' + normalized
        
        return normalized
    
    async def start_webhook_server(self, host: str = '0.0.0.0', port: int = 5000):
        """Start webhook server for incoming messages"""
        from fastapi import FastAPI, Request, HTTPException
        from fastapi.responses import JSONResponse
        
        app = FastAPI()
        
        @app.post("/webhook/whatsapp")
        async def whatsapp_webhook(request: Request):
            """Handle incoming WhatsApp webhook"""
            try:
                data = await request.json()
                
                # Extract message details
                from_number = data.get('From', '').replace('whatsapp:', '')
                message_body = data.get('Body', '')
                message_id = data.get('MessageSid', '')
                
                # Process message
                await self.process_incoming_message(from_number, message_body, message_id)
                
                return JSONResponse({"status": "success"})
                
            except Exception as e:
                self.logger.error(f"❌ Webhook error: {e}")
                return JSONResponse(
                    {"status": "error", "message": str(e)},
                    status_code=500
                )
        
        @app.get("/webhook/whatsapp")
        async def webhook_verify():
            """Verify webhook with WhatsApp"""
            return JSONResponse({"status": "active"})
        
        import uvicorn
        self.logger.info(f"🚀 Starting WhatsApp webhook server on {host}:{port}")
        uvicorn.run(app, host=host, port=port)
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on WhatsApp gateway"""
        try:
            # Check Twilio connection
            account = self.client.api.v2010.accounts.get(self.twilio_account_sid).fetch()
            
            return {
                'status': 'healthy',
                'twilio_status': 'connected',
                'whatsapp_number': self.whatsapp_number,
                'queue_size': self.message_queue.qsize(),
                'processing_messages': self.processing_messages,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
