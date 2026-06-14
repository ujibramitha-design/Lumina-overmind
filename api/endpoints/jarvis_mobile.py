"""
JARVIS Mobile API Bridge
========================

Backend API and WebSocket gateway for JARVIS Mobile Command Center
Provides secure endpoints for mobile app communication using Service Token auth
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging
import json
import os

# Import JARVIS service authentication
from api.middleware.jarvis_service_auth import verify_jarvis_token, JarvisServiceAuth

router = APIRouter(prefix="/api/jarvis-mobile", tags=["jarvis-mobile"])

# Configure logging
logger = logging.getLogger(__name__)

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"Mobile client connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info(f"Mobile client disconnected. Total connections: {len(self.active_connections)}")
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to client: {e}")
    
    async def send_personal(self, message: dict, websocket: WebSocket):
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error(f"Error sending personal message: {e}")

manager = ConnectionManager()

# Pydantic models
class MobileMessage(BaseModel):
    type: str
    data: Dict[str, Any]
    timestamp: Optional[str] = None

class SystemMetrics(BaseModel):
    cpu: float
    memory: float
    disk: float
    network: Dict[str, float]
    uptime: str
    active_users: int
    total_commands: int
    success_rate: float

class ConnectionStatus(BaseModel):
    whatsapp: Dict[str, Any]
    telegram: Dict[str, Any]
    websocket: Dict[str, Any]

class JarvisThought(BaseModel):
    status: str
    current_task: str
    confidence: float
    processing_time: str
    last_action: str

class CodeSearchRequest(BaseModel):
    query: str
    filters: Optional[List[str]] = None

class CodeSearchResult(BaseModel):
    id: str
    file: str
    type: str
    description: str
    relevance: float

class CodeExplanation(BaseModel):
    file: str
    summary: str
    key_functions: List[Dict[str, str]]
    dependencies: List[str]
    lines_of_code: int
    last_modified: str

# Health check endpoint
@router.get("/health")
async def health_check():
    """Health check endpoint for mobile app"""
    return JSONResponse({
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "jarvis-mobile-bridge",
        "connections": len(manager.active_connections)
    })

# System metrics endpoint
@router.get("/metrics")
async def get_system_metrics(jarvis = Depends(verify_jarvis_token)):
    """Get real-time system metrics"""
    # In production, this would fetch actual metrics from the system
    metrics = SystemMetrics(
        cpu=45.0,
        memory=62.0,
        disk=38.0,
        network={"upload": 125.0, "download": 340.0},
        uptime="15d 4h 32m",
        active_users=23,
        total_commands=1547,
        success_rate=98.5
    )
    return metrics

# Connection status endpoint
@router.get("/connections")
async def get_connection_status(jarvis = Depends(verify_jarvis_token)):
    """Get status of all communication channels"""
    # In production, this would fetch actual status from jarvis/channels
    status = ConnectionStatus(
        whatsapp={"connected": True, "last_seen": "2m ago"},
        telegram={"connected": True, "last_seen": "1m ago"},
        websocket={"connected": True, "latency": 45}
    )
    return status

# JARVIS thought process endpoint
@router.get("/thought-process")
async def get_jarvis_thought(jarvis = Depends(verify_jarvis_token)):
    """Get current JARVIS thought process"""
    # In production, this would fetch actual thought process from JARVIS agent
    thought = JarvisThought(
        status="active",
        current_task="Analyzing system performance metrics",
        confidence=0.92,
        processing_time="0.23s",
        last_action="Generated daily summary report"
    )
    return thought

# Code search endpoint
@router.post("/code/search")
async def search_code(request: CodeSearchRequest, jarvis = Depends(verify_jarvis_token)):
    """Search codebase using JARVIS awareness module"""
    # In production, this would use the codebase awareness module
    results = [
        CodeSearchResult(
            id="1",
            file="api/endpoints/jarvis.py",
            type="python",
            description="JARVIS API endpoints for voice commands and system control",
            relevance=0.95
        ),
        CodeSearchResult(
            id="2",
            file="dashboard/components/JarvisAssistant.tsx",
            type="typescript",
            description="React component for JARVIS chat interface with voice waveform",
            relevance=0.88
        )
    ]
    return {"results": results}

# Code explanation endpoint
@router.get("/code/explain/{file_path:path}")
async def explain_code(file_path: str, jarvis = Depends(verify_jarvis_token)):
    """Get explanation for a specific file"""
    # In production, this would use the codebase awareness module
    explanation = CodeExplanation(
        file=file_path,
        summary="This file contains the main API endpoints for the JARVIS AI system.",
        key_functions=[
            {
                "name": "process_voice_command",
                "description": "Processes incoming voice commands and routes them to the appropriate handler"
            }
        ],
        dependencies=["fastapi", "pydantic", "speech_recognition"],
        lines_of_code=754,
        last_modified="2024-01-15"
    )
    return explanation

# WebSocket endpoint for real-time communication
@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time bi-directional communication"""
    await manager.connect(websocket)
    
    try:
        # Send initial connection message
        await websocket.send_json({
            "type": "connected",
            "data": {
                "message": "Connected to JARVIS Mobile Bridge",
                "timestamp": datetime.utcnow().isoformat()
            }
        })
        
        # Listen for messages from mobile app
        while True:
            data = await websocket.receive_json()
            
            # Process message
            message_type = data.get("type")
            message_data = data.get("data", {})
            
            logger.info(f"Received message from mobile: {message_type}")
            
            # Handle different message types
            if message_type == "chat":
                # Route to JARVIS agent
                response = await handle_chat_message(message_data)
                await manager.send_personal(response, websocket)
            
            elif message_type == "metrics_request":
                # Send current metrics
                metrics = await get_system_metrics_for_ws()
                await manager.send_personal(metrics, websocket)
            
            elif message_type == "code_search":
                # Search codebase
                results = await search_code_for_ws(message_data)
                await manager.send_personal(results, websocket)
            
            elif message_type == "ping":
                # Respond to ping
                await manager.send_personal({
                    "type": "pong",
                    "data": {"timestamp": datetime.utcnow().isoformat()}
                }, websocket)
            
            else:
                logger.warning(f"Unknown message type: {message_type}")
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info("Mobile client disconnected")
    
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)

# Helper functions for WebSocket
async def handle_chat_message(data: Dict[str, Any]) -> Dict[str, Any]:
    """Handle chat message from mobile app"""
    # In production, this would route to JARVIS agent
    user_message = data.get("message", "")
    
    # Simulate JARVIS response
    response = {
        "type": "chat_response",
        "data": {
            "message": f"I understand your request: \"{user_message}\". Processing this command now...",
            "sender": "jarvis",
            "timestamp": datetime.utcnow().isoformat()
        }
    }
    
    return response

async def get_system_metrics_for_ws() -> Dict[str, Any]:
    """Get system metrics for WebSocket"""
    return {
        "type": "metrics",
        "data": {
            "cpu": 45.0,
            "memory": 62.0,
            "disk": 38.0,
            "network": {"upload": 125.0, "download": 340.0},
            "uptime": "15d 4h 32m",
            "timestamp": datetime.utcnow().isoformat()
        }
    }

async def search_code_for_ws(data: Dict[str, Any]) -> Dict[str, Any]:
    """Search codebase for WebSocket"""
    query = data.get("query", "")
    
    return {
        "type": "code_search_results",
        "data": {
            "query": query,
            "results": [
                {
                    "id": "1",
                    "file": "api/endpoints/jarvis.py",
                    "type": "python",
                    "description": "JARVIS API endpoints for voice commands and system control",
                    "relevance": 0.95
                }
            ]
        }
    }

# Broadcast endpoint for sending updates to all connected mobile clients
@router.post("/broadcast")
async def broadcast_update(message: MobileMessage, jarvis = Depends(verify_jarvis_token)):
    """Broadcast message to all connected mobile clients"""
    await manager.broadcast(message.dict())
    return {"status": "broadcasted", "connections": len(manager.active_connections)}
