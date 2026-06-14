"""
JARVIS Webhook Security Middleware
=================================

Security middleware for protecting webhook routes from unauthorized access.
Verifies requests come from trusted sources (Telegram IP ranges) or contain valid secrets.
"""

from fastapi import Request, HTTPException, status
from typing import Optional, List
import ipaddress
import logging
import os
from functools import wraps

logger = logging.getLogger(__name__)

# Telegram IP ranges (as of 2024)
TELEGRAM_IP_RANGES = [
    # Telegram IPv4 ranges
    ipaddress.ip_network('149.154.160.0/20'),
    ipaddress.ip_network('91.108.4.0/22'),
]

class WebhookSecurity:
    """
    Security middleware for webhook endpoints
    """
    
    def __init__(self, config: dict = None):
        self.config = config or {}
        
        # Secret token for webhook verification
        self.webhook_secret = self.config.get('webhook_secret', os.getenv('WEBHOOK_SECRET'))
        
        # Enable IP whitelist
        self.enable_ip_whitelist = self.config.get('enable_ip_whitelist', True)
        
        # Trusted IP ranges (Telegram + custom)
        self.trusted_ip_ranges = TELEGRAM_IP_RANGES.copy()
        
        # Add custom IP ranges if provided
        custom_ranges = self.config.get('custom_ip_ranges', [])
        for range_str in custom_ranges:
            try:
                self.trusted_ip_ranges.append(ipaddress.ip_network(range_str))
            except ValueError as e:
                logger.warning(f"Invalid IP range: {range_str} - {e}")
        
        # Enable Cloudflare verification
        self.enable_cloudflare = self.config.get('enable_cloudflare', True)
        
        # Cloudflare trusted IPs
        self.cloudflare_ips = self.config.get('cloudflare_ips', [])
    
    def verify_ip(self, ip_str: str) -> bool:
        """
        Verify if IP address is in trusted ranges
        """
        if not self.enable_ip_whitelist:
            return True
        
        try:
            ip = ipaddress.ip_address(ip_str)
            
            # Check if IP is in any trusted range
            for network in self.trusted_ip_ranges:
                if ip in network:
                    return True
            
            # Check Cloudflare IPs if enabled
            if self.enable_cloudflare:
                for cf_ip in self.cloudflare_ips:
                    if ip == ipaddress.ip_address(cf_ip):
                        return True
            
            logger.warning(f"IP not in trusted ranges: {ip_str}")
            return False
        
        except ValueError as e:
            logger.error(f"Invalid IP address: {ip_str} - {e}")
            return False
    
    def verify_secret(self, secret: str) -> bool:
        """
        Verify webhook secret token
        """
        if not self.webhook_secret:
            logger.warning("Webhook secret not configured")
            return False
        
        return secret == self.webhook_secret
    
    def verify_cloudflare(self, request: Request) -> bool:
        """
        Verify request comes through Cloudflare
        """
        if not self.enable_cloudflare:
            return True
        
        # Check for Cloudflare headers
        cf_ray = request.headers.get('CF-Ray')
        cf_connecting_ip = request.headers.get('CF-Connecting-IP')
        cf_visitor = request.headers.get('CF-Visitor')
        
        if not cf_ray:
            logger.warning("Request missing CF-Ray header")
            return False
        
        # Verify CF-Connecting-IP is present
        if not cf_connecting_ip:
            logger.warning("Request missing CF-Connecting-IP header")
            return False
        
        return True

# Global security instance
webhook_security: Optional[WebhookSecurity] = None

def get_webhook_security(config: dict = None) -> WebhookSecurity:
    """Get or create webhook security instance"""
    global webhook_security
    
    if webhook_security is None:
        webhook_security = WebhookSecurity(config)
    
    return webhook_security

# FastAPI dependency for webhook verification
async def verify_webhook_request(request: Request) -> dict:
    """
    Verify webhook request is legitimate
    Checks IP whitelist, secret token, and Cloudflare headers
    """
    security = get_webhook_security()
    
    # Get client IP
    client_ip = request.client.host if request.client else None
    x_forwarded_for = request.headers.get('X-Forwarded-For')
    
    # Use X-Forwarded-For if available (behind proxy)
    if x_forwarded_for:
        client_ip = x_forwarded_for.split(',')[0].strip()
    
    logger.info(f"Webhook request from IP: {client_ip}")
    
    # Verify IP
    if not security.verify_ip(client_ip):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"IP not whitelisted: {client_ip}"
        )
    
    # Verify Cloudflare
    if not security.verify_cloudflare(request):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Request not from Cloudflare"
        )
    
    # Verify secret token (if required)
    secret = request.headers.get('X-Webhook-Secret')
    if secret and not security.verify_secret(secret):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid webhook secret"
        )
    
    return {
        'verified': True,
        'ip': client_ip,
        'cloudflare': security.enable_cloudflare,
    }

# Express middleware for webhook security (for Node.js)
def create_webhook_middleware(config: dict = None):
    """
    Create Express middleware for webhook security
    """
    security = WebhookSecurity(config)
    
    def middleware(req, res, next):
        try:
            # Get client IP
            client_ip = req.ip
            x_forwarded_for = req.headers['x-forwarded-for']
            
            if x_forwarded_for:
                client_ip = x_forwarded_for.split(',')[0].strip()
            
            logger.info(f"Webhook request from IP: {client_ip}")
            
            # Verify IP
            if not security.verify_ip(client_ip):
                logger.warning(f"IP not whitelisted: {client_ip}")
                return res.status(403).json({ error: 'IP not whitelisted' })
            
            # Verify Cloudflare
            if security.enable_cloudflare:
                cf_ray = req.headers.get('cf-ray')
                if not cf_ray:
                    logger.warning("Request missing CF-Ray header")
                    return res.status(403).json({ error: 'Not from Cloudflare' })
            
            # Verify secret token
            secret = req.headers.get('x-webhook-secret')
            if secret and not security.verify_secret(secret):
                logger.warning("Invalid webhook secret")
                return res.status(403).json({ error: 'Invalid secret' })
            
            # All checks passed
            next()
        
        except Exception as e:
            logger.error(f"Webhook security error: {e}")
            return res.status(500).json({ error: 'Security check failed' })
    
    return middleware

# Usage example for Express
if __name__ == '__main__':
    from flask import Flask, request, jsonify
    
    app = Flask(__name__)
    
    # Apply middleware
    webhook_middleware = create_webhook_middleware({
        'webhook_secret': 'your_secret_here',
        'enable_ip_whitelist': True,
        'enable_cloudflare': True,
    })
    
    @app.route('/telegram-webhook', methods=['POST'])
    def telegram_webhook():
        # Apply middleware
        webhook_middleware(request, None, lambda: None)
        
        # Process webhook
        data = request.json
        return jsonify({'status': 'ok'})
