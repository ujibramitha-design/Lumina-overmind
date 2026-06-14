"""
LUMINA OS ENTERPRISE - MAIN API APPLICATION
FastAPI application with VR, Visual, and Intelligence endpoints
"""

import os
import sys
import json
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import uvicorn
import socketio

# Add root directory to Python path
root_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root_dir)

# Import WebSocket handler
from api.websocket_handler import sio, create_socketio_app, ws_manager
# Import JWT middleware
from api.middleware.jwt_auth import JWTAuthenticationMiddleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Setup rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("🚀 Starting LUMINA OS Enterprise API...")
    
    # Initialize Prisma database connection
    from core_modules.db_manager import prisma_manager
    await prisma_manager.get_db()
    
    # Initialize Celery connection (optional - workers may not be running yet)
    try:
        from tasks.celery_app import celery_app
        celery_status = celery_app.control.inspect().stats()
        if celery_status:
            logger.info("✅ Celery workers connected")
        else:
            logger.info("ℹ️ No Celery workers running yet (start with: celery -A tasks.celery_app worker --loglevel=info)")
    except Exception as e:
        logger.warning(f"⚠️ Celery not ready (start worker manually): {e}")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down LUMINA OS Enterprise API...")

# Basic Auth for documentation
DOCS_USERNAME = os.getenv("DOCS_USERNAME", "lumina_admin")
DOCS_PASSWORD = os.getenv("DOCS_PASSWORD", "lumina_docs_2024")

# Create FastAPI application
app = FastAPI(
    title="LUMINA OS Enterprise API",
    description="Enterprise-grade Intelligence, Visual Design, and VR System",
    version="2.0.0",
    lifespan=lifespan,
    docs_url=None,  # Disable default docs
    redoc_url=None  # Disable default redoc
)

# Add rate limiter to app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Custom docs endpoints with basic auth
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

security = HTTPBasic()

async def verify_docs_auth(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, DOCS_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, DOCS_PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials

@app.get("/docs", include_in_schema=False)
async def custom_docs(credentials: HTTPBasicCredentials = Depends(verify_docs_auth)):
    """Custom docs endpoint with basic authentication"""
    from fastapi.openapi.docs import get_swagger_ui_html
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=f"{app.title} - Documentation",
        oauth2_redirect_url="/docs/oauth2-redirect",
    )

@app.get("/redoc", include_in_schema=False)
async def custom_redoc(credentials: HTTPBasicCredentials = Depends(verify_docs_auth)):
    """Custom redoc endpoint with basic authentication"""
    from fastapi.openapi.docs import get_redoc_html
    return get_redoc_html(
        openapi_url="/openapi.json",
        title=f"{app.title} - ReDoc",
    )

# Configure CORS
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Add JWT authentication middleware
app.add_middleware(JWTAuthenticationMiddleware)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/output", StaticFiles(directory="output"), name="output")

# Mount LUMINA OS dashboard
dashboard_path = os.path.join(os.path.dirname(root_dir), "lumina_os", "src")
if os.path.exists(dashboard_path):
    app.mount("/dashboard", StaticFiles(directory=dashboard_path), name="dashboard")
    logger.info(f"✅ Dashboard mounted at /dashboard")
else:
    logger.warning(f"⚠️ Dashboard directory not found: {dashboard_path}")


# Security modules integration
try:
    from core_modules.security.admin_auth import AdminAuth
    from core_modules.security.data_encryption import DataEncryption
    from core_modules.finance.cost_controller import CostController
    
    # Initialize security modules
    admin_auth = AdminAuth()
    data_encryption = DataEncryption()
    cost_controller = CostController()
    
    logger.info("Security modules initialized")
except ImportError as e:
    logger.warning(f"Security modules not available: {e}")
    admin_auth = None
    data_encryption = None
    cost_controller = None



# Security modules integration
try:
    from core_modules.security.admin_auth import AdminAuth
    from core_modules.security.data_encryption import DataEncryption
    from core_modules.finance.cost_controller import CostController
    
    # Initialize security modules
    admin_auth = AdminAuth()
    data_encryption = DataEncryption()
    cost_controller = CostController()
    
    logger.info("Security modules initialized")
except ImportError as e:
    logger.warning(f"Security modules not available: {e}")
    admin_auth = None
    data_encryption = None
    cost_controller = None



# Security modules integration
try:
    from core_modules.security.admin_auth import AdminAuth
    from core_modules.security.data_encryption import DataEncryption
    from core_modules.finance.cost_controller import CostController
    
    # Initialize security modules
    admin_auth = AdminAuth()
    data_encryption = DataEncryption()
    cost_controller = CostController()
    
    logger.info("Security modules initialized")
except ImportError as e:
    logger.warning(f"Security modules not available: {e}")
    admin_auth = None
    data_encryption = None
    cost_controller = None


# Import and include routers
try:
    from api.endpoints.intelligence import router as intelligence_router
    app.include_router(intelligence_router, prefix="/api/intelligence", tags=["Intelligence"])
    logger.info("✅ Intelligence router included")
except ImportError as e:
    logger.warning(f"⚠️ Intelligence router not available: {e}")

try:
    from api.endpoints.leads import router as leads_router
    app.include_router(leads_router, tags=["Leads"])
    logger.info("✅ Leads router included")
except ImportError as e:
    logger.warning(f"⚠️ Leads router not available: {e}")

try:
    from api.endpoints.visual import router as visual_router
    app.include_router(visual_router, prefix="/api/visual", tags=["Visual"])
    logger.info("✅ Visual router included")
except ImportError as e:
    logger.warning(f"⚠️ Visual router not available: {e}")

try:
    from api.endpoints.vr import router as vr_router
    app.include_router(vr_router, prefix="/api/vr", tags=["VR"])
    logger.info("✅ VR router included")
except ImportError as e:
    logger.warning(f"⚠️ VR router not available: {e}")

try:
    from api.endpoints.notifications import router as notifications_router
    app.include_router(notifications_router, prefix="/api/notifications", tags=["Notifications"])
    logger.info("✅ Notifications router included")
except ImportError as e:
    logger.warning(f"⚠️ Notifications router not available: {e}")

# Projects router
try:
    from api.endpoints.projects import router as projects_router
    app.include_router(projects_router, tags=["Projects"])
    logger.info("✅ Projects router included")
except ImportError as e:
    logger.warning(f"⚠️ Projects router not available: {e}")

# J.A.R.V.I.S. router
try:
    from api.endpoints.jarvis import router as jarvis_router
    app.include_router(jarvis_router, tags=["J.A.R.V.I.S."])
    logger.info("✅ J.A.R.V.I.S. router included")
except ImportError as e:
    logger.warning(f"⚠️ J.A.R.V.I.S. router not available: {e}")

# Security router
try:
    from api.endpoints.security import router as security_router
    app.include_router(security_router, prefix="/api/security", tags=["Security"])
    logger.info("✅ Security router included")
except ImportError as e:
    logger.warning(f"⚠️ Security router not available: {e}")


# Security router
try:
    from api.endpoints.security import router as security_router
    app.include_router(security_router, prefix="/api/security", tags=["Security"])
    logger.info("✅ Security router included")
except ImportError as e:
    logger.warning(f"⚠️ Security router not available: {e}")


# Security router
try:
    from api.endpoints.security import router as security_router
    app.include_router(security_router, prefix="/api/security", tags=["Security"])
    logger.info("✅ Security router included")
except ImportError as e:
    logger.warning(f"⚠️ Security router not available: {e}")

# Classified Vault router - Temporarily disabled due to Prisma issues
# try:
#     from api.endpoints.config_vault import router as vault_router
#     app.include_router(vault_router, tags=["Classified Vault"])
#     logger.info("✅ Classified Vault router included")
# except ImportError as e:
#     logger.warning(f"⚠️ Classified Vault router not available: {e}")

# License router
try:
    from api.endpoints.license import router as license_router
    app.include_router(license_router, tags=["License"])
    logger.info("✅ License router included")
except ImportError as e:
    logger.warning(f"⚠️ License router not available: {e}")

# Authentication router
try:
    from api.endpoints.auth import router as auth_router
    app.include_router(auth_router, tags=["Authentication"])
    logger.info("✅ Authentication router included")
except ImportError as e:
    logger.warning(f"⚠️ Authentication router not available: {e}")

# Workflow router
try:
    from api.endpoints.workflows import router as workflows_router
    app.include_router(workflows_router)
    logger.info("✅ Workflows router included")
except ImportError as e:
    logger.warning(f"⚠️ Workflows router not available: {e}")

# Add license middleware - Temporarily disabled for testing
# try:
#     from api.middleware.license_middleware import LicenseMiddleware
#     app.add_middleware(LicenseMiddleware)
#     logger.info("✅ License middleware added")
# except ImportError as e:
#     logger.warning(f"⚠️ License middleware not available: {e}")

# Asset Importer router - Temporarily disabled due to Prisma issues
# try:
#     from api.endpoints.asset_importer import router as asset_importer_router
#     app.include_router(asset_importer_router, tags=["Asset Importer"])
#     logger.info("✅ Asset Importer router included")
# except ImportError as e:
#     logger.warning(f"⚠️ Asset Importer router not available: {e}")

# M2M Webhooks router - Temporarily disabled due to Prisma issues
# try:
#     from api.endpoints.webhooks import router as webhook_router
#     app.include_router(webhook_router, tags=["M2M Webhooks"])
#     logger.info("✅ M2M Webhooks router included")
# except ImportError as e:
#     logger.warning(f"⚠️ M2M Webhooks router not available: {e}")

# Archidep Webhook router
try:
    from api.endpoints.archidep_webhook import router as archidep_router
    app.include_router(archidep_router, tags=["Archidep Webhooks"])
    logger.info("✅ Archidep Webhook router included")
except ImportError as e:
    logger.warning(f"⚠️ Archidep Webhook router not available: {e}")

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """System health check"""
    from core_modules.db_manager import prisma_manager
    from tasks.celery_app import celery_app
    import psutil
    from datetime import datetime

    # Database health
    db_health = await prisma_manager.health_check()

    # Celery health
    celery_status_msg = "connected"
    worker_count = 0
    try:
        celery_stats = celery_app.control.inspect().stats()
        if not celery_stats:
            celery_status_msg = "disconnected (no workers found)"
        else:
            worker_count = len(celery_stats)
    except Exception as e:
        celery_status_msg = f"disconnected ({e})"

    # System info
    system_info = {
        'cpu_percent': psutil.cpu_percent(),
        'memory_percent': psutil.virtual_memory().percent,
        'disk_percent': psutil.disk_usage('/').percent
    }

    overall_status = 'healthy' if db_health['status'] == 'healthy' else 'unhealthy'

    response_data = {
        'status': overall_status,
        'timestamp': datetime.now().isoformat(),
        'version': '2.0.0',
        'database': db_health,
        'celery': {
            'workers': worker_count,
            'status': celery_status_msg
        },
        'system': system_info
    }

    status_code = 200 if overall_status == 'healthy' else 503
    return JSONResponse(status_code=status_code, content=response_data)

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to LUMINA OS Enterprise API",
        "version": "2.0.0",
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "intelligence": "/api/intelligence",
            "visual": "/api/visual",
            "vr": "/api/vr",
            "notifications": "/api/notifications",
            "projects": "/api/projects",
            "jarvis": "/api/jarvis"
        }
    }

# System statistics endpoint
@app.get("/api/stats", tags=["System"])
async def get_system_stats():
    """Get comprehensive system statistics"""
    try:
        # Database statistics
        from core_modules.db_manager_postgres import postgres_db_manager
        db_stats = await postgres_db_manager.get_system_statistics()
        
        # Task statistics
        from tasks.celery_app import TaskMonitor
        task_stats = TaskMonitor.get_task_stats()
        
        # System performance
        import psutil
        performance = {
            'cpu': psutil.cpu_percent(),
            'memory': psutil.virtual_memory()._asdict(),
            'disk': psutil.disk_usage('/').percent
        }
        
        return {
            'database': db_stats,
            'tasks': task_stats,
            'performance': performance,
            'timestamp': '2024-01-01T00:00:00Z'
        }
        
    except Exception as e:
        logger.error(f"Failed to get system stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "Endpoint not found", "path": str(request.url)}
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    logger.error(f"Internal server error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )

# Mount Socket.IO for WebSocket support
app.mount("/socket.io", create_socketio_app())

# Add Socket.IO routes to FastAPI
@app.websocket("/ws")
async def websocket_endpoint():
    """WebSocket endpoint for Socket.IO compatibility"""
    pass

# Development server
if __name__ == "__main__":
    # Create Socket.IO app for development
    socketio_app = create_socketio_app()
    
    # Run with Socket.IO support
    uvicorn.run(
        "api.main:socketio_app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
