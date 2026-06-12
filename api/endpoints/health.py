"""
LUMINA OVERMIND SYSTEM - Health Check Endpoints
==============================================

Comprehensive health monitoring for system components
"""

import asyncio
import time
import psutil
from datetime import datetime
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("/")
async def health_check() -> Dict[str, Any]:
    """
    Basic health check endpoint
    
    Returns:
        Dict with basic system health status
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "LUMINA OVERMIND API",
        "version": "2.0.0"
    }

@router.get("/detailed")
async def detailed_health_check() -> Dict[str, Any]:
    """
    Detailed health check with component status
    
    Returns:
        Dict with detailed health information for all components
    """
    start_time = time.time()
    
    # Check system resources
    system_health = await check_system_resources()
    
    # Check database connection
    database_health = await check_database_health()
    
    # Check Redis connection
    redis_health = await check_redis_health()
    
    # Check Celery workers
    celery_health = await check_celery_health()
    
    # Calculate overall status
    overall_status = "healthy"
    if any([
        system_health["status"] != "healthy",
        database_health["status"] != "healthy", 
        redis_health["status"] != "healthy",
        celery_health["status"] != "healthy"
    ]):
        overall_status = "unhealthy"
    
    response_time = time.time() - start_time
    
    return {
        "status": overall_status,
        "timestamp": datetime.utcnow().isoformat(),
        "service": "LUMINA OVERMIND API",
        "version": "2.0.0",
        "response_time_ms": round(response_time * 1000, 2),
        "components": {
            "system": system_health,
            "database": database_health,
            "redis": redis_health,
            "celery": celery_health
        }
    }

@router.get("/system")
async def system_health() -> Dict[str, Any]:
    """
    System resource health check
    
    Returns:
        Dict with system resource usage
    """
    return await check_system_resources()

@router.get("/database")
async def database_health() -> Dict[str, Any]:
    """
    Database health check
    
    Returns:
        Dict with database connection status
    """
    return await check_database_health()

@router.get("/redis")
async def redis_health() -> Dict[str, Any]:
    """
    Redis health check
    
    Returns:
        Dict with Redis connection status
    """
    return await check_redis_health()

@router.get("/celery")
async def celery_health() -> Dict[str, Any]:
    """
    Celery workers health check
    
    Returns:
        Dict with Celery worker status
    """
    return await check_celery_health()

async def check_system_resources() -> Dict[str, Any]:
    """Check system resource usage"""
    try:
        # CPU metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        
        # Memory metrics
        memory = psutil.virtual_memory()
        
        # Disk metrics
        disk = psutil.disk_usage('/')
        
        # Network metrics
        network = psutil.net_io_counters()
        
        # Determine health based on thresholds
        status = "healthy"
        warnings = []
        
        if cpu_percent > 80:
            status = "degraded"
            warnings.append("High CPU usage")
        
        if memory.percent > 85:
            status = "degraded"
            warnings.append("High memory usage")
        
        if disk.percent > 90:
            status = "degraded"
            warnings.append("Low disk space")
        
        return {
            "status": status,
            "cpu": {
                "percent": cpu_percent,
                "count": cpu_count
            },
            "memory": {
                "total": memory.total,
                "available": memory.available,
                "percent": memory.percent,
                "used": memory.used
            },
            "disk": {
                "total": disk.total,
                "used": disk.used,
                "free": disk.free,
                "percent": disk.percent
            },
            "network": {
                "bytes_sent": network.bytes_sent,
                "bytes_recv": network.bytes_recv,
                "packets_sent": network.packets_sent,
                "packets_recv": network.packets_recv
            },
            "warnings": warnings
        }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }

async def check_database_health() -> Dict[str, Any]:
    """Check database connection and performance"""
    try:
        from prisma import Client
        from prisma.errors import PrismaError
        
        client = Client()
        
        # Test connection
        start_time = time.time()
        await client.connect()
        connection_time = time.time() - start_time
        
        # Test query performance
        start_time = time.time()
        user_count = await client.user.count()
        query_time = time.time() - start_time
        
        await client.disconnect()
        
        # Determine health based on response times
        status = "healthy"
        warnings = []
        
        if connection_time > 5.0:
            status = "degraded"
            warnings.append("Slow database connection")
        
        if query_time > 2.0:
            status = "degraded"
            warnings.append("Slow query performance")
        
        return {
            "status": status,
            "connection_time_ms": round(connection_time * 1000, 2),
            "query_time_ms": round(query_time * 1000, 2),
            "user_count": user_count,
            "warnings": warnings
        }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }

async def check_redis_health() -> Dict[str, Any]:
    """Check Redis connection and performance"""
    try:
        import redis
        from redis.exceptions import RedisError
        
        # Connect to Redis
        r = redis.Redis(
            host='localhost',
            port=6379,
            password='redis_secure_password_2024',
            decode_responses=True
        )
        
        # Test connection
        start_time = time.time()
        r.ping()
        ping_time = time.time() - start_time
        
        # Get Redis info
        info = r.info()
        
        # Test basic operations
        start_time = time.time()
        test_key = "health_check_test"
        r.set(test_key, "test_value")
        r.get(test_key)
        r.delete(test_key)
        operation_time = time.time() - start_time
        
        # Determine health based on metrics
        status = "healthy"
        warnings = []
        
        if ping_time > 1.0:
            status = "degraded"
            warnings.append("Slow Redis ping")
        
        if operation_time > 0.1:
            status = "degraded"
            warnings.append("Slow Redis operations")
        
        memory_usage = info.get('used_memory_human', 'N/A')
        connected_clients = info.get('connected_clients', 0)
        
        return {
            "status": status,
            "ping_time_ms": round(ping_time * 1000, 2),
            "operation_time_ms": round(operation_time * 1000, 2),
            "memory_usage": memory_usage,
            "connected_clients": connected_clients,
            "warnings": warnings
        }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }

async def check_celery_health() -> Dict[str, Any]:
    """Check Celery workers and queue status"""
    try:
        from tasks.celery_app import celery_app
        
        # Get active workers
        inspect = celery_app.control.inspect()
        stats = inspect.stats()
        
        # Get active tasks
        active_tasks = inspect.active()
        scheduled_tasks = inspect.scheduled()
        
        # Calculate metrics
        total_workers = len(stats) if stats else 0
        total_active_tasks = sum(len(tasks) for tasks in (active_tasks or {}).values())
        total_scheduled_tasks = sum(len(tasks) for tasks in (scheduled_tasks or {}).values())
        
        # Determine health
        status = "healthy"
        warnings = []
        
        if total_workers == 0:
            status = "unhealthy"
            warnings.append("No active workers")
        elif total_workers < 2:
            status = "degraded"
            warnings.append("Insufficient workers")
        
        return {
            "status": status,
            "total_workers": total_workers,
            "active_tasks": total_active_tasks,
            "scheduled_tasks": total_scheduled_tasks,
            "worker_stats": stats,
            "warnings": warnings
        }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }

# Docker-specific health check
@router.get("/docker")
async def docker_health_check() -> JSONResponse:
    """
    Simplified health check for Docker health checks
    
    Returns:
        JSONResponse with HTTP status code based on health
    """
    try:
        # Quick checks for Docker health
        system_ok = (await check_system_resources()).get("status") == "healthy"
        
        if system_ok:
            return JSONResponse(
                content={"status": "healthy"},
                status_code=200
            )
        else:
            return JSONResponse(
                content={"status": "unhealthy"},
                status_code=503
            )
            
    except Exception:
        return JSONResponse(
            content={"status": "unhealthy"},
            status_code=503
        )
