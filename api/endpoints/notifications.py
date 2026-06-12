"""
Notifications API Endpoints
Email, WhatsApp, Telegram, SMS, and multi-channel notifications
"""

import os
import sys
import logging
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel
from datetime import datetime

# Add root directory to Python path
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(root_dir)

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Pydantic models
class EmailNotificationRequest(BaseModel):
    to: str
    subject: str
    template: str
    template_data: Dict[str, Any]
    cc: Optional[List[str]] = None
    bcc: Optional[List[str]] = None
    attachments: Optional[List[Dict[str, Any]]] = None

class WhatsAppNotificationRequest(BaseModel):
    to: str
    message: str
    media_url: Optional[str] = None
    media_type: Optional[str] = None

class TelegramNotificationRequest(BaseModel):
    chat_id: str
    message: str
    parse_mode: str = "HTML"
    disable_web_page_preview: bool = False
    reply_to_message_id: Optional[str] = None

class SMSNotificationRequest(BaseModel):
    to: str
    message: str
    sender_id: Optional[str] = None

class CampaignNotificationRequest(BaseModel):
    campaign_id: str
    notification_type: str
    recipients: List[Dict[str, Any]]
    template: str
    template_data: Dict[str, Any]
    channels: List[str] = ["email"]

class HotLeadAlertRequest(BaseModel):
    lead_data: Dict[str, Any]
    channels: List[str] = ["telegram", "email"]

# Dependency for database connection
async def get_db():
    """Get database connection"""
    try:
        from core_modules.db_manager_postgres import postgres_db_manager
        return postgres_db_manager
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {e}")

@router.post("/send-email")
async def send_email_notification(
    request: EmailNotificationRequest,
    background_tasks: BackgroundTasks,
    db = Depends(get_db)
):
    """
    Send email notification
    """
    try:
        logger.info(f"Sending email to: {request.to}")
        
        # Submit task to Celery
        from tasks.notification_tasks import send_email
        task = send_email.s(
            to=request.to,
            subject=request.subject,
            template=request.template,
            template_data=request.template_data,
            cc=request.cc,
            bcc=request.bcc,
            attachments=request.attachments
        )
        
        result = task.apply_async()
        
        return {
            "success": True,
            "task_id": result.id,
            "status": "submitted",
            "to": request.to,
            "subject": request.subject,
            "message": "Email notification task submitted successfully"
        }
        
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/send-whatsapp")
async def send_whatsapp_notification(
    request: WhatsAppNotificationRequest,
    background_tasks: BackgroundTasks,
    db = Depends(get_db)
):
    """
    Send WhatsApp message
    """
    try:
        logger.info(f"Sending WhatsApp to: {request.to}")
        
        # Submit task to Celery
        from tasks.notification_tasks import send_whatsapp
        task = send_whatsapp.s(
            to=request.to,
            message=request.message,
            media_url=request.media_url,
            media_type=request.media_type
        )
        
        result = task.apply_async()
        
        return {
            "success": True,
            "task_id": result.id,
            "status": "submitted",
            "to": request.to,
            "message": "WhatsApp notification task submitted successfully"
        }
        
    except Exception as e:
        logger.error(f"Failed to send WhatsApp: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/send-telegram")
async def send_telegram_notification(
    request: TelegramNotificationRequest,
    background_tasks: BackgroundTasks,
    db = Depends(get_db)
):
    """
    Send Telegram message
    """
    try:
        logger.info(f"Sending Telegram to chat: {request.chat_id}")
        
        # Submit task to Celery
        from tasks.notification_tasks import send_telegram
        task = send_telegram.s(
            chat_id=request.chat_id,
            message=request.message,
            parse_mode=request.parse_mode,
            disable_web_page_preview=request.disable_web_page_preview,
            reply_to_message_id=request.reply_to_message_id
        )
        
        result = task.apply_async()
        
        return {
            "success": True,
            "task_id": result.id,
            "status": "submitted",
            "chat_id": request.chat_id,
            "message": "Telegram notification task submitted successfully"
        }
        
    except Exception as e:
        logger.error(f"Failed to send Telegram: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/send-sms")
async def send_sms_notification(
    request: SMSNotificationRequest,
    background_tasks: BackgroundTasks,
    db = Depends(get_db)
):
    """
    Send SMS message
    """
    try:
        logger.info(f"Sending SMS to: {request.to}")
        
        # Submit task to Celery
        from tasks.notification_tasks import send_sms
        task = send_sms.s(
            to=request.to,
            message=request.message,
            sender_id=request.sender_id
        )
        
        result = task.apply_async()
        
        return {
            "success": True,
            "task_id": result.id,
            "status": "submitted",
            "to": request.to,
            "message": "SMS notification task submitted successfully"
        }
        
    except Exception as e:
        logger.error(f"Failed to send SMS: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/send-campaign")
async def send_campaign_notification(
    request: CampaignNotificationRequest,
    background_tasks: BackgroundTasks,
    db = Depends(get_db)
):
    """
    Send campaign notifications across multiple channels
    """
    try:
        logger.info(f"Sending campaign notification: {request.campaign_id}")
        
        # Submit task to Celery
        from tasks.notification_tasks import send_campaign_notification
        task = send_campaign_notification.s(
            campaign_id=request.campaign_id,
            notification_type=request.notification_type,
            recipients=request.recipients,
            template=request.template,
            template_data=request.template_data,
            channels=request.channels
        )
        
        result = task.apply_async()
        
        return {
            "success": True,
            "task_id": result.id,
            "status": "submitted",
            "campaign_id": request.campaign_id,
            "notification_type": request.notification_type,
            "channels": request.channels,
            "total_recipients": len(request.recipients),
            "message": "Campaign notification task submitted successfully"
        }
        
    except Exception as e:
        logger.error(f"Failed to send campaign notification: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/send-brochure")
async def send_brochure_notification(
    recipient_email: str,
    recipient_name: str,
    brochure_path: str,
    property_details: Dict[str, Any],
    custom_message: Optional[str] = None,
    background_tasks: BackgroundTasks = None,
    db = Depends(get_db)
):
    """
    Send brochure notification with attachment
    """
    try:
        logger.info(f"Sending brochure notification to: {recipient_email}")
        
        # Submit task to Celery
        from tasks.notification_tasks import send_brochure_notification
        task = send_brochure_notification.s(
            recipient_email=recipient_email,
            recipient_name=recipient_name,
            brochure_path=brochure_path,
            property_details=property_details,
            custom_message=custom_message
        )
        
        result = task.apply_async()
        
        return {
            "success": True,
            "task_id": result.id,
            "status": "submitted",
            "recipient_email": recipient_email,
            "recipient_name": recipient_name,
            "brochure_path": brochure_path,
            "message": "Brochure notification task submitted successfully"
        }
        
    except Exception as e:
        logger.error(f"Failed to send brochure notification: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/send-hot-lead-alert")
async def send_hot_lead_alert(
    request: HotLeadAlertRequest,
    background_tasks: BackgroundTasks,
    db = Depends(get_db)
):
    """
    Send hot lead alert to sales team
    """
    try:
        logger.info(f"Sending hot lead alert for lead: {request.lead_data.get('id', 'Unknown')}")
        
        # Submit task to Celery
        from tasks.notification_tasks import send_hot_lead_alert
        task = send_hot_lead_alert.s(
            lead_data=request.lead_data,
            channels=request.channels
        )
        
        result = task.apply_async()
        
        return {
            "success": True,
            "task_id": result.id,
            "status": "submitted",
            "lead_id": request.lead_data.get('id'),
            "channels": request.channels,
            "message": "Hot lead alert task submitted successfully"
        }
        
    except Exception as e:
        logger.error(f"Failed to send hot lead alert: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/templates")
async def get_notification_templates():
    """
    Get available notification templates
    """
    try:
        templates = [
            {
                "name": "brochure_notification",
                "type": "email",
                "description": "Brochure notification with property details"
            },
            {
                "name": "hot_lead_alert",
                "type": "email",
                "description": "Hot lead alert for sales team"
            },
            {
                "name": "welcome_message",
                "type": "whatsapp",
                "description": "Welcome message for new leads"
            },
            {
                "name": "follow_up",
                "type": "sms",
                "description": "Follow-up message for leads"
            }
        ]
        
        return {
            "success": True,
            "templates": templates,
            "total": len(templates)
        }
        
    except Exception as e:
        logger.error(f"Failed to get notification templates: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/channels")
async def get_notification_channels():
    """
    Get available notification channels
    """
    try:
        channels = [
            {
                "name": "email",
                "description": "Email notifications",
                "enabled": True,
                "config_required": ["SMTP_SERVER", "SMTP_USERNAME", "SMTP_PASSWORD"]
            },
            {
                "name": "whatsapp",
                "description": "WhatsApp messages",
                "enabled": True,
                "config_required": ["WHATSAPP_API_URL", "WHATSAPP_TOKEN"]
            },
            {
                "name": "telegram",
                "description": "Telegram messages",
                "enabled": True,
                "config_required": ["TELEGRAM_BOT_TOKEN"]
            },
            {
                "name": "sms",
                "description": "SMS messages",
                "enabled": True,
                "config_required": ["SMS_API_URL", "SMS_API_KEY"]
            }
        ]
        
        return {
            "success": True,
            "channels": channels,
            "total": len(channels)
        }
        
    except Exception as e:
        logger.error(f"Failed to get notification channels: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats")
async def get_notification_stats(db = Depends(get_db)):
    """
    Get notification statistics
    """
    try:
        # Get task statistics
        from tasks.celery_app import TaskMonitor
        task_stats = TaskMonitor.get_task_stats()
        
        # Get notification logs from database
        notification_logs = await db.execute_query(
            """
            SELECT channel, status, COUNT(*) as count 
            FROM NotificationLog 
            GROUP BY channel, status 
            ORDER BY count DESC
            """
        )
        
        return {
            "success": True,
            "task_statistics": task_stats,
            "notification_logs": notification_logs,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get notification stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/task/{task_id}")
async def get_notification_task_status(task_id: str):
    """
    Get notification task status by ID
    """
    try:
        from tasks.celery_app import celery_app
        
        result = celery_app.AsyncResult(task_id)
        
        return {
            "success": True,
            "task_id": task_id,
            "status": result.status,
            "result": result.result if result.ready() else None,
            "ready": result.ready()
        }
        
    except Exception as e:
        logger.error(f"Failed to get task status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/test-connection")
async def test_notification_connections():
    """
    Test connections to all notification services
    """
    try:
        results = {}
        
        # Test email connection
        try:
            import smtplib
            smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
            smtp_port = int(os.getenv('SMTP_PORT', '587'))
            
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.quit()
            results['email'] = {'status': 'connected', 'message': 'SMTP connection successful'}
        except Exception as e:
            results['email'] = {'status': 'failed', 'message': str(e)}
        
        # Test Telegram connection
        try:
            import telegram
            bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
            if bot_token:
                bot = telegram.Bot(token=bot_token)
                await bot.get_me()
                results['telegram'] = {'status': 'connected', 'message': 'Telegram bot connected'}
            else:
                results['telegram'] = {'status': 'failed', 'message': 'TELEGRAM_BOT_TOKEN not configured'}
        except Exception as e:
            results['telegram'] = {'status': 'failed', 'message': str(e)}
        
        # Test WhatsApp connection
        try:
            whatsapp_token = os.getenv('WHATSAPP_TOKEN')
            if whatsapp_token:
                results['whatsapp'] = {'status': 'connected', 'message': 'WhatsApp API token available'}
            else:
                results['whatsapp'] = {'status': 'failed', 'message': 'WHATSAPP_TOKEN not configured'}
        except Exception as e:
            results['whatsapp'] = {'status': 'failed', 'message': str(e)}
        
        # Test SMS connection
        try:
            sms_api_key = os.getenv('SMS_API_KEY')
            if sms_api_key:
                results['sms'] = {'status': 'connected', 'message': 'SMS API key available'}
            else:
                results['sms'] = {'status': 'failed', 'message': 'SMS_API_KEY not configured'}
        except Exception as e:
            results['sms'] = {'status': 'failed', 'message': str(e)}
        
        return {
            "success": True,
            "connections": results,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to test notification connections: {e}")
        raise HTTPException(status_code=500, detail=str(e))
