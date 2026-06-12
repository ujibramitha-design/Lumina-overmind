"""
Database Manager Module - Prisma Async Wrapper
==============================================
Handles all asynchronous database operations using the Prisma Client.
This module acts as a bridge between the application and the database,
ensuring that all connections and queries are handled efficiently.
"""

import logging
import asyncio
from prisma import Prisma
from typing import Optional, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PrismaManager:
    """
    An asynchronous wrapper for the Prisma client to manage database connections and queries.
    """
    _db: Optional[Prisma] = None
    _lock = asyncio.Lock()

    async def get_db(self) -> Prisma:
        """
        Lazily connects to the database and returns the client instance.
        Ensures a single connection is maintained.
        """
        async with self._lock:
            if self._db is None or not self._db.is_connected():
                logger.info("🔌 Initializing new Prisma database connection...")
                try:
                    self._db = Prisma(auto_register=True)
                    await self._db.connect()
                    logger.info("✅ Prisma database connected successfully.")
                except Exception as e:
                    logger.critical(f"❌ CRITICAL: Failed to connect to Prisma database: {e}")
                    raise
            return self._db

    async def disconnect(self):
        """
        Disconnects from the database if a connection exists.
        """
        async with self._lock:
            if self._db and self._db.is_connected():
                logger.info("🔌 Disconnecting from Prisma database...")
                await self._db.disconnect()
                logger.info("✅ Prisma database disconnected.")

    async def health_check(self) -> Dict[str, Any]:
        """
        Performs a health check on the database connection.
        """
        try:
            db = await self.get_db()
            await db.query_raw('SELECT 1')
            return {'status': 'healthy', 'message': 'Database connection is OK.'}
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return {'status': 'unhealthy', 'message': str(e)}

# Create a single, globally accessible instance of the PrismaManager
prisma_manager = PrismaManager()

# Convenience function to get the database client
async def get_db_client() -> Prisma:
    """
    Convenience function to be used as a dependency in FastAPI routes.
    """
    return await prisma_manager.get_db()

if __name__ == '__main__':
    # Example of how to use the PrismaManager
    async def main():
        print("Running PrismaManager example...")
        db_client = await get_db_client()
        
        # Perform a simple query
        try:
            user_count = await db_client.user.count()
            print(f"Successfully connected. Found {user_count} users.")
        except Exception as e:
            print(f"An error occurred during query: {e}")
        finally:
            # Disconnect when done
            await prisma_manager.disconnect()

    asyncio.run(main())
