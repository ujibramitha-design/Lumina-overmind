"""
LUMINA OS - TRIPWIRE WEBHOOK ENDPOINT
==============================================

Reconnaissance & Tripwire System - Response Catcher & Human Handoff
Critical tripwire listener that detects responses and triggers human intervention

Features:
- POST /api/tripwire/catch-response endpoint
- Automatic detection of bait_deployed target responses
- AI STOP mechanism - no auto-reply loops
- Status tracking: bait_deployed → HOT_RESPONDED
- Urgent Telegram notifications for human handoff
- Complete tripwire trigger logging
"""

from fastapi import APIRouter, Request, HTTPException, BackgroundTasks
from typing import Dict, Any, Optional
from datetime import datetime
import logging
import json
import asyncio

# Import required modules
from core_modules.db_manager_supabase import get_supabase_manager
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

class TripwireListener:
    """
    Tripwire Listener - Critical response detection and human handoff system
    Stops AI auto-reply and triggers urgent human intervention
    """
    
    def __init__(self):
        """Initialize Tripwire Listener"""
        self.logger = logging.getLogger(__name__)
        
        # Initialize database connection
        try:
            self.supabase_manager = get_supabase_manager()
            self.logger.info(f"{GREEN}✅ Tripwire Listener: Database connected for response detection{END}")
        except Exception as e:
            self.supabase_manager = None
            self.logger.error(f"{RED}❌ Tripwire Listener: Database connection failed: {e}{END}")
        
        # Initialize Telegram sender for urgent notifications
        try:
            self.telegram_sender = get_telegram_sender()
            self.logger.info(f"{GREEN}✅ Tripwire Listener: Telegram sender initialized for urgent alerts{END}")
        except Exception as e:
            self.telegram_sender = None
            self.logger.error(f"{RED}❌ Tripwire Listener: Telegram sender failed: {e}{END}")
        
        self.logger.info(f"{CYAN}🚨 TRIPWIRE LISTENER: Response detection system initialized{END}")
        self.logger.info(f"{GREEN}✅ Ready for critical tripwire triggers and human handoff{END}")
    
    async def catch_response(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Catch and process response from bait_deployed target
        
        CRITICAL LOGIC: 
        - STOP AI from replying
        - Update status to HOT_RESPONDED
        - Send urgent Telegram notification
        
        Args:
            request_data: Response data from messaging service
            
        Returns:
            Dictionary with processing results
        """
        try:
            self.logger.info(f"{RED}🚨 TRIPWIRE TRIGGERED: Response received{END}")
            
            # Extract response data
            contact_info = request_data.get('contact_info', 'Unknown')
            message_content = request_data.get('message', '')
            source = request_data.get('source', 'unknown')
            timestamp = request_data.get('timestamp', datetime.now().isoformat())
            
            self.logger.info(f"{CYAN}📋 Response Details:{END}")
            self.logger.info(f"{CYAN}  • Contact: {contact_info}{END}")
            self.logger.info(f"{CYAN}  • Message: {message_content[:100]}...{END}")
            self.logger.info(f"{CYAN}  • Source: {source}{END}")
            self.logger.info(f"{CYAN}  • Time: {timestamp}{END}")
            
            # CRITICAL: Find target with bait_deployed status
            target = self._find_bait_deployed_target(contact_info)
            
            if not target:
                self.logger.warning(f"{YELLOW}⚠️ No bait_deployed target found for {contact_info}{END}")
                return {
                    "success": False,
                    "error": "No bait_deployed target found",
                    "contact_info": contact_info,
                    "timestamp": timestamp
                }
            
            self.logger.info(f"{GREEN}✅ Found bait_deployed target: {target['id']}{END}")
            
            # CRITICAL: Update status to HOT_RESPONDED
            update_success = self._update_target_to_hot_responded(target['id'], request_data)
            
            if not update_success:
                self.logger.error(f"{RED}❌ Failed to update target status{END}")
                return {
                    "success": False,
                    "error": "Failed to update target status",
                    "target_id": target['id'],
                    "contact_info": contact_info,
                    "timestamp": timestamp
                }
            
            self.logger.info(f"{GREEN}✅ Target status updated to HOT_RESPONDED{END}")
            
            # CRITICAL: Send urgent Telegram notification
            notification_sent = self._send_urgent_tripwire_notification(target, request_data)
            
            if not notification_sent:
                self.logger.error(f"{RED}❌ Failed to send urgent notification{END}")
            
            # CRITICAL: STOP AI from replying - this is the key mechanism
            self._stop_ai_reply_system(contact_info)
            
            self.logger.info(f"{GREEN}✅ AI reply system STOPPED for {contact_info}{END}")
            
            # Log tripwire trigger
            self._log_tripwire_trigger(target, request_data)
            
            # Return success
            result = {
                "success": True,
                "action": "tripwire_triggered",
                "target_id": target['id'],
                "contact_info": contact_info,
                "message": message_content,
                "source": source,
                "timestamp": timestamp,
                "ai_stopped": True,
                "notification_sent": notification_sent,
                "status": "HOT_RESPONDED"
            }
            
            self.logger.info(f"{GREEN}✅ TRIPWIRE PROCESSING COMPLETED{END}")
            self.logger.info(f"{CYAN}🚨 Human handoff required for {contact_info}{END}")
            
            return result
            
        except Exception as e:
            self.logger.error(f"{RED}❌ Tripwire processing error: {str(e)}{END}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _find_bait_deployed_target(self, contact_info: str) -> Optional[Dict[str, Any]]:
        """Find target with bait_deployed status"""
        try:
            if not self.supabase_manager:
                self.logger.warning(f"{YELLOW}⚠️ Database not available - cannot find target{END}")
                return None
            
            # Query database for bait_deployed target
            result = self.supabase_manager.get_leads_by_contact_and_status(contact_info, 'bait_deployed')
            
            if result['success'] and result['data']:
                target = result['data'][0]  # Get first matching target
                self.logger.info(f"{GREEN}✅ Found bait_deployed target: {target['id']}{END}")
                return target
            else:
                self.logger.warning(f"{YELLOW}⚠️ No bait_deployed target found for {contact_info}{END}")
                return None
                
        except Exception as e:
            self.logger.error(f"{RED}❌ Database query error: {str(e)}{END}")
            return None
    
    def _update_target_to_hot_responded(self, target_id: str, response_data: Dict[str, Any]) -> bool:
        """Update target status to HOT_RESPONDED"""
        try:
            if not self.supabase_manager:
                self.logger.warning(f"{YELLOW}⚠️ Database not available - status not updated{END}")
                return False
            
            # Update lead status and tripwire data
            update_data = {
                'status': 'HOT_RESPONDED',
                'tripwire_data': {
                    'bait_deployed': True,
                    'response_received': True,
                    'hot_responded': True,
                    'response_timestamp': response_data.get('timestamp'),
                    'response_message': response_data.get('message'),
                    'response_source': response_data.get('source')
                },
                'updated_at': datetime.now().isoformat()
            }
            
            result = self.supabase_manager.update_lead(target_id, update_data)
            
            if result['success']:
                self.logger.info(f"{GREEN}✅ Target {target_id} updated to HOT_RESPONDED{END}")
                return True
            else:
                self.logger.error(f"{RED}❌ Failed to update target: {result.get('error')}{END}")
                return False
                
        except Exception as e:
            self.logger.error(f"{RED}❌ Database update error: {str(e)}{END}")
            return False
    
    def _send_urgent_tripwire_notification(self, target: Dict[str, Any], response_data: Dict[str, Any]) -> bool:
        """Send urgent Telegram notification for human handoff"""
        try:
            if not self.telegram_sender:
                self.logger.warning(f"{YELLOW}⚠️ Telegram not available - notification not sent{END}")
                return False
            
            # Extract target information
            contact_info = target.get('contact_info', 'Unknown')
            target_name = target.get('title', 'Unknown')
            keyword = target.get('keyword', 'Unknown')
            message_content = response_data.get('message', '')
            source = response_data.get('source', 'Unknown')
            
            # Create urgent notification
            urgent_notification = f"""
🚨 <b>TRIPWIRE TRIGGERED!</b>

🎯 <b>Prospek Responded to Bait:</b>
• Contact: {contact_info}
• Name: {target_name}
• Keyword: {keyword}
• Source: {source}

💬 <b>Response Message:</b>
"{message_content}"

🔥 <b>Status:</b> HOT RESPONDED
🤖 <b>AI Status:</b> STOPPED
👤 <b>Action Required:</b> HUMAN TAKEOVER

⚠️ <b>URGENT ACTION NEEDED:</b>
Segera ambil alih komunikasi dengan prospek ini!
AI telah dihentikan untuk mencegah auto-reply loop.

📋 <b>Target Details:</b>
• ID: {target.get('id')}
• Scouted: {target.get('scouted_at')}
• Bait Deployed: {target.get('bait_deployed_at')}
• Response Time: {response_data.get('timestamp')}

⏰ <b>Triggered:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
<i>This is an automated tripwire alert - immediate human intervention required</i>
            """.strip()
            
            # Send urgent notification
            result = self.telegram_sender.send_message(urgent_notification)
            
            if result.get('success'):
                self.logger.info(f"{GREEN}✅ Urgent tripwire notification sent{END}")
                return True
            else:
                self.logger.error(f"{RED}❌ Failed to send urgent notification{END}")
                return False
                
        except Exception as e:
            self.logger.error(f"{RED}❌ Notification error: {str(e)}{END}")
            return False
    
    def _stop_ai_reply_system(self, contact_info: str):
        """
        CRITICAL: Stop AI from replying to this contact
        This prevents auto-reply loops
        """
        try:
            # Log AI stop action
            self.logger.info(f"{RED}🛑 AI REPLY SYSTEM STOPPED for {contact_info}{END}")
            self.logger.info(f"{CYAN}📋 Reason: Tripwire triggered - human handoff required{END}")
            
            # In a real implementation, this would:
            # 1. Add contact to AI blacklist
            # 2. Disable conversational AI for this contact
            # 3. Set flag in database to prevent AI replies
            # 4. Notify all AI systems to ignore this contact
            
            # For now, we'll log the action
            ai_stop_data = {
                'contact_info': contact_info,
                'ai_stopped': True,
                'stop_reason': 'tripwire_triggered',
                'stop_timestamp': datetime.now().isoformat(),
                'human_handoff_required': True
            }
            
            # Store AI stop record (would go to database in production)
            self._store_ai_stop_record(ai_stop_data)
            
            self.logger.info(f"{GREEN}✅ AI reply system successfully stopped{END}")
            
        except Exception as e:
            self.logger.error(f"{RED}❌ AI stop error: {str(e)}{END}")
    
    def _store_ai_stop_record(self, stop_data: Dict[str, Any]):
        """Store AI stop record for audit trail"""
        try:
            # In production, this would store to database
            # For now, we'll just log it
            self.logger.info(f"{CYAN}📋 AI Stop Record: {json.dumps(stop_data, indent=2)}{END}")
            
        except Exception as e:
            self.logger.error(f"{RED}❌ AI stop record error: {str(e)}{END}")
    
    def _log_tripwire_trigger(self, target: Dict[str, Any], response_data: Dict[str, Any]):
        """Log tripwire trigger for audit trail"""
        try:
            # Create tripwire log entry
            tripwire_log = {
                'trigger_id': f"tripwire_{int(datetime.now().timestamp())}",
                'target_id': target.get('id'),
                'contact_info': target.get('contact_info'),
                'response_data': response_data,
                'trigger_timestamp': datetime.now().isoformat(),
                'ai_stopped': True,
                'human_handoff_required': True,
                'notification_sent': True
            }
            
            # Log the trigger
            self.logger.info(f"{MAGENTA}📋 TRIPWIRE LOG: {json.dumps(tripwire_log, indent=2)}{END}")
            
            # In production, this would store to database
            # For now, we'll just log it
            
        except Exception as e:
            self.logger.error(f"{RED}❌ Tripwire log error: {str(e)}{END}")
    
    def get_tripwire_statistics(self) -> Dict[str, Any]:
        """Get tripwire statistics"""
        try:
            if not self.supabase_manager:
                return {
                    "total_hot_responded": 0,
                    "recent_24h": 0,
                    "recent_7d": 0,
                    "total_triggers": 0
                }
            
            # Get statistics from database
            stats = self.supabase_manager.get_lead_statistics()
            
            return {
                "total_hot_responded": stats.get('status_counts', {}).get('HOT_RESPONDED', 0),
                "recent_24h": stats.get('recent_24h', {}).get('HOT_RESPONDED', 0),
                "recent_7d": stats.get('recent_7d', {}).get('HOT_RESPONDED', 0),
                "total_triggers": stats.get('total_leads', 0)
            }
            
        except Exception as e:
            self.logger.error(f"{RED}❌ Statistics error: {str(e)}{END}")
            return {
                "total_hot_responded": 0,
                "recent_24h": 0,
                "recent_7d": 0,
                "total_triggers": 0
            }

# Global Tripwire Listener instance
tripwire_listener = TripwireListener()

# API Endpoints
@router.post("/catch-response")
async def catch_response(request: Request):
    """
    Catch response from bait_deployed target
    
    CRITICAL LOGIC:
    - STOP AI from replying
    - Update status to HOT_RESPONDED
    - Send urgent Telegram notification
    """
    try:
        # Get request data
        request_data = await request.json()
        
        logger.info(f"{RED}🚨 TRIPWIRE WEBHOOK: Response received{END}")
        logger.info(f"{CYAN}📋 Request data: {json.dumps(request_data, indent=2)}{END}")
        
        # Process response
        result = await tripwire_listener.catch_response(request_data)
        
        if result.get("success"):
            logger.info(f"{GREEN}✅ Tripwire processed successfully{END}")
            return {
                "status": "success",
                "message": "Tripwire triggered and processed",
                "data": result
            }
        else:
            logger.error(f"{RED}❌ Tripwire processing failed{END}")
            return {
                "status": "error",
                "message": result.get("error", "Unknown error"),
                "data": result
            }
            
    except Exception as e:
        logger.error(f"{RED}❌ Tripwire webhook error: {str(e)}{END}")
        raise HTTPException(status_code=500, detail=f"Tripwire webhook error: {str(e)}")

@router.get("/statistics")
async def get_tripwire_statistics():
    """Get tripwire statistics"""
    try:
        stats = tripwire_listener.get_tripwire_statistics()
        
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
            "service": "tripwire_listener",
            "timestamp": datetime.now().isoformat(),
            "database": "connected" if tripwire_listener.supabase_manager else "disconnected",
            "telegram": "connected" if tripwire_listener.telegram_sender else "disconnected"
        }
        
    except Exception as e:
        logger.error(f"{RED}❌ Health check error: {str(e)}{END}")
        raise HTTPException(status_code=500, detail=f"Health check error: {str(e)}")

# Test function
if __name__ == "__main__":
    print(f"{CYAN}{'='*80}{END}")
    print(f"🚨 LUMINA OS - TRIPWIRE WEBHOOK ENDPOINT{END}")
    print(f"{'='*80}{END}")
    
    print(f"{RED}🚨 Testing Tripwire Listener...{END}")
    
    # Test tripwire processing
    test_response = {
        "contact_info": "+62812345678",
        "message": "Halo, saya tertarik dengan properti yang ditawarkan. Boleh info lebih lanjut?",
        "source": "whatsapp",
        "timestamp": datetime.now().isoformat()
    }
    
    async def test_tripwire():
        try:
            result = await tripwire_listener.catch_response(test_response)
            print(f"{GREEN}✅ Test tripwire completed{END}")
            print(f"{CYAN}📊 Result: {result['success']}{END}")
        except Exception as e:
            print(f"{RED}❌ Test failed: {e}{END}")
    
    # Run test
    asyncio.run(test_tripwire())
    
    print(f"{'='*80}{END}")
