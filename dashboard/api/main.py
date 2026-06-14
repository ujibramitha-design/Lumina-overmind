from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Dict, Any
import logging
from datetime import datetime
import asyncio
import json
import random
import uuid
import sys
import os

# Add root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# Import Supabase Cloud Database Manager
try:
    from core_modules.db_manager_supabase import get_supabase_manager
    print("Successfully imported Supabase Cloud Manager")
except ImportError as e:
    print(f"Failed to import Supabase Manager: {e}")
    print("Make sure core_modules/db_manager_supabase.py exists")
    sys.exit(1)
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, EmailStr, HttpUrl
from fastapi import Depends, HTTPException, status

# Import the process manager and security utilities
from utils.process_manager import runner_manager
from utils.security import verify_token, create_access_token, hash_password, verify_password

# Import webhook routers
try:
    from api.endpoints import telegram_webhook
    print("Successfully imported Telegram webhook router")
except ImportError as e:
    print(f"Failed to import Telegram webhook router: {e}")
    print("Make sure api/endpoints/telegram_webhook.py exists")

try:
    from api.endpoints import whatsapp_webhook
    print("Successfully imported WhatsApp webhook router")
except ImportError as e:
    print(f"Failed to import WhatsApp webhook router: {e}")
    print("Make sure api/endpoints/whatsapp_webhook.py exists")

try:
    from api.endpoints import system_control
    print("Successfully imported system control router")
except ImportError as e:
    print(f"Failed to import system control router: {e}")
    print("Make sure api/endpoints/system_control.py exists")

# Import new Black Ops modules
try:
    from api.endpoints import legal_sovereign
    print("Successfully imported legal sovereign router")
except ImportError as e:
    print(f"Failed to import legal sovereign router: {e}")
    print("Make sure api/endpoints/legal_sovereign.py exists")

try:
    from api.endpoints import visual_mirage
    print("Successfully imported visual mirage router")
except ImportError as e:
    print(f"Failed to import visual mirage router: {e}")
    print("Make sure api/endpoints/visual_mirage.py exists")

# Webhook Configuration
LUMINA_WEBHOOK_TOKEN = 'DUMMY-TOKEN-123'

# Pydantic Models for Webhook
class LeadWebhookPayload(BaseModel):
    """Pydantic model for incoming lead webhook payload"""
    nama: str = Field(..., min_length=1, max_length=255, description="Lead name")
    no_hp: str = Field(..., min_length=10, max_length=20, description="Phone number")
    email: Optional[EmailStr] = Field(None, description="Email address")
    sumber: str = Field(..., min_length=1, max_length=100, description="Lead source")
    campaign: Optional[str] = Field(None, max_length=100, description="Campaign name")
    catatan: Optional[str] = Field(None, max_length=1000, description="Additional notes")
    lokasi: Optional[str] = Field(None, max_length=255, description="Location")
    pekerjaan: Optional[str] = Field(None, max_length=100, description="Occupation")

class WebhookResponse(BaseModel):
    """Pydantic model for webhook response"""
    success: bool
    message: str
    data: Dict[str, Any]

# Pydantic Models for Authentication
class User(BaseModel):
    """User model for authentication response"""
    id: int
    name: str
    email: str
    role: str
    created_at: Optional[str] = None

class Token(BaseModel):
    """Token model for authentication response"""
    access_token: str
    token_type: str
    expires_in: int
    user: User

class TokenData(BaseModel):
    """Token data model for token validation"""
    user_id: Optional[int] = None
    email: Optional[str] = None
    role: Optional[str] = None

class LoginRequest(BaseModel):
    """Login request model"""
    email: str = Field(..., description="User email")
    password: str = Field(..., min_length=1, description="User password")

class LoginResponse(BaseModel):
    """Login response model"""
    success: bool
    message: str
    data: Optional[Token] = None

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="HUNTER AGENT API",
    description="API for managing HUNTER AGENT AI MARKETING DIGITAL runners",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js development server
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "detail": str(exc),
            "timestamp": datetime.now().isoformat()
        }
    )

# Authentication Functions
def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get current user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = verify_token(token)
        if payload is None:
            raise credentials_exception
        
        user_id: int = payload.get("user_id")
        email: str = payload.get("email")
        role: str = payload.get("role")
        
        if user_id is None or email is None:
            raise credentials_exception
            
        token_data = TokenData(user_id=user_id, email=email, role=role)
        return token_data
        
    except Exception:
        raise credentials_exception

def get_current_active_user(current_user: TokenData = Depends(get_current_user)):
    """Get current active user"""
    # For now, all authenticated users are considered active
    return current_user

def authenticate_user(email: str, password: str) -> Optional[Dict[str, Any]]:
    """
    Authenticate user with email and password
    Hardcoded authentication for now, can be extended to use database
    """
    # Hardcoded admin credentials
    if email == 'admin@lumina.os' and password == 'hunter2026':
        return {
            "id": 1,
            "name": "Grand Commander",
            "email": "admin@lumina.os",
            "role": "admin",
            "created_at": "2024-01-01T00:00:00Z"
        }
    
    # Additional hardcoded users for testing
    if email == 'agent@lumina.os' and password == 'agent2026':
        return {
            "id": 2,
            "name": "Field Agent",
            "email": "agent@lumina.os",
            "role": "agent",
            "created_at": "2024-01-01T00:00:00Z"
        }
    
    if email == 'analyst@lumina.os' and password == 'analyst2026':
        return {
            "id": 3,
            "name": "Data Analyst",
            "email": "analyst@lumina.os",
            "role": "analyst",
            "created_at": "2024-01-01T00:00:00Z"
        }
    
    return None

# Authentication Endpoints

@app.post("/api/auth/login", response_model=LoginResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    User login endpoint
    
    Args:
        form_data: OAuth2 password request form with username and password
        
    Returns:
        LoginResponse with JWT token and user information
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
        
        return LoginResponse(
            success=True,
            message="Login successful",
            data=token_response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during login"
        )

@app.post("/api/auth/login-json", response_model=LoginResponse)
async def login_json(login_request: LoginRequest):
    """
    User login endpoint with JSON payload
    
    Args:
        login_request: Login request with email and password
        
    Returns:
        LoginResponse with JWT token and user information
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
        
        return LoginResponse(
            success=True,
            message="Login successful",
            data=token_response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during login"
        )

@app.get("/api/auth/me", response_model=User)
async def get_current_user_info(current_user: TokenData = Depends(get_current_active_user)):
    """
    Get current user information
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        User information
    """
    try:
        # Re-authenticate to get fresh user data
        user_data = authenticate_user(current_user.email, "dummy_password")
        
        if user_data:
            return User(
                id=user_data["id"],
                name=user_data["name"],
                email=user_data["email"],
                role=user_data["role"],
                created_at=user_data.get("created_at")
            )
        else:
            # Fallback to token data
            return User(
                id=current_user.user_id or 0,
                name="Unknown User",
                email=current_user.email or "",
                role=current_user.role or "user"
            )
            
    except Exception as e:
        logger.error(f"Get user info error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user information"
        )

@app.post("/api/auth/logout")
async def logout():
    """
    User logout endpoint
    Note: JWT tokens are stateless, actual token invalidation
    would require a token blacklist or refresh token system
    """
    return {
        "success": True,
        "message": "Logout successful"
    }

@app.get("/api/auth/verify")
async def verify_token_endpoint(token: str):
    """
    Verify JWT token endpoint
    
    Args:
        token: JWT token to verify
        
    Returns:
        Token verification result
    """
    try:
        payload = verify_token(token)
        
        if payload is None:
            return {
                "success": False,
                "message": "Invalid or expired token"
            }
        
        return {
            "success": True,
            "message": "Token is valid",
            "data": {
                "user_id": payload.get("user_id"),
                "email": payload.get("email"),
                "role": payload.get("role"),
                "expires_at": payload.get("exp")
            }
        }
        
    except Exception as e:
        logger.error(f"Token verification error: {e}")
        return {
            "success": False,
            "message": "Token verification failed"
        }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "HUNTER AGENT API"
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "HUNTER AGENT AI MARKETING DIGITAL API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "runners": "/api/runners",
            "start_runner": "/api/runners/{runner_name}/start",
            "stop_runner": "/api/runners/{runner_name}/stop",
            "runner_info": "/api/runners/{runner_name}"
        },
        "timestamp": datetime.now().isoformat()
    }

# Get all runners status
@app.get("/api/runners")
async def get_runners_status():
    """Get status of all runners"""
    try:
        status = runner_manager.get_status()
        logger.info(f"Retrieved runners status: {status['total_running']} running")
        return {
            "success": True,
            "data": status,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting runners status: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get runners status: {str(e)}"
        )

# Start a specific runner
@app.post("/api/runners/{runner_name}/start")
async def start_runner(runner_name: str):
    """Start a specific runner"""
    try:
        # Validate runner name
        valid_runners = list(runner_manager.runner_mapping.keys())
        if runner_name not in valid_runners:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid runner name. Valid runners: {valid_runners}"
            )
        
        result = runner_manager.start_runner(runner_name)
        
        if result["success"]:
            logger.info(f"Started runner: {runner_name} (PID: {result.get('pid')})")
            return {
                "success": True,
                "data": result,
                "message": f"Runner {runner_name} started successfully",
                "timestamp": datetime.now().isoformat()
            }
        else:
            logger.warning(f"Failed to start runner {runner_name}: {result.get('error')}")
            raise HTTPException(
                status_code=400,
                detail=result.get("error", "Failed to start runner")
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error starting runner {runner_name}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to start runner: {str(e)}"
        )

# Stop a specific runner
@app.post("/api/runners/{runner_name}/stop")
async def stop_runner(runner_name: str):
    """Stop a specific runner"""
    try:
        result = runner_manager.stop_runner(runner_name)
        
        if result["success"]:
            logger.info(f"Stopped runner: {runner_name}")
            return {
                "success": True,
                "data": result,
                "message": f"Runner {runner_name} stopped successfully",
                "timestamp": datetime.now().isoformat()
            }
        else:
            logger.warning(f"Failed to stop runner {runner_name}: {result.get('error')}")
            raise HTTPException(
                status_code=400,
                detail=result.get("error", "Failed to stop runner")
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error stopping runner {runner_name}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to stop runner: {str(e)}"
        )

# Get specific runner information
@app.get("/api/runners/{runner_name}")
async def get_runner_info(runner_name: str):
    """Get detailed information about a specific runner"""
    try:
        info = runner_manager.get_runner_info(runner_name)
        
        if info is None:
            return {
                "success": True,
                "data": {
                    "script_name": runner_name,
                    "status": "Idle",
                    "message": "Runner not started"
                },
                "timestamp": datetime.now().isoformat()
            }
        
        return {
            "success": True,
            "data": info,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting runner info for {runner_name}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get runner info: {str(e)}"
        )

# Clean up dead processes
@app.post("/api/cleanup")
async def cleanup_dead_processes():
    """Clean up dead processes from tracking"""
    try:
        cleaned_count = runner_manager.cleanup_dead_processes()
        logger.info(f"Cleaned up {cleaned_count} dead processes")
        return {
            "success": True,
            "data": {
                "cleaned_count": cleaned_count,
                "message": f"Cleaned up {cleaned_count} dead processes"
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error during cleanup: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to cleanup: {str(e)}"
        )

# Get system information
@app.get("/api/system")
async def get_system_info():
    """Get system information and statistics"""
    try:
        import psutil
        
        # Get system stats
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Get runner stats
        runner_status = runner_manager.get_status()
        
        system_info = {
            "system": {
                "cpu_percent": cpu_percent,
                "memory": {
                    "total": memory.total,
                    "available": memory.available,
                    "percent": memory.percent,
                    "used": memory.used,
                    "free": memory.free
                },
                "disk": {
                    "total": disk.total,
                    "used": disk.used,
                    "free": disk.free,
                    "percent": (disk.used / disk.total) * 100
                }
            },
            "runners": {
                "total": len(runner_manager.runner_mapping),
                "running": runner_status["total_running"],
                "idle": len(runner_manager.runner_mapping) - runner_status["total_running"]
            },
            "timestamp": datetime.now().isoformat()
        }
        
        return {
            "success": True,
            "data": system_info,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting system info: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get system info: {str(e)}"
        )

# Get available runners
@app.get("/api/runners/available")
async def get_available_runners():
    """Get list of available runners with their script mappings"""
    try:
        runners_info = {}
        for runner_name, script_file in runner_manager.runner_mapping.items():
            runners_info[runner_name] = {
                "script_file": script_file,
                "description": self._get_runner_description(runner_name),
                "category": self._get_runner_category(runner_name)
            }
        
        return {
            "success": True,
            "data": {
                "runners": runners_info,
                "total": len(runner_manager.runner_mapping)
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting available runners: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get available runners: {str(e)}"
        )

def _get_runner_description(runner_name: str) -> str:
    """Get description for a runner"""
    descriptions = {
        'lead_generation': 'Multi-engine lead acquisition system',
        'banten_government': 'PNS/P3K market analysis and intelligence',
        'ride_hailing': 'Transportation patterns and mobility analysis',
        'property_scraper': 'Real estate data monitoring and scraping',
        'social_verifier': 'Social media sentiment and proof verification',
        'behavioral_tester': 'User behavior tracking and analysis'
    }
    return descriptions.get(runner_name, 'Unknown runner')

def _get_runner_category(runner_name: str) -> str:
    """Get category for a runner"""
    categories = {
        'lead_generation': 'Lead Generation',
        'banten_government': 'Government Intelligence',
        'ride_hailing': 'Transportation',
        'property_scraper': 'Real Estate',
        'social_verifier': 'Social Media',
        'behavioral_tester': 'Analytics'
    }
    return categories.get(runner_name, 'General')

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Error sending message to WebSocket: {e}")
                disconnected.append(connection)
        
        # Remove disconnected connections
        for conn in disconnected:
            self.disconnect(conn)

manager = ConnectionManager()

# Log message templates
LOG_TEMPLATES = {
    'system': [
        "🔧 SYSTEM: Hunter AI Engine initialized successfully",
        "🔧 SYSTEM: Process manager started with {runner_count} runners",
        "🔧 SYSTEM: Database connection established",
        "🔧 SYSTEM: API server listening on port 8000",
        "🔧 SYSTEM: WebSocket server ready for connections",
        "🔧 SYSTEM: Security protocols activated",
        "🔧 SYSTEM: Cache warming completed",
        "🔧 SYSTEM: Health check passed",
    ],
    'intelligence': [
        "🧠 INTELLIGENCE: Lead scoring model deployed",
        "🧠 INTELLIGENCE: Market analysis completed for {region}",
        "🧠 INTELLIGENCE: Competitor price drift detected",
        "🧠 INTELLIGENCE: New lead pattern identified",
        "🧠 INTELLIGENCE: Sentiment analysis updated",
        "🧠 INTELLIGENCE: Trend detection algorithm optimized",
        "🧠 INTELLIGENCE: Entity extraction accuracy: {accuracy}%",
        "🧠 INTELLIGENCE: Intent classification model trained",
    ],
    'runner': [
        "🚀 RUNNER: {runner_name} started successfully",
        "🚀 RUNNER: {runner_name} process monitoring active",
        "🚀 RUNNER: {runner_name} completed {count} operations",
        "🚀 RUNNER: {runner_name} memory usage: {memory}%",
        "🚀 RUNNER: {runner_name} CPU usage: {cpu}%",
        "🚀 RUNNER: {runner_name} stopped gracefully",
        "🚀 RUNNER: {runner_name} restarted after crash",
        "🚀 RUNNER: {runner_name} performance optimized",
    ],
    'security': [
        "🛡️ SECURITY: Authentication token refreshed",
        "🛡️ SECURITY: Rate limit threshold reached",
        "🛡️ SECURITY: Suspicious activity detected from {ip}",
        "🛡️ SECURITY: Firewall rule updated",
        "🛡️ SECURITY: SSL certificate renewed",
        "🛡️ SECURITY: Access control policy enforced",
        "🛡️ SECURITY: Security audit completed",
        "🛡️ SECURITY: Threat intelligence updated",
    ],
    'error': [
        "❌ ERROR: Database connection timeout",
        "❌ ERROR: Failed to start {runner_name} runner",
        "❌ ERROR: Memory usage exceeded threshold",
        "❌ ERROR: API rate limit exceeded",
        "❌ ERROR: Invalid authentication token",
        "❌ ERROR: Process {pid} not found",
        "❌ ERROR: Network connection lost",
        "❌ ERROR: Configuration file corrupted",
    ],
    'success': [
        "✅ SUCCESS: All runners operational",
        "✅ SUCCESS: Data backup completed",
        "✅ SUCCESS: System update installed",
        "✅ SUCCESS: Performance optimization applied",
        "✅ SUCCESS: Cache cleared successfully",
        "✅ SUCCESS: Database migration completed",
        "✅ SUCCESS: Load balancer configured",
        "✅ SUCCESS: Monitoring alerts configured",
    ],
    'warning': [
        "⚠️ WARNING: High memory usage detected",
        "⚠️ WARNING: Runner {runner_name} unresponsive",
        "⚠️ WARNING: Disk space running low",
        "⚠️ WARNING: API response time degraded",
        "⚠️ WARNING: SSL certificate expiring soon",
        "⚠️ WARNING: Backup service delayed",
        "⚠️ WARNING: Cache hit rate below threshold",
        "⚠️ WARNING: Log rotation needed",
    ]
}

# Generate realistic log messages
def generate_log_message():
    categories = list(LOG_TEMPLATES.keys())
    category = random.choice(categories)
    templates = LOG_TEMPLATES[category]
    template = random.choice(templates)
    
    # Format message with dynamic values
    try:
        if '{runner_name}' in template:
            runner_names = ['lead_generation', 'banten_government', 'ride_hailing', 
                           'property_scraper', 'social_verifier', 'behavioral_tester']
            runner_name = random.choice(runner_names)
            message = template.format(runner_name=runner_name)
        elif '{region}' in template:
            regions = ['Serang', 'Jakarta', 'Bandung', 'Surabaya', 'Medan']
            message = template.format(region=random.choice(regions))
        elif '{accuracy}' in template:
            accuracy = random.randint(85, 99)
            message = template.format(accuracy=f"{accuracy}%")
        elif '{memory}' in template:
            memory = random.randint(20, 80)
            message = template.format(memory=f"{memory}%")
        elif '{cpu}' in template:
            cpu = random.randint(10, 60)
            message = template.format(cpu=f"{cpu}%")
        elif '{count}' in template:
            count = random.randint(10, 1000)
            message = template.format(count=count)
        elif '{pid}' in template:
            pid = random.randint(1000, 9999)
            message = template.format(pid=pid)
        elif '{ip}' in template:
            ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
            message = template.format(ip=ip)
        else:
            message = template
    except Exception:
        message = template
    
    # Create log entry
    log_entry = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(),
        "level": "INFO" if category in ['system', 'intelligence', 'runner', 'success'] else 
                "ERROR" if category == 'error' else 
                "WARNING",
        "category": category.upper(),
        "message": message,
        "source": random.choice([
            "HUNTER_AI_ENGINE",
            "PROCESS_MANAGER", 
            "INTELLIGENCE_MODULE",
            "SECURITY_LAYER",
            "RUNNER_CONTROLLER",
            "API_GATEWAY"
        ])
    }
    
    return log_entry

# WebSocket endpoint for real-time log streaming
@app.websocket("/api/ws/logs")
async def websocket_logs(websocket: WebSocket):
    await manager.connect(websocket)
    
    try:
        # Send initial connection message
        initial_message = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "level": "INFO",
            "category": "SYSTEM",
            "message": "🔌 WebSocket connection established. Real-time log streaming active.",
            "source": "WEBSOCKET_SERVER"
        }
        await manager.send_personal_message(json.dumps(initial_message), websocket)
        
        # Start log streaming task
        log_task = asyncio.create_task(stream_logs(websocket))
        
        # Keep connection alive and handle incoming messages
        try:
            while True:
                data = await websocket.receive_text()
                # Handle any incoming messages if needed
                logger.debug(f"Received WebSocket message: {data}")
        except WebSocketDisconnect:
            logger.info("WebSocket client disconnected")
        finally:
            log_task.cancel()
            
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected during connection setup")
    finally:
        manager.disconnect(websocket)

async def stream_logs(websocket: WebSocket):
    """Stream log messages to WebSocket client"""
    try:
        while True:
            # Generate and send log message every 2 seconds
            log_entry = generate_log_message()
            
            # Add some variety to timing
            delay = random.uniform(1.5, 2.5)
            
            await manager.send_personal_message(json.dumps(log_entry), websocket)
            await asyncio.sleep(delay)
            
    except asyncio.CancelledError:
        logger.info("Log streaming task cancelled")
    except Exception as e:
        logger.error(f"Error in log streaming: {e}")
        # Send error message to client
        error_message = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "level": "ERROR",
            "category": "SYSTEM",
            "message": f"🔌 Log streaming error: {str(e)}",
            "source": "WEBSOCKET_SERVER"
        }
        try:
            await manager.send_personal_message(json.dumps(error_message), websocket)
        except:
            pass

# Global search endpoint
@app.get("/api/search")
async def global_search(q: str = ""):
    """
    Global search across leads, runners, and campaigns
    """
    if not q or len(q.strip()) < 2:
        return JSONResponse(
            content={
                "success": True,
                "data": {
                    "leads": [],
                    "runners": [],
                    "campaigns": []
                },
                "timestamp": datetime.now().isoformat()
            }
        )
    
    query = q.strip().lower()
    
    # Search runners
    runners_data = runner_manager.get_all_runners()
    matching_runners = []
    
    for runner_name, runner_info in runners_data.items():
        # Search in runner name and description
        if (query in runner_name.lower() or 
            query in _get_runner_description(runner_name).lower() or
            query in _get_runner_category(runner_name).lower()):
            
            matching_runners.append({
                "id": runner_name,
                "name": runner_name.replace('_', ' ').title(),
                "description": _get_runner_description(runner_name),
                "category": _get_runner_category(runner_name),
                "status": runner_info.get('status', 'idle'),
                "type": "runner"
            })
    
    # Generate dummy leads (in real implementation, this would search the database)
    dummy_leads = []
    if any(keyword in query for keyword in ['rumah', 'house', 'properti', 'property']):
        dummy_leads.extend([
            {
                "id": "lead_1",
                "title": f"Rumah Dijual di {query.title()} Area",
                "description": f"Properti dengan 3 kamar tidur, lokasi strategis dekat {query.title()}",
                "price": "Rp 450.000.000",
                "location": query.title(),
                "type": "lead",
                "score": 8
            },
            {
                "id": "lead_2", 
                "title": f"Apartemen {query.title()} City Center",
                "description": f"Unit studio dengan view kota, cocok untuk investasi di {query.title()}",
                "price": "Rp 285.000.000",
                "location": query.title(),
                "type": "lead",
                "score": 7
            }
        ])
    
    # Generate dummy campaigns
    dummy_campaigns = []
    if any(keyword in query for keyword in ['campaign', 'promo', 'diskon', 'marketing']):
        dummy_campaigns.extend([
            {
                "id": "campaign_1",
                "title": f"Flash Sale {query.title()} Properties",
                "description": f"Diskon hingga 20% untuk pembelian properti di {query.title()}",
                "discount": "20%",
                "valid_until": "2026-06-30",
                "type": "campaign",
                "status": "active"
            },
            {
                "id": "campaign_2",
                "title": f"KPR Special {query.title()}",
                "description": f"Bunga KPR rendah khusus untuk properti di {query.title()}",
                "interest_rate": "4.5%",
                "valid_until": "2026-07-15",
                "type": "campaign", 
                "status": "active"
            }
        ])
    
    return JSONResponse(
        content={
            "success": True,
            "data": {
                "leads": dummy_leads,
                "runners": matching_runners,
                "campaigns": dummy_campaigns
            },
            "timestamp": datetime.now().isoformat()
        }
    )

# Database helper function - Supabase Cloud Database
def get_supabase_manager_instance():
    """Get Supabase manager instance with proper error handling"""
    try:
        manager = get_supabase_manager()
        return manager
    except Exception as e:
        logger.error(f"Supabase connection error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Supabase connection failed: {str(e)}"
        )

# Omni-Channel Inbox Endpoints

@app.get("/api/inbox/pending")
async def get_pending_leads():
    """
    Get all leads with status 'Follow Up' and non-null catatan_followup
    Parse catatan_followup JSON and return structured data
    """
    try:
        supabase_manager = get_supabase_manager_instance()
        
        # Query leads with Follow Up status and non-null catatan_followup
        result = supabase_manager.supabase.table('leads')\
            .select('*')\
            .eq('status', 'Follow Up')\
            .not_.is_('catatan_followup', 'null')\
            .neq('catatan_followup', '')\
            .order('date_found', desc=True)\
            .execute()
        
        leads_data = result.data if result.data else []
        pending_leads = []
        
        for lead in leads_data:
            lead_data = {
                "id": lead["id"],
                "business_name": lead["business_name"],
                "contact": lead["contact"],
                "url": lead["url"],
                "keywords": lead["keywords"],
                "source": lead["source"],
                "score": lead["score"],
                "status": lead["status"],
                "location": lead["location"],
                "date_found": lead["date_found"],
                "created_at": lead["created_at"],
                "updated_at": lead["updated_at"],
                "catatan_followup": None
            }
            
            # Parse catatan_followup JSON safely
            try:
                if lead["catatan_followup"]:
                    followup_data = json.loads(lead["catatan_followup"])
                    
                    # Extract message and metadata from Gemini response
                    parsed_followup = {
                        "message": followup_data.get("message", ""),
                        "metadata": followup_data.get("metadata", {}),
                        "raw_json": lead["catatan_followup"]
                    }
                    lead_data["catatan_followup"] = parsed_followup
                    
            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse catatan_followup for lead {lead['id']}: {e}")
                # Keep raw data if parsing fails
                lead_data["catatan_followup"] = {
                    "message": lead["catatan_followup"],
                    "metadata": {},
                    "raw_json": lead["catatan_followup"],
                    "parse_error": str(e)
                }
            except Exception as e:
                logger.error(f"Unexpected error parsing catatan_followup for lead {lead['id']}: {e}")
                lead_data["catatan_followup"] = {
                    "message": "Error parsing follow-up notes",
                    "metadata": {},
                    "raw_json": lead["catatan_followup"],
                    "parse_error": str(e)
                }
            
            pending_leads.append(lead_data)
        
        logger.info(f"Retrieved {len(pending_leads)} pending leads from Supabase Cloud")
        
        return {
            "success": True,
            "data": {
                "leads": pending_leads,
                "total": len(pending_leads)
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Supabase error in get_pending_leads: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Database query failed: {str(e)}"
        )

@app.post("/api/inbox/approve/{lead_id}")
async def approve_lead(lead_id: int):
    """
    Update lead status to 'Contacted'
    """
    try:
        # Validate lead_id
        if not isinstance(lead_id, int) or lead_id <= 0:
            raise HTTPException(
                status_code=400,
                detail="Invalid lead ID. Must be a positive integer."
            )
        
        supabase_manager = get_supabase_manager_instance()
        
        # Check if lead exists
        result = supabase_manager.supabase.table('leads')\
            .select('id, status')\
            .eq('id', lead_id)\
            .execute()
        
        if not result.data or len(result.data) == 0:
            raise HTTPException(
                status_code=404,
                detail=f"Lead with ID {lead_id} not found"
            )
        
        lead = result.data[0]
        old_status = lead["status"]
        
        # Update lead status to 'Contacted'
        update_result = supabase_manager.update_lead_status(
            lead_id=lead_id,
            status='Contacted'
        )
        
        if not update_result['success']:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to update lead status: {update_result['error']}"
            )
        
        new_status = 'Contacted'
        
        logger.info(f"Lead {lead_id} status updated from '{old_status}' to '{new_status}' in Supabase Cloud")
        
        return {
            "success": True,
            "data": {
                "lead_id": lead_id,
                "old_status": old_status,
                "new_status": new_status,
                "updated_at": datetime.now().isoformat()
            },
            "message": f"Lead {lead_id} approved and marked as contacted",
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Supabase error in approve_lead {lead_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to approve lead: {str(e)}"
        )

@app.get("/api/inbox/stats")
async def get_inbox_stats():
    """
    Get inbox statistics including pending leads count
    """
    try:
        supabase_manager = get_supabase_manager_instance()
        
        # Get lead count by status
        result = supabase_manager.supabase.table('leads')\
            .select('status')\
            .execute()
        
        leads_data = result.data if result.data else []
        status_counts = {}
        
        for lead in leads_data:
            status = lead["status"]
            status_counts[status] = status_counts.get(status, 0) + 1
        
        # Get pending leads count (Follow Up with catatan_followup)
        pending_result = supabase_manager.supabase.table('leads')\
            .select('id')\
            .eq('status', 'Follow Up')\
            .not_.is_('catatan_followup', 'null')\
            .neq('catatan_followup', '')\
            .execute()
        
        pending_count = len(pending_result.data) if pending_result.data else 0
        
        # Get total leads
        total_result = supabase_manager.supabase.table('leads')\
            .select('id', count='exact')\
            .execute()
        
        total_leads = total_result.count if total_result.count else 0
        
        stats = {
            "total_leads": total_leads,
            "pending_leads": pending_count,
            "status_breakdown": status_counts,
            "pending_breakdown": {
                "follow_up_with_notes": pending_count,
                "follow_up_total": status_counts.get("Follow Up", 0),
                "new_leads": status_counts.get("New", 0),
                "contacted_leads": status_counts.get("Contacted", 0),
                "qualified_leads": status_counts.get("Qualified", 0),
                "closed_leads": status_counts.get("Closed", 0)
            }
        }
        
        return {
            "success": True,
            "data": stats,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Supabase error in get_inbox_stats: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Database query failed: {str(e)}"
        )

# Webhook Dependency Function
def verify_webhook_token(x_lumina_token: str = None):
    """
    Dependency function to validate X-Lumina-Token header
    """
    if x_lumina_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="X-Lumina-Token header is missing"
        )
    
    if x_lumina_token != LUMINA_WEBHOOK_TOKEN:
        logger.warning(f"Invalid webhook token: {x_lumina_token}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid X-Lumina-Token"
        )
    
    return x_lumina_token

# Webhook Endpoints

@app.get("/api/webhook/health")
async def webhook_health():
    """
    Webhook health check endpoint
    """
    return {
        "status": "OK",
        "service": "Lumina Webhook Intake Engine",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

@app.post("/api/webhook/incoming-lead", status_code=status.HTTP_201_CREATED)
async def incoming_lead_webhook(
    payload: LeadWebhookPayload,
    token: str = Depends(verify_webhook_token)
):
    """
    Process incoming lead webhook with AI scoring, encryption, and database storage
    Protected by X-Lumina-Token dependency
    """
    try:
        logger.info(f"Received webhook lead: {payload.nama} from {payload.sumber}")
        
        # Import LeadScorer and DataVault
        from api.utils.predictive_scoring import LeadScorer
        from api.utils.encryption import DataVault
        
        # Initialize scorer and encryption system with error handling
        scorer = LeadScorer()
        
        try:
            vault = DataVault()
        except Exception as e:
            logger.error(f"Failed to initialize DataVault encryption system: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Data encryption system unavailable"
            )
        
        # Create combined text for scoring
        combined_text = f"{payload.nama} {payload.catatan or ''} {payload.lokasi or ''} {payload.pekerjaan or ''}"
        
        # Score the lead
        scoring_result = scorer.calculate_score(
            title=payload.nama,
            description=combined_text,
            source=payload.sumber
        )
        
        # Prepare sensitive data for encryption
        sensitive_data = {
            'phone': payload.no_hp,
            'email': payload.email,
            'contact_info': None
        }
        
        # Create contact info string
        contact_parts = []
        if payload.no_hp:
            contact_parts.append(f"Phone: {payload.no_hp}")
        if payload.email:
            contact_parts.append(f"Email: {payload.email}")
        if payload.pekerjaan:
            contact_parts.append(f"Occupation: {payload.pekerjaan}")
        if payload.lokasi:
            contact_parts.append(f"Location: {payload.lokasi}")
        if payload.catatan:
            contact_parts.append(f"Notes: {payload.catatan}")
        
        sensitive_data['contact_info'] = ", ".join(contact_parts)
        
        # Encrypt sensitive data with comprehensive error handling
        try:
            encrypted_data = vault.encrypt_sensitive_fields(sensitive_data)
            
            # Verify encryption success
            if not encrypted_data.get('phone') and payload.no_hp:
                logger.error(f"Failed to encrypt phone number for lead {payload.nama}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to encrypt sensitive phone data"
                )
            
            if not encrypted_data.get('email') and payload.email:
                logger.error(f"Failed to encrypt email for lead {payload.nama}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to encrypt sensitive email data"
                )
            
            if not encrypted_data.get('contact_info'):
                logger.error(f"Failed to encrypt contact info for lead {payload.nama}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to encrypt contact information"
                )
            
            # Prepare data for database insertion with encryption
            business_name = payload.nama
            contact = encrypted_data['contact_info']
            
            # Log encryption status
            logger.info(f"Sensitive data encrypted for lead {payload.nama}")
            logger.info(f"Phone encrypted: {'✅' if encrypted_data['phone'] else '❌'}")
            logger.info(f"Email encrypted: {'✅' if encrypted_data['email'] else '❌'}")
            logger.info(f"Contact info encrypted: {'✅' if encrypted_data['contact_info'] else '❌'}")
            logger.info(f"Encryption compliance: Indonesia PDP Regulation")
            
        except Exception as e:
            logger.error(f"Encryption failed for lead {payload.nama}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Data encryption failed: {str(e)}"
            )
        
        url = f"webhook_{payload.sumber}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        keywords = f"webhook,{payload.sumber.lower()}"
        if payload.campaign:
            keywords += f",{payload.campaign.lower()}"
        if payload.lokasi:
            keywords += f",{payload.lokasi.lower()}"
        
        # Get database connection (Supabase)
        supabase_manager = get_supabase_manager_instance()
        
        # Prepare lead data for Supabase
        lead_data = {
            'business_name': business_name,
            'contact': contact,
            'url': url,
            'keywords': keywords,
            'source': payload.sumber,
            'score': scoring_result.score,
            'status': scoring_result.status,
            'location': payload.lokasi or 'Unknown',
            'date_found': datetime.now().isoformat(),
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        # Insert lead into Supabase cloud database
        insert_result = supabase_manager.insert_lead(lead_data)
        
        if not insert_result['success']:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to save lead to Supabase: {insert_result['error']}"
            )
        
        lead_id = insert_result['data']['id']
        
        # Prepare response data
        response_data = {
            "lead_id": lead_id,
            "nama": payload.nama,
            "no_hp": payload.no_hp,
            "email": payload.email,
            "sumber": payload.sumber,
            "campaign": payload.campaign,
            "lokasi": payload.lokasi,
            "pekerjaan": payload.pekerjaan,
            "score": scoring_result.score,
            "status": scoring_result.status,
            "keywords_found": scoring_result.keywords_found,
            "processed_at": datetime.now().isoformat()
        }
        
        logger.info(f"Successfully processed lead {lead_id}: {payload.nama} (Score: {scoring_result.score}, Status: {scoring_result.status})")
        
        return WebhookResponse(
            success=True,
            message="Lead processed successfully",
            data=response_data
        )
        
    except HTTPException:
        raise
    except ImportError as e:
        logger.error(f"Failed to import required modules: {e}")
        if 'DataVault' in str(e):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Data encryption service unavailable"
            )
        elif 'LeadScorer' in str(e):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Lead scoring service unavailable"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Required services unavailable"
            )
    except Exception as e:
        logger.error(f"Supabase error in webhook: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save lead to Supabase Cloud Database"
        )
    except Exception as e:
        logger.error(f"Unexpected error in webhook: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process lead: {str(e)}"
        )

# Register all webhook routers
try:
    app.include_router(telegram_webhook.router, prefix="/api/telegram", tags=["Telegram Control"])
    print("Telegram webhook router registered successfully")
except Exception as e:
    print(f"Failed to register Telegram webhook router: {e}")

try:
    app.include_router(whatsapp_webhook.router, prefix="/api/whatsapp", tags=["WhatsApp Control"])
    print("WhatsApp webhook router registered successfully")
except Exception as e:
    print(f"Failed to register WhatsApp webhook router: {e}")

try:
    app.include_router(system_control.router, prefix="/api/system-control", tags=["System Control"])
    print("System control router registered successfully")
except Exception as e:
    print(f"Failed to register system control router: {e}")

# Register Black Ops modules
try:
    app.include_router(legal_sovereign.router, tags=["Legal & OCR"])
    print("Legal sovereign router registered successfully")
except Exception as e:
    print(f"Failed to register legal sovereign router: {e}")

try:
    app.include_router(visual_mirage.router, tags=["Visual & AI"])
    print("Visual mirage router registered successfully")
except Exception as e:
    print(f"Failed to register visual mirage router: {e}")

# Register Tripwire Webhook router
try:
    from api.endpoints.tripwire_webhook import router as tripwire_router
    app.include_router(tripwire_router, prefix="/api/tripwire", tags=["Tripwire"])
    print("Tripwire webhook router registered successfully")
except Exception as e:
    print(f"Failed to register tripwire webhook router: {e}")

# Register Tactical Operations router
try:
    from api.endpoints.tactical_ops import router as tactical_router
    app.include_router(tactical_router, prefix="/api/tactical", tags=["Tactical Operations"])
    print("Tactical operations router registered successfully")
except Exception as e:
    print(f"Failed to register tactical operations router: {e}")

# Add the helper functions to the app namespace
app._get_runner_description = _get_runner_description
app._get_runner_category = _get_runner_category

if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting HUNTER AGENT API server...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
