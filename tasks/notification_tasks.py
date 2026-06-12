"""
LUMINA OS - NOTIFICATION TASKS
================================

Async notification tasks for email, WhatsApp, Telegram,
and other communication channels.

Features:
- Email sending with HTML templates
- WhatsApp message delivery
- Telegram notifications
- SMS integration
- Push notifications
- Multi-channel campaign management
"""

import os
import sys
import json
import asyncio
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import requests
from jinja2 import Template

# Add root directory to Python path
root_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root_dir)

# Import Celery app
from tasks.celery_app import celery_app, notification_task

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@notification_task
def send_email(
    self,
    to: str,
    subject: str,
    template: str,
    template_data: Dict[str, Any],
    attachments: Optional[List[Dict[str, Any]]] = None,
    cc: Optional[List[str]] = None,
    bcc: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Send email with HTML template and attachments
    
    Args:
        to: Recipient email address
        subject: Email subject
        template: Email template name or HTML content
        template_data: Data for template rendering
        attachments: List of attachment data
        cc: CC recipients
        bcc: BCC recipients
    
    Returns:
        Dictionary containing sending results
    """
    
    try:
        logger.info(f"Sending email to: {to}")
        
        # Email configuration
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', '587'))
        smtp_username = os.getenv('SMTP_USERNAME')
        smtp_password = os.getenv('SMTP_PASSWORD')
        
        if not all([smtp_username, smtp_password]):
            raise Exception("SMTP credentials not configured")
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = smtp_username
        msg['To'] = to
        
        if cc:
            msg['Cc'] = ', '.join(cc)
        
        # Render template
        if template.endswith('.html') or '<' in template:
            # HTML template
            html_content = render_template(template, template_data)
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
        else:
            # Plain text template
            text_content = render_template(template, template_data)
            text_part = MIMEText(text_content, 'plain')
            msg.attach(text_part)
        
        # Add attachments
        if attachments:
            for attachment in attachments:
                add_attachment(msg, attachment)
        
        # Send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        
        recipients = [to]
        if cc:
            recipients.extend(cc)
        if bcc:
            recipients.extend(bcc)
        
        server.sendmail(smtp_username, recipients, msg.as_string())
        server.quit()
        
        logger.info(f"Email sent successfully to: {to}")
        
        return {
            'success': True,
            'to': to,
            'subject': subject,
            'template': template,
            'sent_at': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Email sending failed: {e}")
        raise self.retry(exc=e, countdown=60, max_retries=3)

@notification_task
def send_whatsapp(
    self,
    to: str,
    message: str,
    media_url: Optional[str] = None,
    media_type: Optional[str] = None
) -> Dict[str, Any]:
    """
    Send WhatsApp message
    
    Args:
        to: Recipient phone number (with country code)
        message: Message content
        media_url: URL of media file (optional)
        media_type: Type of media (image, document, audio, video)
    
    Returns:
        Dictionary containing sending results
    """
    
    try:
        logger.info(f"Sending WhatsApp to: {to}")
        
        # WhatsApp API configuration
        whatsapp_api_url = os.getenv('WHATSAPP_API_URL')
        whatsapp_token = os.getenv('WHATSAPP_TOKEN')
        
        if not all([whatsapp_api_url, whatsapp_token]):
            raise Exception("WhatsApp API credentials not configured")
        
        # Prepare message payload
        payload = {
            'messaging_product': 'whatsapp',
            'recipient_type': 'individual',
            'to': to,
            'type': 'text' if not media_url else media_type,
            'text': {
                'body': message
            }
        }
        
        # Add media if provided
        if media_url:
            payload[media_type] = {
                'link': media_url
            }
        
        # Send message
        headers = {
            'Authorization': f'Bearer {whatsapp_token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            f"{whatsapp_api_url}/messages",
            json=payload,
            headers=headers,
            timeout=30
        )
        
        response.raise_for_status()
        
        result = response.json()
        
        logger.info(f"WhatsApp sent successfully to: {to}")
        
        return {
            'success': True,
            'to': to,
            'message_id': result.get('messages', [{}])[0].get('id'),
            'sent_at': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"WhatsApp sending failed: {e}")
        raise self.retry(exc=e, countdown=60, max_retries=3)

@notification_task
def send_telegram(
    self,
    chat_id: str,
    message: str,
    parse_mode: str = 'HTML',
    disable_web_page_preview: bool = False,
    reply_to_message_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Send Telegram message
    
    Args:
        chat_id: Telegram chat ID
        message: Message content
        parse_mode: Parse mode (HTML, Markdown)
        disable_web_page_preview: Disable link preview
        reply_to_message_id: Reply to specific message
    
    Returns:
        Dictionary containing sending results
    """
    
    try:
        logger.info(f"Sending Telegram to chat: {chat_id}")
        
        # Telegram bot token
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        
        if not bot_token:
            raise Exception("Telegram bot token not configured")
        
        # Prepare message payload
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': parse_mode,
            'disable_web_page_preview': disable_web_page_preview
        }
        
        if reply_to_message_id:
            payload['reply_to_message_id'] = reply_to_message_id
        
        # Send message
        telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        
        response = requests.post(
            telegram_url,
            json=payload,
            timeout=30
        )
        
        response.raise_for_status()
        
        result = response.json()
        
        logger.info(f"Telegram sent successfully to chat: {chat_id}")
        
        return {
            'success': True,
            'chat_id': chat_id,
            'message_id': result.get('result', {}).get('message_id'),
            'sent_at': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Telegram sending failed: {e}")
        raise self.retry(exc=e, countdown=60, max_retries=3)

@notification_task
def send_sms(
    self,
    to: str,
    message: str,
    sender_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Send SMS message
    
    Args:
        to: Recipient phone number
        message: Message content
        sender_id: Sender ID
    
    Returns:
        Dictionary containing sending results
    """
    
    try:
        logger.info(f"Sending SMS to: {to}")
        
        # SMS API configuration
        sms_api_url = os.getenv('SMS_API_URL')
        sms_api_key = os.getenv('SMS_API_KEY')
        sms_sender_id = sender_id or os.getenv('SMS_SENDER_ID')
        
        if not all([sms_api_url, sms_api_key]):
            raise Exception("SMS API credentials not configured")
        
        # Prepare message payload
        payload = {
            'api_key': sms_api_key,
            'to': to,
            'message': message,
            'sender': sms_sender_id
        }
        
        # Send SMS
        response = requests.post(
            sms_api_url,
            json=payload,
            timeout=30
        )
        
        response.raise_for_status()
        
        result = response.json()
        
        logger.info(f"SMS sent successfully to: {to}")
        
        return {
            'success': True,
            'to': to,
            'message_id': result.get('message_id'),
            'sent_at': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"SMS sending failed: {e}")
        raise self.retry(exc=e, countdown=60, max_retries=3)

@notification_task
def send_campaign_notification(
    self,
    campaign_id: str,
    notification_type: str,
    recipients: List[Dict[str, Any]],
    template: str,
    template_data: Dict[str, Any],
    channels: List[str] = ['email']
) -> Dict[str, Any]:
    """
    Send campaign notifications across multiple channels
    
    Args:
        campaign_id: Campaign ID
        notification_type: Type of notification
        recipients: List of recipient data
        template: Template name or content
        template_data: Data for template rendering
        channels: List of channels to use
    
    Returns:
        Dictionary containing campaign results
    """
    
    try:
        logger.info(f"Sending campaign notification: {campaign_id}")
        
        results = {
            'campaign_id': campaign_id,
            'notification_type': notification_type,
            'total_recipients': len(recipients),
            'channel_results': {},
            'sent_at': datetime.now().isoformat()
        }
        
        # Send notifications for each channel
        for channel in channels:
            channel_results = []
            
            for recipient in recipients:
                try:
                    # Prepare recipient-specific template data
                    recipient_data = {
                        **template_data,
                        'recipient': recipient
                    }
                    
                    # Send based on channel
                    if channel == 'email':
                        result = send_email.s(
                            to=recipient.get('email'),
                            subject=template_data.get('subject', 'Campaign Notification'),
                            template=template,
                            template_data=recipient_data
                        )
                    elif channel == 'whatsapp':
                        result = send_whatsapp.s(
                            to=recipient.get('phone'),
                            message=render_template(template, recipient_data)
                        )
                    elif channel == 'telegram':
                        result = send_telegram.s(
                            chat_id=recipient.get('telegram_chat_id'),
                            message=render_template(template, recipient_data)
                        )
                    elif channel == 'sms':
                        result = send_sms.s(
                            to=recipient.get('phone'),
                            message=render_template(template, recipient_data)
                        )
                    else:
                        logger.warning(f"Unsupported channel: {channel}")
                        continue
                    
                    channel_results.append({
                        'recipient_id': recipient.get('id'),
                        'success': result.get('success', False),
                        'message_id': result.get('message_id'),
                        'error': result.get('error')
                    })
                    
                except Exception as e:
                    logger.error(f"Error sending {channel} to recipient {recipient.get('id')}: {e}")
                    channel_results.append({
                        'recipient_id': recipient.get('id'),
                        'success': False,
                        'error': str(e)
                    })
            
            # Calculate channel statistics
            successful = sum(1 for r in channel_results if r['success'])
            results['channel_results'][channel] = {
                'sent': len(channel_results),
                'successful': successful,
                'failed': len(channel_results) - successful,
                'success_rate': successful / len(channel_results) if channel_results else 0,
                'results': channel_results
            }
        
        # Calculate overall statistics
        total_sent = sum(r['sent'] for r in results['channel_results'].values())
        total_successful = sum(r['successful'] for r in results['channel_results'].values())
        
        results['overall'] = {
            'total_sent': total_sent,
            'total_successful': total_successful,
            'total_failed': total_sent - total_successful,
            'overall_success_rate': total_successful / total_sent if total_sent > 0 else 0
        }
        
        logger.info(f"Campaign notification completed: {total_successful}/{total_sent} successful")
        
        return {
            'success': True,
            'results': results
        }
        
    except Exception as e:
        logger.error(f"Campaign notification failed: {e}")
        raise self.retry(exc=e, countdown=60, max_retries=3)

@notification_task
def send_brochure_notification(
    self,
    recipient_email: str,
    recipient_name: str,
    brochure_path: str,
    property_details: Dict[str, Any],
    custom_message: Optional[str] = None
) -> Dict[str, Any]:
    """
    Send brochure notification with attachment
    
    Args:
        recipient_email: Recipient email address
        recipient_name: Recipient name
        brochure_path: Path to brochure file
        property_details: Property information
        custom_message: Custom message
    
    Returns:
        Dictionary containing sending results
    """
    
    try:
        logger.info(f"Sending brochure notification to: {recipient_email}")
        
        # Prepare template data
        template_data = {
            'recipient_name': recipient_name,
            'property_details': property_details,
            'custom_message': custom_message or 'Thank you for your interest in our property.',
            'company_name': 'Lumina OS',
            'contact_phone': '+62 812-3456-7890',
            'contact_email': 'info@lumina-os.com'
        }
        
        # Prepare attachment
        attachment = {
            'filename': os.path.basename(brochure_path),
            'path': brochure_path,
            'type': 'application/pdf'
        }
        
        # Send email
        result = send_email.s(
            to=recipient_email,
            subject=f'Property Brochure - {property_details.get("title", "Your Dream Property")}',
            template='brochure_notification.html',
            template_data=template_data,
            attachments=[attachment]
        )
        
        logger.info(f"Brochure notification sent to: {recipient_email}")
        
        return result
        
    except Exception as e:
        logger.error(f"Brochure notification failed: {e}")
        raise self.retry(exc=e, countdown=60, max_retries=3)

@notification_task
def send_hot_lead_alert(
    self,
    lead_data: Dict[str, Any],
    channels: List[str] = ['telegram', 'email']
) -> Dict[str, Any]:
    """
    Send hot lead alert to sales team
    
    Args:
        lead_data: Lead information
        channels: Notification channels
    
    Returns:
        Dictionary containing alert results
    """
    
    try:
        logger.info(f"Sending hot lead alert: {lead_data.get('id', 'Unknown')}")
        
        # Prepare alert message
        alert_message = f"""
🔥 HOT LEAD ALERT 🔥

Lead ID: {lead_data.get('id', 'Unknown')}
Name: {lead_data.get('name', 'Unknown')}
Phone: {lead_data.get('phone', 'Unknown')}
Email: {lead_data.get('email', 'Unknown')}
Score: {lead_data.get('score', 0):.2f}
Intent: {lead_data.get('intent', 'Unknown')}
Campaign: {lead_data.get('campaign', 'Unknown')}
Area: {lead_data.get('area', 'Unknown')}

Message: {lead_data.get('message', 'No message')}

🚨 IMMEDIATE ACTION REQUIRED 🚨
        """.strip()
        
        results = {}
        
        # Send to each channel
        for channel in channels:
            try:
                if channel == 'telegram':
                    # Send to Telegram sales group
                    sales_chat_id = os.getenv('TELEGRAM_SALES_CHAT_ID')
                    if sales_chat_id:
                        result = send_telegram.s(
                            chat_id=sales_chat_id,
                            message=alert_message,
                            parse_mode='HTML'
                        )
                        results[channel] = result
                
                elif channel == 'email':
                    # Send to sales team email
                    sales_email = os.getenv('SALES_EMAIL')
                    if sales_email:
                        result = send_email.s(
                            to=sales_email,
                            subject=f'🔥 HOT LEAD ALERT - {lead_data.get("name", "Unknown")}',
                            template='hot_lead_alert.html',
                            template_data={'lead': lead_data}
                        )
                        results[channel] = result
                
            except Exception as e:
                logger.error(f"Error sending hot lead alert via {channel}: {e}")
                results[channel] = {'success': False, 'error': str(e)}
        
        logger.info(f"Hot lead alert sent via {len(results)} channels")
        
        return {
            'success': True,
            'lead_id': lead_data.get('id'),
            'channels': list(results.keys()),
            'results': results,
            'sent_at': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Hot lead alert failed: {e}")
        raise self.retry(exc=e, countdown=60, max_retries=3)

# Helper functions

def render_template(template: str, data: Dict[str, Any]) -> str:
    """Render template with data"""
    
    try:
        # If template is a file path
        if template.endswith('.html') or template.endswith('.txt'):
            template_path = os.path.join(root_dir, 'templates', template)
            with open(template_path, 'r') as f:
                template_content = f.read()
        else:
            template_content = template
        
        # Render with Jinja2
        jinja_template = Template(template_content)
        return jinja_template.render(**data)
        
    except Exception as e:
        logger.error(f"Template rendering failed: {e}")
        return str(data.get('message', 'Template rendering failed'))

def add_attachment(msg: MIMEMultipart, attachment: Dict[str, Any]) -> None:
    """Add attachment to email message"""
    
    try:
        attachment_path = attachment.get('path')
        attachment_filename = attachment.get('filename', os.path.basename(attachment_path))
        attachment_type = attachment.get('type', 'application/octet-stream')
        
        with open(attachment_path, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
        
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename= {attachment_filename}'
        )
        
        msg.attach(part)
        
    except Exception as e:
        logger.error(f"Error adding attachment: {e}")

# Email templates
def create_email_templates() -> None:
    """Create default email templates"""
    
    templates_dir = os.path.join(root_dir, 'templates')
    os.makedirs(templates_dir, exist_ok=True)
    
    # Brochure notification template
    brochure_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Property Brochure</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f4f4f4; }
            .container { max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .header { text-align: center; margin-bottom: 30px; }
            .logo { font-size: 24px; font-weight: bold; color: #333; }
            .content { margin-bottom: 30px; }
            .property-details { background-color: #f9f9f9; padding: 20px; border-radius: 5px; margin-bottom: 20px; }
            .footer { text-align: center; color: #666; font-size: 12px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo">{{ company_name }}</div>
                <h1>Property Brochure</h1>
            </div>
            
            <div class="content">
                <p>Dear {{ recipient_name }},</p>
                <p>{{ custom_message }}</p>
                
                <div class="property-details">
                    <h2>{{ property_details.title }}</h2>
                    <p><strong>Type:</strong> {{ property_details.type }}</p>
                    <p><strong>Size:</strong> {{ property_details.size }}</p>
                    <p><strong>Price:</strong> {{ property_details.price }}</p>
                    <p><strong>Location:</strong> {{ property_details.location }}</p>
                </div>
                
                <p>Please find the complete brochure attached to this email.</p>
                
                <p>If you have any questions or would like to schedule a viewing, please don't hesitate to contact us:</p>
                <p>
                    Phone: {{ contact_phone }}<br>
                    Email: {{ contact_email }}
                </p>
            </div>
            
            <div class="footer">
                <p>&copy; 2024 {{ company_name }}. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    with open(os.path.join(templates_dir, 'brochure_notification.html'), 'w', encoding='utf-8') as f:
        f.write(brochure_template)
    
    # Hot lead alert template
    hot_lead_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Hot Lead Alert</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #fff3cd; }
            .container { max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; border: 2px solid #ffc107; }
            .alert { background-color: #ffc107; color: #856404; padding: 15px; border-radius: 5px; margin-bottom: 20px; text-align: center; font-weight: bold; }
            .lead-details { margin-bottom: 20px; }
            .footer { text-align: center; color: #666; font-size: 12px; margin-top: 20px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="alert">
                🔥 HOT LEAD ALERT - IMMEDIATE ACTION REQUIRED 🔥
            </div>
            
            <div class="lead-details">
                <h2>Lead Information</h2>
                <p><strong>ID:</strong> {{ lead.id }}</p>
                <p><strong>Name:</strong> {{ lead.name }}</p>
                <p><strong>Phone:</strong> {{ lead.phone }}</p>
                <p><strong>Email:</strong> {{ lead.email }}</p>
                <p><strong>Score:</strong> {{ "%.2f"|format(lead.score) }}</p>
                <p><strong>Intent:</strong> {{ lead.intent }}</p>
                <p><strong>Campaign:</strong> {{ lead.campaign }}</p>
                <p><strong>Area:</strong> {{ lead.area }}</p>
                
                <h3>Message:</h3>
                <p>{{ lead.message }}</p>
            </div>
            
            <div class="footer">
                <p>This alert was generated automatically by Lumina OS</p>
                <p>{{ "now"|strftime("%Y-%m-%d %H:%M:%S") }}</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    with open(os.path.join(templates_dir, 'hot_lead_alert.html'), 'w', encoding='utf-8') as f:
        f.write(hot_lead_template)

# Create templates on module import
create_email_templates()
