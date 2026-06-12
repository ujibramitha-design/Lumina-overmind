"""
LUMINA OS - AI Model Fallback & Agnostic Architecture
Enterprise-grade model management with automatic fallback capabilities
"""

import os
import logging
import asyncio
import json
from typing import Dict, Any, Optional, List, Union
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

# Import vault manager for secure API key retrieval
from core_modules.vault_manager import vault_manager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelProvider(Enum):
    """AI model providers"""
    OPENAI = "openai"
    GOOGLE = "google"
    ANTHROPIC = "anthropic"
    LOCAL = "local"
    FALLBACK = "fallback"

class ModelType(Enum):
    """Types of AI models"""
    CHAT = "chat"
    COMPLETION = "completion"
    EMBEDDING = "embedding"
    VISION = "vision"
    AUDIO = "audio"

class ModelStatus(Enum):
    """Model status"""
    ACTIVE = "active"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"
    MAINTENANCE = "maintenance"

@dataclass
class AIModel:
    """AI model configuration"""
    id: str
    name: str
    provider: ModelProvider
    model_type: ModelType
    model_id: str  # e.g., "gpt-4o", "gemini-1.5-pro"
    api_key: str
    api_base: str
    max_tokens: int
    temperature: float
    timeout: int
    retry_count: int
    status: ModelStatus
    last_health_check: Optional[datetime]
    error_count: int
    success_count: int
    avg_response_time: float
    cost_per_1k_tokens: float
    priority: int  # Lower number = higher priority

@dataclass
class ModelRequest:
    """AI model request"""
    id: str
    model_type: ModelType
    prompt: str
    context: Optional[Dict[str, Any]]
    max_tokens: Optional[int]
    temperature: Optional[float]
    user_id: str
    session_id: str
    created_at: datetime

@dataclass
class ModelResponse:
    """AI model response"""
    request_id: str
    model_used: str
    provider: ModelProvider
    content: str
    tokens_used: int
    response_time: float
    cost: float
    success: bool
    error_message: Optional[str]
    fallback_used: bool
    created_at: datetime

class ModelFallback:
    """
    Enterprise-grade AI model fallback system
    Provides model-agnostic architecture with automatic failover
    """
    
    def __init__(self):
        """Initialize model fallback system"""
        self.logger = logging.getLogger(__name__)
        
        # Model registry
        self.models: Dict[str, AIModel] = {}
        
        # Active models by type and priority
        self.active_models: Dict[ModelType, List[AIModel]] = {}
        
        # Health monitoring
        self.health_status: Dict[str, Dict[str, Any]] = {}
        
        # Usage statistics
        self.usage_stats: Dict[str, Dict[str, Any]] = {}
        
        # Fallback configuration
        self.fallback_config = self._initialize_fallback_config()
        
        # Initialize models
        self._initialize_models()
        
        self.logger.info("🤖 Model Fallback System initialized")
        self.logger.info(f"📋 Models loaded: {len(self.models)}")
        self.logger.info(f"🔄 Fallback rules: {len(self.fallback_config)}")
    
    def _initialize_fallback_config(self) -> Dict[str, Any]:
        """Initialize fallback configuration"""
        return {
            'auto_failover': True,
            'health_check_interval': 300,  # 5 minutes
            'max_error_rate': 0.1,  # 10% error rate threshold
            'max_response_time': 30.0,  # 30 seconds
            'circuit_breaker_threshold': 5,  # 5 consecutive failures
            'fallback_timeout': 10.0,  # 10 seconds for fallback
            'cost_optimization': True,  # Prefer cheaper models for non-critical tasks
            'geographic_routing': True,  # Route to nearest models
            'load_balancing': True  # Distribute load across models
        }
    
    def _initialize_models(self):
        """Initialize AI models with fallback hierarchy"""
        try:
            # OpenAI Models
            self._add_model(AIModel(
                id="gpt-4o",
                name="GPT-4o",
                provider=ModelProvider.OPENAI,
                model_type=ModelType.CHAT,
                model_id="gpt-4o",
                api_key="",  # Will be fetched from vault_manager
                api_base="https://api.openai.com/v1",
                max_tokens=4096,
                temperature=0.7,
                timeout=30,
                retry_count=3,
                status=ModelStatus.ACTIVE,
                last_health_check=None,
                error_count=0,
                success_count=0,
                avg_response_time=0.0,
                cost_per_1k_tokens=0.015,  # $0.015 per 1K tokens
                priority=1  # Highest priority
            ))
            
            self._add_model(AIModel(
                id="gpt-4o-mini",
                name="GPT-4o Mini",
                provider=ModelProvider.OPENAI,
                model_type=ModelType.CHAT,
                model_id="gpt-4o-mini",
                api_key="",  # Will be fetched from vault_manager
                api_base="https://api.openai.com/v1",
                max_tokens=4096,
                temperature=0.7,
                timeout=30,
                retry_count=3,
                status=ModelStatus.ACTIVE,
                last_health_check=None,
                error_count=0,
                success_count=0,
                avg_response_time=0.0,
                cost_per_1k_tokens=0.0005,  # $0.0005 per 1K tokens
                priority=2
            ))
            
            # Google Models
            self._add_model(AIModel(
                id="gemini-1.5-pro",
                name="Gemini 1.5 Pro",
                provider=ModelProvider.GOOGLE,
                model_type=ModelType.CHAT,
                model_id="gemini-1.5-pro",
                api_key="",  # Will be fetched from vault_manager
                api_base="https://generativelanguage.googleapis.com/v1",
                max_tokens=4096,
                temperature=0.7,
                timeout=30,
                retry_count=3,
                status=ModelStatus.ACTIVE,
                last_health_check=None,
                error_count=0,
                success_count=0,
                avg_response_time=0.0,
                cost_per_1k_tokens=0.0035,  # $0.0035 per 1K tokens
                priority=3
            ))
            
            self._add_model(AIModel(
                id="gemini-1.5-flash",
                name="Gemini 1.5 Flash",
                provider=ModelProvider.GOOGLE,
                model_type=ModelType.CHAT,
                model_id="gemini-1.5-flash",
                api_key="",  # Will be fetched from vault_manager
                api_base="https://generativelanguage.googleapis.com/v1",
                max_tokens=4096,
                temperature=0.7,
                timeout=30,
                retry_count=3,
                status=ModelStatus.ACTIVE,
                last_health_check=None,
                error_count=0,
                success_count=0,
                avg_response_time=0.0,
                cost_per_1k_tokens=0.00015,  # $0.00015 per 1K tokens
                priority=4
            ))
            
            # Anthropic Models (if available)
            if os.getenv("ANTHROPIC_API_KEY"):
                self._add_model(AIModel(
                    id="claude-3-5-sonnet",
                    name="Claude 3.5 Sonnet",
                    provider=ModelProvider.ANTHROPIC,
                    model_type=ModelType.CHAT,
                    model_id="claude-3-5-sonnet-20241022",
                    api_key=os.getenv("ANTHROPIC_API_KEY", ""),
                    api_base="https://api.anthropic.com/v1",
                    max_tokens=4096,
                    temperature=0.7,
                    timeout=30,
                    retry_count=3,
                    status=ModelStatus.ACTIVE,
                    last_health_check=None,
                    error_count=0,
                    success_count=0,
                    avg_response_time=0.0,
                    cost_per_1k_tokens=0.015,  # $0.015 per 1K tokens
                    priority=5
                ))
            
            # Local Models (if available)
            self._add_model(AIModel(
                id="local-llama",
                name="Local LLaMA",
                provider=ModelProvider.LOCAL,
                model_type=ModelType.CHAT,
                model_id="llama-3.1-8b",
                api_key="local",
                api_base="http://localhost:8000/v1",
                max_tokens=4096,
                temperature=0.7,
                timeout=60,
                retry_count=2,
                status=ModelStatus.ACTIVE,
                last_health_check=None,
                error_count=0,
                success_count=0,
                avg_response_time=0.0,
                cost_per_1k_tokens=0.0,  # Free
                priority=10  # Lowest priority
            ))
            
            # Organize models by type
            self._organize_models_by_type()
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize models: {e}")
    
    def _add_model(self, model: AIModel):
        """Add model to registry"""
        self.models[model.id] = model
        
        # Initialize usage stats
        self.usage_stats[model.id] = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'total_tokens': 0,
            'total_cost': 0.0,
            'avg_response_time': 0.0,
            'last_used': None
        }
        
        # Initialize health status
        self.health_status[model.id] = {
            'status': model.status.value,
            'last_check': None,
            'error_rate': 0.0,
            'avg_response_time': 0.0,
            'consecutive_failures': 0,
            'circuit_breaker_open': False
        }
    
    def _organize_models_by_type(self):
        """Organize models by type and priority"""
        self.active_models = {}
        
        for model_type in ModelType:
            models_of_type = [m for m in self.models.values() if m.model_type == model_type]
            models_of_type.sort(key=lambda x: x.priority)
            self.active_models[model_type] = models_of_type
    
    async def execute_request(self, request: ModelRequest) -> ModelResponse:
        """
        Execute AI request with automatic fallback
        
        Args:
            request: AI model request
            
        Returns:
            ModelResponse: Response from AI model
        """
        try:
            start_time = asyncio.get_event_loop().time()
            
            # Get available models for this type
            available_models = self._get_available_models(request.model_type)
            
            if not available_models:
                return self._create_error_response(request, "No available models")
            
            # Try models in priority order
            last_error = None
            for model in available_models:
                try:
                    # Check if model is healthy
                    if not self._is_model_healthy(model.id):
                        self.logger.warning(f"⚠️ Model {model.id} is unhealthy, trying next")
                        continue
                    
                    # Execute request
                    response = await self._execute_with_model(model, request)
                    
                    # Update usage stats
                    self._update_usage_stats(model.id, response, True)
                    
                    # Update health status
                    self._update_health_status(model.id, True, response.response_time)
                    
                    self.logger.info(f"✅ Request completed: {request.id} using {model.id}")
                    
                    return response
                    
                except Exception as e:
                    last_error = e
                    self.logger.warning(f"⚠️ Model {model.id} failed: {e}")
                    
                    # Update usage stats
                    self._update_usage_stats(model.id, None, False)
                    
                    # Update health status
                    self._update_health_status(model.id, False, 0.0)
                    
                    # Try next model
                    continue
            
            # All models failed
            return self._create_error_response(request, f"All models failed: {last_error}")
            
        except Exception as e:
            self.logger.error(f"❌ Request execution failed: {e}")
            return self._create_error_response(request, f"Execution error: {str(e)}")
    
    async def _execute_with_model(self, model: AIModel, request: ModelRequest) -> ModelResponse:
        """Execute request with specific model"""
        try:
            # Create request ID
            request_id = f"req_{int(datetime.now().timestamp() * 1000000)}"
            
            # Execute based on provider
            if model.provider == ModelProvider.OPENAI:
                response_data = await self._execute_openai(model, request)
            elif model.provider == ModelProvider.GOOGLE:
                response_data = await self._execute_google(model, request)
            elif model.provider == ModelProvider.ANTHROPIC:
                response_data = await self._execute_anthropic(model, request)
            elif model.provider == ModelProvider.LOCAL:
                response_data = await self._execute_local(model, request)
            else:
                raise ValueError(f"Unsupported provider: {model.provider}")
            
            # Calculate cost
            cost = self._calculate_cost(model, response_data.get('tokens_used', 0))
            
            # Create response
            response = ModelResponse(
                request_id=request_id,
                model_used=model.id,
                provider=model.provider,
                content=response_data.get('content', ''),
                tokens_used=response_data.get('tokens_used', 0),
                response_time=response_data.get('response_time', 0.0),
                cost=cost,
                success=True,
                error_message=None,
                fallback_used=False,
                created_at=datetime.now()
            )
            
            return response
            
        except Exception as e:
            raise Exception(f"Model execution failed: {str(e)}")
    
    async def _execute_openai(self, model: AIModel, request: ModelRequest) -> Dict[str, Any]:
        """Execute request with OpenAI model"""
        try:
            import openai
            
            # Configure client
            client = openai.AsyncOpenAI(
                api_key=model.api_key,
                base_url=model.api_base,
                timeout=model.timeout
            )
            
            # Prepare messages
            messages = [{"role": "user", "content": request.prompt}]
            
            # Add context if provided
            if request.context:
                messages.insert(0, {"role": "system", "content": str(request.context)})
            
            # Execute request
            start_time = asyncio.get_event_loop().time()
            response = await client.chat.completions.create(
                model=model.model_id,
                messages=messages,
                max_tokens=request.max_tokens or model.max_tokens,
                temperature=request.temperature or model.temperature
            )
            response_time = asyncio.get_event_loop().time() - start_time
            
            # Extract response
            content = response.choices[0].message.content
            tokens_used = response.usage.total_tokens
            
            return {
                'content': content,
                'tokens_used': tokens_used,
                'response_time': response_time
            }
            
        except Exception as e:
            raise Exception(f"OpenAI execution failed: {str(e)}")
    
    async def _execute_google(self, model: AIModel, request: ModelRequest) -> Dict[str, Any]:
        """Execute request with Google model"""
        try:
            import google.generativeai as genai
            
            # Configure client
            genai.configure(api_key=model.api_key)
            model_instance = genai.GenerativeModel(model.model_id)
            
            # Execute request
            start_time = asyncio.get_event_loop().time()
            response = await model_instance.generate_content_async(request.prompt)
            response_time = asyncio.get_event_loop().time() - start_time
            
            # Extract response
            content = response.text
            tokens_used = len(content.split())  # Approximation
            
            return {
                'content': content,
                'tokens_used': tokens_used,
                'response_time': response_time
            }
            
        except Exception as e:
            raise Exception(f"Google execution failed: {str(e)}")
    
    async def _execute_anthropic(self, model: AIModel, request: ModelRequest) -> Dict[str, Any]:
        """Execute request with Anthropic model"""
        try:
            import anthropic
            
            # Configure client
            client = anthropic.AsyncAnthropic(
                api_key=model.api_key,
                base_url=model.api_base,
                timeout=model.timeout
            )
            
            # Execute request
            start_time = asyncio.get_event_loop().time()
            response = await client.messages.create(
                model=model.model_id,
                max_tokens=request.max_tokens or model.max_tokens,
                temperature=request.temperature or model.temperature,
                messages=[{"role": "user", "content": request.prompt}]
            )
            response_time = asyncio.get_event_loop().time() - start_time
            
            # Extract response
            content = response.content[0].text
            tokens_used = response.usage.input_tokens + response.usage.output_tokens
            
            return {
                'content': content,
                'tokens_used': tokens_used,
                'response_time': response_time
            }
            
        except Exception as e:
            raise Exception(f"Anthropic execution failed: {str(e)}")
    
    async def _execute_local(self, model: AIModel, request: ModelRequest) -> Dict[str, Any]:
        """Execute request with local model"""
        try:
            import aiohttp
            
            # Prepare request
            payload = {
                "model": model.model_id,
                "messages": [{"role": "user", "content": request.prompt}],
                "max_tokens": request.max_tokens or model.max_tokens,
                "temperature": request.temperature or model.temperature
            }
            
            # Execute request
            start_time = asyncio.get_event_loop().time()
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{model.api_base}/chat/completions",
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=model.timeout)
                ) as response:
                    data = await response.json()
                    response_time = asyncio.get_event_loop().time() - start_time
                    
                    if response.status != 200:
                        raise Exception(f"Local model error: {data}")
                    
                    # Extract response
                    content = data['choices'][0]['message']['content']
                    tokens_used = data.get('usage', {}).get('total_tokens', 0)
                    
                    return {
                        'content': content,
                        'tokens_used': tokens_used,
                        'response_time': response_time
                    }
            
        except Exception as e:
            raise Exception(f"Local model execution failed: {str(e)}")
    
    def _get_available_models(self, model_type: ModelType) -> List[AIModel]:
        """Get available models for type"""
        return [m for m in self.active_models.get(model_type, []) 
                if self._is_model_healthy(m.id)]
    
    def _is_model_healthy(self, model_id: str) -> bool:
        """Check if model is healthy"""
        health = self.health_status.get(model_id, {})
        
        # Check circuit breaker
        if health.get('circuit_breaker_open', False):
            return False
        
        # Check error rate
        error_rate = health.get('error_rate', 0.0)
        if error_rate > self.fallback_config['max_error_rate']:
            return False
        
        # Check response time
        avg_response_time = health.get('avg_response_time', 0.0)
        if avg_response_time > self.fallback_config['max_response_time']:
            return False
        
        # Check status
        model = self.models.get(model_id)
        if model and model.status != ModelStatus.ACTIVE:
            return False
        
        return True
    
    def _update_usage_stats(self, model_id: str, response: Optional[ModelResponse], success: bool):
        """Update usage statistics"""
        stats = self.usage_stats.get(model_id, {})
        
        stats['total_requests'] += 1
        
        if success and response:
            stats['successful_requests'] += 1
            stats['total_tokens'] += response.tokens_used
            stats['total_cost'] += response.cost
            stats['avg_response_time'] = (stats['avg_response_time'] * (stats['successful_requests'] - 1) + response.response_time) / stats['successful_requests']
            stats['last_used'] = datetime.now()
        else:
            stats['failed_requests'] += 1
    
    def _update_health_status(self, model_id: str, success: bool, response_time: float):
        """Update health status"""
        health = self.health_status.get(model_id, {})
        
        health['last_check'] = datetime.now()
        
        if success:
            health['consecutive_failures'] = 0
            health['circuit_breaker_open'] = False
            
            # Update error rate
            stats = self.usage_stats.get(model_id, {})
            total_requests = stats.get('total_requests', 1)
            failed_requests = stats.get('failed_requests', 0)
            health['error_rate'] = failed_requests / total_requests
            
            # Update response time
            stats = self.usage_stats.get(model_id, {})
            health['avg_response_time'] = stats.get('avg_response_time', 0.0)
        else:
            health['consecutive_failures'] += 1
            
            # Open circuit breaker if threshold reached
            if health['consecutive_failures'] >= self.fallback_config['circuit_breaker_threshold']:
                health['circuit_breaker_open'] = True
                self.logger.warning(f"🚨 Circuit breaker opened for model: {model_id}")
    
    def _calculate_cost(self, model: AIModel, tokens_used: int) -> float:
        """Calculate cost for model usage"""
        return (tokens_used / 1000) * model.cost_per_1k_tokens
    
    def _create_error_response(self, request: ModelRequest, error_message: str) -> ModelResponse:
        """Create error response"""
        return ModelResponse(
            request_id=request.id,
            model_used="none",
            provider=ModelProvider.FALLBACK,
            content="",
            tokens_used=0,
            response_time=0.0,
            cost=0.0,
            success=False,
            error_message=error_message,
            fallback_used=True,
            created_at=datetime.now()
        )
    
    async def health_check_all_models(self) -> Dict[str, Dict[str, Any]]:
        """Perform health check on all models"""
        try:
            health_results = {}
            
            for model_id, model in self.models.items():
                try:
                    # Simple health check - send a short test request
                    test_request = ModelRequest(
                        id=f"health_{model_id}_{int(datetime.now().timestamp())}",
                        model_type=model.model_type,
                        prompt="Hello",
                        context=None,
                        max_tokens=10,
                        temperature=0.1,
                        user_id="health_check",
                        session_id="health_check",
                        created_at=datetime.now()
                    )
                    
                    response = await self._execute_with_model(model, test_request)
                    
                    health_results[model_id] = {
                        'status': 'healthy',
                        'response_time': response.response_time,
                        'error': None
                    }
                    
                    # Update model status
                    model.status = ModelStatus.ACTIVE
                    model.last_health_check = datetime.now()
                    
                except Exception as e:
                    health_results[model_id] = {
                        'status': 'unhealthy',
                        'response_time': 0.0,
                        'error': str(e)
                    }
                    
                    # Update model status
                    model.status = ModelStatus.UNAVAILABLE
                    model.last_health_check = datetime.now()
                    model.error_count += 1
            
            self.logger.info(f"🏥 Health check completed: {len(health_results)} models")
            
            return health_results
            
        except Exception as e:
            self.logger.error(f"❌ Health check failed: {e}")
            return {}
    
    def get_model_statistics(self) -> Dict[str, Any]:
        """Get model usage statistics"""
        try:
            stats = {
                'total_models': len(self.models),
                'active_models': len([m for m in self.models.values() if m.status == ModelStatus.ACTIVE]),
                'total_requests': sum(s.get('total_requests', 0) for s in self.usage_stats.values()),
                'successful_requests': sum(s.get('successful_requests', 0) for s in self.usage_stats.values()),
                'failed_requests': sum(s.get('failed_requests', 0) for s in self.usage_stats.values()),
                'total_tokens': sum(s.get('total_tokens', 0) for s in self.usage_stats.values()),
                'total_cost': sum(s.get('total_cost', 0.0) for s in self.usage_stats.values()),
                'models_by_provider': {},
                'models_by_type': {}
            }
            
            # Group by provider
            for model in self.models.values():
                provider = model.provider.value
                stats['models_by_provider'][provider] = stats['models_by_provider'].get(provider, 0) + 1
            
            # Group by type
            for model in self.models.values():
                model_type = model.model_type.value
                stats['models_by_type'][model_type] = stats['models_by_type'].get(model_type, 0) + 1
            
            return stats
            
        except Exception as e:
            self.logger.error(f"❌ Failed to get model statistics: {e}")
            return {}
    
    def add_model(self, model: AIModel):
        """Add new model to registry"""
        self._add_model(model)
        self._organize_models_by_type()
        self.logger.info(f"➕ Model added: {model.id}")
    
    def remove_model(self, model_id: str) -> bool:
        """Remove model from registry"""
        try:
            if model_id in self.models:
                del self.models[model_id]
                del self.usage_stats[model_id]
                del self.health_status[model_id]
                self._organize_models_by_type()
                self.logger.info(f"➖ Model removed: {model_id}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"❌ Failed to remove model: {e}")
            return False
    
    def update_model_status(self, model_id: str, status: ModelStatus) -> bool:
        """Update model status"""
        try:
            if model_id in self.models:
                self.models[model_id].status = status
                self.logger.info(f"🔄 Model status updated: {model_id} → {status.value}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"❌ Failed to update model status: {e}")
            return False

# Global model fallback instance
model_fallback = ModelFallback()
