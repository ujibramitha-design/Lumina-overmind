"""
J.A.R.V.I.S. API Tests
======================

Unit tests for J.A.R.V.I.S. AI system endpoints
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime
import json
from unittest.mock import Mock, patch, MagicMock

# Import the main app
from api.main import app

# Create test client
client = TestClient(app)

# Mock JWT token for testing
MOCK_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test"
MOCK_USER = {
    "sub": "test_user",
    "username": "testuser",
    "role": "USER",
    "type": "access"
}

MOCK_ADMIN_USER = {
    "sub": "admin_user",
    "username": "admin",
    "role": "ADMIN",
    "type": "access"
}


@pytest.fixture
def mock_jwt_auth():
    """Mock JWT authentication dependency"""
    with patch('api.middleware.jwt_auth.get_current_user') as mock:
        mock.return_value = MOCK_USER
        yield mock


@pytest.fixture
def mock_admin_auth():
    """Mock admin authentication dependency"""
    with patch('api.middleware.jwt_auth.get_admin_user') as mock:
        mock.return_value = MOCK_ADMIN_USER
        yield mock


@pytest.fixture
def mock_jarvis_brain():
    """Mock JARVIS brain functions"""
    with patch('api.endpoints.jarvis.get_smart_reply') as mock_reply, \
         patch('api.endpoints.jarvis.get_ai_status') as mock_status, \
         patch('api.endpoints.jarvis.omni_bot') as mock_bot:
        mock_reply.return_value = "Test response from JARVIS"
        mock_status.return_value = {
            "provider": "gemini",
            "capabilities": ["chat", "voice", "system"],
            "status": "active"
        }
        mock_bot.tools = Mock()
        yield mock_reply, mock_status, mock_bot


class TestJarvisChatEndpoint:
    """Test cases for /api/jarvis/chat endpoint"""
    
    def test_chat_success(self, mock_jwt_auth, mock_jarvis_brain):
        """Test successful chat request"""
        response = client.post(
            "/api/jarvis/chat",
            json={
                "message": "Hello JARVIS",
                "platform": "dashboard",
                "project_type": "KOMERSIL"
            },
            headers={"Authorization": f"Bearer {MOCK_TOKEN}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert "timestamp" in data
        assert "jarvis_status" in data
        assert "execution_time" in data
    
    def test_chat_without_auth(self):
        """Test chat request without authentication"""
        response = client.post(
            "/api/jarvis/chat",
            json={"message": "Hello JARVIS"}
        )
        
        assert response.status_code == 401
    
    def test_chat_jarvis_inactive(self, mock_jwt_auth):
        """Test chat when JARVIS is deactivated"""
        with patch('api.endpoints.jarvis.jarvis_state', {"is_active": False}):
            response = client.post(
                "/api/jarvis/chat",
                json={"message": "Hello JARVIS"},
                headers={"Authorization": f"Bearer {MOCK_TOKEN}"}
            )
            
            assert response.status_code == 403
            assert "deactivated" in response.json()["detail"]


class TestJarvisVoiceCommandEndpoint:
    """Test cases for /api/jarvis/voice-command endpoint"""
    
    def test_voice_command_with_transcript(self, mock_jwt_auth, mock_jarvis_brain):
        """Test voice command with pre-transcribed text"""
        response = client.post(
            "/api/jarvis/voice-command",
            json={
                "transcript": "Berikan saya statistik sistem",
                "language": "id-ID"
            },
            headers={"Authorization": f"Bearer {MOCK_TOKEN}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert data["platform"] == "voice"
    
    def test_voice_command_with_audio(self, mock_jwt_auth, mock_jarvis_brain):
        """Test voice command with audio data"""
        # Mock speech-to-text function
        with patch('api.endpoints.jarvis.transcribe_audio') as mock_stt:
            mock_stt.return_value = "Berikan saya statistik sistem"
            
            response = client.post(
                "/api/jarvis/voice-command",
                json={
                    "audio_data": "base64encodedaudiodata",
                    "language": "id-ID"
                },
                headers={"Authorization": f"Bearer {MOCK_TOKEN}"}
            )
            
            assert response.status_code == 200
    
    def test_voice_command_without_data(self, mock_jwt_auth):
        """Test voice command without audio or transcript"""
        response = client.post(
            "/api/jarvis/voice-command",
            json={},
            headers={"Authorization": f"Bearer {MOCK_TOKEN}"}
        )
        
        assert response.status_code == 400
        assert "No audio data or transcript" in response.json()["detail"]


class TestJarvisSystemCommandEndpoint:
    """Test cases for /api/jarvis/system-command endpoint"""
    
    def test_system_command_success(self, mock_jwt_auth, mock_jarvis_brain):
        """Test successful system command"""
        with patch('api.endpoints.jarvis._execute_system_command') as mock_exec:
            mock_exec.return_value = {
                "status": "success",
                "result": "Command executed"
            }
            
            response = client.post(
                "/api/jarvis/system-command",
                json={
                    "command": "get_system_stats",
                    "parameters": {}
                },
                headers={"Authorization": f"Bearer {MOCK_TOKEN}"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "success"
    
    def test_system_command_without_auth(self):
        """Test system command without authentication"""
        response = client.post(
            "/api/jarvis/system-command",
            json={"command": "get_system_stats"}
        )
        
        assert response.status_code == 401


class TestJarvisStatusEndpoint:
    """Test cases for /api/jarvis/status endpoint"""
    
    def test_status_success(self, mock_jwt_auth, mock_jarvis_brain):
        """Test successful status request"""
        response = client.get(
            "/api/jarvis/status",
            headers={"Authorization": f"Bearer {MOCK_TOKEN}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "provider" in data
        assert "capabilities" in data
        assert "is_active" in data
        assert "system_health" in data
    
    def test_status_without_auth(self):
        """Test status request without authentication"""
        response = client.get("/api/jarvis/status")
        
        assert response.status_code == 401


class TestJarvisToggleEndpoint:
    """Test cases for /api/jarvis/toggle endpoint"""
    
    def test_toggle_success(self, mock_admin_auth):
        """Test successful toggle request (admin only)"""
        response = client.post(
            "/api/jarvis/toggle",
            headers={"Authorization": f"Bearer {MOCK_TOKEN}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "is_active" in data
        assert "message" in data
    
    def test_toggle_without_admin(self, mock_jwt_auth):
        """Test toggle request without admin access"""
        response = client.post(
            "/api/jarvis/toggle",
            headers={"Authorization": f"Bearer {MOCK_TOKEN}"}
        )
        
        assert response.status_code == 403


class TestJarvisAnalyticsEndpoint:
    """Test cases for /api/jarvis/analytics endpoint"""
    
    def test_analytics_success(self, mock_jwt_auth):
        """Test successful analytics request"""
        response = client.get(
            "/api/jarvis/analytics",
            headers={"Authorization": f"Bearer {MOCK_TOKEN}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "usage_stats" in data
        assert "performance_metrics" in data
        assert "popular_commands" in data
    
    def test_analytics_without_auth(self):
        """Test analytics request without authentication"""
        response = client.get("/api/jarvis/analytics")
        
        assert response.status_code == 401


class TestJarvisCommandsEndpoint:
    """Test cases for /api/jarvis/commands endpoint"""
    
    def test_commands_success(self, mock_jwt_auth):
        """Test successful commands request"""
        response = client.get(
            "/api/jarvis/commands",
            headers={"Authorization": f"Bearer {MOCK_TOKEN}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "voice_commands" in data
        assert "system_commands" in data
        assert "chat_capabilities" in data
    
    def test_commands_without_auth(self):
        """Test commands request without authentication"""
        response = client.get("/api/jarvis/commands")
        
        assert response.status_code == 401


class TestSpeechToText:
    """Test cases for speech-to-text functionality"""
    
    @pytest.mark.asyncio
    async def test_transcribe_audio_success(self):
        """Test successful audio transcription"""
        from api.endpoints.jarvis import transcribe_audio
        
        # Mock speech recognition
        with patch('api.endpoints.jarvis.sr') as mock_sr:
            mock_recognizer = Mock()
            mock_sr.Recognizer.return_value = mock_recognizer
            mock_recognizer.recognize_google.return_value = "Test transcript"
            
            result = await transcribe_audio("base64encodedaudiodata", "id-ID")
            
            assert result == "Test transcript"
    
    @pytest.mark.asyncio
    async def test_transcribe_audio_error(self):
        """Test audio transcription with error"""
        from api.endpoints.jarvis import transcribe_audio
        
        # Mock invalid base64
        result = await transcribe_audio("invalid_base64", "id-ID")
        
        assert "error" in result.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
