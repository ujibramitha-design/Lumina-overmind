"""
LUMINA OS - WEBSOCKET HANDLER
=============================

Real-time WebSocket server for runner status updates
and system monitoring without polling.
"""

import asyncio
import json
import logging
from typing import Dict, Any, Set
from datetime import datetime
import socketio
from fastapi import FastAPI
from dashboard.api.utils.process_manager import runner_manager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create Socket.IO server
sio = socketio.AsyncServer(
    cors_allowed_origins="*",
    async_mode='asgi',
    logger=True,
    engineio_logger=True
)

class WebSocketManager:
    """Manager for WebSocket connections and real-time updates"""
    
    def __init__(self):
        self.connected_clients: Set[str] = set()
        self.runner_status_cache: Dict[str, Any] = {}
        self.system_status_cache: Dict[str, Any] = {}
        self.broadcast_task: asyncio.Task | None = None
        
    async def start_broadcasting(self):
        """Start background task for broadcasting updates"""
        if self.broadcast_task is None or self.broadcast_task.done():
            self.broadcast_task = asyncio.create_task(self._broadcast_loop())
            logger.info("📡 Started WebSocket broadcasting loop")
    
    async def stop_broadcasting(self):
        """Stop background broadcasting task"""
        if self.broadcast_task and not self.broadcast_task.done():
            self.broadcast_task.cancel()
            try:
                await self.broadcast_task
            except asyncio.CancelledError:
                pass
            logger.info("📡 Stopped WebSocket broadcasting loop")
    
    async def _broadcast_loop(self):
        """Background loop for broadcasting periodic updates"""
        while True:
            try:
                # Get current runner status
                runner_status = runner_manager.get_status()
                
                # Check if status changed
                if self.runner_status_cache != runner_status:
                    self.runner_status_cache = runner_status.copy()
                    await sio.emit('runners_status', {
                        'data': runner_status,
                        'timestamp': datetime.now().isoformat()
                    })
                    logger.debug(f"📊 Broadcasted runners status to {len(self.connected_clients)} clients")
                
                # Broadcast every 10 seconds (much less frequent than polling)
                await asyncio.sleep(10)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Error in broadcast loop: {e}")
                await asyncio.sleep(5)
    
    async def send_runner_update(self, runner_id: str, status: Dict[str, Any]):
        """Send immediate update for specific runner"""
        await sio.emit('runner_update', {
            'runner_id': runner_id,
            'timestamp': datetime.now().isoformat(),
            **status
        })
        logger.info(f"🔄 Sent immediate update for runner {runner_id}")
    
    async def send_system_status(self, status: Dict[str, Any]):
        """Send system status update"""
        self.system_status_cache = status.copy()
        await sio.emit('system_status', {
            'system_status': status,
            'timestamp': datetime.now().isoformat()
        })
        logger.info(f"🖥️ Sent system status update")

# Global WebSocket manager
ws_manager = WebSocketManager()

@sio.event
async def connect(sid, environ):
    """Handle client connection"""
    ws_manager.connected_clients.add(sid)
    logger.info(f"🔌 Client connected: {sid}. Total clients: {len(ws_manager.connected_clients)}")
    
    # Send initial data
    try:
        runner_status = runner_manager.get_status()
        await sio.emit('runners_status', {
            'data': runner_status,
            'timestamp': datetime.now().isoformat()
        }, room=sid)
        
        # Send system status if available
        if ws_manager.system_status_cache:
            await sio.emit('system_status', {
                'system_status': ws_manager.system_status_cache,
                'timestamp': datetime.now().isoformat()
            }, room=sid)
            
    except Exception as e:
        logger.error(f"❌ Error sending initial data to {sid}: {e}")
    
    # Start broadcasting if this is the first client
    if len(ws_manager.connected_clients) == 1:
        await ws_manager.start_broadcasting()

@sio.event
async def disconnect(sid):
    """Handle client disconnection"""
    ws_manager.connected_clients.discard(sid)
    logger.info(f"🔌 Client disconnected: {sid}. Total clients: {len(ws_manager.connected_clients)}")
    
    # Stop broadcasting if no clients connected
    if len(ws_manager.connected_clients) == 0:
        await ws_manager.stop_broadcasting()

@sio.event
async def get_runners_status(sid):
    """Handle request for runners status"""
    try:
        runner_status = runner_manager.get_status()
        await sio.emit('runners_status', {
            'data': runner_status,
            'timestamp': datetime.now().isoformat()
        }, room=sid)
    except Exception as e:
        logger.error(f"❌ Error getting runners status for {sid}: {e}")
        await sio.emit('error', {
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        }, room=sid)

@sio.event
async def get_system_status(sid):
    """Handle request for system status"""
    try:
        if ws_manager.system_status_cache:
            await sio.emit('system_status', {
                'system_status': ws_manager.system_status_cache,
                'timestamp': datetime.now().isoformat()
            }, room=sid)
        else:
            await sio.emit('error', {
                'message': 'System status not available',
                'timestamp': datetime.now().isoformat()
            }, room=sid)
    except Exception as e:
        logger.error(f"❌ Error getting system status for {sid}: {e}")
        await sio.emit('error', {
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        }, room=sid)

@sio.event
async def toggle_runner(sid, data):
    """Handle runner toggle request"""
    try:
        runner_id = data.get('runner_id')
        action = data.get('action')  # 'start' or 'stop'
        
        if not runner_id or not action:
            await sio.emit('error', {
                'message': 'Missing runner_id or action',
                'timestamp': datetime.now().isoformat()
            }, room=sid)
            return
        
        if action == 'start':
            result = runner_manager.start_runner(runner_id)
        elif action == 'stop':
            result = runner_manager.stop_runner(runner_id)
        else:
            await sio.emit('error', {
                'message': 'Invalid action. Must be "start" or "stop"',
                'timestamp': datetime.now().isoformat()
            }, room=sid)
            return
        
        # Send immediate update
        await ws_manager.send_runner_update(runner_id, {
            'action': action,
            'result': result
        })
        
        # Broadcast updated status
        runner_status = runner_manager.get_status()
        await sio.emit('runners_status', {
            'data': runner_status,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"❌ Error toggling runner {data.get('runner_id')}: {e}")
        await sio.emit('error', {
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        }, room=sid)

def create_socketio_app() -> socketio.ASGIApp:
    """Create Socket.IO ASGI app"""
    return socketio.ASGIApp(sio)

async def update_system_status(status: Dict[str, Any]):
    """Update system status and broadcast to clients"""
    await ws_manager.send_system_status(status)
