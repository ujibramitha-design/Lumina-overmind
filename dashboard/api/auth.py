"""
HUNTER AGENT AI MARKETING DIGITAL - Authentication Endpoints
Enhanced login endpoints with HTTP-only cookie support
"""

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse, Response
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import logging

from .main import (
    app, User, Token, LoginResponse, LoginRequest,
    authenticate_user, create_access_token
)

logger = logging.getLogger(__name__)

@app.post("/api/auth/login", response_model=LoginResponse)
async def login_with_cookie(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Enhanced user login endpoint with HTTP-only cookie support
    
    Args:
        form_data: OAuth2 password request form with username and password
        
    Returns:
        LoginResponse with JWT token, user information, and HTTP-only cookie
    """
    try:
        # Extract email and password from form data
        email = form_data.username
        password = form_data.password
        
        logger.info(f"Login attempt for email: {email}")
        
        # Authenticate user
        user_data = authenticate_user(email, password)
        
        if not user_data:
            logger.warning(f"Login failed for email: {email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create access token
        token_data = {
            "user_id": user_data["id"],
            "email": user_data["email"],
            "role": user_data["role"],
            "name": user_data["name"]
        }
        
        access_token = create_access_token(data=token_data, expires_delta=24)
        
        # Create user object
        user = User(
            id=user_data["id"],
            name=user_data["name"],
            email=user_data["email"],
            role=user_data["role"],
            created_at=user_data.get("created_at")
        )
        
        # Create token response
        token_response = Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=24 * 3600,  # 24 hours in seconds
            user=user
        )
        
        logger.info(f"Login successful for email: {email}")
        
        # Create response with HTTP-only cookie
        response = JSONResponse(
            content={
                "success": True,
                "message": "Login successful",
                "data": token_response.dict()
            }
        )
        
        # Set HTTP-only cookie
        response.set_cookie(
            key="lumina_token",
            value=access_token,
            max_age=24 * 3600,  # 24 hours
            expires=datetime.utcnow() + timedelta(hours=24),
            path="/",
            domain=None,
            secure=False,  # Set to True in production with HTTPS
            httponly=True,
            samesite="lax"
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during login"
        )

@app.post("/api/auth/login-json", response_model=LoginResponse)
async def login_json_with_cookie(login_request: LoginRequest):
    """
    Enhanced user login endpoint with JSON payload and HTTP-only cookie
    
    Args:
        login_request: Login request with email and password
        
    Returns:
        LoginResponse with JWT token, user information, and HTTP-only cookie
    """
    try:
        email = login_request.email
        password = login_request.password
        
        logger.info(f"Login attempt for email: {email}")
        
        # Authenticate user
        user_data = authenticate_user(email, password)
        
        if not user_data:
            logger.warning(f"Login failed for email: {email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create access token
        token_data = {
            "user_id": user_data["id"],
            "email": user_data["email"],
            "role": user_data["role"],
            "name": user_data["name"]
        }
        
        access_token = create_access_token(data=token_data, expires_delta=24)
        
        # Create user object
        user = User(
            id=user_data["id"],
            name=user_data["name"],
            email=user_data["email"],
            role=user_data["role"],
            created_at=user_data.get("created_at")
        )
        
        # Create token response
        token_response = Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=24 * 3600,  # 24 hours in seconds
            user=user
        )
        
        logger.info(f"Login successful for email: {email}")
        
        # Create response with HTTP-only cookie
        response = JSONResponse(
            content={
                "success": True,
                "message": "Login successful",
                "data": token_response.dict()
            }
        )
        
        # Set HTTP-only cookie
        response.set_cookie(
            key="lumina_token",
            value=access_token,
            max_age=24 * 3600,  # 24 hours
            expires=datetime.utcnow() + timedelta(hours=24),
            path="/",
            domain=None,
            secure=False,  # Set to True in production with HTTPS
            httponly=True,
            samesite="lax"
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during login"
        )

@app.post("/api/auth/logout")
async def logout_with_cookie():
    """
    User logout endpoint with cookie clearing
    
    Returns:
        Success response with cleared cookie
    """
    try:
        # Create response with cleared cookie
        response = JSONResponse(
            content={
                "success": True,
                "message": "Logout successful"
            }
        )
        
        # Clear the HTTP-only cookie
        response.delete_cookie(
            key="lumina_token",
            path="/",
            domain=None
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Logout error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during logout"
        )
