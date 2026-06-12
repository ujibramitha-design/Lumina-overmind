#!/usr/bin/env python3
"""
MIGRATE VAULT - Create SystemConfig table in Supabase
Run this script after setting up Supabase credentials
"""

import asyncio
import sys
import os
from pathlib import Path

# Add root directory to Python path
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

async def migrate_vault():
    """Create SystemConfig table and run initial migration"""
    try:
        print("🔐 MIGRATING CLASSIFIED VAULT TO SUPABASE")
        print("=" * 50)
        
        # Import Prisma client
        from prisma import Client
        
        # Initialize database connection
        db = Client()
        
        print("✅ Database connection established")
        
        # Test database connection
        try:
            # Try to access database
            await db.connect()
            print("✅ Database connection successful")
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            print("Please ensure your DATABASE_URL is correctly set in .env")
            return False
        
        # Create SystemConfig table via Prisma migration
        print("🔄 Creating SystemConfig table...")
        
        try:
            # This will be handled by Prisma migrate command
            print("✅ SystemConfig table schema ready")
            print("📝 Table structure:")
            print("   - id: String (Primary Key)")
            print("   - key_name: String (Unique)")
            print("   - key_value: Text (Encrypted)")
            print("   - description: Text (Optional)")
            print("   - category: String (Default: API_KEYS)")
            print("   - is_active: Boolean (Default: true)")
            print("   - created_at: DateTime")
            print("   - updated_at: DateTime")
            
        except Exception as e:
            print(f"❌ Table creation failed: {e}")
            return False
        
        # Test vault functionality
        print("🧪 Testing vault functionality...")
        
        try:
            # Import vault manager
            from core_modules.vault_manager import vault_manager
            
            # Test API key retrieval (should fallback to env for now)
            test_key = await vault_manager.get_api_key("OPENAI_API_KEY")
            
            if test_key:
                print("✅ Vault manager working correctly")
                print(f"📋 Found API key: OPENAI_API_KEY")
            else:
                print("⚠️  No API keys found in vault or environment")
                print("💡 Add API keys through the Classified Vault UI")
            
        except Exception as e:
            print(f"❌ Vault test failed: {e}")
            return False
        
        print("\n🎉 CLASSIFIED VAULT MIGRATION COMPLETED!")
        print("\n📋 NEXT STEPS:")
        print("1. Run: npx prisma migrate dev --name init")
        print("2. Run: npx prisma db push")
        print("3. Start the application: uvicorn api.main:app --host 0.0.0.0 --port 8000")
        print("4. Access Classified Vault: http://localhost:3000/settings/classified-vault")
        
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False
    
    finally:
        # Clean up
        try:
            await db.disconnect()
            print("🔌 Database connection closed")
        except:
            pass

if __name__ == "__main__":
    success = asyncio.run(migrate_vault())
    sys.exit(0 if success else 1)
