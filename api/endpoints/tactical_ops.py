"""
LUMINA OS - TACTICAL OPERATIONS MODULE
=========================================

Tripwire System - Shadow Wingman & Psychological Weapons
Military-grade tactical operations for strategic prospect engagement

Features:
- Shadow Wingman FOMO trigger deployment
- Hardcoded psychological messages (no AI)
- Campaign mode integration
- Lead-specific tactical operations
- Database integration for prospect targeting
"""

from fastapi import APIRouter, Request, HTTPException
from typing import Dict, Any, Optional
from datetime import datetime
import logging
import json

# Import required modules
from core_modules.db_manager_supabase import get_supabase_manager
from core_modules.notifications.whatsapp_sender import get_whatsapp_sender
from core_modules.notifications.telegram_sender import get_telegram_sender

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ANSI color codes for terminal output
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
BOLD = '\033[1m'
END = '\033[0m'

# Create router
router = APIRouter()

class TacticalOperations:
    """
    Tactical Operations - Shadow Wingman and Psychological Weapons
    Military-grade tactical operations for strategic prospect engagement
    """
    
    def __init__(self):
        """Initialize Tactical Operations"""
        self.logger = logging.getLogger(__name__)
        
        # Initialize database connection
        try:
            self.supabase_manager = get_supabase_manager()
            self.logger.info(f"{GREEN}✅ Tactical Ops: Database connected for tactical operations{END}")
        except Exception as e:
            self.supabase_manager = None
            self.logger.error(f"{RED}❌ Tactical Ops: Database connection failed: {e}{END}")
        
        # Initialize messaging services
        try:
            self.whatsapp_sender = get_whatsapp_sender()
            self.logger.info(f"{GREEN}✅ Tactical Ops: WhatsApp sender initialized{END}")
        except Exception as e:
            self.whatsapp_sender = None
            self.logger.warning(f"{YELLOW}⚠️ WhatsApp sender not available: {e}{END}")
        
        try:
            self.telegram_sender = get_telegram_sender()
            self.logger.info(f"{GREEN}✅ Tactical Ops: Telegram sender initialized{END}")
        except Exception as e:
            self.telegram_sender = None
            self.logger.warning(f"{YELLOW}⚠️ Telegram sender not available: {e}{END}")
        
        # Shadow Wingman FOMO trigger message
        self.shadow_wingman_message = """⚠️ [LUMINA SYSTEM ALERT] Perhatian. Unit yang sedang Anda tinjau baru saja mendapatkan jadwal survei baru dari pihak lain. Harga sistem akan otomatis naik pada periode berikutnya. Harap hubungi konsultan Anda segera."""
        
        self.logger.info(f"{CYAN}🎯 TACTICAL OPERATIONS: Shadow Wingman system initialized{END}")
        self.logger.info(f"{GREEN}✅ Ready for psychological weapon deployment{END}")
    
    def deploy_shadow_wingman(self, lead_id: str) -> Dict[str, Any]:
        """
        Deploy Shadow Wingman FOMO trigger to specific lead
        
        Args:
            lead_id: Target lead ID for tactical operation
            
        Returns:
            Dictionary with deployment results
        """
        try:
            self.logger.info(f"{RED}🎯 SHADOW WINGMAN: Deploying FOMO trigger{END}")
            self.logger.info(f"{CYAN}📋 Target Lead ID: {lead_id}{END}")
            
            # Get lead information from database
            lead_info = self._get_lead_info(lead_id)
            
            if not lead_info:
                self.logger.error(f"{RED}❌ Lead not found: {lead_id}{END}")
                return {
                    "success": False,
                    "error": f"Lead not found: {lead_id}",
                    "lead_id": lead_id,
                    "timestamp": datetime.now().isoformat()
                }
            
            contact_info = lead_info.get('contact_info')
            if not contact_info:
                self.logger.error(f"{RED}❌ No contact info found for lead: {lead_id}{END}")
                return {
                    "success": False,
                    "error": "No contact info found",
                    "lead_id": lead_id,
                    "timestamp": datetime.now().isoformat()
                }
            
            self.logger.info(f"{CYAN}📋 Target Contact: {contact_info}{END}")
            self.logger.info(f"{CYAN}📋 Lead Title: {lead_info.get('title', 'Unknown')}{END}")
            
            # Deploy Shadow Wingman message
            deployment_success = self._deploy_wingman_message(contact_info, lead_info)
            
            if deployment_success:
                # Update lead status
                self._update_lead_tactical_status(lead_id, 'shadow_wingman_deployed')
                
                # Log tactical operation
                self._log_tactical_operation('shadow_wingman', lead_id, contact_info, 'success')
                
                self.logger.info(f"{GREEN}✅ Shadow Wingman deployed successfully{END}")
                
                return {
                    "success": True,
                    "operation": "shadow_wingman_deployed",
                    "lead_id": lead_id,
                    "contact_info": contact_info,
                    "message": self.shadow_wingman_message,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                self.logger.error(f"{RED}❌ Shadow Wingman deployment failed{END}")
                return {
                    "success": False,
                    "error": "Message deployment failed",
                    "lead_id": lead_id,
                    "contact_info": contact_info,
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            self.logger.error(f"{RED}❌ Shadow Wingman deployment error: {str(e)}{END}")
            return {
                "success": False,
                "error": str(e),
                "lead_id": lead_id,
                "timestamp": datetime.now().isoformat()
            }
    
    def _get_lead_info(self, lead_id: str) -> Optional[Dict[str, Any]]:
        """Get lead information from database"""
        try:
            if not self.supabase_manager:
                self.logger.warning(f"{YELLOW}⚠️ Database not available - cannot get lead info{END}")
                return None
            
            # Query database for lead
            result = self.supabase_manager.get_lead_by_id(lead_id)
            
            if result['success'] and result['data']:
                lead_info = result['data']
                self.logger.info(f"{GREEN}✅ Found lead info: {lead_info.get('title', 'Unknown')}{END}")
                return lead_info
            else:
                self.logger.warning(f"{YELLOW}⚠️ Lead not found: {lead_id}{END}")
                return None
                
        except Exception as e:
            self.logger.error(f"{RED}❌ Database query error: {str(e)}{END}")
            return None
    
    def _deploy_wingman_message(self, contact_info: str, lead_info: Dict[str, Any]) -> bool:
        """Deploy Shadow Wingman message via messaging services"""
        try:
            success = False
            
            # Try WhatsApp first
            if self.whatsapp_sender:
                whatsapp_success = self._send_wingman_whatsapp(contact_info, lead_info)
                if whatsapp_success:
                    success = True
                    self.logger.info(f"{GREEN}✅ Shadow Wingman sent via WhatsApp{END}")
            
            # Try Telegram as fallback
            if not success and self.telegram_sender:
                telegram_success = self._send_wingman_telegram(contact_info, lead_info)
                if telegram_success:
                    success = True
                    self.logger.info(f"{GREEN}✅ Shadow Wingman sent via Telegram{END}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"{RED}❌ Wingman message deployment error: {str(e)}{END}")
            return False
    
    def _send_wingman_whatsapp(self, contact_info: str, lead_info: Dict[str, Any]) -> bool:
        """Send Shadow Wingman message via WhatsApp"""
        try:
            # Format message with lead context
            wingman_message = f"{self.shadow_wingman_message}\n\n📋 Lead: {lead_info.get('title', 'Unknown')}\n📱 Ref: {lead_info.get('id', 'Unknown')}"
            
            # Send WhatsApp message
            result = self.whatsapp_sender.send_message(wingman_message, contact_info)
            
            return result.get('success', False)
            
        except Exception as e:
            self.logger.error(f"{RED}❌ WhatsApp send error: {str(e)}{END}")
            return False
    
    def _send_wingman_telegram(self, contact_info: str, lead_info: Dict[str, Any]) -> bool:
        """Send Shadow Wingman notification via Telegram"""
        try:
            # Create notification for tactical team
            notification_message = f"""
🎯 <b>SHADOW WINGMAN DEPLOYED</b>

📋 <b>Target Information:</b>
• Lead ID: {lead_info.get('id', 'Unknown')}
• Contact: {contact_info}
• Title: {lead_info.get('title', 'Unknown')}
• Keyword: {lead_info.get('keyword', 'Unknown')}
• Status: {lead_info.get('status', 'Unknown')}

⚠️ <b>FOMO Trigger Message:</b>
"{self.shadow_wingman_message}"

📱 <b>Delivery Method:</b> WhatsApp
🤖 <b>AI Status:</b> DISABLED (Hardcoded Message)
⚡ <b>Psychological Weapon:</b> FOMO Trigger

⏰ <b>Deployed:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
<i>Shadow Wingman tactical operation completed</i>
            """.strip()
            
            # Send Telegram notification
            chat_id = self.telegram_sender.get_chat_id()
            result = self.telegram_sender.send_message(notification_message, chat_id)
            
            return result.get('success', False)
            
        except Exception as e:
            self.logger.error(f"{RED}❌ Telegram send error: {str(e)}{END}")
            return False
    
    def _update_lead_tactical_status(self, lead_id: str, status: str) -> bool:
        """Update lead tactical status in database"""
        try:
            if not self.supabase_manager:
                self.logger.warning(f"{YELLOW}⚠️ Database not available - status not updated{END}")
                return False
            
            # Update lead status
            update_data = {
                'tactical_status': status,
                'tactical_data': {
                    'shadow_wingman_deployed': status == 'shadow_wingman_deployed',
                    'deployment_timestamp': datetime.now().isoformat(),
                    'message_type': 'fomo_trigger'
                },
                'updated_at': datetime.now().isoformat()
            }
            
            result = self.supabase_manager.update_lead(lead_id, update_data)
            
            if result['success']:
                self.logger.info(f"{GREEN}✅ Lead {lead_id} tactical status updated to: {status}{END}")
                return True
            else:
                self.logger.error(f"{RED}❌ Failed to update lead status: {result.get('error')}{END}")
                return False
                
        except Exception as e:
            self.logger.error(f"{RED}❌ Database update error: {str(e)}{END}")
            return False
    
    def _log_tactical_operation(self, operation_type: str, lead_id: str, contact_info: str, status: str):
        """Log tactical operation for audit trail"""
        try:
            # Create tactical operation log
            operation_log = {
                'operation_id': f"tactical_{int(datetime.now().timestamp())}",
                'operation_type': operation_type,
                'lead_id': lead_id,
                'contact_info': contact_info,
                'status': status,
                'timestamp': datetime.now().isoformat(),
                'ai_disabled': True,
                'psychological_weapon': 'fomo_trigger'
            }
            
            # Log the operation
            self.logger.info(f"{MAGENTA}📋 TACTICAL LOG: {json.dumps(operation_log, indent=2)}{END}")
            
            # In production, this would store to database
            # For now, we'll just log it
            
        except Exception as e:
            self.logger.error(f"{RED}❌ Tactical log error: {str(e)}{END}")
    
    def get_tactical_statistics(self) -> Dict[str, Any]:
        """Get tactical operations statistics"""
        try:
            if not self.supabase_manager:
                return {
                    "total_shadow_wingman": 0,
                    "recent_24h": 0,
                    "recent_7d": 0,
                    "total_operations": 0
                }
            
            # Get statistics from database
            stats = self.supabase_manager.get_lead_statistics()
            
            return {
                "total_shadow_wingman": stats.get('tactical_status_counts', {}).get('shadow_wingman_deployed', 0),
                "recent_24h": stats.get('recent_24h', {}).get('shadow_wingman_deployed', 0),
                "recent_7d": stats.get('recent_7d', {}).get('shadow_wingman_deployed', 0),
                "total_operations": stats.get('total_leads', 0)
            }
            
        except Exception as e:
            self.logger.error(f"{RED}❌ Statistics error: {str(e)}{END}")
            return {
                "total_shadow_wingman": 0,
                "recent_24h": 0,
                "recent_7d": 0,
                "total_operations": 0
            }

# Global Tactical Operations instance
tactical_ops = TacticalOperations()

# API Endpoints
@router.post("/deploy-wingman")
async def deploy_shadow_wingman(request: Request):
    """
    Deploy Shadow Wingman FOMO trigger to specific lead
    
    Args:
        request: Request containing lead_id in JSON body
        
    Returns:
        Dictionary with deployment results
    """
    try:
        # Get request data
        request_data = await request.json()
        
        lead_id = request_data.get('lead_id')
        if not lead_id:
            raise HTTPException(status_code=400, detail="lead_id is required")
        
        logger.info(f"{RED}🎯 TACTICAL OPS: Shadow Wingman deployment request{END}")
        logger.info(f"{CYAN}📋 Lead ID: {lead_id}{END}")
        
        # Deploy Shadow Wingman
        result = tactical_ops.deploy_shadow_wingman(lead_id)
        
        if result.get("success"):
            logger.info(f"{GREEN}✅ Shadow Wingman deployed successfully{END}")
            return {
                "status": "success",
                "message": "Shadow Wingman FOMO trigger deployed successfully",
                "data": result
            }
        else:
            logger.error(f"{RED}❌ Shadow Wingman deployment failed{END}")
            return {
                "status": "error",
                "message": result.get("error", "Unknown error"),
                "data": result
            }
            
    except Exception as e:
        logger.error(f"{RED}❌ Tactical ops endpoint error: {str(e)}{END}")
        raise HTTPException(status_code=500, detail=f"Tactical ops error: {str(e)}")

@router.get("/statistics")
async def get_tactical_statistics():
    """Get tactical operations statistics"""
    try:
        stats = tactical_ops.get_tactical_statistics()
        
        return {
            "status": "success",
            "data": stats,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"{RED}❌ Statistics endpoint error: {str(e)}{END}")
        raise HTTPException(status_code=500, detail=f"Statistics error: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        return {
            "status": "healthy",
            "service": "tactical_operations",
            "timestamp": datetime.now().isoformat(),
            "database": "connected" if tactical_ops.supabase_manager else "disconnected",
            "whatsapp": "connected" if tactical_ops.whatsapp_sender else "disconnected",
            "telegram": "connected" if tactical_ops.telegram_sender else "disconnected",
            "shadow_wingman": "ready"
        }
        
    except Exception as e:
        logger.error(f"{RED}❌ Health check error: {str(e)}{END}")
        raise HTTPException(status_code=500, detail=f"Health check error: {str(e)}")

# Test function
if __name__ == "__main__":
    print(f"{CYAN}{'='*80}{END}")
    print(f"🎯 LUMINA OS - TACTICAL OPERATIONS MODULE{END}")
    print(f"{'='*80}{END}")
    
    print(f"{RED}🎯 Testing Shadow Wingman...{END}")
    
    # Test Shadow Wingman deployment
    test_lead_id = "test_lead_123"
    result = tactical_ops.deploy_shadow_wingman(test_lead_id)
    
    print(f"{GREEN}✅ Test Shadow Wingman completed{END}")
    print(f"{CYAN}📊 Result: {result['success']}{END}")
    
    print(f"{'='*80}{END}")
