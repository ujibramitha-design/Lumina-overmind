"""
DOOM SENTINEL - Main Application
Digital Overwatch & Operations Machine - Main Entry Point
"""

import os
import sys
import logging
import asyncio
from datetime import datetime

# Add root directory to Python path
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_dir)

# Import DOOM components
from core_modules.doom_sentinel.telegram_gateway import TelegramGateway
from core_modules.doom_sentinel.whatsapp_gateway import WhatsAppGateway
from core_modules.doom_sentinel.security_middleware import SecurityMiddleware
from core_modules.doom_sentinel.rbac_manager import RBACManager
from core_modules.doom_sentinel.alert_system import AlertSystem, AlertLevel

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DOOMSentinel:
    """
    Main DOOM Sentinel application
    Coordinates all components and manages system operations
    """
    
    def __init__(self):
        """Initialize DOOM Sentinel"""
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.security = SecurityMiddleware()
        self.rbac = RBACManager()
        self.alert_system = AlertSystem()
        
        # Initialize gateways
        self.telegram_gateway = None
        self.whatsapp_gateway = None
        
        # System state
        self.running = False
        self.start_time = datetime.now()
        
        self.logger.info("🤖 DOOM Sentinel initializing...")
    
    async def initialize(self):
        """Initialize all components"""
        try:
            # Initialize gateways
            self.telegram_gateway = TelegramGateway()
            self.whatsapp_gateway = WhatsAppGateway()
            
            # Set up cross-component references
            self.telegram_gateway.alert_system = self.alert_system
            self.whatsapp_gateway.alert_system = self.alert_system
            
            # Start monitoring
            await self.alert_system.start_monitoring()
            
            self.logger.info("✅ DOOM Sentinel initialized successfully")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize DOOM Sentinel: {e}")
            raise
    
    async def start(self):
        """Start DOOM Sentinel"""
        if self.running:
            self.logger.warning("⚠️ DOOM Sentinel already running")
            return
        
        try:
            await self.initialize()
            
            self.running = True
            
            # Start gateways
            telegram_task = asyncio.create_task(self._start_telegram_gateway())
            whatsapp_task = asyncio.create_task(self._start_whatsapp_gateway())
            
            # Send startup alert
            await self.alert_system.send_custom_alert(
                "DOOM Sentinel Online",
                f"DOOM (Digital Overwatch & Operations Machine) is now online and monitoring\n"
                f"Started at: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"Components: Telegram Gateway, WhatsApp Gateway, Alert System",
                AlertLevel.INFO
            )
            
            self.logger.info("🚀 DOOM Sentinel started successfully")
            
            # Wait for tasks to complete (they should run indefinitely)
            await asyncio.gather(telegram_task, whatsapp_task)
            
        except KeyboardInterrupt:
            self.logger.info("🛑 Received keyboard interrupt")
        except Exception as e:
            self.logger.error(f"❌ Error starting DOOM Sentinel: {e}")
        finally:
            await self.stop()
    
    async def _start_telegram_gateway(self):
        """Start Telegram gateway"""
        try:
            self.logger.info("📱 Starting Telegram Gateway...")
            self.telegram_gateway.start_bot()
        except Exception as e:
            self.logger.error(f"❌ Telegram gateway error: {e}")
            await self.alert_system.send_custom_alert(
                "Telegram Gateway Error",
                f"Telegram gateway encountered an error: {str(e)}",
                AlertLevel.CRITICAL
            )
    
    async def _start_whatsapp_gateway(self):
        """Start WhatsApp gateway"""
        try:
            self.logger.info("📞 Starting WhatsApp Gateway...")
            await self.whatsapp_gateway.start_webhook_server()
        except Exception as e:
            self.logger.error(f"❌ WhatsApp gateway error: {e}")
            await self.alert_system.send_custom_alert(
                "WhatsApp Gateway Error",
                f"WhatsApp gateway encountered an error: {str(e)}",
                AlertLevel.CRITICAL
            )
    
    async def stop(self):
        """Stop DOOM Sentinel"""
        if not self.running:
            return
        
        self.running = False
        
        try:
            # Stop monitoring
            await self.alert_system.stop_monitoring()
            
            # Stop gateways
            if self.telegram_gateway:
                await self.telegram_gateway.stop_bot()
            
            # Send shutdown alert
            await self.alert_system.send_custom_alert(
                "DOOM Sentinel Shutdown",
                f"DOOM Sentinel is shutting down\n"
                f"Uptime: {datetime.now() - self.start_time}",
                AlertLevel.INFO
            )
            
            self.logger.info("🛑 DOOM Sentinel stopped successfully")
            
        except Exception as e:
            self.logger.error(f"❌ Error stopping DOOM Sentinel: {e}")
    
    def get_system_status(self):
        """Get current system status"""
        return {
            'running': self.running,
            'start_time': self.start_time.isoformat(),
            'uptime': str(datetime.now() - self.start_time),
            'components': {
                'telegram_gateway': self.telegram_gateway is not None,
                'whatsapp_gateway': self.whatsapp_gateway is not None,
                'alert_system': self.alert_system.monitoring_active
            },
            'security': self.security.get_active_sessions_count(),
            'alerts': self.alert_system.get_alert_statistics()
        }

# Main execution
async def main():
    """Main execution function"""
    doom = DOOMSentinel()
    
    try:
        await doom.start()
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Check environment variables
    required_env_vars = [
        'TELEGRAM_BOT_TOKEN',
        'TWILIO_ACCOUNT_SID',
        'TWILIO_AUTH_TOKEN',
        'TWILIO_WHATSAPP_NUMBER',
        'ADMIN_WA_NUMBER',
        'ADMIN_TELE_ID'
    ]
    
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"❌ Missing required environment variables: {missing_vars}")
        logger.error("Please set all required environment variables in .env file")
        sys.exit(1)
    
    # Start DOOM Sentinel
    logger.info("🤖 Starting DOOM Sentinel...")
    asyncio.run(main())
