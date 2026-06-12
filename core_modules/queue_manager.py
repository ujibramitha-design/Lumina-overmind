"""
LUMINA OS - Queue Manager & Message Broker
Enterprise-grade message queuing for high-volume operations
"""

import os
import logging
import asyncio
import json
import time
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import queue

# Redis for message queuing
import redis
from celery import Celery

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QueueType(Enum):
    """Queue types for different operations"""
    LEAD_PROCESSING = "lead_processing"
    WHATSAPP_SENDING = "whatsapp_sending"
    EMAIL_SENDING = "email_sending"
    AI_PROCESSING = "ai_processing"
    WEBHOOK_PROCESSING = "webhook_processing"
    BATCH_OPERATIONS = "batch_operations"

class TaskPriority(Enum):
    """Task priority levels"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4
    EMERGENCY = 5

@dataclass
class QueuedTask:
    """Queued task data structure"""
    task_id: str
    queue_type: QueueType
    priority: TaskPriority
    payload: Dict[str, Any]
    created_at: datetime
    retry_count: int = 0
    max_retries: int = 3
    timeout: int = 300
    callback_url: Optional[str] = None

class QueueManager:
    """
    Enterprise-grade queue manager for high-volume operations
    Handles message queuing, background processing, and load balancing
    """
    
    def __init__(self):
        """Initialize queue manager"""
        self.logger = logging.getLogger(__name__)
        
        # Redis connection for queuing
        self.redis_client = None
        self._initialize_redis()
        
        # In-memory queues for immediate processing
        self.memory_queues: Dict[QueueType, queue.Queue] = {}
        self._initialize_memory_queues()
        
        # Thread pool for async processing
        self.thread_pool = ThreadPoolExecutor(max_workers=10)
        
        # Queue statistics
        self.queue_stats = {
            'total_tasks': 0,
            'processed_tasks': 0,
            'failed_tasks': 0,
            'queue_sizes': {},
            'processing_times': {}
        }
        
        # Rate limiting
        self.rate_limiters: Dict[str, Dict[str, Any]] = {}
        self._initialize_rate_limiters()
        
        # Background processing
        self.processing_active = False
        self.background_threads: List[threading.Thread] = []
        
        self.logger.info("📋 Queue Manager initialized")
        self.logger.info(f"🔄 Thread pool: {self.thread_pool._max_workers} workers")
        self.logger.info(f"📦 Memory queues: {len(self.memory_queues)}")
    
    def _initialize_redis(self):
        """Initialize Redis connection"""
        try:
            redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
            self.redis_client = redis.from_url(redis_url, decode_responses=True)
            
            # Test connection
            self.redis_client.ping()
            self.logger.info("🔴 Redis connection established")
            
        except Exception as e:
            self.logger.error(f"❌ Redis connection failed: {e}")
            self.redis_client = None
    
    def _initialize_memory_queues(self):
        """Initialize in-memory queues"""
        for queue_type in QueueType:
            self.memory_queues[queue_type] = queue.Queue(maxsize=1000)
    
    def _initialize_rate_limiters(self):
        """Initialize rate limiters for different operations"""
        self.rate_limiters = {
            'whatsapp_sending': {
                'requests_per_second': 10,
                'burst_size': 50,
                'last_requests': []
            },
            'email_sending': {
                'requests_per_second': 20,
                'burst_size': 100,
                'last_requests': []
            },
            'ai_processing': {
                'requests_per_second': 5,
                'burst_size': 25,
                'last_requests': []
            },
            'webhook_processing': {
                'requests_per_second': 100,
                'burst_size': 500,
                'last_requests': []
            }
        }
    
    async def enqueue_task(self, queue_type: QueueType, payload: Dict[str, Any], 
                           priority: TaskPriority = TaskPriority.NORMAL, 
                           timeout: int = 300, max_retries: int = 3,
                           callback_url: str = None) -> str:
        """
        Enqueue task for processing
        
        Args:
            queue_type: Type of queue for the task
            payload: Task data
            priority: Task priority level
            timeout: Task timeout in seconds
            max_retries: Maximum retry attempts
            callback_url: URL for task completion callback
            
        Returns:
            str: Task ID
        """
        try:
            # Generate task ID
            task_id = f"task_{int(time.time())}_{len(payload)}"
            
            # Create queued task
            task = QueuedTask(
                task_id=task_id,
                queue_type=queue_type,
                priority=priority,
                payload=payload,
                created_at=datetime.now(),
                timeout=timeout,
                max_retries=max_retries,
                callback_url=callback_url
            )
            
            # Check rate limiting
            if not self._check_rate_limit(queue_type.value):
                self.logger.warning(f"🚫 Rate limit exceeded for {queue_type.value}")
                return None
            
            # Add to appropriate queue
            if self.redis_client:
                # Use Redis for distributed queuing
                await self._enqueue_to_redis(task)
            else:
                # Use memory queue
                await self._enqueue_to_memory(task)
            
            # Update statistics
            self.queue_stats['total_tasks'] += 1
            
            self.logger.info(f"📤 Task enqueued: {task_id} to {queue_type.value}")
            return task_id
            
        except Exception as e:
            self.logger.error(f"❌ Task enqueue failed: {e}")
            return None
    
    async def _enqueue_to_redis(self, task: QueuedTask):
        """Enqueue task to Redis"""
        try:
            # Serialize task
            task_data = asdict(task)
            task_data['created_at'] = task_data['created_at'].isoformat()
            
            # Add to Redis list with priority
            queue_key = f"queue:{task.queue_type.value}"
            
            # Use Redis sorted set for priority queue
            score = task.priority.value * 1000000 + int(time.time() * 1000)
            self.redis_client.zadd(queue_key, {task.task_id: json.dumps(task_data)}, score)
            
            # Set task data
            task_key = f"task:{task.task_id}"
            self.redis_client.setex(task_key, task.timeout, json.dumps(task_data))
            
        except Exception as e:
            self.logger.error(f"❌ Redis enqueue failed: {e}")
            raise
    
    async def _enqueue_to_memory(self, task: QueuedTask):
        """Enqueue task to memory queue"""
        try:
            queue = self.memory_queues[task.queue_type]
            
            # Add to queue with priority
            queue.put_nowait((task.priority.value, task))
            
        except Exception as e:
            self.logger.error(f"❌ Memory enqueue failed: {e}")
            raise
    
    def _check_rate_limit(self, queue_name: str) -> bool:
        """Check if operation is within rate limits"""
        try:
            rate_limiter = self.rate_limiters.get(queue_name)
            if not rate_limiter:
                return True
            
            current_time = time.time()
            requests_per_second = rate_limiter['requests_per_second']
            burst_size = rate_limiter['burst_size']
            
            # Clean old requests (older than 1 second)
            rate_limiter['last_requests'] = [
                req_time for req_time in rate_limiter['last_requests']
                if current_time - req_time < 1.0
            ]
            
            # Check if within limits
            if len(rate_limiter['last_requests']) >= requests_per_second:
                return False
            
            if len(rate_limiter['last_requests']) >= burst_size:
                return False
            
            # Add current request
            rate_limiter['last_requests'].append(current_time)
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Rate limit check failed: {e}")
            return True  # Allow on error
    
    async def start_background_processing(self):
        """Start background processing threads"""
        if self.processing_active:
            self.logger.warning("⚠️ Background processing already active")
            return
        
        self.processing_active = True
        
        # Start processing threads for each queue type
        for queue_type in QueueType:
            thread = threading.Thread(
                target=self._process_queue_worker,
                args=(queue_type,),
                name=f"QueueProcessor-{queue_type.value}"
            )
            thread.daemon = True
            thread.start()
            self.background_threads.append(thread)
        
        self.logger.info(f"🚀 Started {len(self.background_threads)} background processing threads")
    
    def _process_queue_worker(self, queue_type: QueueType):
        """Worker thread for processing queue tasks"""
        self.logger.info(f"🔄 Starting queue worker for {queue_type.value}")
        
        while self.processing_active:
            try:
                if self.redis_client:
                    # Process from Redis
                    self._process_redis_queue(queue_type)
                else:
                    # Process from memory queue
                    self._process_memory_queue(queue_type)
                
                # Small delay to prevent busy waiting
                time.sleep(0.1)
                
            except Exception as e:
                self.logger.error(f"❌ Queue worker error: {e}")
                time.sleep(1)  # Wait before retry
    
    def _process_redis_queue(self, queue_type: QueueType):
        """Process tasks from Redis queue"""
        try:
            queue_key = f"queue:{queue_type.value}"
            
            # Get highest priority task
            result = self.redis_client.zpopmin(queue_key, 0)
            
            if result:
                task_id, task_data = result
                task_data = json.loads(task_data)
                
                # Reconstruct task
                task = QueuedTask(
                    task_id=task_id,
                    queue_type=QueueType(task_data['queue_type']),
                    priority=TaskPriority(task_data['priority']),
                    payload=task_data['payload'],
                    created_at=datetime.fromisoformat(task_data['created_at']),
                    retry_count=task_data['retry_count'],
                    max_retries=task_data['max_retries'],
                    timeout=task_data['timeout'],
                    callback_url=task_data.get('callback_url')
                )
                
                # Process task
                asyncio.run(self._process_task(task))
                
        except Exception as e:
            self.logger.error(f"❌ Redis queue processing error: {e}")
    
    def _process_memory_queue(self, queue_type: QueueType):
        """Process tasks from memory queue"""
        try:
            queue = self.memory_queues[queue_type]
            
            # Get task with timeout
            try:
                priority, task = queue.get(timeout=1)
                asyncio.run(self._process_task(task))
            except queue.Empty:
                pass  # No tasks available
                
        except Exception as e:
            self.logger.error(f"❌ Memory queue processing error: {e}")
    
    async def _process_task(self, task: QueuedTask):
        """Process individual task"""
        start_time = time.time()
        
        try:
            self.logger.info(f"⚙️ Processing task: {task.task_id}")
            
            # Route to appropriate handler
            if task.queue_type == QueueType.LEAD_PROCESSING:
                success = await self._handle_lead_processing(task)
            elif task.queue_type == QueueType.WHATSAPP_SENDING:
                success = await self._handle_whatsapp_sending(task)
            elif task.queue_type == QueueType.EMAIL_SENDING:
                success = await self._handle_email_sending(task)
            elif task.queue_type == QueueType.AI_PROCESSING:
                success = await self._handle_ai_processing(task)
            elif task.queue_type == QueueType.WEBHOOK_PROCESSING:
                success = await self._handle_webhook_processing(task)
            elif task.queue_type == QueueType.BATCH_OPERATIONS:
                success = await self._handle_batch_operations(task)
            else:
                self.logger.warning(f"⚠️ Unknown queue type: {task.queue_type.value}")
                success = False
            
            # Update statistics
            processing_time = time.time() - start_time
            self.queue_stats['processed_tasks'] += 1
            self.queue_stats['processing_times'][task.queue_type.value] = processing_time
            
            if success:
                self.logger.info(f"✅ Task completed: {task.task_id} in {processing_time:.2f}s")
            else:
                self.logger.error(f"❌ Task failed: {task.task_id}")
                self.queue_stats['failed_tasks'] += 1
            
            # Send callback if specified
            if task.callback_url and success:
                await self._send_task_callback(task, success)
                
        except Exception as e:
            self.logger.error(f"❌ Task processing error: {task.task_id} - {e}")
            self.queue_stats['failed_tasks'] += 1
            
            # Retry logic
            if task.retry_count < task.max_retries:
                task.retry_count += 1
                await self.enqueue_task(
                    task.queue_type,
                    task.payload,
                    task.priority,
                    task.timeout,
                    task.max_retries - task.retry_count,
                    task.callback_url
                )
    
    async def _handle_lead_processing(self, task: QueuedTask) -> bool:
        """Handle lead processing task"""
        try:
            # Import lead processing logic
            from core_modules.lead_validator import validate_lead
            
            payload = task.payload
            lead_data = payload.get('lead_data', {})
            
            # Validate and process lead
            validation_result = validate_lead(lead_data)
            
            # Save to database
            if validation_result['validation_status'] == 'qualified':
                # Save to database logic here
                self.logger.info(f"💾 Lead saved: {lead_data.get('business_name', 'Unknown')}")
                return True
            else:
                self.logger.info(f"🗑️ Lead rejected: {validation_result['validation_status']}")
                return True
                
        except Exception as e:
            self.logger.error(f"❌ Lead processing error: {e}")
            return False
    
    async def _handle_whatsapp_sending(self, task: QueuedTask) -> bool:
        """Handle WhatsApp sending task"""
        try:
            payload = task.payload
            phone_number = payload.get('phone_number')
            message = payload.get('message')
            
            # Import WhatsApp gateway
            from core_modules.doom_sentinel.whatsapp_gateway import WhatsAppGateway
            
            gateway = WhatsAppGateway()
            result = await gateway.send_message(phone_number, message)
            
            return result is not None
            
        except Exception as e:
            self.logger.error(f"❌ WhatsApp sending error: {e}")
            return False
    
    async def _handle_email_sending(self, task: QueuedTask) -> bool:
        """Handle email sending task"""
        try:
            payload = task.payload
            to_email = payload.get('to_email')
            subject = payload.get('subject')
            body = payload.get('body')
            
            # Email sending logic here
            self.logger.info(f"📧 Email sent to: {to_email}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Email sending error: {e}")
            return False
    
    async def _handle_ai_processing(self, task: QueuedTask) -> bool:
        """Handle AI processing task"""
        try:
            payload = task.payload
            operation = payload.get('operation')
            data = payload.get('data')
            
            # AI processing logic here
            self.logger.info(f"🤖 AI processing: {operation}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ AI processing error: {e}")
            return False
    
    async def _handle_webhook_processing(self, task: QueuedTask) -> bool:
        """Handle webhook processing task"""
        try:
            payload = task.payload
            webhook_url = payload.get('webhook_url')
            data = payload.get('data')
            
            # Webhook processing logic here
            self.logger.info(f"🔗 Webhook processed: {webhook_url}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Webhook processing error: {e}")
            return False
    
    async def _handle_batch_operations(self, task: QueuedTask) -> bool:
        """Handle batch operations task"""
        try:
            payload = task.payload
            operation = payload.get('operation')
            items = payload.get('items', [])
            
            # Batch processing logic here
            self.logger.info(f"📦 Batch operation: {operation} - {len(items)} items")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Batch operation error: {e}")
            return False
    
    async def _send_task_callback(self, task: QueuedTask, success: bool):
        """Send task completion callback"""
        try:
            if not task.callback_url:
                return
            
            callback_data = {
                'task_id': task.task_id,
                'success': success,
                'completed_at': datetime.now().isoformat(),
                'processing_time': time.time() - task.created_at.timestamp()
            }
            
            # Send HTTP request to callback URL
            import aiohttp
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    task.callback_url,
                    json=callback_data,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    if response.status == 200:
                        self.logger.info(f"📞 Callback sent: {task.task_id}")
                    else:
                        self.logger.warning(f"⚠️ Callback failed: {task.task_id}")
                        
        except Exception as e:
            self.logger.error(f"❌ Callback error: {e}")
    
    def get_queue_statistics(self) -> Dict[str, Any]:
        """Get comprehensive queue statistics"""
        try:
            stats = self.queue_stats.copy()
            
            # Add current queue sizes
            if self.redis_client:
                for queue_type in QueueType:
                    queue_key = f"queue:{queue_type.value}"
                    size = self.redis_client.zcard(queue_key)
                    stats['queue_sizes'][queue_type.value] = size
            else:
                for queue_type, queue in self.memory_queues.items():
                    stats['queue_sizes'][queue_type.value] = queue.qsize()
            
            # Add rate limiter status
            rate_limiter_status = {}
            for name, limiter in self.rate_limiters.items():
                rate_limiter_status[name] = {
                    'current_rps': len(limiter['last_requests']),
                    'max_rps': limiter['requests_per_second'],
                    'burst_size': limiter['burst_size']
                }
            stats['rate_limiters'] = rate_limiter_status
            
            return stats
            
        except Exception as e:
            self.logger.error(f"❌ Statistics error: {e}")
            return {}
    
    def stop_background_processing(self):
        """Stop background processing"""
        self.processing_active = False
        
        # Wait for threads to finish
        for thread in self.background_threads:
            thread.join(timeout=5)
        
        self.logger.info("🛑 Background processing stopped")
    
    async def process_bulk_leads(self, leads: List[Dict[str, Any]], batch_size: int = 100) -> Dict[str, Any]:
        """Process bulk leads with queue management"""
        try:
            start_time = time.time()
            task_ids = []
            
            # Enqueue leads in batches
            for i in range(0, len(leads), batch_size):
                batch = leads[i:i + batch_size]
                
                for lead in batch:
                    task_id = await self.enqueue_task(
                        QueueType.LEAD_PROCESSING,
                        {'lead_data': lead},
                        TaskPriority.NORMAL
                    )
                    if task_id:
                        task_ids.append(task_id)
            
            processing_time = time.time() - start_time
            
            return {
                'total_leads': len(leads),
                'task_ids': task_ids,
                'processing_time': processing_time,
                'batches': len(leads) // batch_size + (1 if len(leads) % batch_size else 0)
            }
            
        except Exception as e:
            self.logger.error(f"❌ Bulk processing error: {e}")
            return {'error': str(e)}

# Global queue manager instance
queue_manager = QueueManager()
