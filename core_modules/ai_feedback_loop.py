"""
LUMINA OS - AI Feedback Loop & Learning System
Enterprise-grade AI learning from human feedback and self-improvement
"""

import os
import logging
import asyncio
import json
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

# Database imports
from prisma import Prisma

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FeedbackType(Enum):
    """Types of feedback"""
    REJECT = "reject"           # Human rejected the output
    REVISE = "revise"           # Human requested revision
    APPROVE = "approve"         # Human approved the output
    IMPROVE = "improve"         # Human suggested improvement
    CORRECT = "correct"         # Human corrected factual error
    STYLE = "style"             # Style preference feedback

class FeedbackSource(Enum):
    """Sources of feedback"""
    HUMAN_AGENT = "human_agent"
    CUSTOMER = "customer"
    SYSTEM = "system"
    AI_REVIEW = "ai_review"

class LearningCategory(Enum):
    """Learning categories"""
    CONTENT_STYLE = "content_style"
    TONE_ADJUSTMENT = "tone_adjustment"
    FACTUAL_ACCURACY = "factual_accuracy"
    RESPONSE_FORMAT = "response_format"
    PERSONALIZATION = "personalization"
    COMPLIANCE = "compliance"

@dataclass
class FeedbackRecord:
    """Feedback record for AI learning"""
    id: str
    task_id: str
    model_used: str
    original_prompt: str
    original_response: str
    feedback_type: FeedbackType
    feedback_source: FeedbackSource
    feedback_content: str
    revised_response: Optional[str]
    learning_category: LearningCategory
    confidence_score: float
    user_id: str
    session_id: str
    created_at: datetime
    applied_at: Optional[datetime]

@dataclass
class LearningPattern:
    """Learned pattern from feedback"""
    id: str
    pattern_type: LearningCategory
    pattern_description: str
    trigger_keywords: List[str]
    response_template: str
    success_rate: float
    usage_count: int
    last_updated: datetime
    is_active: bool

@dataclass
class AIImprovement:
    """AI improvement suggestion"""
    id: str
    category: LearningCategory
    improvement_type: str
    description: str
    implementation_code: str
    priority: int
    estimated_impact: float
    created_at: datetime
    implemented_at: Optional[datetime]

class AIFeedbackLoop:
    """
    Enterprise-grade AI feedback loop system
    Enables continuous learning from human feedback
    """
    
    def __init__(self):
        """Initialize AI feedback loop"""
        self.logger = logging.getLogger(__name__)
        
        # Database connection
        self.db = None
        self._initialize_database()
        
        # Feedback storage
        self.feedback_records: List[FeedbackRecord] = []
        
        # Learning patterns
        self.learning_patterns: Dict[str, LearningPattern] = {}
        
        # AI improvements
        self.ai_improvements: List[AIImprovement] = []
        
        # Feedback analysis
        self.feedback_analytics = self._initialize_analytics()
        
        # Learning rules
        self.learning_rules = self._initialize_learning_rules()
        
        # Initialize default patterns
        self._initialize_default_patterns()
        
        self.logger.info("🧠 AI Feedback Loop initialized")
        self.logger.info(f"📋 Learning rules loaded: {len(self.learning_rules)}")
        self.logger.info(f"🎯 Default patterns loaded: {len(self.learning_patterns)}")
    
    def _initialize_database(self):
        """Initialize database connection"""
        try:
            self.db = Prisma()
            self.logger.info("📊 AI Feedback Loop database connected")
        except Exception as e:
            self.logger.error(f"❌ Database connection failed: {e}")
            self.db = None
    
    def _initialize_analytics(self) -> Dict[str, Any]:
        """Initialize feedback analytics"""
        return {
            'total_feedback': 0,
            'feedback_by_type': {},
            'feedback_by_category': {},
            'feedback_by_source': {},
            'learning_patterns_created': 0,
            'improvements_suggested': 0,
            'success_rate_trends': {},
            'model_performance': {}
        }
    
    def _initialize_learning_rules(self) -> List[Dict[str, Any]]:
        """Initialize learning rules"""
        return [
            {
                'id': 'style_learning',
                'name': 'Style Learning',
                'description': 'Learn from style feedback',
                'trigger_types': [FeedbackType.STYLE, FeedbackType.REVISE],
                'min_confidence': 0.7,
                'min_samples': 3,
                'action': 'create_pattern',
                'is_active': True
            },
            {
                'id': 'factual_correction',
                'name': 'Factual Correction',
                'description': 'Learn from factual corrections',
                'trigger_types': [FeedbackType.CORRECT],
                'min_confidence': 0.8,
                'min_samples': 2,
                'action': 'update_knowledge',
                'is_active': True
            },
            {
                'id': 'tone_adjustment',
                'name': 'Tone Adjustment',
                'description': 'Adjust tone based on feedback',
                'trigger_types': [FeedbackType.REVISE, FeedbackType.IMPROVE],
                'min_confidence': 0.6,
                'min_samples': 5,
                'action': 'adjust_tone',
                'is_active': True
            },
            {
                'id': 'format_optimization',
                'name': 'Format Optimization',
                'description': 'Optimize response format',
                'trigger_types': [FeedbackType.REVISE, FeedbackType.IMPROVE],
                'min_confidence': 0.7,
                'min_samples': 4,
                'action': 'update_template',
                'is_active': True
            }
        ]
    
    def _initialize_default_patterns(self):
        """Initialize default learning patterns"""
        default_patterns = [
            LearningPattern(
                id="formal_business_tone",
                pattern_type=LearningCategory.TONE_ADJUSTMENT,
                pattern_description="Use formal business tone for professional inquiries",
                trigger_keywords=["bisnis", "profesional", "formal", "perusahaan"],
                response_template="Bapak/Ibu {name}, terima kasih atas pertanyaan Anda. Kami akan memberikan informasi yang profesional dan komprehensif mengenai {topic}.",
                success_rate=0.85,
                usage_count=0,
                last_updated=datetime.now(),
                is_active=True
            ),
            LearningPattern(
                id="casual_friendly_tone",
                pattern_type=LearningCategory.TONE_ADJUSTMENT,
                pattern_description="Use casual friendly tone for general inquiries",
                trigger_keywords=["tanya", "info", "cari", "harga"],
                response_template="Halo {name}! Senang bisa membantu Anda. Mari kita bahas tentang {topic} dengan cara yang mudah dimengerti.",
                success_rate=0.78,
                usage_count=0,
                last_updated=datetime.now(),
                is_active=True
            ),
            LearningPattern(
                id="property_detail_format",
                pattern_type=LearningCategory.RESPONSE_FORMAT,
                pattern_description="Format property details consistently",
                trigger_keywords=["properti", "rumah", "detail", "spek"],
                response_template="🏠 **{property_name}**\n\n📍 Lokasi: {location}\n💰 Harga: {price}\n📐 Luas: {size}\n🛋️ Fasilitas: {facilities}\n\nHubungi kami untuk info lebih lanjut!",
                success_rate=0.92,
                usage_count=0,
                last_updated=datetime.now(),
                is_active=True
            )
        ]
        
        for pattern in default_patterns:
            self.learning_patterns[pattern.id] = pattern
    
    async def record_feedback(self, task_id: str, model_used: str, original_prompt: str,
                            original_response: str, feedback_type: FeedbackType,
                            feedback_source: FeedbackSource, feedback_content: str,
                            revised_response: Optional[str] = None,
                            user_id: str = "system", session_id: str = "system") -> str:
        """
        Record feedback for AI learning
        
        Args:
            task_id: ID of the original task
            model_used: AI model used
            original_prompt: Original prompt sent to AI
            original_response: Original AI response
            feedback_type: Type of feedback
            feedback_source: Source of feedback
            feedback_content: Feedback content
            revised_response: Revised response (if any)
            user_id: User providing feedback
            session_id: Session ID
            
        Returns:
            str: Feedback record ID
        """
        try:
            # Generate feedback ID
            feedback_id = f"fb_{int(datetime.now().timestamp() * 1000000)}"
            
            # Categorize feedback
            learning_category = self._categorize_feedback(feedback_type, feedback_content)
            
            # Calculate confidence score
            confidence_score = self._calculate_confidence_score(feedback_type, feedback_content)
            
            # Create feedback record
            feedback_record = FeedbackRecord(
                id=feedback_id,
                task_id=task_id,
                model_used=model_used,
                original_prompt=original_prompt,
                original_response=original_response,
                feedback_type=feedback_type,
                feedback_source=feedback_source,
                feedback_content=feedback_content,
                revised_response=revised_response,
                learning_category=learning_category,
                confidence_score=confidence_score,
                user_id=user_id,
                session_id=session_id,
                created_at=datetime.now(),
                applied_at=None
            )
            
            # Store feedback
            self.feedback_records.append(feedback_record)
            
            # Update analytics
            self._update_analytics(feedback_record)
            
            # Save to database
            if self.db:
                await self._save_feedback_record(feedback_record)
            
            # Trigger learning process
            await self._process_feedback_learning(feedback_record)
            
            self.logger.info(f"📝 Feedback recorded: {feedback_id} - {feedback_type.value}")
            self.logger.info(f"🎯 Category: {learning_category.value}, Confidence: {confidence_score:.2f}")
            
            return feedback_id
            
        except Exception as e:
            self.logger.error(f"❌ Failed to record feedback: {e}")
            return ""
    
    async def _process_feedback_learning(self, feedback: FeedbackRecord):
        """Process feedback for learning"""
        try:
            # Check if feedback meets learning criteria
            learning_rule = self._find_applicable_learning_rule(feedback)
            if not learning_rule:
                return
            
            # Check minimum confidence
            if feedback.confidence_score < learning_rule['min_confidence']:
                return
            
            # Check minimum samples
            similar_feedback = self._find_similar_feedback(feedback)
            if len(similar_feedback) < learning_rule['min_samples']:
                return
            
            # Apply learning action
            if learning_rule['action'] == 'create_pattern':
                await self._create_learning_pattern(feedback, similar_feedback)
            elif learning_rule['action'] == 'update_knowledge':
                await self._update_knowledge_base(feedback, similar_feedback)
            elif learning_rule['action'] == 'adjust_tone':
                await self._adjust_response_tone(feedback, similar_feedback)
            elif learning_rule['action'] == 'update_template':
                await self._update_response_template(feedback, similar_feedback)
            
            # Mark feedback as applied
            feedback.applied_at = datetime.now()
            
            # Update in database
            if self.db:
                await self._update_feedback_applied(feedback.id)
            
        except Exception as e:
            self.logger.error(f"❌ Failed to process feedback learning: {e}")
    
    async def _create_learning_pattern(self, feedback: FeedbackRecord, similar_feedback: List[FeedbackRecord]):
        """Create learning pattern from feedback"""
        try:
            # Extract common patterns
            common_keywords = self._extract_common_keywords(similar_feedback)
            pattern_description = self._generate_pattern_description(feedback, similar_feedback)
            response_template = self._generate_response_template(similar_feedback)
            
            # Create pattern
            pattern_id = f"pattern_{int(datetime.now().timestamp() * 1000000)}"
            learning_pattern = LearningPattern(
                id=pattern_id,
                pattern_type=feedback.learning_category,
                pattern_description=pattern_description,
                trigger_keywords=common_keywords,
                response_template=response_template,
                success_rate=0.0,  # Will be updated based on usage
                usage_count=0,
                last_updated=datetime.now(),
                is_active=True
            )
            
            # Store pattern
            self.learning_patterns[pattern_id] = learning_pattern
            
            # Save to database
            if self.db:
                await self._save_learning_pattern(learning_pattern)
            
            # Update analytics
            self.feedback_analytics['learning_patterns_created'] += 1
            
            self.logger.info(f"🎯 Learning pattern created: {pattern_id}")
            self.logger.info(f"📝 Description: {pattern_description}")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to create learning pattern: {e}")
    
    async def _update_knowledge_base(self, feedback: FeedbackRecord, similar_feedback: List[FeedbackRecord]):
        """Update knowledge base from factual corrections"""
        try:
            # Extract corrected facts
            corrections = self._extract_factual_corrections(similar_feedback)
            
            # Create improvement suggestion
            improvement_id = f"improve_{int(datetime.now().timestamp() * 1000000)}"
            improvement = AIImprovement(
                id=improvement_id,
                category=LearningCategory.FACTUAL_ACCURACY,
                improvement_type="knowledge_update",
                description=f"Update knowledge base with corrections: {corrections}",
                implementation_code=f"# Update knowledge\nknowledge_base.update({corrections})",
                priority=8,  # High priority for factual accuracy
                estimated_impact=0.9,
                created_at=datetime.now(),
                implemented_at=None
            )
            
            # Store improvement
            self.ai_improvements.append(improvement)
            
            # Save to database
            if self.db:
                await self._save_ai_improvement(improvement)
            
            # Update analytics
            self.feedback_analytics['improvements_suggested'] += 1
            
            self.logger.info(f"🧠 Knowledge update suggested: {improvement_id}")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to update knowledge base: {e}")
    
    async def _adjust_response_tone(self, feedback: FeedbackRecord, similar_feedback: List[FeedbackRecord]):
        """Adjust response tone based on feedback"""
        try:
            # Analyze tone preferences
            tone_preferences = self._analyze_tone_preferences(similar_feedback)
            
            # Create improvement suggestion
            improvement_id = f"tone_{int(datetime.now().timestamp() * 1000000)}"
            improvement = AIImprovement(
                id=improvement_id,
                category=LearningCategory.TONE_ADJUSTMENT,
                improvement_type="tone_adjustment",
                description=f"Adjust tone to: {tone_preferences}",
                implementation_code=f"# Adjust tone\ntone.set_{tone_preferences}()",
                priority=5,
                estimated_impact=0.7,
                created_at=datetime.now(),
                implemented_at=None
            )
            
            # Store improvement
            self.ai_improvements.append(improvement)
            
            # Save to database
            if self.db:
                await self._save_ai_improvement(improvement)
            
            # Update analytics
            self.feedback_analytics['improvements_suggested'] += 1
            
            self.logger.info(f"🎭 Tone adjustment suggested: {improvement_id}")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to adjust response tone: {e}")
    
    async def _update_response_template(self, feedback: FeedbackRecord, similar_feedback: List[FeedbackRecord]):
        """Update response template based on feedback"""
        try:
            # Generate improved template
            improved_template = self._generate_improved_template(similar_feedback)
            
            # Create improvement suggestion
            improvement_id = f"template_{int(datetime.now().timestamp() * 1000000)}"
            improvement = AIImprovement(
                id=improvement_id,
                category=LearningCategory.RESPONSE_FORMAT,
                improvement_type="template_update",
                description=f"Update response template: {improved_template[:100]}...",
                implementation_code=f"# Update template\ntemplates.set('{feedback.learning_category.value}', '{improved_template}')",
                priority=6,
                estimated_impact=0.8,
                created_at=datetime.now(),
                implemented_at=None
            )
            
            # Store improvement
            self.ai_improvements.append(improvement)
            
            # Save to database
            if self.db:
                await self._save_ai_improvement(improvement)
            
            # Update analytics
            self.feedback_analytics['improvements_suggested'] += 1
            
            self.logger.info(f"📋 Template update suggested: {improvement_id}")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to update response template: {e}")
    
    def _categorize_feedback(self, feedback_type: FeedbackType, feedback_content: str) -> LearningCategory:
        """Categorize feedback into learning category"""
        content_lower = feedback_content.lower()
        
        if feedback_type == FeedbackType.STYLE:
            return LearningCategory.CONTENT_STYLE
        elif feedback_type == FeedbackType.CORRECT:
            return LearningCategory.FACTUAL_ACCURACY
        elif feedback_type == FeedbackType.REVISE:
            if any(word in content_lower for word in ["format", "struktur", "template"]):
                return LearningCategory.RESPONSE_FORMAT
            elif any(word in content_lower for word in ["tone", "gayabahasa", "santai", "formal"]):
                return LearningCategory.TONE_ADJUSTMENT
            else:
                return LearningCategory.CONTENT_STYLE
        elif feedback_type == FeedbackType.IMPROVE:
            if "personalisasi" in content_lower or "nama" in content_lower:
                return LearningCategory.PERSONALIZATION
            elif "aturan" in content_lower or "kebijakan" in content_lower:
                return LearningCategory.COMPLIANCE
            else:
                return LearningCategory.CONTENT_STYLE
        else:
            return LearningCategory.CONTENT_STYLE
    
    def _calculate_confidence_score(self, feedback_type: FeedbackType, feedback_content: str) -> float:
        """Calculate confidence score for feedback"""
        base_score = 0.5
        
        # Adjust based on feedback type
        if feedback_type == FeedbackType.CORRECT:
            base_score += 0.3
        elif feedback_type == FeedbackType.REVISE:
            base_score += 0.2
        elif feedback_type == FeedbackType.IMPROVE:
            base_score += 0.1
        
        # Adjust based on content detail
        content_length = len(feedback_content.split())
        if content_length > 10:
            base_score += 0.1
        if content_length > 20:
            base_score += 0.1
        
        # Adjust based on specificity
        specific_indicators = ["contoh", "seperti", "misalnya", "ganti dengan", "ubah menjadi"]
        if any(indicator in feedback_content.lower() for indicator in specific_indicators):
            base_score += 0.1
        
        return min(1.0, base_score)
    
    def _find_applicable_learning_rule(self, feedback: FeedbackRecord) -> Optional[Dict[str, Any]]:
        """Find applicable learning rule for feedback"""
        for rule in self.learning_rules:
            if (rule['is_active'] and 
                feedback.feedback_type in rule['trigger_types'] and
                feedback.confidence_score >= rule['min_confidence']):
                return rule
        return None
    
    def _find_similar_feedback(self, feedback: FeedbackRecord) -> List[FeedbackRecord]:
        """Find similar feedback records"""
        similar = []
        
        for record in self.feedback_records:
            if (record.id != feedback.id and
                record.learning_category == feedback.learning_category and
                record.feedback_type == feedback.feedback_type):
                
                # Check content similarity
                if self._calculate_content_similarity(feedback.feedback_content, record.feedback_content) > 0.6:
                    similar.append(record)
        
        return similar
    
    def _calculate_content_similarity(self, content1: str, content2: str) -> float:
        """Calculate similarity between two content strings"""
        words1 = set(content1.lower().split())
        words2 = set(content2.lower().split())
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _extract_common_keywords(self, feedback_list: List[FeedbackRecord]) -> List[str]:
        """Extract common keywords from feedback"""
        all_words = []
        for feedback in feedback_list:
            all_words.extend(feedback.feedback_content.lower().split())
        
        # Count word frequency
        word_count = {}
        for word in all_words:
            if len(word) > 3:  # Ignore short words
                word_count[word] = word_count.get(word, 0) + 1
        
        # Get most common words
        sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
        
        # Return top keywords
        return [word for word, count in sorted_words[:5] if count > 1]
    
    def _generate_pattern_description(self, feedback: FeedbackRecord, similar_feedback: List[FeedbackRecord]) -> str:
        """Generate pattern description"""
        category = feedback.learning_category.value.replace("_", " ").title()
        
        # Extract key themes
        all_feedback = similar_feedback + [feedback]
        themes = self._extract_common_keywords(all_feedback)
        
        return f"Use {category.lower()} when dealing with: {', '.join(themes)}"
    
    def _generate_response_template(self, feedback_list: List[FeedbackRecord]) -> str:
        """Generate response template from feedback"""
        # Find the best revised response
        best_response = None
        best_score = 0.0
        
        for feedback in feedback_list:
            if feedback.revised_response and feedback.confidence_score > best_score:
                best_response = feedback.revised_response
                best_score = feedback.confidence_score
        
        if best_response:
            return best_response
        
        # Generate template from original responses
        return "Template generated from feedback patterns"
    
    def _extract_factual_corrections(self, feedback_list: List[FeedbackRecord]) -> str:
        """Extract factual corrections from feedback"""
        corrections = []
        
        for feedback in feedback_list:
            if "salah" in feedback.feedback_content.lower() or "benar" in feedback.feedback_content.lower():
                corrections.append(feedback.feedback_content)
        
        return "; ".join(corrections)
    
    def _analyze_tone_preferences(self, feedback_list: List[FeedbackRecord]) -> str:
        """Analyze tone preferences from feedback"""
        tone_indicators = {
            "formal": ["formal", "profesional", "bisnis", "resmi"],
            "casual": ["santai", "biasa", "sederhana", "ramah"],
            "friendly": ["ramah", "hangat", "ceria", "positif"],
            "empathetic": ["empati", "paham", "simpati", "peduli"]
        }
        
        tone_scores = {}
        for feedback in feedback_list:
            content = feedback.feedback_content.lower()
            for tone, indicators in tone_indicators.items():
                if any(indicator in content for indicator in indicators):
                    tone_scores[tone] = tone_scores.get(tone, 0) + 1
        
        # Return tone with highest score
        if tone_scores:
            return max(tone_scores, key=tone_scores.get)
        
        return "neutral"
    
    def _generate_improved_template(self, feedback_list: List[FeedbackRecord]) -> str:
        """Generate improved template from feedback"""
        # Combine insights from multiple feedback
        insights = []
        
        for feedback in feedback_list:
            if feedback.revised_response:
                insights.append(feedback.revised_response)
        
        if insights:
            return " ".join(insights)
        
        return "Improved template based on feedback analysis"
    
    def _update_analytics(self, feedback: FeedbackRecord):
        """Update feedback analytics"""
        self.feedback_analytics['total_feedback'] += 1
        
        # Update by type
        ftype = feedback.feedback_type.value
        self.feedback_analytics['feedback_by_type'][ftype] = self.feedback_analytics['feedback_by_type'].get(ftype, 0) + 1
        
        # Update by category
        category = feedback.learning_category.value
        self.feedback_analytics['feedback_by_category'][category] = self.feedback_analytics['feedback_by_category'].get(category, 0) + 1
        
        # Update by source
        source = feedback.feedback_source.value
        self.feedback_analytics['feedback_by_source'][source] = self.feedback_analytics['feedback_by_source'].get(source, 0) + 1
    
    async def get_learning_report(self, days: int = 30) -> Dict[str, Any]:
        """Generate learning report"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            # Filter recent feedback
            recent_feedback = [f for f in self.feedback_records if f.created_at >= cutoff_date]
            
            # Calculate metrics
            total_feedback = len(recent_feedback)
            applied_feedback = len([f for f in recent_feedback if f.applied_at])
            application_rate = (applied_feedback / total_feedback * 100) if total_feedback > 0 else 0
            
            # Pattern usage
            pattern_usage = {}
            for pattern in self.learning_patterns.values():
                if pattern.last_updated >= cutoff_date:
                    pattern_usage[pattern.id] = {
                        'usage_count': pattern.usage_count,
                        'success_rate': pattern.success_rate
                    }
            
            # Improvement suggestions
            recent_improvements = [i for i in self.ai_improvements if i.created_at >= cutoff_date]
            
            return {
                'period_days': days,
                'total_feedback': total_feedback,
                'applied_feedback': applied_feedback,
                'application_rate': application_rate,
                'active_patterns': len(pattern_usage),
                'pattern_usage': pattern_usage,
                'improvements_suggested': len(recent_improvements),
                'learning_patterns_total': len(self.learning_patterns),
                'ai_improvements_total': len(self.ai_improvements)
            }
            
        except Exception as e:
            self.logger.error(f"❌ Failed to generate learning report: {e}")
            return {}
    
    async def apply_learning_pattern(self, pattern_id: str, prompt: str) -> Optional[str]:
        """Apply learning pattern to prompt"""
        try:
            pattern = self.learning_patterns.get(pattern_id)
            if not pattern or not pattern.is_active:
                return None
            
            # Check if prompt matches pattern
            if not self._prompt_matches_pattern(prompt, pattern):
                return None
            
            # Apply pattern
            response = pattern.response_template
            
            # Update usage
            pattern.usage_count += 1
            pattern.last_updated = datetime.now()
            
            # Save to database
            if self.db:
                await self._update_pattern_usage(pattern_id)
            
            self.logger.info(f"🎯 Learning pattern applied: {pattern_id}")
            
            return response
            
        except Exception as e:
            self.logger.error(f"❌ Failed to apply learning pattern: {e}")
            return None
    
    def _prompt_matches_pattern(self, prompt: str, pattern: LearningPattern) -> bool:
        """Check if prompt matches learning pattern"""
        prompt_lower = prompt.lower()
        
        # Check trigger keywords
        for keyword in pattern.trigger_keywords:
            if keyword in prompt_lower:
                return True
        
        return False
    
    async def _save_feedback_record(self, feedback: FeedbackRecord):
        """Save feedback record to database"""
        try:
            # This would save to the actual database
            self.logger.debug(f"📝 Feedback record saved: {feedback.id}")
        except Exception as e:
            self.logger.error(f"❌ Failed to save feedback record: {e}")
    
    async def _save_learning_pattern(self, pattern: LearningPattern):
        """Save learning pattern to database"""
        try:
            # This would save to the actual database
            self.logger.debug(f"🎯 Learning pattern saved: {pattern.id}")
        except Exception as e:
            self.logger.error(f"❌ Failed to save learning pattern: {e}")
    
    async def _save_ai_improvement(self, improvement: AIImprovement):
        """Save AI improvement to database"""
        try:
            # This would save to the actual database
            self.logger.debug(f"🧠 AI improvement saved: {improvement.id}")
        except Exception as e:
            self.logger.error(f"❌ Failed to save AI improvement: {e}")
    
    async def _update_feedback_applied(self, feedback_id: str):
        """Update feedback as applied"""
        try:
            # This would update the actual database
            self.logger.debug(f"📝 Feedback updated as applied: {feedback_id}")
        except Exception as e:
            self.logger.error(f"❌ Failed to update feedback applied: {e}")
    
    async def _update_pattern_usage(self, pattern_id: str):
        """Update pattern usage in database"""
        try:
            # This would update the actual database
            self.logger.debug(f"🎯 Pattern usage updated: {pattern_id}")
        except Exception as e:
            self.logger.error(f"❌ Failed to update pattern usage: {e}")

# Global AI feedback loop instance
ai_feedback_loop = AIFeedbackLoop()
