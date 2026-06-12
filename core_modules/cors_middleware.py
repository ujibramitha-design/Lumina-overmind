"""
LUMINA OS - Production CORS Middleware
Secure CORS configuration for production deployment
"""

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import os
from typing import List

def setup_cors_middleware(app: FastAPI) -> None:
    """
    Setup CORS middleware for production environment
    Only allows requests from approved domains
    """
    
    # Get allowed origins from environment
    allowed_origins = os.getenv("CORS_ORIGINS", '["https://lumina.devproflow.com"]')
    
    # Parse JSON string or use default
    try:
        import json
        origins: List[str] = json.loads(allowed_origins)
    except (json.JSONDecodeError, ImportError):
        origins = ["https://lumina.devproflow.com"]
    
    # Add local development origins if not in production
    if os.getenv("ENVIRONMENT", "development") == "development":
        origins.extend([
            "http://localhost:3000",
            "http://localhost:8000",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:8000"
        ])
    
    # Add CORS middleware with strict settings
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=os.getenv("CORS_ALLOW_CREDENTIALS", "true").lower() == "true",
        allow_methods=os.getenv("CORS_ALLOW_METHODS", "GET,POST,PUT,DELETE,OPTIONS").split(","),
        allow_headers=os.getenv("CORS_ALLOW_HEADERS", "*").split(","),
        expose_headers=["Content-Length", "Content-Range", "X-Total-Count"],
        max_age=86400,  # 24 hours cache
    )
    
    # Add custom middleware for additional security headers
    @app.middleware("http")
    async def add_security_headers(request, call_next):
        response = await call_next(request)
        
        # Security headers
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "no-referrer-when-downgrade"
        
        # Only in production
        if os.getenv("ENVIRONMENT") == "production":
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        return response
    
    # Add custom middleware for Cloudflare IP handling
    @app.middleware("http")
    async def handle_cloudflare_ip(request, call_next):
        # Store Cloudflare IP header for rate limiting
        cf_connecting_ip = request.headers.get("CF-Connecting-IP")
        if cf_connecting_ip:
            request.state.client_ip = cf_connecting_ip
        else:
            request.state.client_ip = request.client.host
        
        response = await call_next(request)
        return response

def get_client_ip(request) -> str:
    """
    Get real client IP from Cloudflare headers
    """
    # Try Cloudflare headers first
    cf_connecting_ip = request.headers.get("CF-Connecting-IP")
    if cf_connecting_ip:
        return cf_connecting_ip
    
    # Fallback to standard headers
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    
    # Final fallback
    return request.client.host

def validate_origin(request) -> bool:
    """
    Validate request origin against allowed origins
    """
    origin = request.headers.get("Origin")
    if not origin:
        return True  # Allow non-CORS requests
    
    allowed_origins = os.getenv("CORS_ORIGINS", '["https://lumina.devproflow.com"]')
    try:
        import json
        origins = json.loads(allowed_origins)
        return origin in origins
    except (json.JSONDecodeError, ImportError):
        return origin == "https://lumina.devproflow.com"
