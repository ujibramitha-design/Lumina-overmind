#!/usr/bin/env python3
"""
SECURITY MODULES INTEGRATION SCRIPT
Phase 1 Deployment - Connect Security Modules to Main API
"""

import os
import sys
from pathlib import Path

def integrate_security_modules():
    """Integrate security modules into main API"""
    
    print("INTEGRATING SECURITY MODULES TO LUMINA OS API")
    print("=" * 60)
    
    # Step 1: Update api/main.py
    main_api_path = "api/main.py"
    
    # Read current main.py
    with open(main_api_path, 'r', encoding='utf-8') as f:
        main_content = f.read()
    
    # Security imports to add
    security_imports = """
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
"""
    
    # Find insertion point after existing imports
    insertion_point = main_content.find("# Import and include routers")
    
    if insertion_point == -1:
        print("Could not find insertion point in main.py")
        return False
    
    # Insert security imports
    updated_content = (
        main_content[:insertion_point] + 
        security_imports + "\n\n" +
        main_content[insertion_point:]
    )
    
    # Add security router
    security_router = """
# Security router
try:
    from api.endpoints.security import router as security_router
    app.include_router(security_router, prefix="/api/security", tags=["Security"])
    logger.info("✅ Security router included")
except ImportError as e:
    logger.warning(f"⚠️ Security router not available: {e}")
"""
    
    # Find insertion point after JARVIS router
    jarvis_point = updated_content.find('logger.info("✅ J.A.R.V.I.S. router included")')
    
    if jarvis_point != -1:
        # Find end of the try block
        end_point = updated_content.find("except ImportError", jarvis_point)
        if end_point != -1:
            # Find the end of the except block
            end_block = updated_content.find("\n\n", end_point)
            if end_block != -1:
                updated_content = (
                    updated_content[:end_block] + 
                    "\n" + security_router + 
                    updated_content[end_block:]
                )
    
    # Write updated main.py
    with open(main_api_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"Updated {main_api_path}")
    
    # Step 2: Create security endpoints
    security_endpoint_path = "api/endpoints/security.py"
    
    security_endpoint_content = '''"""
Security Endpoints for LUMINA OS
Admin authentication, data encryption, and security management
"""

import logging
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)
router = APIRouter()

# Pydantic models
class AuthRequest(BaseModel):
    user_id: str
    credentials: str

class EncryptionRequest(BaseModel):
    data: str

class CostAnalysisRequest(BaseModel):
    operation_type: str
    parameters: Dict[str, Any]

@router.post("/authenticate")
async def authenticate_admin(request: AuthRequest):
    """Authenticate admin user"""
    try:
        # Import here to avoid circular imports
        from api.main import admin_auth
        
        if not admin_auth:
            raise HTTPException(status_code=503, detail="Security module not available")
        
        # Authenticate user
        auth_result = admin_auth.authenticate_user(request.user_id, request.credentials)
        
        return {
            "status": "success",
            "authenticated": auth_result,
            "timestamp": "2024-01-01T00:00:00Z"
        }
        
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/encrypt")
async def encrypt_data(request: EncryptionRequest):
    """Encrypt sensitive data"""
    try:
        # Import here to avoid circular imports
        from api.main import data_encryption
        
        if not data_encryption:
            raise HTTPException(status_code=503, detail="Encryption module not available")
        
        # Encrypt data
        encrypted_data = data_encryption.encrypt_data(request.data)
        
        return {
            "status": "success",
            "encrypted_data": encrypted_data,
            "timestamp": "2024-01-01T00:00:00Z"
        }
        
    except Exception as e:
        logger.error(f"Encryption error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/decrypt")
async def decrypt_data(request: EncryptionRequest):
    """Decrypt sensitive data"""
    try:
        # Import here to avoid circular imports
        from api.main import data_encryption
        
        if not data_encryption:
            raise HTTPException(status_code=503, detail="Encryption module not available")
        
        # Decrypt data
        decrypted_data = data_encryption.decrypt_data(request.data)
        
        return {
            "status": "success",
            "decrypted_data": decrypted_data,
            "timestamp": "2024-01-01T00:00:00Z"
        }
        
    except Exception as e:
        logger.error(f"Decryption error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/cost-analysis")
async def analyze_costs(request: CostAnalysisRequest):
    """Analyze operation costs"""
    try:
        # Import here to avoid circular imports
        from api.main import cost_controller
        
        if not cost_controller:
            raise HTTPException(status_code=503, detail="Cost controller not available")
        
        # Analyze costs
        cost_analysis = cost_controller.analyze_operation_cost(
            request.operation_type,
            request.parameters
        )
        
        return {
            "status": "success",
            "cost_analysis": cost_analysis,
            "timestamp": "2024-01-01T00:00:00Z"
        }
        
    except Exception as e:
        logger.error(f"Cost analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/security-status")
async def get_security_status():
    """Get security modules status"""
    try:
        # Import here to avoid circular imports
        from api.main import admin_auth, data_encryption, cost_controller
        
        return {
            "status": "active",
            "modules": {
                "admin_auth": admin_auth is not None,
                "data_encryption": data_encryption is not None,
                "cost_controller": cost_controller is not None
            },
            "timestamp": "2024-01-01T00:00:00Z"
        }
        
    except Exception as e:
        logger.error(f"Security status error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
'''
    
    # Create security endpoints directory if not exists
    os.makedirs("api/endpoints", exist_ok=True)
    
    # Write security endpoints
    with open(security_endpoint_path, 'w', encoding='utf-8') as f:
        f.write(security_endpoint_content)
    
    print(f"Created {security_endpoint_path}")
    
    # Step 3: Fix Docker configuration
    dockerfile_fix()
    
    print("\nSECURITY MODULES INTEGRATION COMPLETED!")
    print("NEXT STEPS:")
    print("1. Test the security endpoints: /api/security/security-status")
    print("2. Update .env with ENCRYPTION_KEY")
    print("3. Deploy to production")
    
    return True

def dockerfile_fix():
    """Fix Docker configuration for production"""
    
    print("\nFIXING DOCKER CONFIGURATION")
    
    # Rename Dockerfile.fastapi to Dockerfile.backend
    old_dockerfile = "Dockerfile.fastapi"
    new_dockerfile = "Dockerfile.backend"
    
    if os.path.exists(old_dockerfile) and not os.path.exists(new_dockerfile):
        os.rename(old_dockerfile, new_dockerfile)
        print(f"Renamed {old_dockerfile} -> {new_dockerfile}")
    
    # Create Dockerfile.frontend for Next.js
    dockerfile_frontend = '''# Next.js Frontend Dockerfile
FROM node:18-alpine AS base

# Install dependencies only when needed
FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

# Install dependencies based on the preferred package manager
COPY package.json yarn.lock* package-lock.json* pnpm-lock.yaml* ./
RUN \
  if [ -f yarn.lock ]; then yarn --frozen-lockfile; \
  elif [ -f package-lock.json ]; then npm ci; \
  elif [ -f pnpm-lock.yaml ]; then yarn global add pnpm && pnpm i --frozen-lockfile; \
  else echo "Lockfile not found." && exit 1; \
  fi

# Rebuild the source code only when needed
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Next.js collects completely anonymous telemetry data about general usage.
# Learn more here: https://nextjs.org/telemetry
# Uncomment the following line in case you want to disable telemetry during the build.
ENV NEXT_TELEMETRY_DISABLED 1

RUN npm run build

# Production image, copy all the files and run next
FROM base AS runner
WORKDIR /app

ENV NODE_ENV production
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public

# Set the correct permission for prerender cache
RUN mkdir .next
RUN chown nextjs:nodejs .next

# Automatically leverage output traces to reduce image size
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

CMD ["node", "server.js"]
'''
    
    with open("Dockerfile.frontend", 'w', encoding='utf-8') as f:
        f.write(dockerfile_frontend)
    
    print("Created Dockerfile.frontend")
    
    # Update docker-compose.production.yml to use correct Dockerfiles
    compose_file = "docker-compose.production.yml"
    
    if os.path.exists(compose_file):
        with open(compose_file, 'r', encoding='utf-8') as f:
            compose_content = f.read()
        
        # Update backend service
        updated_compose = compose_content.replace(
            "context: .\n        dockerfile: Dockerfile.backend",
            "context: .\n        dockerfile: Dockerfile.backend"
        )
        
        # Update frontend service
        updated_compose = updated_compose.replace(
            "context: ./dashboard\n        dockerfile: Dockerfile",
            "context: ./dashboard\n        dockerfile: ../Dockerfile.frontend"
        )
        
        with open(compose_file, 'w', encoding='utf-8') as f:
            f.write(updated_compose)
        
        print(f"Updated {compose_file}")

if __name__ == "__main__":
    integrate_security_modules()
