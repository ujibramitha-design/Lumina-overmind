"""
LUMINA OS - Prompt Manager & AI Brain Configuration
Enterprise-grade prompt versioning and dynamic AI personality management
"""

import os
import logging
import asyncio
import json
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum

# Database imports
from prisma import Prisma

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PromptCategory(Enum):
    """Categories of AI prompts"""
    CMO = "cmo"  # Chief Marketing Officer
    SALES_REP = "sales_rep"  # Sales Representative
    CUSTOMER_SERVICE = "customer_service"  # Customer Service
    LEAD_SCOUT = "lead_scout"  # Lead Generation
    CONTENT_CREATOR = "content_creator"  # Content Creation
    ANALYST = "analyst"  # Data Analysis
    NEGOTIATOR = "negotiator"  # Negotiation

class PromptTone(Enum):
    """AI personality tones"""
    FORMAL = "formal"
    CASUAL = "casual"
    PROFESSIONAL = "professional"
    FRIENDLY = "friendly"
    AUTHORITATIVE = "authoritative"
    EMPATHETIC = "empathetic"
    PLAYFUL = "playful"

@dataclass
class PromptTemplate:
    """AI prompt template with metadata"""
    id: str
    name: str
    category: PromptCategory
    tone: PromptTone
    template: str
    variables: List[str]
    version: str
    created_at: datetime
    updated_at: datetime
    is_active: bool
    usage_count: int
    success_rate: float
    last_used: Optional[datetime]

@dataclass
class PromptExecution:
    """Prompt execution record"""
    id: str
    prompt_id: str
    variables: Dict[str, Any]
    execution_time: float
    success: bool
    error_message: Optional[str]
    user_id: str
    session_id: str
    created_at: datetime

class PromptManager:
    """
    Enterprise-grade prompt management system
    Handles AI prompt versioning, dynamic personality changes, and performance tracking
    """
    
    def __init__(self):
        """Initialize prompt manager"""
        self.logger = logging.getLogger(__name__)
        
        # Database connection
        self.db = None
        self._initialize_database()
        
        # In-memory prompt cache for immediate access
        self.prompt_cache: Dict[str, PromptTemplate] = {}
        
        # Default prompts
        self.default_prompts = self._initialize_default_prompts()
        
        # Performance tracking
        self.execution_history: List[PromptExecution] = []
        
        self.logger.info("🧠 Prompt Manager initialized")
        self.logger.info(f"📝 Default prompts loaded: {len(self.default_prompts)}")
    
    def _initialize_database(self):
        """Initialize database connection"""
        try:
            self.db = Prisma()
            self.logger.info("📊 Prompt Manager database connected")
        except Exception as e:
            self.logger.error(f"❌ Database connection failed: {e}")
            self.db = None
    
    def _initialize_default_prompts(self) -> Dict[str, PromptTemplate]:
        """Initialize default prompt templates"""
        prompts = {}
        
        # CMO Prompts
        prompts['cmo_campaign_strategy'] = PromptTemplate(
            id="cmo_campaign_strategy",
            name="CMO Campaign Strategy",
            category=PromptCategory.CMO,
            tone=PromptTone.PROFESSIONAL,
            template="""
            Anda adalah Chief Marketing Officer (CMO) untuk proyek perumahan {project_name}.
            
            TASK: Buat strategi marketing komprehensif dengan fokus:
            1. Target audience: {target_audience}
            2. Value proposition: {value_proposition}
            3. Marketing channels: {marketing_channels}
            4. Budget allocation: {budget_allocation}
            5. Timeline: {timeline}
            
            STYLE: {tone}
            OUTPUT FORMAT: Markdown dengan heading dan bullet points
            """,
            variables=["project_name", "target_audience", "value_proposition", "marketing_channels", "budget_allocation", "timeline"],
            version="1.0.0",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            is_active=True,
            usage_count=0,
            success_rate=0.0,
            last_used=None
        )
        
        # Sales Representative Prompts
        prompts['sales_follow_up'] = PromptTemplate(
            id="sales_follow_up",
            name="Sales Follow-up Message",
            category=PromptCategory.SALES_REP,
            tone=PromptTone.FRIENDLY,
            template="""
            Anda adalah Sales Representative untuk {project_name}.
            
            TASK: Buat pesan follow-up untuk prospek dengan detail:
            - Nama Prospek: {prospect_name}
            - Status: {prospect_status}
            - Interest Level: {interest_level}
            - Last Contact: {last_contact}
            
            STYLE: {tone}
            REQUIREMENTS:
            - Personalized dengan nama prospek
            - Mention last interaction
            - Call to action yang jelas
            - Maksimal 150 kata
            
            OUTPUT: Pesan WhatsApp yang siap dikirim
            """,
            variables=["project_name", "prospect_name", "prospect_status", "interest_level", "last_contact"],
            version="1.0.0",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            is_active=True,
            usage_count=0,
            success_rate=0.0,
            last_used=None
        )
        
        # Customer Service Prompts
        prompts['customer_service_response'] = PromptTemplate(
            id="customer_service_response",
            name="Customer Service Response",
            category=PromptCategory.CUSTOMER_SERVICE,
            tone=PromptTone.EMPATHETIC,
            template="""
            Anda adalah Customer Service Representative untuk {project_name}.
            
            TASK: Buat respons untuk pertanya pelanggan:
            - Pelanggan: {customer_name}
            - Pertanyaan: {customer_question}
            - Kategori: {question_category}
            - Urgency: {urgency_level}
            
            STYLE: {tone}
            REQUIREMENTS:
            - Empati dan paham kebutuhan pelanggan
            - Berikan solusi yang jelas
            - Informasi kontak jika perlu follow-up
            - Maksimal 200 kata
            
            OUTPUT: Respons customer service yang profesional
            """,
            variables=["project_name", "customer_name", "customer_question", "question_category", "urgency_level"],
            version="1.0.0",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            is_active=True,
            usage_count=0,
            success_rate=0.0,
            last_used=None
        )
        
        # Lead Scout Prompts
        prompts['lead_scout_analysis'] = PromptTemplate(
            id="lead_scout_analysis",
            name="Lead Scout Analysis",
            category=PromptCategory.LEAD_SCOUT,
            tone=PromptTone.ANALYTICAL,
            template="""
            Anda adalah Lead Scout Analyst untuk {project_name}.
            
            TASK: Analisis data prospek:
            - Data Prospek: {prospect_data}
            - Sumber: {data_source}
            - Area: {target_area}
            - Kriteria: {scouting_criteria}
            
            STYLE: {tone}
            REQUIREMENTS:
            - Identifikasi intent level (Low/Medium/High)
            - Extract key information points
            - Recommend next action
            - Score lead quality (1-10)
            
            OUTPUT: JSON dengan analisis lengkap
            """,
            variables=["project_name", "prospect_data", "data_source", "target_area", "scouting_criteria"],
            version="1.0.0",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            is_active=True,
            usage_count=0,
            success_rate=0.0,
            last_used=None
        )
        
        # Content Creator Prompts
        prompts['content_creation'] = PromptTemplate(
            id="content_creation",
            name="Content Creation",
            category=PromptCategory.CONTENT_CREATOR,
            tone=PromptTone.CREATIVE,
            template="""
            Anda adalah Content Creator untuk {project_name}.
            
            TASK: Buat konten marketing:
            - Platform: {platform}
            - Format: {content_format}
            - Target Audience: {target_audience}
            - Key Message: {key_message}
            - Call to Action: {cta}
            
            STYLE: {tone}
            REQUIREMENTS:
            - Engaging dan menarik perhatian
            - Sesuai dengan platform guidelines
            - Include relevant hashtags
            - Maksimal 300 kata
            
            OUTPUT: Konten marketing yang siap publish
            """,
            variables=["project_name", "platform", "content_format", "target_audience", "key_message", "cta"],
            version="1.0.0",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            is_active=True,
            usage_count=0,
            success_rate=0.0,
            last_used=None
        )
        
        # Analyst Prompts
        prompts['data_analysis'] = PromptTemplate(
            id="data_analysis",
            name="Data Analysis",
            category=PromptCategory.ANALYST,
            tone=PromptTone.ANALYTICAL,
            template="""
            Anda adalah Data Analyst untuk {project_name}.
            
            TASK: Analisis data marketing:
            - Dataset: {dataset_description}
            - Time Period: {time_period}
            - Metrics: {key_metrics}
            - Objective: {analysis_objective}
            
            STYLE: {tone}
            REQUIREMENTS:
            - Statistical analysis
            - Trend identification
            - Actionable insights
            - Data visualization recommendations
            
            OUTPUT: Laporan analisis dengan insights
            """,
            variables=["project_name", "dataset_description", "time_period", "key_metrics", "analysis_objective"],
            version="1.0.0",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            is_active=True,
            usage_count=0,
            success_rate=0.0,
            last_used=None
        )
        
        # Negotiator Prompts
        prompts['negotiation_strategy'] = PromptTemplate(
            id="negotiation_strategy",
            name="Negotiation Strategy",
            category=PromptCategory.NEGOTIATOR,
            tone=PromptTone.AUTHORITATIVE,
            template="""
            Anda adalah Negotiator untuk {project_name}.
            
            TASK: Buat strategi negosiasi:
            - Prospek: {prospect_name}
            - Position: {prospect_position}
            - Budget: {budget_range}
            - Timeline: {timeline}
            - Key Points: {negotiation_points}
            
            STYLE: {tone}
            REQUIREMENTS:
            - Win-win approach
            - Clear value proposition
            - Risk assessment
            - Alternative options
            
            OUTPUT: Strategi negosiasi dengan action plan
            """,
            variables=["project_name", "prospect_name", "prospect_position", "budget_range", "timeline", "negotiation_points"],
            version="1.0.0",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            is_active=True,
            usage_count=0,
            success_rate=0.0,
            last_used=None
        )
        
        return prompts
    
    async def get_prompt_template(self, prompt_id: str) -> Optional[PromptTemplate]:
        """Get prompt template by ID"""
        try:
            # Check cache first
            if prompt_id in self.prompt_cache:
                return self.prompt_cache[prompt_id]
            
            # Check database
            if self.db:
                # This would query the database for the prompt
                # For now, return from default prompts
                pass
            
            # Return from default prompts
            return self.default_prompts.get(prompt_id)
            
        except Exception as e:
            self.logger.error(f"❌ Failed to get prompt template {prompt_id}: {e}")
            return None
    
    async def execute_prompt(self, prompt_id: str, variables: Dict[str, Any], 
                             user_id: str = None, session_id: str = None) -> Dict[str, Any]:
        """
        Execute prompt with variables and track performance
        
        Args:
            prompt_id: ID of the prompt template
            variables: Variables to substitute in template
            user_id: ID of the user executing the prompt
            session_id: Session ID for tracking
            
        Returns:
            Dict with execution result
        """
        try:
            start_time = asyncio.get_event_loop().time()
            
            # Get prompt template
            template = await self.get_prompt_template(prompt_id)
            if not template:
                return {
                    'success': False,
                    'error': f'Prompt template not found: {prompt_id}',
                    'execution_time': 0.0
                }
            
            # Substitute variables
            try:
                final_prompt = template.template.format(**variables)
            except KeyError as e:
                return {
                    'success': False,
                    'error': f'Missing variable in template: {str(e)}',
                    'execution_time': 0.0
                }
            
            # Track execution
            execution_id = f"exec_{int(datetime.now().timestamp() * 1000000)}"
            execution_time = asyncio.get_event_loop().time() - start_time
            
            execution = PromptExecution(
                id=execution_id,
                prompt_id=prompt_id,
                variables=variables,
                execution_time=execution_time,
                success=True,
                error_message=None,
                user_id=user_id or "system",
                session_id=session_id or "system",
                created_at=datetime.now()
            )
            
            self.execution_history.append(execution)
            
            # Update template usage
            template.usage_count += 1
            template.last_used = datetime.now()
            
            # Save to database
            if self.db:
                await self._save_execution(execution)
                await self._update_template_usage(template)
            
            self.logger.info(f"📝 Prompt executed: {prompt_id} in {execution_time:.2f}s")
            
            return {
                'success': True,
                'prompt_id': prompt_id,
                'final_prompt': final_prompt,
                'execution_time': execution_time,
                'template_info': {
                    'name': template.name,
                    'category': template.category.value,
                    'tone': template.tone.value,
                    'version': template.version
                }
            }
            
        except Exception as e:
            self.logger.error(f"❌ Prompt execution failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'execution_time': 0.0
            }
    
    async def update_prompt_tone(self, prompt_id: str, new_tone: PromptTone) -> bool:
        """
        Update prompt tone dynamically
        
        Args:
            prompt_id: ID of the prompt to update
            new_tone: New tone to apply
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            template = await self.get_prompt_template(prompt_id)
            if not template:
                self.logger.error(f"❌ Prompt template not found: {prompt_id}")
                return False
            
            # Update tone
            old_tone = template.tone
            template.tone = new_tone
            template.updated_at = datetime.now()
            
            # Update in cache
            self.prompt_cache[prompt_id] = template
            
            # Save to database
            if self.db:
                await self._save_template(template)
            
            self.logger.info(f"🎭 Prompt tone updated: {prompt_id} {old_tone.value} → {new_tone.value}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to update prompt tone: {e}")
            return False
    
    async def create_prompt_template(self, name: str, category: PromptCategory, 
                                   tone: PromptTone, template: str, 
                                   variables: List[str]) -> str:
        """
        Create new prompt template
        
        Args:
            name: Name of the prompt
            category: Category of the prompt
            tone: Tone of the prompt
            template: Template string
            variables: List of variables in template
            
        Returns:
            str: ID of the created prompt
        """
        try:
            prompt_id = f"prompt_{int(datetime.now().timestamp() * 1000000)}"
            
            new_template = PromptTemplate(
                id=prompt_id,
                name=name,
                category=category,
                tone=tone,
                template=template,
                variables=variables,
                version="1.0.0",
                created_at=datetime.now(),
                updated_at=datetime.now(),
                is_active=True,
                usage_count=0,
                success_rate=0.0,
                last_used=None
            )
            
            # Add to cache
            self.prompt_cache[prompt_id] = new_template
            
            # Save to database
            if self.db:
                await self._save_template(new_template)
            
            self.logger.info(f"📝 Prompt template created: {name} ({prompt_id})")
            
            return prompt_id
            
        except Exception as e:
            self.logger.error(f"❌ Failed to create prompt template: {e}")
            return ""
    
    async def get_prompt_analytics(self, days: int = 30) -> Dict[str, Any]:
        """
        Get prompt usage analytics
        
        Args:
            days: Number of days to analyze
            
        Returns:
            Dict with analytics data
        """
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            # Filter execution history
            recent_executions = [
                exec for exec in self.execution_history
                if exec.created_at >= cutoff_date
            ]
            
            # Calculate analytics
            total_executions = len(recent_executions)
            successful_executions = len([e for e in recent_executions if e.success])
            success_rate = (successful_executions / total_executions * 100) if total_executions > 0 else 0
            
            # Prompt usage by category
            category_usage = {}
            for execution in recent_executions:
                template = await self.get_prompt_template(execution.prompt_id)
                if template:
                    category = template.category.value
                    category_usage[category] = category_usage.get(category, 0) + 1
            
            # Average execution time
            avg_execution_time = sum(e.execution_time for e in recent_executions) / len(recent_executions) if recent_executions else 0
            
            # Most used prompts
            prompt_usage = {}
            for execution in recent_executions:
                prompt_usage[execution.prompt_id] = prompt_usage.get(execution.prompt_id, 0) + 1
            
            most_used = sorted(prompt_usage.items(), key=lambda x: x[1], reverse=True)[:10]
            
            return {
                'period_days': days,
                'total_executions': total_executions,
                'successful_executions': successful_executions,
                'success_rate': success_rate,
                'avg_execution_time': avg_execution_time,
                'category_usage': category_usage,
                'most_used_prompts': most_used,
                'active_templates': len(self.prompt_cache)
            }
            
        except Exception as e:
            self.logger.error(f"❌ Failed to get prompt analytics: {e}")
            return {}
    
    async def _save_template(self, template: PromptTemplate):
        """Save template to database"""
        try:
            # This would save to the actual database
            self.logger.debug(f"📝 Template saved to database: {template.id}")
        except Exception as e:
            self.logger.error(f"❌ Failed to save template: {e}")
    
    async def _save_execution(self, execution: PromptExecution):
        """Save execution to database"""
        try:
            # This would save to the actual database
            self.logger.debug(f"📊 Execution saved to database: {execution.id}")
        except Exception as e:
            self.logger.error(f"❌ Failed to save execution: {e}")
    
    async def _update_template_usage(self, template: PromptTemplate):
        """Update template usage in database"""
        try:
            # This would update the actual database
            self.logger.debug(f"📊 Template usage updated: {template.id}")
        except Exception as e:
            self.logger.error(f"❌ Failed to update template usage: {e}")
    
    def get_all_prompts(self) -> Dict[str, PromptTemplate]:
        """Get all available prompts"""
        return self.prompt_cache
    
    def get_prompts_by_category(self, category: PromptCategory) -> List[PromptTemplate]:
        """Get prompts by category"""
        return [p for p in self.prompt_cache.values() if p.category == category]
    
    def get_prompts_by_tone(self, tone: PromptTone) -> List[PromptTemplate]:
        """Get prompts by tone"""
        return [p for p in self.prompt_cache.values() if p.tone == tone]

# Global prompt manager instance
prompt_manager = PromptManager()
