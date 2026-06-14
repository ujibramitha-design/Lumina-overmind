"""
Supabase Authentication Integration
Handles user authentication using Supabase Auth
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any
import httpx
import os
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/auth/supabase", tags=["supabase-auth"])

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

class SignUpRequest(BaseModel):
    email: str
    password: str
    full_name: Optional[str] = None

class SignInRequest(BaseModel):
    email: str
    password: str

class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    user: Dict[str, Any]

async def supabase_request(
    method: str,
    endpoint: str,
    data: Optional[Dict[str, Any]] = None,
    use_service_role: bool = False
) -> Dict[str, Any]:
    """Make request to Supabase Auth API"""
    if not SUPABASE_URL:
        raise HTTPException(status_code=500, detail="Supabase URL not configured")
    
    headers = {
        "apikey": SUPABASE_SERVICE_ROLE_KEY if use_service_role else SUPABASE_ANON_KEY,
        "Content-Type": "application/json"
    }
    
    url = f"{SUPABASE_URL}/auth/v1{endpoint}"
    
    async with httpx.AsyncClient() as client:
        try:
            if method == "POST":
                response = await client.post(url, json=data, headers=headers)
            elif method == "GET":
                response = await client.get(url, headers=headers)
            else:
                raise HTTPException(status_code=400, detail="Unsupported method")
            
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Supabase request error: {e}")
            raise HTTPException(status_code=500, detail="Authentication service error")

@router.post("/signup")
async def signup(request: SignUpRequest) -> AuthResponse:
    """Register new user with Supabase"""
    try:
        data = {
            "email": request.email,
            "password": request.password,
            "data": {
                "full_name": request.full_name or request.email.split("@")[0]
            }
        }
        
        response = await supabase_request("POST", "/signup", data)
        
        return AuthResponse(
            access_token=response.get("access_token", ""),
            refresh_token=response.get("refresh_token", ""),
            user=response.get("user", {})
        )
    except Exception as e:
        logger.error(f"Signup error: {e}")
        raise HTTPException(status_code=400, detail=f"Signup failed: {str(e)}")

@router.post("/signin")
async def signin(request: SignInRequest) -> AuthResponse:
    """Sign in user with Supabase"""
    try:
        data = {
            "email": request.email,
            "password": request.password
        }
        
        response = await supabase_request("POST", "/token?grant_type=password", data)
        
        return AuthResponse(
            access_token=response.get("access_token", ""),
            refresh_token=response.get("refresh_token", ""),
            user=response.get("user", {})
        )
    except Exception as e:
        logger.error(f"Signin error: {e}")
        raise HTTPException(status_code=401, detail="Invalid credentials")

@router.post("/refresh")
async def refresh_token(refresh_token: str) -> AuthResponse:
    """Refresh access token using refresh token"""
    try:
        data = {
            "refresh_token": refresh_token,
            "grant_type": "refresh_token"
        }
        
        response = await supabase_request("POST", "/token", data)
        
        return AuthResponse(
            access_token=response.get("access_token", ""),
            refresh_token=response.get("refresh_token", ""),
            user=response.get("user", {})
        )
    except Exception as e:
        logger.error(f"Token refresh error: {e}")
        raise HTTPException(status_code=401, detail="Invalid refresh token")

@router.get("/user")
async def get_user(access_token: str) -> Dict[str, Any]:
    """Get current user from Supabase"""
    try:
        headers = {
            "Authorization": f"Bearer {access_token}",
            "apikey": SUPABASE_ANON_KEY
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SUPABASE_URL}/auth/v1/user",
                headers=headers
            )
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logger.error(f"Get user error: {e}")
        raise HTTPException(status_code=401, detail="Invalid access token")

@router.post("/signout")
async def signout(access_token: str) -> Dict[str, str]:
    """Sign out user from Supabase"""
    try:
        headers = {
            "Authorization": f"Bearer {access_token}",
            "apikey": SUPABASE_ANON_KEY
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SUPABASE_URL}/auth/v1/logout",
                headers=headers
            )
            response.raise_for_status()
            return {"message": "Successfully signed out"}
    except Exception as e:
        logger.error(f"Signout error: {e}")
        raise HTTPException(status_code=400, detail="Signout failed")
