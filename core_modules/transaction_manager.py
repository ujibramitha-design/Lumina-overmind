"""
LUMINA OS - Transaction Manager & Database Locking
Enterprise-grade transaction management with race condition prevention
"""

import os
import logging
import asyncio
import json
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
from contextlib import contextmanager
import threading
import time

# Database imports
from prisma import Prisma
from prisma.errors import PrismaError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LockType(Enum):
    """Database lock types"""
    EXCLUSIVE = "exclusive"
    SHARED = "shared"
    INTENT_EXCLUSIVE = "intent_exclusive"
    PESSIMISTIC = "pessimistic"

class TransactionStatus(Enum):
    """Transaction status"""
    PENDING = "pending"
    ACTIVE = "active"
    COMMITTED = "committed"
    ROLLED_BACK = "rolled_back"
    FAILED = "failed"

@dataclass
class TransactionInfo:
    """Transaction information"""
    transaction_id: str
    status: TransactionStatus
    lock_type: LockType
    resource_id: str
    resource_type: str
    created_at: datetime
    expires_at: Optional[datetime]
    owner_id: str
    operations: List[str]

@dataclass
class LockInfo:
    """Lock information"""
    lock_id: str
    lock_type: LockType
    resource_id: str
    resource_type: str
    owner_id: str
    created_at: datetime
    expires_at: Optional[datetime]
    is_active: bool

class TransactionManager:
    """
    Enterprise-grade transaction manager with database locking
    Handles race conditions, concurrent access, and data consistency
    """
    
    def __init__(self):
        """Initialize transaction manager"""
        self.logger = logging.getLogger(__name__)
        
        # Database connection
        self.db = None
        self._initialize_database()
        
        # In-memory lock storage for immediate access
        self.active_locks: Dict[str, LockInfo] = {}
        self.lock_timeouts: Dict[LockType, int] = {
            LockType.EXCLUSIVE: 30,  # 30 seconds
            LockType.SHARED: 60,     # 60 seconds
            LockType.INTENT_EXCLUSIVE: 45,  # 45 seconds
            LockType.PESSIMISTIC: 15      # 15 seconds
        }
        
        # Transaction tracking
        self.active_transactions: Dict[str, TransactionInfo] = {}
        self.transaction_timeout = 300  # 5 minutes
        
        # Thread safety
        self._lock = threading.RLock()
        
        # Deadlock detection
        self.deadlock_detection_enabled = True
        self.deadlock_timeout = 60  # 1 minute
        
        self.logger.info("🔐 Transaction Manager initialized")
        self.logger.info(f"🔒 Lock timeouts: {self.lock_timeouts}")
    
    def _initialize_database(self):
        """Initialize database connection"""
        try:
            self.db = Prisma()
            self.logger.info("📊 Transaction Manager database connected")
        except Exception as e:
            self.logger.error(f"❌ Database connection failed: {e}")
            self.db = None
    
    @contextmanager
    async def transaction(self, lock_type: LockType = LockType.EXCLUSIVE, 
                           resource_id: str = None, resource_type: str = None,
                           timeout: int = 30):
        """
        Context manager for database transactions with locking
        
        Args:
            lock_type: Type of lock to acquire
            resource_id: ID of resource to lock
            resource_type: Type of resource being locked
            timeout: Lock timeout in seconds
            
        Yields:
            TransactionInfo: Active transaction information
        """
        transaction_id = self._generate_transaction_id()
        owner_id = self._get_current_user_id()
        
        # Create transaction info
        transaction_info = TransactionInfo(
            transaction_id=transaction_id,
            status=TransactionStatus.PENDING,
            lock_type=lock_type,
            resource_id=resource_id,
            resource_type=resource_type,
            created_at=datetime.now(),
            expires_at=datetime.now() + timedelta(seconds=self.transaction_timeout),
            owner_id=owner_id,
            operations=[]
        )
        
        try:
            # Acquire lock
            await self._acquire_lock(transaction_info, timeout)
            
            # Start database transaction
            if self.db:
                await self.db.start_transaction()
            
            # Update transaction status
            transaction_info.status = TransactionStatus.ACTIVE
            self.active_transactions[transaction_id] = transaction_info
            
            self.logger.info(f"🔒 Transaction started: {transaction_id} ({lock_type.value})")
            
            yield transaction_info
            
            # Commit transaction
            await self._commit_transaction(transaction_id)
            
        except Exception as e:
            # Rollback transaction
            await self._rollback_transaction(transaction_id)
            self.logger.error(f"❌ Transaction failed: {transaction_id} - {e}")
            raise
        finally:
            # Clean up
            await self._cleanup_transaction(transaction_id)
    
    async def _acquire_lock(self, transaction_info: TransactionInfo, timeout: int):
        """Acquire database lock"""
        try:
            lock_id = self._generate_lock_id()
            
            # Check for existing locks
            existing_lock = self._check_existing_lock(
                transaction_info.resource_id,
                transaction_info.resource_type,
                transaction_info.lock_type
            )
            
            if existing_lock and self._is_lock_conflict(existing_lock, transaction_info):
                # Wait for lock to be released or timeout
                await self._wait_for_lock_release(existing_lock, timeout)
            
            # Create lock
            lock_info = LockInfo(
                lock_id=lock_id,
                lock_type=transaction_info.lock_type,
                resource_id=transaction_info.resource_id,
                resource_type=transaction_info.resource_type,
                owner_id=transaction_info.owner_id,
                created_at=datetime.now(),
                expires_at=datetime.now() + timedelta(seconds=timeout),
                is_active=True
            )
            
            # Store lock
            self.active_locks[lock_id] = lock_info
            
            # Store in database if available
            if self.db:
                await self._store_lock_in_database(lock_info)
            
            self.logger.info(f"🔐 Lock acquired: {lock_id} for {transaction_info.resource_type}:{transaction_info.resource_id}")
            
        except Exception as e:
            self.logger.error(f"❌ Lock acquisition failed: {e}")
            raise
    
    def _check_existing_lock(self, resource_id: str, resource_type: str, lock_type: LockType) -> Optional[LockInfo]:
        """Check for existing locks on resource"""
        try:
            with self._lock:
                for lock_info in self.active_locks.values():
                    if (lock_info.resource_id == resource_id and 
                        lock_info.resource_type == resource_type and
                        lock_info.is_active):
                        
                        # Check lock compatibility
                        if self._is_lock_conflict(lock_info, 
                                              TransactionInfo("", lock_type, resource_id, resource_type, "", datetime.now())):
                            return lock_info
            
            return None
            
        except Exception as e:
            self.logger.error(f"❌ Lock check failed: {e}")
            return None
    
    def _is_lock_conflict(self, existing_lock: LockInfo, transaction_info: TransactionInfo) -> bool:
        """Check if locks conflict"""
        try:
            # Same owner - no conflict
            if existing_lock.owner_id == transaction_info.owner_id:
                return False
            
            # Different lock types - check compatibility
            if existing_lock.lock_type == LockType.EXCLUSIVE:
                return True  # Exclusive locks conflict with everything
            
            if existing_lock.lock_type == LockType.SHARED:
                return transaction_info.lock_type == LockType.EXCLUSIVE
            
            if existing_lock.lock_type == LockType.INTENT_EXCLUSIVE:
                return transaction_info.lock_type in [LockType.EXCLUSIVE, LockType.INTENT_EXCLUSIVE]
            
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Lock conflict check failed: {e}")
            return True  # Assume conflict on error
    
    async def _wait_for_lock_release(self, conflicting_lock: LockInfo, timeout: int):
        """Wait for lock to be released"""
        try:
            start_time = time.time()
            
            while (conflicting_lock.is_active and 
                   time.time() - start_time < timeout):
                
                # Check if lock has expired
                if conflicting_lock.expires_at and datetime.now() > conflicting_lock.expires_at:
                    await self._release_lock(conflicting_lock.lock_id)
                    break
                
                # Small delay to prevent busy waiting
                await asyncio.sleep(0.1)
                
                # Update lock info
                conflicting_lock = self.active_locks.get(conflicting_lock.lock_id)
                if not conflicting_lock:
                    break
            
            if conflicting_lock and conflicting_lock.is_active:
                raise TimeoutError(f"Lock timeout after {timeout} seconds")
                
        except Exception as e:
            self.logger.error(f"❌ Lock wait failed: {e}")
            raise
    
    async def _commit_transaction(self, transaction_id: str):
        """Commit database transaction"""
        try:
            if self.db:
                await self.db.commit()
            
            # Update transaction status
            if transaction_id in self.active_transactions:
                self.active_transactions[transaction_id].status = TransactionStatus.COMMITTED
            
            self.logger.info(f"✅ Transaction committed: {transaction_id}")
            
        except Exception as e:
            self.logger.error(f"❌ Transaction commit failed: {e}")
            raise
    
    async def _rollback_transaction(self, transaction_id: str):
        """Rollback database transaction"""
        try:
            if self.db:
                await self.db.rollback()
            
            # Update transaction status
            if transaction_id in self.active_transactions:
                self.active_transactions[transaction_id].status = TransactionStatus.ROLLED_BACK
            
            self.logger.info(f"↩️ Transaction rolled back: {transaction_id}")
            
        except Exception as e:
            self.logger.error(f"❌ Transaction rollback failed: {e}")
    
    async def _cleanup_transaction(self, transaction_id: str):
        """Clean up transaction resources"""
        try:
            # Remove from active transactions
            if transaction_id in self.active_transactions:
                transaction_info = self.active_transactions[transaction_id]
                del self.active_transactions[transaction_id]
                
                # Release locks
                await self._release_transaction_locks(transaction_id)
            
        except Exception as e:
            self.logger.error(f"❌ Transaction cleanup failed: {e}")
    
    async def _release_transaction_locks(self, transaction_id: str):
        """Release all locks for a transaction"""
        try:
            locks_to_release = []
            
            with self._lock:
                for lock_id, lock_info in list(self.active_locks.items()):
                    if lock_info.owner_id == transaction_id:
                        locks_to_release.append(lock_id)
            
            for lock_id in locks_to_release:
                await self._release_lock(lock_id)
                
        except Exception as e:
            self.logger.error(f"❌ Lock release failed: {e}")
    
    async def _release_lock(self, lock_id: str):
        """Release specific lock"""
        try:
            with self._lock:
                if lock_id in self.active_locks:
                    lock_info = self.active_locks[lock_id]
                    lock_info.is_active = False
                    
                    # Remove from active locks
                    del self.active_locks[lock_id]
                    
                    # Remove from database
                    if self.db:
                        await self._remove_lock_from_database(lock_id)
                    
                    self.logger.info(f"🔓 Lock released: {lock_id}")
                
        except Exception as e:
            self.logger.error(f"❌ Lock release failed: {e}")
    
    async def _store_lock_in_database(self, lock_info: LockInfo):
        """Store lock information in database"""
        try:
            # This would store lock in database table
            # For now, just log the action
            self.logger.debug(f"📦 Lock stored in database: {lock_info.lock_id}")
            
        except Exception as e:
            self.logger.error(f"❌ Database lock storage failed: {e}")
    
    async def _remove_lock_from_database(self, lock_id: str):
        """Remove lock information from database"""
        try:
            # This would remove lock from database table
            # For now, just log the action
            self.logger.debug(f"🗑️ Lock removed from database: {lock_id}")
            
        except Exception as e:
            self.logger.error(f"❌ Database lock removal failed: {e}")
    
    def _generate_transaction_id(self) -> str:
        """Generate unique transaction ID"""
        return f"txn_{int(time.time() * 1000000)}_{threading.current_thread().ident}"
    
    def _generate_lock_id(self) -> str:
        """Generate unique lock ID"""
        return f"lock_{int(time.time() * 1000000)}_{threading.current_thread().ident}"
    
    def _get_current_user_id(self) -> str:
        """Get current user ID (mock implementation)"""
        # This would get user ID from authentication system
        return f"user_{threading.current_thread().ident}"
    
    async def handle_concurrent_lead_update(self, lead_id: str, update_data: Dict[str, Any]) -> bool:
        """
        Handle concurrent lead updates with proper locking
        
        Args:
            lead_id: ID of lead to update
            update_data: Data to update
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            async with self.transaction(
                lock_type=LockType.PESSIMISTIC,
                resource_id=lead_id,
                resource_type="lead",
                timeout=15
            ) as txn:
                
                # Perform lead update
                if self.db:
                    # Update lead in database
                    await self.db.lead.update(
                        where={'id': lead_id},
                        data=update_data
                    )
                
                txn.operations.append(f"update_lead:{lead_id}")
                
                self.logger.info(f"🔄 Lead updated: {lead_id}")
                return True
                
        except Exception as e:
            self.logger.error(f"❌ Concurrent lead update failed: {e}")
            return False
    
    async def handle_concurrent_project_update(self, project_id: str, update_data: Dict[str, Any]) -> bool:
        """
        Handle concurrent project updates with proper locking
        
        Args:
            project_id: ID of project to update
            update_data: Data to update
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            async with self.transaction(
                lock_type=LockType.EXCLUSIVE,
                resource_id=project_id,
                resource_type="project",
                timeout=30
            ) as txn:
                
                # Perform project update
                if self.db:
                    # Update project in database
                    await self.db.project.update(
                        where={'id': project_id},
                        data=update_data
                    )
                
                txn.operations.append(f"update_project:{project_id}")
                
                self.logger.info(f"🔄 Project updated: {project_id}")
                return True
                
        except Exception as e:
            self.logger.error(f"❌ Concurrent project update failed: {e}")
            return False
    
    def get_transaction_statistics(self) -> Dict[str, Any]:
        """Get transaction and lock statistics"""
        try:
            stats = {
                'active_transactions': len(self.active_transactions),
                'active_locks': len(self.active_locks),
                'transaction_status_counts': {},
                'lock_type_counts': {},
                'resource_type_counts': {}
            }
            
            # Count transaction statuses
            for txn in self.active_transactions.values():
                status = txn.status.value
                stats['transaction_status_counts'][status] = stats['transaction_status_counts'].get(status, 0) + 1
            
            # Count lock types
            for lock in self.active_locks.values():
                lock_type = lock.lock_type.value
                stats['lock_type_counts'][lock_type] = stats['lock_type_counts'].get(lock_type, 0) + 1
                
                resource_type = lock.resource_type
                stats['resource_type_counts'][resource_type] = stats['resource_type_counts'].get(resource_type, 0) + 1
            
            return stats
            
        except Exception as e:
            self.logger.error(f"❌ Statistics generation failed: {e}")
            return {}
    
    async def detect_deadlocks(self) -> List[Dict[str, Any]]:
        """Detect potential deadlocks in active transactions"""
        try:
            deadlocks = []
            
            with self._lock:
                current_time = datetime.now()
                
                for txn_id, txn in self.active_transactions.items():
                    # Check for long-running transactions
                    if current_time - txn.created_at > timedelta(seconds=self.deadlock_timeout):
                        deadlocks.append({
                            'transaction_id': txn_id,
                            'owner_id': txn.owner_id,
                            'resource_id': txn.resource_id,
                            'resource_type': txn.resource_type,
                            'lock_type': txn.lock_type.value,
                            'duration_seconds': (current_time - txn.created_at).total_seconds(),
                            'operations': txn.operations
                        })
            
            return deadlocks
            
        except Exception as e:
            self.logger.error(f"❌ Deadlock detection failed: {e}")
            return []
    
    async def resolve_deadlock(self, transaction_id: str) -> bool:
        """Resolve deadlock by rolling back transaction"""
        try:
            if transaction_id in self.active_transactions:
                await self._rollback_transaction(transaction_id)
                self.logger.warning(f"🚨 Deadlock resolved: {transaction_id}")
                return True
            else:
                self.logger.warning(f"⚠️ Transaction not found: {transaction_id}")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Deadlock resolution failed: {e}")
            return False

# Global transaction manager instance
transaction_manager = TransactionManager()
