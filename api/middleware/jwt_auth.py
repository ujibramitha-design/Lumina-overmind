"""
LUMINA OS - JWT AUTHENTICATION MIDDLEWARE
=========================================

JWT-based authentication middleware for protecting API endpoints
"""

import os
import jwt
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "lumina_super_secret_key_2024")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# HTTP Bearer scheme
security = HTTPBearer(auto_error=False)

class JWTManager:
    """Manager for JWT token operations"""
    
    def __init__(self):
        self.secret_key = SECRET_KEY
        self.algorithm = ALGORITHM
        self.access_token_expire_minutes = ACCESS_TOKEN_EXPIRE_MINUTES
    
    def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        
        to_encode.update({"exp": expire, "iat": datetime.utcnow()})
        
        try:
            encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
            logger.info(f"✅ Created access token for user: {data.get('sub', 'unknown')}")
            return encoded_jwt
        except Exception as e:
            logger.error(f"❌ Failed to create access token: {e}")
            raise HTTPException(status_code=500, detail="Failed to create access token")
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            
            # Check expiration
            exp = payload.get("exp")
            if exp is None:
                raise HTTPException(status_code=401, detail="Token missing expiration")
            
            if datetime.utcnow() > datetime.fromtimestamp(exp):
                raise HTTPException(status_code=401, detail="Token has expired")
            
            # Check required fields
            sub = payload.get("sub")
            if sub is None:
                raise HTTPException(status_code=401, detail="Token missing subject")
            
            logger.debug(f"✅ Verified token for user: {sub}")
            return payload
            
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.JWTError as e:
            raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
        except Exception as e:
            logger.error(f"❌ Token verification error: {e}")
            raise HTTPException(status_code=401, detail="Token verification failed")
    
    def create_user_token(self, user_id: str, username: str, role: str = "USER") -> str:
        """Create token for authenticated user"""
        return self.create_access_token({
            "sub": user_id,
            "username": username,
            "role": role,
            "type": "access"
        })

# Global JWT manager
jwt_manager = JWTManager()

async def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> Dict[str, Any]:
    """Dependency to get current authenticated user"""
    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        payload = jwt_manager.verify_token(credentials.credentials)
        return payload
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Authentication error: {e}")
        raise HTTPException(status_code=401, detail="Authentication failed")

async def get_current_active_user(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """Dependency to get current active user"""
    # Check if user is active (you might want to add this check to database)
    if current_user.get("status") == "inactive":
        raise HTTPException(status_code=400, detail="Inactive user")
    
    return current_user

async def get_admin_user(current_user: Dict[str, Any] = Depends(get_current_active_user)) -> Dict[str, Any]:
    """Dependency to get admin user (for sensitive operations)"""
    role = current_user.get("role", "").upper()
    if role not in ["ADMIN", "SUPER_ADMIN"]:
        raise HTTPException(
            status_code=403, 
            detail="Not enough permissions. Admin access required."
        )
    
    return current_user

def require_auth():
    """Decorator to require authentication for endpoints"""
    return Depends(get_current_user)

def require_admin():
    """Decorator to require admin access for endpoints"""
    return Depends(get_admin_user)

# Public endpoints that don't require authentication
PUBLIC_ENDPOINTS = [
    "/",
    "/health",
    "/docs",
    "/redoc",
    "/api/auth/login",
    "/api/auth/register",
    "/api/auth/verify",
    "/static/",
    "/output/",
    "/socket.io/",
    "/ws"
]

# Admin-only endpoints
ADMIN_ENDPOINTS = [
    "/api/system-control/",
    "/api/runners/",
    "/api/security/",
    "/api/config-vault/",
    "/settings/classified-vault"
]

def is_public_endpoint(path: str) -> bool:
    """Check if endpoint is public"""
    for public_path in PUBLIC_ENDPOINTS:
        if path.startswith(public_path):
            return True
    return False

def is_admin_endpoint(path: str) -> bool:
    """Check if endpoint requires admin access"""
    for admin_path in ADMIN_ENDPOINTS:
        if path.startswith(admin_path):
            return True
    return False

class JWTAuthenticationMiddleware:
    """Custom middleware for JWT authentication"""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        # Skip authentication for WebSocket connections
        if scope.get("type") == "websocket":
            await self.app(scope, receive, send)
            return
        
        # Get request path
        path = scope.get("path", "")
        
        # Skip authentication for public endpoints
        if is_public_endpoint(path):
            await self.app(scope, receive, send)
            return
        
        # Get authorization header
        headers = dict(scope.get("headers", []))
        auth_header = headers.get(b"authorization", b"").decode()
        
        if not auth_header.startswith("Bearer "):
            # Send 401 Unauthorized
            response = {
                "type": "http.response.start",
                "status": 401,
                "headers": [[b"content-type", b"application/json"]],
            }
            await send(response)
            
            response_body = json.dumps({
                "error": "Not authenticated",
                "detail": "Missing or invalid authorization header"
            }).encode()
            
            response = {
                "type": "http.response.body",
                "body": response_body,
            }
            await send(response)
            return
        
        # Extract token
        token = auth_header[7:]  # Remove "Bearer "
        
        try:
            # Verify token
            payload = jwt_manager.verify_token(token)
            
            # Check admin endpoints
            if is_admin_endpoint(path):
                role = payload.get("role", "").upper()
                if role not in ["ADMIN", "SUPER_ADMIN"]:
                    # Send 403 Forbidden
                    response = {
                        "type": "http.response.start",
                        "status": 403,
                        "headers": [[b"content-type", b"application/json"]],
                    }
                    await send(response)
                    
                    response_body = json.dumps({
                        "error": "Forbidden",
                        "detail": "Admin access required"
                    }).encode()
                    
                    response = {
                        "type": "http.response.body",
                        "body": response_body,
                    }
                    await send(response)
                    return
            
            # Add user info to scope
            scope["user"] = payload
            
            # Continue with request
            await self.app(scope, receive, send)
            
        except HTTPException as e:
            # Send error response
            response = {
                "type": "http.response.start",
                "status": e.status_code,
                "headers": [[b"content-type", b"application/json"]],
            }
            await send(response)
            
            response_body = json.dumps({
                "error": e.detail,
                "detail": getattr(e, "detail", "Authentication failed")
            }).encode()
            
            response = {
                "type": "http.response.body",
                "body": response_body,
            }
            await send(response)
            return
