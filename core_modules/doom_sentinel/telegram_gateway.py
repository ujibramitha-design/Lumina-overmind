"""
DOOM SENTINEL - Telegram Gateway
Military-grade Telegram bot integration with RBAC and proactive monitoring
"""

import os
import logging
import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum

# Telegram Bot API
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Internal modules
from .security_middleware import SecurityMiddleware, AccessLevel
from .rbac_manager import RBACManager
from .alert_system import AlertSystem

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TelegramGateway:
    """
    DOOM Telegram Gateway - Military-grade Telegram bot integration
    Handles dual personality responses based on user access level
    """
    
    def __init__(self):
        """Initialize Telegram gateway"""
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.security = SecurityMiddleware()
        self.rbac = RBACManager()
        self.alert_system = AlertSystem()
        
        # Telegram bot configuration
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not self.bot_token:
            raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")
        
        # Initialize bot
        self.bot = Bot(token=self.bot_token)
        self.application = Application.builder().token(self.bot_token).build()
        
        # Register handlers
        self._register_handlers()
        
        self.logger.info("🤖 DOOM Telegram Gateway initialized")
        self.logger.info(f"🔑 Bot token configured: {self.bot_token[:10]}...")
    
    def _register_handlers(self):
        """Register command and message handlers"""
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.handle_start))
        self.application.add_handler(CommandHandler("help", self.handle_help))
        self.application.add_handler(CommandHandler("status", self.handle_status))
        self.application.add_handler(CommandHandler("deploy_scout", self.handle_deploy_scout))
        self.application.add_handler(CommandHandler("approve_ads", self.handle_approve_ads))
        self.application.add_handler(CommandHandler("system_control", self.handle_system_control))
        
        # Message handler
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        # Error handler
        self.application.add_error_handler(self.handle_error)
    
    async def handle_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user_id = str(update.effective_user.id)
        username = update.effective_user.username or "Unknown"
        
        # Verify access
        access_level = self.security.verify_admin_access(user_id, 'telegram')
        
        if access_level == AccessLevel.ADMIN:
            response = (
                "🎖️ **DOOM COMMAND SYSTEM ONLINE**\n\n"
                f"Welcome, Commander {username}!\n"
                "DOOM (Digital Overwatch & Operations Machine) is ready for your commands.\n\n"
                "📋 **Available Commands:**\n"
                "• `/status` - System health report\n"
                "• `/deploy_scout` - Deploy AI Hunter\n"
                "• `/approve_ads` - Approve ad campaigns\n"
                "• `/system_control` - System control panel\n\n"
                "🔒 All commands require admin authorization."
            )
        else:
            response = (
                "👋 **Hello! I'm your Virtual Assistant**\n\n"
                "I'm here to help you with information about our property projects.\n"
                "How can I assist you today?\n\n"
                "You can ask me about:\n"
                "• Available properties\n"
                "• Project information\n"
                "• General inquiries"
            )
        
        await update.message.reply_text(response, parse_mode='Markdown')
    
    async def handle_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        user_id = str(update.effective_user.id)
        access_level = self.security.verify_admin_access(user_id, 'telegram')
        
        if access_level == AccessLevel.ADMIN:
            response = (
                "🎖️ **DOOM COMMAND HELP**\n\n"
                "**Admin Commands:**\n"
                "• `/status` - Server health, leads today, budget status\n"
                "• `/deploy_scout <location>` - Deploy Hunter to location\n"
                "• `/approve_ads <campaign_id>` - Approve ad campaign\n"
                "• `/system_control` - Advanced system controls\n\n"
                "**Monitoring:**\n"
                "• Proactive alerts enabled\n"
                "• Real-time server monitoring\n"
                "• Automatic error notifications\n\n"
                "🔒 Access restricted to authorized personnel only."
            )
        else:
            response = (
                "👋 **Virtual Assistant Help**\n\n"
                "I can help you with:\n\n"
                "🏠 **Property Information:**\n"
                "• Available units and pricing\n"
                "• Location details\n"
                "• Project facilities\n\n"
                "📞 **Contact & Support:**\n"
                "• Schedule property visits\n"
                "• Request brochures\n"
                "• General inquiries\n\n"
                "💬 Just type your question and I'll help you!"
            )
        
        await update.message.reply_text(response, parse_mode='Markdown')
    
    async def handle_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command - Admin only"""
        user_id = str(update.effective_user.id)
        
        # Check permission
        permission = self.security.check_command_permission(user_id, 'telegram', '/status')
        
        if not permission['allowed']:
            await update.message.reply_text(permission['response'])
            return
        
        # Generate status report
        status_report = await self.rbac.generate_status_report()
        
        response = (
            "🎖️ **DOOM SYSTEM STATUS**\n\n"
            f"📊 **Server Health:** {status_report['server_health']}\n"
            f"💾 **Database:** {status_report['database_status']}\n"
            f"👥 **Leads Today:** {status_report['leads_today']}\n"
            f"💰 **Budget Remaining:** {status_report['budget_remaining']}\n"
            f"🤖 **AI Agents:** {status_report['active_agents']}/{status_report['total_agents']}\n"
            f"⚡ **System Uptime:** {status_report['uptime']}\n\n"
            f"🕐 **Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        
        await update.message.reply_text(response, parse_mode='Markdown')
    
    async def handle_deploy_scout(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /deploy_scout command - Admin only"""
        user_id = str(update.effective_user.id)
        
        # Check permission
        permission = self.security.check_command_permission(user_id, 'telegram', '/deploy_scout')
        
        if not permission['allowed']:
            await update.message.reply_text(permission['response'])
            return
        
        # Extract location from command
        location = ' '.join(context.args) if context.args else 'default'
        
        # Deploy scout
        deployment_result = await self.rbac.deploy_scout(location)
        
        response = (
            "🎖️ **DOOM SCOUT DEPLOYMENT**\n\n"
            f"📍 **Location:** {location}\n"
            f"🤖 **Agent:** {deployment_result['agent_name']}\n"
            f"📊 **Status:** {deployment_result['status']}\n"
            f"⏱️ **ETA:** {deployment_result['eta']}\n\n"
            f"🔍 **Mission:** {deployment_result['mission_description']}"
        )
        
        await update.message.reply_text(response, parse_mode='Markdown')
    
    async def handle_approve_ads(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /approve_ads command - Admin only"""
        user_id = str(update.effective_user.id)
        
        # Check permission
        permission = self.security.check_command_permission(user_id, 'telegram', '/approve_ads')
        
        if not permission['allowed']:
            await update.message.reply_text(permission['response'])
            return
        
        # Extract campaign ID
        campaign_id = context.args[0] if context.args else None
        
        if not campaign_id:
            await update.message.reply_text(
                "🎖️ **DOOM ADS APPROVAL**\n\n"
                "❌ Please provide campaign ID: `/approve_ads <campaign_id>`"
            )
            return
        
        # Approve campaign
        approval_result = await self.rbac.approve_ads(campaign_id)
        
        response = (
            "🎖️ **DOOM ADS APPROVAL**\n\n"
            f"📢 **Campaign ID:** {campaign_id}\n"
            f"✅ **Status:** {approval_result['status']}\n"
            f"💰 **Budget:** {approval_result['budget']}\n"
            f"🎯 **Target:** {approval_result['target_audience']}\n\n"
            f"🚀 **Launch Time:** {approval_result['launch_time']}"
        )
        
        await update.message.reply_text(response, parse_mode='Markdown')
    
    async def handle_system_control(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /system_control command - Admin only"""
        user_id = str(update.effective_user.id)
        
        # Check permission
        permission = self.security.check_command_permission(user_id, 'telegram', '/system_control')
        
        if not permission['allowed']:
            await update.message.reply_text(permission['response'])
            return
        
        # Create control panel
        keyboard = [
            [
                InlineKeyboardButton("🔄 Restart Services", callback_data="restart_services"),
                InlineKeyboardButton("📊 View Logs", callback_data="view_logs"),
            ],
            [
                InlineKeyboardButton("🔧 Database Maintenance", callback_data="db_maintenance"),
                InlineKeyboardButton("🚨 Emergency Stop", callback_data="emergency_stop"),
            ],
            [
                InlineKeyboardButton("📈 Performance Metrics", callback_data="performance"),
                InlineKeyboardButton("🔍 System Diagnostics", callback_data="diagnostics"),
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        response = (
            "🎖️ **DOOM SYSTEM CONTROL**\n\n"
            "Select an action from the control panel below:"
        )
        
        await update.message.reply_text(response, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular messages - Customer service mode for guests"""
        user_id = str(update.effective_user.id)
        message_text = update.message.text
        
        # Verify access
        access_level = self.security.verify_admin_access(user_id, 'telegram')
        
        if access_level == AccessLevel.ADMIN:
            # Admin can send natural commands
            await self._handle_admin_message(update, context, message_text)
        else:
            # Guest gets customer service response
            await self._handle_guest_message(update, context, message_text)
    
    async def _handle_admin_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE, message: str):
        """Handle messages from admin users"""
        # Process as natural command
        response = await self.rbac.process_natural_command(message)
        
        await update.message.reply_text(
            f"🎖️ **DOOM RESPONSE**\n\n{response}",
            parse_mode='Markdown'
        )
    
    async def _handle_guest_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE, message: str):
        """Handle messages from guest users - Customer service mode"""
        # Process as customer service inquiry
        response = await self.rbac.process_customer_service_inquiry(message)
        
        await update.message.reply_text(
            f"👋 **Virtual Assistant**\n\n{response}",
            parse_mode='Markdown'
        )
    
    async def handle_error(self, update: object, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors in the bot"""
        logger.error(f"Exception while handling an update: {context.error}")
        
        # Send alert to admin
        await self.alert_system.send_telegram_alert(
            f"🚨 **DOOM TELEGRAM ERROR**\n\n"
            f"❌ Error: {context.error}\n"
            f"🕐 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
    
    async def send_alert_to_admin(self, message: str):
        """Send proactive alert to admin"""
        admin_ids = self.security.admin_telegram_ids
        
        for admin_id in admin_ids:
            try:
                await self.bot.send_message(
                    chat_id=admin_id,
                    text=f"🚨 **DOOM ALERT**\n\n{message}",
                    parse_mode='Markdown'
                )
                self.logger.info(f"📨 Alert sent to admin {admin_id}")
            except Exception as e:
                self.logger.error(f"❌ Failed to send alert to admin {admin_id}: {e}")
    
    def start_bot(self):
        """Start the Telegram bot"""
        self.logger.info("🚀 Starting DOOM Telegram Bot...")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)
    
    async def stop_bot(self):
        """Stop the Telegram bot"""
        self.logger.info("🛑 Stopping DOOM Telegram Bot...")
        await self.application.stop()
        await self.application.shutdown()
