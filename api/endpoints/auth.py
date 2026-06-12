"""
Authentication Endpoint for LUMINA OS
Handles user authentication and JWT token management
"""

from fastapi import APIRouter, HTTPException, status, Depends, Form
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
from typing import Optional, Dict, Any
import logging
import os

# Import JWT manager
from api.middleware.jwt_auth import jwt_manager

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/auth", tags=["authentication"])

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# Mock user database (in production, use proper database)
USERS_DB = {
    "admin@lumina.os": {
        "id": 1,
        "username": "admin@lumina.os",
        "full_name": "LUMINA OS Admin",
        "email": "admin@lumina.os",
        "hashed_password": pwd_context.hash("admin123"),
        "role": "ADMIN",
        "active": True
    },
    "demo@lumina.os": {
        "id": 2,
        "username": "demo@lumina.os",
        "full_name": "Demo User",
        "email": "demo@lumina.os",
        "hashed_password": pwd_context.hash("demo123"),
        "role": "USER",
        "active": True
    },
    "operator@lumina.os": {
        "id": 3,
        "username": "operator@lumina.os",
        "full_name": "System Operator",
        "email": "operator@lumina.os",
        "hashed_password": pwd_context.hash("operator123"),
        "role": "OPERATOR",
        "active": True
    }
}

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    user: Dict[str, Any]

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    id: int
    name: str
    email: str
    role: str

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def get_user(db: Dict, username: str) -> Optional[Dict]:
    """Get user from database"""
    if username in db:
        user_dict = db[username]
        return user_dict
    return None

def authenticate_user(db: Dict, username: str, password: str) -> Optional[Dict]:
    """Authenticate user"""
    user = get_user(db, username)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token using JWT manager"""
    return jwt_manager.create_access_token(data, expires_delta)

async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict:
    """Get current user from token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.PyJWTError:
        raise credentials_exception
    
    user = get_user(USERS_DB, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

@router.post("/login", response_model=Token)
async def login_for_access_token(
    username: str = Form(...),
    password: str = Form(...)
):
    """
    Login endpoint for authentication
    Accepts form data with username and password
    Returns JWT token and user information
    """
    try:
        logger.info(f"Login attempt for user: {username}")
        
        # Authenticate user
        user = authenticate_user(USERS_DB, username, password)
        if not user:
            logger.warning(f"Login failed for user: {username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user["username"]}, expires_delta=access_token_expires
        )
        
        # Prepare response
        response_data = {
            "success": True,
            "message": "Authentication successful",
            "data": {
                "access_token": access_token,
                "token_type": "bearer",
                "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                "user": {
                    "id": user["id"],
                    "name": user["full_name"],
                    "email": user["email"],
                    "role": user["role"]
                }
            }
        }
        
        logger.info(f"Login successful for user: {username}")
        return response_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during authentication"
        )

@router.get("/me", response_model=User)
async def read_users_me(current_user: Dict = Depends(get_current_user)):
    """
    Get current user information
    Requires valid JWT token
    """
    return User(
        id=current_user["id"],
        name=current_user["full_name"],
        email=current_user["email"],
        role=current_user["role"]
    )

@router.post("/logout")
async def logout():
    """
    Logout endpoint
    In a real application, you might want to invalidate the token
    For now, just return success message
    """
    return {
        "success": True,
        "message": "Logout successful"
    }

@router.get("/verify")
async def verify_token(token: str = Depends(oauth2_scheme)):
    """
    Verify JWT token validity
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        user = get_user(USERS_DB, username=username)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        return {
            "success": True,
            "message": "Token is valid",
            "user": {
                "id": user["id"],
                "name": user["full_name"],
                "email": user["email"],
                "role": user["role"]
            }
        }
        
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

# Demo credentials for testing
@router.get("/demo-credentials")
async def get_demo_credentials():
    """
    Get demo credentials for testing
    Only available in development mode
    """
    return {
        "success": True,
        "message": "Demo credentials for testing",
        "credentials": [
            {
                "username": "admin@elitehunter.com",
                "password": "admin123",
                "role": "admin"
            },
            {
                "username": "demo@elitehunter.com", 
                "password": "demo123",
                "role": "user"
            }
        ],
        "note": "These are demo credentials for testing purposes only"
    }
