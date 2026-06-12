#!/usr/bin/env python3
"""
LUMINA OVERMIND SYSTEM - Database Migration Script
===============================================

Automated database migration script for Docker container startup
Ensures database schema is up-to-date before application starts
"""

import os
import sys
import logging
import asyncio
from pathlib import Path
from typing import Optional

# Add root directory to Python path
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def check_database_connection() -> bool:
    """Check if database is accessible"""
    try:
        from prisma import Client
        from prisma.errors import PrismaError
        
        client = Client()
        await client.connect()
        
        # Test connection with simple query
        await client.user.find_first()
        
        await client.disconnect()
        logger.info("✅ Database connection successful")
        return True
        
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        return False

async def run_database_migrations() -> bool:
    """Run Prisma database migrations"""
    try:
        logger.info("🔄 Starting database migrations...")
        
        # Change to root directory for Prisma CLI
        os.chdir(root_dir)
        
        # Run Prisma db push (for development/containers)
        import subprocess
        
        result = subprocess.run(
            ["npx", "prisma", "db", "push", "--accept-data-loss"],
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes timeout
        )
        
        if result.returncode == 0:
            logger.info("✅ Database migrations completed successfully")
            logger.info(f"Migration output: {result.stdout}")
            return True
        else:
            logger.error(f"❌ Database migrations failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        logger.error("❌ Database migrations timed out")
        return False
    except Exception as e:
        logger.error(f"❌ Database migration error: {e}")
        return False

async def seed_initial_data() -> bool:
    """Seed initial data if needed"""
    try:
        logger.info("🌱 Checking if initial data seeding is needed...")
        
        from prisma import Client
        
        client = Client()
        await client.connect()
        
        # Check if admin user exists
        admin_user = await client.user.find_first(
            where={"role": "ADMIN"}
        )
        
        if not admin_user:
            logger.info("🌱 Seeding initial admin user...")
            
            # Create default admin user
            from dashboard.api.utils.security import hash_password
            
            admin_password = hash_password("LuminaAdmin2024!")
            
            await client.user.create({
                "data": {
                    "email": "admin@lumina-overmind.com",
                    "username": "admin",
                    "firstName": "System",
                    "lastName": "Administrator",
                    "role": "ADMIN",
                    "isActive": True,
                    "password": admin_password
                }
            })
            
            logger.info("✅ Initial admin user created")
        else:
            logger.info("✅ Admin user already exists")
        
        # Check if default project exists
        default_project = await client.project.find_first()
        
        if not default_project:
            logger.info("🌱 Creating default project...")
            
            await client.project.create({
                "data": {
                    "namaProyek": "Lumina Overmind Demo",
                    "tipeProyek": "KOMERSIL",
                    "lokasi": "Jakarta, Indonesia",
                    "hargaStart": 500000000,
                    "targetMarket": "Premium Investors",
                    "tipeInputLokasi": "NAMA_WILAYAH",
                    "namaWilayah": "Jakarta Selatan",
                    "latitude": -6.2088,
                    "longitude": 106.8456,
                    "radiusKm": 10,
                    "aiPromptStyle": "Professional & Modern",
                    "dorkingTargets": ["property", "investment", "jakarta"],
                    "isActive": True
                }
            })
            
            logger.info("✅ Default project created")
        else:
            logger.info("✅ Default project already exists")
        
        await client.disconnect()
        return True
        
    except Exception as e:
        logger.error(f"❌ Data seeding error: {e}")
        return False

async def verify_database_setup() -> bool:
    """Verify database is properly set up"""
    try:
        logger.info("🔍 Verifying database setup...")
        
        from prisma import Client
        
        client = Client()
        await client.connect()
        
        # Check critical tables exist and are accessible
        user_count = await client.user.count()
        project_count = await client.project.count()
        
        logger.info(f"✅ Database verification passed:")
        logger.info(f"   - Users: {user_count}")
        logger.info(f"   - Projects: {project_count}")
        
        await client.disconnect()
        return True
        
    except Exception as e:
        logger.error(f"❌ Database verification failed: {e}")
        return False

async def main():
    """Main migration function"""
    logger.info("🚀 LUMINA OVERMIND - Database Migration Process Started")
    
    # Step 1: Check database connection
    if not await check_database_connection():
        logger.error("❌ Cannot proceed without database connection")
        sys.exit(1)
    
    # Step 2: Run migrations
    if not await run_database_migrations():
        logger.error("❌ Migration failed, cannot start application")
        sys.exit(1)
    
    # Step 3: Seed initial data
    if not await seed_initial_data():
        logger.warning("⚠️ Data seeding failed, but continuing...")
    
    # Step 4: Verify setup
    if not await verify_database_setup():
        logger.error("❌ Database verification failed")
        sys.exit(1)
    
    logger.info("🎉 Database migration process completed successfully!")
    logger.info("✅ Ready to start LUMINA OVERMIND application")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Migration process interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"💥 Unexpected error during migration: {e}")
        sys.exit(1)
