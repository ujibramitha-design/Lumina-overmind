"""
DOOM SENTINEL - AI Guardrails & Safety Controls
Output validation, safety constraints, and hallucination prevention
"""

import os
import logging
import re
import json
from typing import Dict, Any, Optional, List
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RiskLevel(Enum):
    """Risk level for AI responses"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class ValidationResult:
    """AI output validation result"""
    is_safe: bool
    risk_level: RiskLevel
    violations: List[str]
    warnings: List[str]
    sanitized_output: str
    confidence_score: float

class AIGuardrails:
    """
    AI Safety Guardrails System
    Validates AI outputs and prevents hallucinations/false promises
    """
    
    def __init__(self):
        """Initialize AI guardrails"""
        self.logger = logging.getLogger(__name__)
        
        # Safety constraints
        self.forbidden_topics = [
            'illegal activities', 'violence', 'hate speech', 'discrimination',
            'medical advice', 'legal advice', 'financial advice'
        ]
        
        # False promise patterns
        self.false_promise_patterns = [
            r'gratis\s+100%',
            r'gratis\s+dp',
            r'tanpa\s+dp',
            r'tanpa\s+biaya',
            r'dijamin\s+disetujui',
            r'pasti\s+disetujui',
            r'100%\s+disetujui',
            r'jamin\s+lulus',
            r'pasti\s+lulus',
            r'garansi\s+sukses'
        ]
        
        # Price validation patterns
        self.price_patterns = [
            r'rp\s*(\d+(?:\.\d+)?)\s*(?:juta|miliar|ribu)',
            r'(\d+(?:\.\d+)?)\s*(?:juta|miliar|ribu)\s*rupiah',
            r'harga\s*(?:rp|rupiah)?\s*(\d+(?:\.\d+)?)',
            r'cicilan\s*(?:rp|rupiah)?\s*(\d+(?:\.\d+)?)'
        ]
        
        # Project data validation
        self.required_project_fields = [
            'nama_proyek', 'tipe_proyek', 'lokasi', 'harga_start', 
            'target_market', 'is_active'
        ]
        
        # Safety prompts
        self.safety_prompt = """
        SAFETY INSTRUCTIONS:
        1. NEVER make promises about pricing, financing, or approval
        2. NEVER use absolute language (100%, guaranteed, always)
        3. NEVER provide medical, legal, or financial advice
        4. ALWAYS use cautious language (typically, usually, may)
        5. ALWAYS refer to official sources for accurate information
        6. NEVER invent specific numbers or dates
        7. ALWAYS include disclaimer about verification
        """
        
        self.logger.info("🛡️ AI Guardrails initialized")
        self.logger.info(f"⚠️ Forbidden topics: {len(self.forbidden_topics)}")
        self.logger.info(f"🚫 False promise patterns: {len(self.false_promise_patterns)}")
    
    def validate_ai_output(self, ai_output: str, project_data: Dict[str, Any] = None) -> ValidationResult:
        """
        Validate AI output for safety and accuracy
        
        Args:
            ai_output: AI generated text
            project_data: Project data for validation context
            
        Returns:
            ValidationResult: Validation results with safety assessment
        """
        try:
            violations = []
            warnings = []
            sanitized_output = ai_output
            risk_level = RiskLevel.LOW
            
            # Check for forbidden topics
            topic_violations = self._check_forbidden_topics(ai_output)
            violations.extend(topic_violations)
            
            # Check for false promises
            promise_violations = self._check_false_promises(ai_output)
            violations.extend(promise_violations)
            
            # Validate pricing information
            price_violations, price_warnings = self._validate_pricing_info(ai_output, project_data)
            violations.extend(price_violations)
            warnings.extend(price_warnings)
            
            # Check for absolute language
            absolute_violations = self._check_absolute_language(ai_output)
            violations.extend(absolute_violations)
            
            # Validate against project data
            if project_data:
                data_violations = self._validate_against_project_data(ai_output, project_data)
                violations.extend(data_violations)
            
            # Sanitize output
            sanitized_output = self._sanitize_output(ai_output, violations)
            
            # Determine risk level
            risk_level = self._calculate_risk_level(len(violations), len(warnings))
            
            # Calculate confidence score
            confidence_score = self._calculate_confidence_score(len(violations), len(warnings))
            
            return ValidationResult(
                is_safe=len(violations) == 0,
                risk_level=risk_level,
                violations=violations,
                warnings=warnings,
                sanitized_output=sanitized_output,
                confidence_score=confidence_score
            )
            
        except Exception as e:
            self.logger.error(f"❌ AI output validation failed: {e}")
            return ValidationResult(
                is_safe=False,
                risk_level=RiskLevel.CRITICAL,
                violations=["Validation error"],
                warnings=[],
                sanitized_output=ai_output,
                confidence_score=0.0
            )
    
    def _check_forbidden_topics(self, text: str) -> List[str]:
        """Check for forbidden topics in text"""
        violations = []
        text_lower = text.lower()
        
        for topic in self.forbidden_topics:
            if topic in text_lower:
                violations.append(f"Forbidden topic detected: {topic}")
        
        return violations
    
    def _check_false_promises(self, text: str) -> List[str]:
        """Check for false promises in text"""
        violations = []
        text_lower = text.lower()
        
        for pattern in self.false_promise_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                violations.append(f"False promise detected: {pattern}")
        
        return violations
    
    def _validate_pricing_info(self, text: str, project_data: Dict[str, Any] = None) -> tuple[List[str], List[str]]:
        """Validate pricing information against project data"""
        violations = []
        warnings = []
        
        # Extract prices from text
        extracted_prices = []
        for pattern in self.price_patterns:
            matches = re.findall(pattern, text.lower())
            extracted_prices.extend(matches)
        
        # Validate against project data
        if project_data and extracted_prices:
            project_price = project_data.get('harga_start', 0)
            
            for price_str in extracted_prices:
                try:
                    # Convert price string to number
                    price_num = self._parse_price_string(price_str)
                    
                    if price_num > 0:
                        # Check if price is reasonable compared to project
                        if project_price > 0:
                            price_ratio = price_num / project_price
                            
                            # Flag suspicious pricing
                            if price_ratio < 0.5:
                                warnings.append(f"Price too low: {price_str} (should be ~{project_price})")
                            elif price_ratio > 2.0:
                                warnings.append(f"Price too high: {price_str} (should be ~{project_price})")
                        
                        # Flag unrealistic prices
                        if price_num < 1000000:  # Less than 1 million
                            warnings.append(f"Unrealistically low price: {price_str}")
                        elif price_num > 10000000000:  # More than 10 billion
                            warnings.append(f"Unrealistically high price: {price_str}")
                
                except Exception as e:
                    warnings.append(f"Price parsing error: {price_str}")
        
        return violations, warnings
    
    def _parse_price_string(self, price_str: str) -> float:
        """Parse price string to number"""
        try:
            # Remove non-numeric characters
            clean_price = re.sub(r'[^\d.]', '', price_str)
            
            if not clean_price:
                return 0.0
            
            price_num = float(clean_price)
            
            # Handle multipliers
            if 'juta' in price_str.lower():
                price_num *= 1000000
            elif 'miliar' in price_str.lower():
                price_num *= 1000000000
            elif 'ribu' in price_str.lower():
                price_num *= 1000
            
            return price_num
            
        except Exception:
            return 0.0
    
    def _check_absolute_language(self, text: str) -> List[str]:
        """Check for absolute language that should be avoided"""
        violations = []
        text_lower = text.lower()
        
        absolute_patterns = [
            r'100%',
            r'pasti\s+(?:akan|bisa|disetujui)',
            r'jamin\s+(?:akan|bisa|disetujui)',
            r'tentu\s+(?:akan|bisa|disetujui)',
            r'selalu\s+(?:berhasil|disetujui)',
            r'pasti\s+(?:berhasil|disetujui)'
        ]
        
        for pattern in absolute_patterns:
            if re.search(pattern, text_lower):
                violations.append(f"Absolute language detected: {pattern}")
        
        return violations
    
    def _validate_against_project_data(self, text: str, project_data: Dict[str, Any]) -> List[str]:
        """Validate text against actual project data"""
        violations = []
        
        # Check project name
        project_name = project_data.get('nama_proyek', '')
        if project_name and project_name.lower() not in text.lower():
            violations.append("Project name not mentioned in response")
        
        # Check project type
        project_type = project_data.get('tipe_proyek', '')
        if project_type and project_type.lower() not in text.lower():
            violations.append("Project type not mentioned in response")
        
        # Check location
        location = project_data.get('lokasi', '')
        if location and location.lower() not in text.lower():
            violations.append("Project location not mentioned in response")
        
        return violations
    
    def _sanitize_output(self, text: str, violations: List[str]) -> str:
        """Sanitize AI output by removing problematic content"""
        sanitized = text
        
        # Replace absolute language with cautious alternatives
        replacements = {
            r'100%': 'biasanya',
            r'pasti\s+akan': 'mungkin akan',
            r'jamin\s+akan': 'cenderung akan',
            r'tentu\s+akan': 'kemungkinan akan',
            r'selalu\s+berhasil': 'sering berhasil',
            r'gratis\s+100%': 'dengan syarat tertentu',
            r'tanpa\s+dp': 'dengan dp minimal',
            r'dijamin\s+disetujui': 'memiliki peluang baik untuk disetujui'
        }
        
        for pattern, replacement in replacements.items():
            sanitized = re.sub(pattern, replacement, sanitized, flags=re.IGNORECASE)
        
        # Add safety disclaimer if violations detected
        if violations:
            disclaimer = "\n\n*Catatan: Informasi di atas bersifat estimasi. Untuk detail akurat, silakan hubungi konsultan properti kami.*"
            sanitized += disclaimer
        
        return sanitized
    
    def _calculate_risk_level(self, violations_count: int, warnings_count: int) -> RiskLevel:
        """Calculate risk level based on violations and warnings"""
        if violations_count >= 3:
            return RiskLevel.CRITICAL
        elif violations_count >= 2:
            return RiskLevel.HIGH
        elif violations_count >= 1 or warnings_count >= 3:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW
    
    def _calculate_confidence_score(self, violations_count: int, warnings_count: int) -> float:
        """Calculate confidence score (0-1)"""
        total_issues = violations_count + (warnings_count * 0.5)
        max_score = 10.0  # Maximum expected issues
        
        score = max(0.0, 1.0 - (total_issues / max_score))
        return round(score, 2)
    
    def generate_safety_prompt(self, project_data: Dict[str, Any] = None) -> str:
        """Generate safety-prompt for AI system"""
        base_prompt = self.safety_prompt
        
        if project_data:
            project_context = f"""
            PROJECT CONTEXT:
            - Project Name: {project_data.get('nama_proyek', 'Unknown')}
            - Project Type: {project_data.get('tipe_proyek', 'Unknown')}
            - Location: {project_data.get('lokasi', 'Unknown')}
            - Starting Price: Rp {project_data.get('harga_start', 0):,}
            - Target Market: {project_data.get('target_market', 'Unknown')}
            
            ADDITIONAL CONSTRAINTS:
            1. Only mention prices that are in the project data
            2. Use the exact project name and location from data
            3. Refer to actual project type (KOMERSIL/SUBSIDI)
            4. Do not invent features or amenities not in project
            5. Use cautious language for financing options
            """
            
            return base_prompt + project_context
        
        return base_prompt
    
    def get_validation_summary(self, validation_result: ValidationResult) -> str:
        """Generate human-readable validation summary"""
        summary = f"🛡️ **AI Output Validation**\n\n"
        
        # Safety status
        status_emoji = "✅" if validation_result.is_safe else "⚠️"
        summary += f"{status_emoji} **Safety Status**: {validation_result.risk_level.value.upper()}\n"
        summary += f"📊 **Confidence Score**: {validation_result.confidence_score:.2f}/1.0\n\n"
        
        # Violations
        if validation_result.violations:
            summary += "🚨 **Violations**:\n"
            for violation in validation_result.violations:
                summary += f"• {violation}\n"
            summary += "\n"
        
        # Warnings
        if validation_result.warnings:
            summary += "⚠️ **Warnings**:\n"
            for warning in validation_result.warnings:
                summary += f"• {warning}\n"
            summary += "\n"
        
        # Sanitized output
        if validation_result.sanitized_output != validation_result.sanitized_output:
            summary += "**Sanitized Output Available**: Yes\n\n"
        
        return summary
    
    async def log_validation_result(self, validation_result: ValidationResult, context: str = ""):
        """Log validation result for monitoring"""
        try:
            log_data = {
                'timestamp': datetime.now().isoformat(),
                'is_safe': validation_result.is_safe,
                'risk_level': validation_result.risk_level.value,
                'violations_count': len(validation_result.violations),
                'warnings_count': len(validation_result.warnings),
                'confidence_score': validation_result.confidence_score,
                'context': context
            }
            
            # Log to file
            with open('logs/ai_guardrails.log', 'a') as f:
                f.write(json.dumps(log_data) + '\n')
            
            # Send alert if high risk
            if validation_result.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
                from .doom_sentinel.alert_system import AlertSystem
                alert_system = AlertSystem()
                await alert_system.send_custom_alert(
                    "AI Safety Alert",
                    f"High-risk AI output detected: {validation_result.risk_level.value}",
                    "warning"
                )
            
        except Exception as e:
            self.logger.error(f"❌ Validation logging failed: {e}")

# Global AI guardrails instance
ai_guardrails = AIGuardrails()
