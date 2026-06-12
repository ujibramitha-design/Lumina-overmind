"""
J.A.R.V.I.S. AI System - Super Admin Voice Assistant API
=========================================================

Advanced AI system endpoints for dashboard integration,
voice commands, and system control capabilities.
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging
import asyncio
import json

# Import J.A.R.V.I.S. brain
from api.utils.conversational_ai import get_smart_reply, get_ai_status, omni_bot

router = APIRouter(prefix="/api/jarvis", tags=["jarvis"])

# Configure logging
logger = logging.getLogger(__name__)

# Pydantic models
class ChatRequest(BaseModel):
    message: str
    platform: str = "dashboard"
    project_type: Optional[str] = None
    user_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    timestamp: str
    platform: str
    jarvis_status: Dict[str, Any]
    execution_time: float

class VoiceCommandRequest(BaseModel):
    audio_data: Optional[str] = None  # Base64 encoded audio
    transcript: Optional[str] = None  # Pre-transcribed text
    language: str = "id-ID"
    user_id: Optional[str] = None

class SystemCommandRequest(BaseModel):
    command: str
    parameters: Optional[Dict[str, Any]] = {}
    user_id: Optional[str] = None

class JarvisStatusResponse(BaseModel):
    status: str
    provider: str
    capabilities: List[str]
    is_active: bool
    last_activity: str
    system_health: Dict[str, Any]
    timestamp: str

# Global J.A.R.V.I.S. state
jarvis_state = {
    "is_active": True,
    "last_activity": datetime.now().isoformat(),
    "total_commands": 0,
    "voice_commands": 0,
    "system_commands": 0,
    "chat_sessions": 0,
    "errors": 0
}

@router.post("/chat", response_model=ChatResponse)
async def jarvis_chat(request: ChatRequest):
    """
    J.A.R.V.I.S. chat endpoint for dashboard integration
    """
    try:
        start_time = datetime.now()
        
        # Check if J.A.R.V.I.S. is active
        if not jarvis_state["is_active"]:
            raise HTTPException(status_code=403, detail="J.A.R.V.I.S. is currently deactivated")
        
        # Get AI response
        response = get_smart_reply(
            request.message, 
            request.platform, 
            request.project_type
        )
        
        # Update state
        jarvis_state["last_activity"] = datetime.now().isoformat()
        jarvis_state["chat_sessions"] += 1
        jarvis_state["total_commands"] += 1
        
        # Calculate execution time
        execution_time = (datetime.now() - start_time).total_seconds()
        
        # Get J.A.R.V.I.S. status
        jarvis_status = get_ai_status()
        
        logger.info(f"✅ J.A.R.V.I.S. Chat: {request.message[:50]}...")
        
        return ChatResponse(
            response=response,
            timestamp=datetime.now().isoformat(),
            platform=request.platform,
            jarvis_status=jarvis_status,
            execution_time=execution_time
        )
        
    except Exception as e:
        jarvis_state["errors"] += 1
        logger.error(f"❌ J.A.R.V.I.S. Chat Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/voice-command", response_model=ChatResponse)
async def jarvis_voice_command(request: VoiceCommandRequest):
    """
    Process voice commands for J.A.R.V.I.S.
    """
    try:
        start_time = datetime.now()
        
        # Check if J.A.R.V.I.S. is active
        if not jarvis_state["is_active"]:
            raise HTTPException(status_code=403, detail="J.A.R.V.I.S. is currently deactivated")
        
        # Process voice command
        if request.transcript:
            transcript = request.transcript
        elif request.audio_data:
            # TODO: Implement speech-to-text processing
            transcript = "Voice processing not implemented yet"
        else:
            raise HTTPException(status_code=400, detail="No audio data or transcript provided")
        
        # Get J.A.R.V.I.S. response
        response = get_smart_reply(transcript, "voice", None)
        
        # Update state
        jarvis_state["last_activity"] = datetime.now().isoformat()
        jarvis_state["voice_commands"] += 1
        jarvis_state["total_commands"] += 1
        
        # Calculate execution time
        execution_time = (datetime.now() - start_time).total_seconds()
        
        # Get J.A.R.V.I.S. status
        jarvis_status = get_ai_status()
        
        logger.info(f"🎤 J.A.R.V.I.S. Voice: {transcript[:50]}...")
        
        return ChatResponse(
            response=response,
            timestamp=datetime.now().isoformat(),
            platform="voice",
            jarvis_status=jarvis_status,
            execution_time=execution_time
        )
        
    except Exception as e:
        jarvis_state["errors"] += 1
        logger.error(f"❌ J.A.R.V.I.S. Voice Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/system-command", response_model=Dict[str, Any])
async def jarvis_system_command(request: SystemCommandRequest):
    """
    Execute system commands via J.A.R.V.I.S.
    """
    try:
        start_time = datetime.now()
        
        # Check if J.A.R.V.I.S. is active
        if not jarvis_state["is_active"]:
            raise HTTPException(status_code=403, detail="J.A.R.V.I.S. is currently deactivated")
        
        # Execute system command
        result = await _execute_system_command(request.command, request.parameters)
        
        # Update state
        jarvis_state["last_activity"] = datetime.now().isoformat()
        jarvis_state["system_commands"] += 1
        jarvis_state["total_commands"] += 1
        
        # Calculate execution time
        execution_time = (datetime.now() - start_time).total_seconds()
        
        logger.info(f"⚙️ J.A.R.V.I.S. System Command: {request.command}")
        
        return {
            "status": "success",
            "command": request.command,
            "result": result,
            "execution_time": execution_time,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        jarvis_state["errors"] += 1
        logger.error(f"❌ J.A.R.V.I.S. System Command Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status", response_model=JarvisStatusResponse)
async def jarvis_status():
    """
    Get current J.A.R.V.I.S. system status
    """
    try:
        # Get AI status
        ai_status = get_ai_status()
        
        # System health check
        system_health = {
            "database_status": "online",  # TODO: Implement actual health check
            "api_status": "online",
            "memory_usage": "normal",
            "cpu_usage": "normal",
            "last_error": None
        }
        
        return JarvisStatusResponse(
            status="active" if jarvis_state["is_active"] else "inactive",
            provider=ai_status["provider"],
            capabilities=ai_status["capabilities"],
            is_active=jarvis_state["is_active"],
            last_activity=jarvis_state["last_activity"],
            system_health=system_health,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"❌ J.A.R.V.I.S. Status Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/toggle")
async def toggle_jarvis():
    """
    Toggle J.A.R.V.I.S. activation status
    """
    try:
        # Toggle state
        jarvis_state["is_active"] = not jarvis_state["is_active"]
        jarvis_state["last_activity"] = datetime.now().isoformat()
        
        status_text = "activated" if jarvis_state["is_active"] else "deactivated"
        
        logger.info(f"🔄 J.A.R.V.I.S. {status_text}")
        
        return {
            "status": "success",
            "is_active": jarvis_state["is_active"],
            "message": f"J.A.R.V.I.S. has been {status_text}",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ J.A.R.V.I.S. Toggle Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analytics")
async def jarvis_analytics():
    """
    Get J.A.R.V.I.S. usage analytics
    """
    try:
        return {
            "usage_stats": jarvis_state,
            "performance_metrics": {
                "avg_response_time": 0.5,  # TODO: Calculate actual metrics
                "success_rate": 98.5,
                "error_rate": 1.5
            },
            "popular_commands": [
                {"command": "get_system_stats", "usage": 45},
                {"command": "trigger_hunter_agent", "usage": 32},
                {"command": "get_market_intelligence", "usage": 28}
            ],
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ J.A.R.V.I.S. Analytics Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/commands")
async def get_available_commands():
    """
    Get list of available J.A.R.V.I.S. commands
    """
    try:
        return {
            "voice_commands": [
                "Jarvis, berikan saya statistik sistem",
                "Jarvis, deploy hunter agent ke Serang",
                "Jarvis, berikan intelijen pasar",
                "Jarvis, buat presentasi untuk [nama]",
                "Jarvis, render interior dapur modern",
                "Jarvis, generate dokumen legal untuk [nama]"
            ],
            "system_commands": [
                "get_system_stats",
                "trigger_hunter_agent",
                "get_market_intelligence",
                "create_personalized_presentation",
                "render_interior_visual",
                "generate_legal_document",
                "analyze_vvip_prospect"
            ],
            "chat_capabilities": [
                "Natural conversation",
                "System queries",
                "Market analysis",
                "Lead management",
                "Document generation",
                "Visual content creation"
            ],
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ J.A.R.V.I.S. Commands Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Helper functions
async def _execute_system_command(command: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute system command via J.A.R.V.I.S.
    """
    try:
        # Map commands to J.A.R.V.I.S. tools
        command_map = {
            "get_system_stats": lambda: omni_bot.tools.get_system_stats(),
            "trigger_hunter_agent": lambda: omni_bot.tools.trigger_hunter_agent(
                parameters.get("location", "Serang"), 
                parameters.get("project_type")
            ),
            "get_market_intelligence": lambda: omni_bot.tools.get_market_intelligence(),
            "create_personalized_presentation": lambda: omni_bot.create_personalized_presentation(
                parameters.get("name"),
                parameters.get("budget"),
                parameters.get("location")
            ),
            "render_interior_visual": lambda: omni_bot.render_interior_visual(
                parameters.get("prompt"),
                parameters.get("style", "modern"),
                parameters.get("room_type", "living_room")
            ),
            "generate_legal_document": lambda: omni_bot.generate_legal_document(
                parameters.get("document_type", "SPR"),
                parameters.get("customer_name"),
                parameters.get("unit_info", {})
            ),
            "analyze_vvip_prospect": lambda: omni_bot.analyze_vvip_prospect(
                parameters.get("prospect_data", {})
            )
        }
        
        if command in command_map:
            result = command_map[command]()
            return {
                "status": "success",
                "result": result,
                "command": command
            }
        else:
            return {
                "status": "error",
                "message": f"Unknown command: {command}",
                "available_commands": list(command_map.keys())
            }
            
    except Exception as e:
        logger.error(f"❌ System Command Execution Error: {e}")
        return {
            "status": "error",
            "message": str(e),
            "command": command
        }
