"""
LUMINA OVERMIND SYSTEM - Plugin API Endpoints
============================================

External service integrations for workflow automation
"""

import os
import httpx
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, Field
from api.middleware.jwt_auth import get_current_user

router = APIRouter(prefix="/api/plugins", tags=["Plugins"])

# Configure logging
logger = logging.getLogger(__name__)

# Plugin configuration models
class WhatsAppConfig(BaseModel):
    phone_number: str
    api_key: str
    webhook_url: Optional[str] = None

class EmailConfig(BaseModel):
    smtp_host: str
    smtp_port: int
    username: str
    password: str
    from_email: str

class SlackConfig(BaseModel):
    webhook_url: str
    channel: Optional[str] = "#general"
    username: Optional[str] = "Lumina Overmind"

# Message models
class WhatsAppMessage(BaseModel):
    to: str
    message: str
    media_url: Optional[str] = None

class EmailMessage(BaseModel):
    to: List[str]
    subject: str
    html_body: Optional[str] = None
    text_body: Optional[str] = None

class SlackMessage(BaseModel):
    text: str
    channel: Optional[str] = None
    username: Optional[str] = None
    icon_emoji: Optional[str] = ":robot_face:"

# Plugin execution models
class PluginExecution(BaseModel):
    plugin_type: str = Field(..., regex="^(whatsapp|email|slack)$")
    action: str = Field(..., regex="^(send_message|send_notification)$")
    config: Dict[str, Any]
    data: Dict[str, Any]

@router.post("/whatsapp/send")
async def send_whatsapp_message(
    message: WhatsAppMessage,
    config: WhatsAppConfig,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Send WhatsApp message via external API
    
    Args:
        message: WhatsApp message details
        config: WhatsApp API configuration
        current_user: Authenticated user
        
    Returns:
        Dict with message sending result
    """
    try:
        # WhatsApp API integration (example with Twilio-like API)
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://api.twilio.com/2010-04-01/Accounts/{config.phone_number}/Messages.json",
                auth=(config.phone_number, config.api_key),
                data={
                    "To": f"whatsapp:{message.to}",
                    "From": f"whatsapp:{config.phone_number}",
                    "Body": message.message,
                    **({"MediaUrl": message.media_url} if message.media_url else {})
                },
                timeout=30.0
            )
            
            if response.status_code == 201:
                result = response.json()
                logger.info(f"✅ WhatsApp message sent to {message.to}")
                
                return {
                    "success": True,
                    "message_id": result.get("sid"),
                    "status": "sent",
                    "to": message.to,
                    "timestamp": datetime.utcnow().isoformat()
                }
            else:
                logger.error(f"❌ WhatsApp API error: {response.status_code} - {response.text}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Failed to send WhatsApp message: {response.text}"
                )
                
    except httpx.RequestError as e:
        logger.error(f"❌ WhatsApp API request error: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="WhatsApp service unavailable"
        )
    except Exception as e:
        logger.error(f"❌ WhatsApp send error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.post("/email/send")
async def send_email_message(
    message: EmailMessage,
    config: EmailConfig,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Send email via SMTP
    
    Args:
        message: Email message details
        config: SMTP configuration
        current_user: Authenticated user
        
    Returns:
        Dict with email sending result
    """
    try:
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        from email.mime.html import MIMEText as MIMETextHTML
        
        # Create email message
        email_msg = MIMEMultipart('alternative')
        email_msg['Subject'] = message.subject
        email_msg['From'] = f"{config.from_email}"
        email_msg['To'] = ", ".join(message.to)
        
        # Add body
        if message.html_body:
            html_part = MIMETextHTML(message.html_body, 'html')
            email_msg.attach(html_part)
        
        if message.text_body:
            text_part = MIMEText(message.text_body, 'plain')
            email_msg.attach(text_part)
        
        # Send email
        with smtplib.SMTP(config.smtp_host, config.smtp_port) as server:
            server.starttls()
            server.login(config.username, config.password)
            server.send_message(email_msg)
        
        logger.info(f"✅ Email sent to {message.to}")
        
        return {
            "success": True,
            "message_id": f"email_{datetime.utcnow().timestamp()}",
            "status": "sent",
            "to": message.to,
            "subject": message.subject,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except smtplib.SMTPAuthenticationError:
        logger.error("❌ SMTP authentication failed")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="SMTP authentication failed"
        )
    except smtplib.SMTPRecipientsRefused:
        logger.error(f"❌ All recipients refused: {message.to}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="All recipients refused"
        )
    except Exception as e:
        logger.error(f"❌ Email send error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send email"
        )

@router.post("/slack/send")
async def send_slack_message(
    message: SlackMessage,
    config: SlackConfig,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Send Slack message via webhook
    
    Args:
        message: Slack message details
        config: Slack webhook configuration
        current_user: Authenticated user
        
    Returns:
        Dict with message sending result
    """
    try:
        payload = {
            "text": message.text,
            "username": message.username or config.username,
            "icon_emoji": message.icon_emoji,
            "channel": message.channel or config.channel
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                config.webhook_url,
                json=payload,
                timeout=30.0
            )
            
            if response.status_code == 200:
                logger.info(f"✅ Slack message sent to {payload['channel']}")
                
                return {
                    "success": True,
                    "message_id": f"slack_{datetime.utcnow().timestamp()}",
                    "status": "sent",
                    "channel": payload['channel'],
                    "timestamp": datetime.utcnow().isoformat()
                }
            else:
                logger.error(f"❌ Slack API error: {response.status_code} - {response.text}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Failed to send Slack message: {response.text}"
                )
                
    except httpx.RequestError as e:
        logger.error(f"❌ Slack API request error: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Slack service unavailable"
        )
    except Exception as e:
        logger.error(f"❌ Slack send error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.post("/execute")
async def execute_plugin(
    execution: PluginExecution,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Execute plugin action based on workflow node
    
    Args:
        execution: Plugin execution details
        current_user: Authenticated user
        
    Returns:
        Dict with execution result
    """
    try:
        logger.info(f"🔧 Executing plugin: {execution.plugin_type} - {execution.action}")
        
        if execution.plugin_type == "whatsapp":
            if execution.action == "send_message":
                message = WhatsAppMessage(**execution.data)
                config = WhatsAppConfig(**execution.config)
                
                result = await send_whatsapp_message(message, config, current_user)
                return {
                    "plugin": "whatsapp",
                    "action": "send_message",
                    "result": result,
                    "timestamp": datetime.utcnow().isoformat()
                }
        
        elif execution.plugin_type == "email":
            if execution.action == "send_message":
                message = EmailMessage(**execution.data)
                config = EmailConfig(**execution.config)
                
                result = await send_email_message(message, config, current_user)
                return {
                    "plugin": "email",
                    "action": "send_message", 
                    "result": result,
                    "timestamp": datetime.utcnow().isoformat()
                }
        
        elif execution.plugin_type == "slack":
            if execution.action == "send_message":
                message = SlackMessage(**execution.data)
                config = SlackConfig(**execution.config)
                
                result = await send_slack_message(message, config, current_user)
                return {
                    "plugin": "slack",
                    "action": "send_message",
                    "result": result,
                    "timestamp": datetime.utcnow().isoformat()
                }
        
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported plugin: {execution.plugin_type}"
            )
            
    except Exception as e:
        logger.error(f"❌ Plugin execution error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Plugin execution failed"
        )

@router.get("/status")
async def get_plugin_status(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get status of all available plugins
    
    Args:
        current_user: Authenticated user
        
    Returns:
        Dict with plugin status information
    """
    return {
        "plugins": {
            "whatsapp": {
                "status": "available",
                "actions": ["send_message"],
                "description": "Send WhatsApp messages via Twilio API"
            },
            "email": {
                "status": "available", 
                "actions": ["send_message"],
                "description": "Send emails via SMTP"
            },
            "slack": {
                "status": "available",
                "actions": ["send_message"],
                "description": "Send Slack messages via webhook"
            }
        },
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/config/{plugin_type}")
async def get_plugin_config_template(
    plugin_type: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get configuration template for a plugin
    
    Args:
        plugin_type: Type of plugin
        current_user: Authenticated user
        
    Returns:
        Dict with configuration template
    """
    templates = {
        "whatsapp": {
            "phone_number": "string (required)",
            "api_key": "string (required)",
            "webhook_url": "string (optional)"
        },
        "email": {
            "smtp_host": "string (required)",
            "smtp_port": "integer (required)",
            "username": "string (required)",
            "password": "string (required)",
            "from_email": "string (required)"
        },
        "slack": {
            "webhook_url": "string (required)",
            "channel": "string (optional, default: #general)",
            "username": "string (optional, default: Lumina Overmind)"
        }
    }
    
    if plugin_type not in templates:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plugin template not found: {plugin_type}"
        )
    
    return {
        "plugin_type": plugin_type,
        "config_template": templates[plugin_type],
        "timestamp": datetime.utcnow().isoformat()
    }
