"""
J.A.R.V.I.S. AI System - Super Admin Voice Assistant API
=========================================================

Advanced AI system endpoints for dashboard integration,
voice commands, and system control capabilities.
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import logging
import asyncio
import json
import base64
import os
import tempfile

# Import J.A.R.V.I.S. brain
from api.utils.conversational_ai import get_smart_reply, get_ai_status, omni_bot
# Import JWT authentication
from api.middleware.jwt_auth import get_current_user, get_admin_user

# Redis caching
try:
    import redis
    REDIS_AVAILABLE = True
    redis_client = None
except ImportError:
    REDIS_AVAILABLE = False
    redis_client = None

router = APIRouter(prefix="/api/jarvis", tags=["jarvis"])

# Configure logging
logger = logging.getLogger(__name__)

# Initialize Redis client
def get_redis_client():
    """Get or create Redis client"""
    global redis_client
    if not REDIS_AVAILABLE:
        return None
    
    if redis_client is None:
        try:
            redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
            redis_client = redis.from_url(redis_url, decode_responses=True)
            logger.info("✅ Redis client initialized")
        except Exception as e:
            logger.error(f"❌ Redis connection failed: {e}")
            redis_client = None
    
    return redis_client

def cache_get(key: str) -> Optional[str]:
    """Get value from cache"""
    if not REDIS_AVAILABLE:
        return None
    
    try:
        client = get_redis_client()
        if client:
            return client.get(key)
    except Exception as e:
        logger.warning(f"⚠️ Redis get error: {e}")
    
    return None

def cache_set(key: str, value: str, ttl: int = 300):
    """Set value in cache with TTL"""
    if not REDIS_AVAILABLE:
        return
    
    try:
        client = get_redis_client()
        if client:
            client.setex(key, ttl, value)
    except Exception as e:
        logger.warning(f"⚠️ Redis set error: {e}")

def cache_delete(key: str):
    """Delete value from cache"""
    if not REDIS_AVAILABLE:
        return
    
    try:
        client = get_redis_client()
        if client:
            client.delete(key)
    except Exception as e:
        logger.warning(f"⚠️ Redis delete error: {e}")

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

# Command history for analytics
command_history = []

# Command whitelist for security
ALLOWED_SYSTEM_COMMANDS = [
    "get_system_stats",
    "analyze_specific_lead",
    "trigger_hunter_agent",
    "get_market_intelligence",
    "create_personalized_presentation",
    "render_interior_visual",
    "generate_legal_document",
    "analyze_vvip_prospect"
]

# Command blacklist for security
BLOCKED_COMMANDS = [
    "rm",
    "delete",
    "drop",
    "truncate",
    "format",
    "shutdown",
    "reboot",
    "sudo",
    "su",
    "chmod",
    "chown",
    "eval",
    "exec",
    "system",
    "shell"
]

def validate_command(command: str) -> tuple[bool, str]:
    """
    Validate system command for security
    
    Args:
        command: Command to validate
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check if command is in whitelist
    if command not in ALLOWED_SYSTEM_COMMANDS:
        return False, f"Command '{command}' is not in the allowed commands list"
    
    # Check if command contains blocked keywords
    command_lower = command.lower()
    for blocked in BLOCKED_COMMANDS:
        if blocked in command_lower:
            return False, f"Command contains blocked keyword: {blocked}"
    
    return True, ""

async def _check_system_health() -> Dict[str, Any]:
    """
    Check system health including database, API, and resources
    
    Returns:
        Dictionary with health status for each component
    """
    import psutil
    from pathlib import Path
    
    health_status = {
        "database_status": "unknown",
        "api_status": "online",
        "memory_usage": "normal",
        "cpu_usage": "normal",
        "last_error": None
    }
    
    try:
        # Check database health
        db_path = Path(__file__).parent.parent.parent / "data" / "leads.db"
        if db_path.exists():
            try:
                # Try to check if database is accessible
                import sqlite3
                conn = sqlite3.connect(str(db_path), timeout=2)
                conn.execute("SELECT 1")
                conn.close()
                health_status["database_status"] = "online"
            except Exception as e:
                health_status["database_status"] = "offline"
                health_status["last_error"] = f"Database error: {str(e)}"
        else:
            health_status["database_status"] = "not_found"
        
        # Check memory usage
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        if memory_percent > 80:
            health_status["memory_usage"] = "high"
        elif memory_percent > 60:
            health_status["memory_usage"] = "moderate"
        else:
            health_status["memory_usage"] = "normal"
        
        # Check CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        if cpu_percent > 80:
            health_status["cpu_usage"] = "high"
        elif cpu_percent > 60:
            health_status["cpu_usage"] = "moderate"
        else:
            health_status["cpu_usage"] = "normal"
        
        logger.info(f"✅ System health check completed: DB={health_status['database_status']}, MEM={health_status['memory_usage']}, CPU={health_status['cpu_usage']}")
        
    except ImportError:
        logger.warning("⚠️ psutil not available, using basic health check")
        # Fallback to basic checks without psutil
        if db_path.exists():
            health_status["database_status"] = "online"
        else:
            health_status["database_status"] = "not_found"
    except Exception as e:
        logger.error(f"❌ System health check error: {e}")
        health_status["last_error"] = str(e)
    
    return health_status

# Speech-to-Text helper function
async def transcribe_audio(audio_data: str, language: str = "id-ID") -> str:
    """
    Transcribe audio data using speech-to-text
    
    Args:
        audio_data: Base64 encoded audio data
        language: Language code (default: id-ID for Indonesian)
    
    Returns:
        Transcribed text
    """
    try:
        # Decode base64 audio data
        audio_bytes = base64.b64decode(audio_data)
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            temp_file.write(audio_bytes)
            temp_file_path = temp_file.name
        
        try:
            # Try using SpeechRecognition library
            import speech_recognition as sr
            
            recognizer = sr.Recognizer()
            with sr.AudioFile(temp_file_path) as source:
                audio = recognizer.record(source)
                
                # Try Google Speech Recognition (free tier)
                try:
                    transcript = recognizer.recognize_google(audio, language=language)
                    logger.info(f"✅ Speech-to-text successful: {transcript[:50]}...")
                    return transcript
                except sr.UnknownValueError:
                    logger.warning("⚠️ Speech recognition could not understand audio")
                    return "Speech recognition could not understand audio"
                except sr.RequestError as e:
                    logger.warning(f"⚠️ Speech recognition service error: {e}")
                    # Fallback to OpenAI Whisper if available
                    return await _transcribe_with_whisper(temp_file_path, language)
                    
        except ImportError:
            logger.warning("⚠️ SpeechRecognition library not available, trying Whisper")
            # Fallback to OpenAI Whisper
            return await _transcribe_with_whisper(temp_file_path, language)
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
                
    except Exception as e:
        logger.error(f"❌ Speech-to-text error: {e}")
        return f"Speech-to-text error: {str(e)}"

async def _transcribe_with_whisper(audio_file_path: str, language: str = "id-ID") -> str:
    """
    Transcribe audio using OpenAI Whisper API
    
    Args:
        audio_file_path: Path to audio file
        language: Language code
    
    Returns:
        Transcribed text
    """
    try:
        import openai
        
        # Check if OpenAI API key is available
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            logger.warning("⚠️ OpenAI API key not available")
            return "Speech-to-text service not available"
        
        # OpenAI client
        client = openai.OpenAI(api_key=openai_api_key)
        
        # Transcribe using Whisper
        with open(audio_file_path, "rb") as audio_file:
            response = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language=language.split("-")[0]  # Extract language code (e.g., "id" from "id-ID")
            )
        
        transcript = response.text
        logger.info(f"✅ Whisper transcription successful: {transcript[:50]}...")
        return transcript
        
    except ImportError:
        logger.warning("⚠️ OpenAI library not available")
        return "Speech-to-text service not available"
    except Exception as e:
        logger.error(f"❌ Whisper transcription error: {e}")
        return f"Whisper transcription error: {str(e)}"

@router.post("/chat", response_model=ChatResponse)
async def jarvis_chat(request: ChatRequest, current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    J.A.R.V.I.S. chat endpoint for dashboard integration
    Requires authentication
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
        
        # Calculate execution time
        execution_time = (datetime.now() - start_time).total_seconds()
        
        # Update state
        jarvis_state["last_activity"] = datetime.now().isoformat()
        jarvis_state["chat_sessions"] += 1
        jarvis_state["total_commands"] += 1
        
        # Add to command history
        command_history.append({
            "type": "chat",
            "message": request.message,
            "platform": request.platform,
            "timestamp": datetime.now().isoformat(),
            "execution_time": execution_time,
            "success": True
        })
        
        # Keep only last 1000 commands
        if len(command_history) > 1000:
            command_history.pop(0)
        
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
        
        # Add failed command to history
        command_history.append({
            "type": "chat",
            "message": request.message,
            "platform": request.platform,
            "timestamp": datetime.now().isoformat(),
            "execution_time": 0,
            "success": False,
            "error": str(e)
        })
        
        logger.error(f"❌ J.A.R.V.I.S. Chat Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/voice-command", response_model=ChatResponse)
async def jarvis_voice_command(request: VoiceCommandRequest, current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Process voice commands for J.A.R.V.I.S.
    Requires authentication
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
            # Use speech-to-text processing
            transcript = await transcribe_audio(request.audio_data, request.language)
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
async def jarvis_system_command(request: SystemCommandRequest, current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Execute system commands via J.A.R.V.I.S.
    Requires authentication
    """
    try:
        start_time = datetime.now()
        
        # Check if J.A.R.V.I.S. is active
        if not jarvis_state["is_active"]:
            raise HTTPException(status_code=403, detail="J.A.R.V.I.S. is currently deactivated")
        
        # Validate command for security
        is_valid, error_message = validate_command(request.command)
        if not is_valid:
            logger.warning(f"⚠️ Blocked command: {request.command} - {error_message}")
            raise HTTPException(status_code=403, detail=f"Command validation failed: {error_message}")
        
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
async def jarvis_status(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Get current J.A.R.V.I.S. system status
    Requires authentication
    """
    try:
        # Check cache first
        cache_key = "jarvis:status"
        cached_status = cache_get(cache_key)
        if cached_status:
            logger.debug("✅ Returning cached JARVIS status")
            return json.loads(cached_status)
        
        # Get AI status
        ai_status = get_ai_status()
        
        # System health check
        system_health = await _check_system_health()
        
        response = JarvisStatusResponse(
            status="active" if jarvis_state["is_active"] else "inactive",
            provider=ai_status["provider"],
            capabilities=ai_status["capabilities"],
            is_active=jarvis_state["is_active"],
            last_activity=jarvis_state["last_activity"],
            system_health=system_health,
            timestamp=datetime.now().isoformat()
        )
        
        # Cache the response for 15 seconds
        cache_set(cache_key, json.dumps(response.dict()), ttl=15)
        
        return response
        
    except Exception as e:
        logger.error(f"❌ J.A.R.V.I.S. Status Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/toggle")
async def toggle_jarvis(current_user: Dict[str, Any] = Depends(get_admin_user)):
    """
    Toggle J.A.R.V.I.S. activation status
    Requires admin access
    """
    try:
        # Toggle state
        jarvis_state["is_active"] = not jarvis_state["is_active"]
        jarvis_state["last_activity"] = datetime.now().isoformat()
        
        # Invalidate cache
        cache_delete("jarvis:status")
        
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
async def jarvis_analytics(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Get J.A.R.V.I.S. usage analytics
    Requires authentication
    """
    try:
        # Calculate actual metrics from command history
        if command_history:
            successful_commands = [c for c in command_history if c.get("success", False)]
            avg_response_time = sum(c.get("execution_time", 0) for c in successful_commands) / len(successful_commands) if successful_commands else 0
            success_rate = (len(successful_commands) / len(command_history)) * 100
            error_rate = 100 - success_rate
        else:
            avg_response_time = 0
            success_rate = 100
            error_rate = 0
        
        # Get popular commands
        command_counts = {}
        for cmd in command_history:
            cmd_type = cmd.get("type", "unknown")
            command_counts[cmd_type] = command_counts.get(cmd_type, 0) + 1
        
        popular_commands = sorted(
            [{"command": k, "usage": v} for k, v in command_counts.items()],
            key=lambda x: x["usage"],
            reverse=True
        )[:10]
        
        return {
            "usage_stats": jarvis_state,
            "performance_metrics": {
                "avg_response_time": round(avg_response_time, 3),
                "success_rate": round(success_rate, 2),
                "error_rate": round(error_rate, 2),
                "total_commands": len(command_history)
            },
            "popular_commands": popular_commands,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ J.A.R.V.I.S. Analytics Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/commands")
async def get_available_commands(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Get list of available J.A.R.V.I.S. commands
    Requires authentication
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
    Execute system command via J.A.R.V.I.S. with fallback behavior.
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
            try:
                result = command_map[command]()
                return {
                    "status": "success",
                    "result": result,
                    "command": command
                }
            except Exception as e:
                # Fallback response for command execution errors
                logger.warning(f"⚠️ Command {command} failed, using fallback: {e}")
                return {
                    "status": "fallback",
                    "message": f"Command '{command}' encountered an error. Using fallback response.",
                    "fallback_response": f"I couldn't execute {command} due to: {str(e)}. Please try again or check system status.",
                    "command": command
                }
        else:
            # Fallback for unknown commands
            logger.warning(f"⚠️ Unknown command: {command}")
            return {
                "status": "fallback",
                "message": f"Unknown command: {command}",
                "available_commands": list(command_map.keys()),
                "fallback_response": f"I don't recognize the command '{command}'. Available commands are: {', '.join(command_map.keys())}"
            }
            
    except Exception as e:
        logger.error(f"❌ System Command Execution Error: {e}")
        return {
            "status": "error",
            "message": str(e),
            "command": command,
            "fallback_response": "An unexpected error occurred. Please check system logs and try again."
        }
