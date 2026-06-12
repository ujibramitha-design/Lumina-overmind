"""
LUMINA OS - PROJECT HIVEMIND
====================================

Multi-Agent VVIP Strategy System
Simulated Multi-Agent Intelligence with Prompt Chaining

Features:
- Multi-Agent Simulation with Prompt Chaining
- VVIP Prospect Analysis
- Agent Specialization (Data Analyst, Psychologist, Negotiator)
- Strategic Briefing Generation
- Executive Decision Support
"""

import os
import sys
import json
import time
import logging
import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime
from dataclasses import dataclass, asdict
from pathlib import Path

# Add root directory to Python path
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(root_dir)

# Import required modules
try:
    import google.generativeai as genai
    from core_modules.db_manager_supabase import get_supabase_manager
    from core_modules.notifications.telegram_sender import get_telegram_sender
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Installing required packages...")
    os.system("pip install google-generativeai")
    print("Please restart the script after installation")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ANSI color codes for terminal output
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
BOLD = '\033[1m'
END = '\033[0m'

@dataclass
class AgentAnalysis:
    """Agent analysis result structure"""
    agent_name: str
    analysis_type: str
    insights: Dict[str, Any]
    recommendations: List[str]
    confidence_score: float
    processing_time: float
    created_at: datetime

@dataclass
class VVIPBriefing:
    """VVIP Executive Briefing structure"""
    prospect_id: str
    prospect_name: str
    prospect_data: Dict[str, Any]
    data_analysis: AgentAnalysis
    psychology_analysis: AgentAnalysis
    negotiation_strategy: AgentAnalysis
    executive_summary: str
    tactical_steps: List[str]
    discount_limits: Dict[str, float]
    closing_probability: float
    created_at: datetime
    total_processing_time: float

class HivemindSwarm:
    """
    Project Hivemind - Multi-Agent VVIP Strategy System
    Simulated multi-agent intelligence with prompt chaining for VVIP prospect analysis
    """
    
    def __init__(self):
        """Initialize Hivemind Swarm"""
        self.logger = logging.getLogger(__name__)
        
        # Initialize Gemini
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.gemini_model = genai.GenerativeModel('gemini-pro')
            self.logger.info(f"{GREEN}✅ Gemini initialized for multi-agent analysis{END}")
        else:
            self.gemini_model = None
            self.logger.warning(f"{YELLOW}⚠️ Gemini API key not found - using fallback analysis{END}")
        
        # Initialize database
        try:
            self.supabase_manager = get_supabase_manager()
            self.logger.info(f"{GREEN}✅ Database connected for VVIP analysis{END}")
        except Exception as e:
            self.supabase_manager = None
            self.logger.error(f"{RED}❌ Database connection failed: {e}{END}")
        
        # Initialize Telegram sender
        try:
            self.telegram_sender = get_telegram_sender()
            self.logger.info(f"{GREEN}✅ Telegram sender initialized for VVIP notifications{END}")
        except Exception as e:
            self.telegram_sender = None
            self.logger.error(f"{RED}❌ Telegram sender failed: {e}{END}")
        
        # Agent configurations
        self.agents = {
            "data_analyst": {
                "name": "Data Intelligence Analyst",
                "role": "Intelligence and Data Analysis",
                "expertise": ["financial analysis", "background verification", "risk assessment", "data intelligence"],
                "prompt_template": """
                Sebagai Analis Intelijen Data ahli, bedah latar belakang dan kapasitas finansial prospek ini secara mendalam:
                
                DATA PROSPEK:
                {prospect_data}
                
                Lakukan analisis komprehensif meliputi:
                1. **Analisis Kapasitas Finansial**:
                   - Estimasi pendapatan berdasarkan profesi dan lokasi
                   - Potensi pembelian (cash vs KPR)
                   - Risiko finansial dan kemampuan bayar
                
                2. **Background Intelligence**:
                   - Verifikasi profesi dan perusahaan
                   - Analisis lokasi dan area tinggal
                   - Indikator status sosial dan ekonomi
                
                3. **Risk Assessment**:
                   - Tingkat risiko transaksi
                   - Potensi masalah pembayaran
                   - Red flags yang perlu diwaspadai
                
                4. **Opportunity Analysis**:
                   - Potensi upsell dan cross-sell
                   - Kemungkinan repeat business
                   - Jaringan dan referral potential
                
                Format output dalam JSON:
                {{
                    "financial_capacity": {{
                        "estimated_income": "Rp X/bulan",
                        "payment_method": "Cash/KPR/Campuran",
                        "affordability_score": 8.5,
                        "financial_risk": "Low/Medium/High"
                    }},
                    "background_intelligence": {{
                        "profession_verification": "Verified/Likely/Unverified",
                        "area_analysis": "Premium/Middle/Standard",
                        "social_status": "High/Middle/Low",
                        "credibility_score": 8.0
                    }},
                    "risk_assessment": {{
                        "transaction_risk": "Low/Medium/High",
                        "payment_risk": "Low/Medium/High", 
                        "red_flags": ["flag1", "flag2"],
                        "overall_risk_score": 2.5
                    }},
                    "opportunity_analysis": {{
                        "upsell_potential": "High/Medium/Low",
                        "repeat_business": "High/Medium/Low",
                        "referral_value": "High/Medium/Low",
                        "network_value": "High/Medium/Low"
                    }},
                    "key_insights": ["insight1", "insight2", "insight3"],
                    "confidence_score": 8.5
                }}
                """
            },
            "psychologist": {
                "name": "Behavioral Psychology Specialist",
                "role": "Psychological and Behavioral Analysis",
                "expertise": ["behavioral psychology", "communication analysis", "motivation profiling", "decision patterns"],
                "prompt_template": """
                Sebagai Psikolog Perilaku ahli, analisis data analisis intelijen ini dan tentukan cara komunikasi terbaik serta kelemahan emosional prospek:
                
                HASIL ANALISIS DATA:
                {data_analysis}
                
                Lakukan analisis psikologis mendalam:
                1. **Profil Psikologis**:
                   - Tipe kepribadian dominan
                   - Gaya pengambilan keputusan
                   - Motivasi utama pembelian
                   - Faktor pemicu emosional
                
                2. **Communication Strategy**:
                   - Gaya komunikasi yang paling efektif
                   - Bahasa dan tone yang disukai
                   - Topik yang harus dihindari
                   - Pendekatan yang optimal
                
                3. **Emotional Triggers**:
                   - Kelemahan emosional yang bisa dimanfaatkan
                   - Pemicu positif untuk closing
                   - Fear of missing out (FOMO) factors
                   - Status dan prestige drivers
                
                4. **Decision Making Pattern**:
                   - Proses pengambilan keputusan
                   - Influencers dalam keputusan
                   - Timeline untuk closing
                   - Resistance points
                
                Format output dalam JSON:
                {{
                    "psychological_profile": {{
                        "personality_type": "Analytical/Driver/Amiable/Expressive",
                        "decision_style": "Logical/Emotional/Mixed",
                        "primary_motivation": "Security/Status/Comfort/Investment",
                        "emotional_triggers": ["trigger1", "trigger2"]
                    }},
                    "communication_strategy": {{
                        "optimal_approach": "Direct/Consultative/Relationship",
                        "preferred_language": "Formal/Casual/Technical",
                        "tone": "Authoritative/Friendly/Professional",
                        "key_topics": ["topic1", "topic2"],
                        "avoid_topics": ["topic1", "topic2"]
                    }},
                    "emotional_leverage": {{
                        "weaknesses": ["weakness1", "weakness2"],
                        "positive_triggers": ["trigger1", "trigger2"],
                        "fomo_factors": ["factor1", "factor2"],
                        "status_drivers": ["driver1", "driver2"]
                    }},
                    "decision_pattern": {{
                        "process": "Quick/Deliberate/Consultative",
                        "influencers": ["influencer1", "influencer2"],
                        "closing_timeline": "Immediate/Weeks/Months",
                        "resistance_points": ["point1", "point2"]
                    }},
                    "psychological_insights": ["insight1", "insight2"],
                    "confidence_score": 8.0
                }}
                """
            },
            "master_negotiator": {
                "name": "Elite Executive Negotiator",
                "role": "Strategic Negotiation and Closing",
                "expertise": ["advanced negotiation", "closing strategies", "deal structuring", "executive persuasion"],
                "prompt_template": """
                Sebagai Direktur Penjualan elit, rumuskan strategi closing 3 langkah taktis berdasarkan analisis data dan psikologis ini:
                
                ANALISIS DATA:
                {data_analysis}
                
                ANALISIS PSIKOLOGIS:
                {psychology_analysis}
                
                Buat strategi closing yang presisi:
                1. **3-Step Tactical Approach**:
                   - Langkah 1: Opening dan value proposition
                   - Langkah 2: Negotiation dan objection handling  
                   - Langkah 3: Closing dan follow-up
                
                2. **Strategi Diskon**:
                   - Batas maksimal diskon yang bisa diberikan
                   - Strategi penawaran diskon (timing dan kondisi)
                   - Value trade-offs untuk mengurangi diskon
                   - Psikologis pricing strategy
                
                3. **Closing Tactics**:
                   - Teknik closing yang paling efektif
                   - Urgency creation methods
                   - Risk reversal strategies
                   - Final persuasion techniques
                
                4. **Executive Briefing**:
                   - Summary strategi untuk manajemen
                   - Resource requirements
                   - Success probability
                   - Contingency plans
                
                Format output dalam JSON:
                {{
                    "tactical_approach": {{
                        "step_1": {{
                            "objective": "Opening objective",
                            "method": "Opening method",
                            "key_messages": ["message1", "message2"],
                            "expected_outcome": "Expected outcome"
                        }},
                        "step_2": {{
                            "objective": "Negotiation objective", 
                            "method": "Negotiation method",
                            "objection_handling": ["objection1", "objection2"],
                            "expected_outcome": "Expected outcome"
                        }},
                        "step_3": {{
                            "objective": "Closing objective",
                            "method": "Closing method", 
                            "urgency_tactics": ["tactic1", "tactic2"],
                            "expected_outcome": "Expected outcome"
                        }}
                    }},
                    "discount_strategy": {{
                        "max_discount_percentage": 15.0,
                        "discount_triggers": ["trigger1", "trigger2"],
                        "value_trade_offs": ["tradeoff1", "tradeoff2"],
                        "psychological_pricing": "Pricing strategy",
                        "discount_timing": "Timing strategy"
                    }},
                    "closing_tactics": {{
                        "primary_technique": "Assumptive/Straight-line/Urgency",
                        "urgency_creation": ["method1", "method2"],
                        "risk_reversal": ["guarantee1", "guarantee2"],
                        "final_persuasion": ["technique1", "technique2"]
                    }},
                    "executive_briefing": {{
                        "strategy_summary": "Brief summary",
                        "resource_requirements": ["resource1", "resource2"],
                        "success_probability": 85.0,
                        "key_risks": ["risk1", "risk2"],
                        "contingency_plans": ["plan1", "plan2"]
                    }},
                    "negotiation_insights": ["insight1", "insight2"],
                    "confidence_score": 9.0
                }}
                """
            }
        }
        
        # VVIP threshold configuration
        self.vvip_thresholds = {
            "min_income_estimate": 50000000,  # Rp 50 juta/bulan
            "min_affordability_score": 8.0,
            "min_credibility_score": 8.5,
            "max_risk_score": 3.0,
            "required_high_opportunity": 2  # At least 2 high opportunity indicators
        }
        
        self.logger.info(f"{MAGENTA}🧠 PROJECT HIVEMIND: Multi-Agent VVIP Strategy System initialized{END}")
        self.logger.info(f"{CYAN}🤖 Agents configured: {list(self.agents.keys())}{END}")
        self.logger.info(f"{GREEN}✅ Ready for VVIP prospect analysis{END}")
    
    async def analyze_with_agent(self, agent_key: str, input_data: Dict[str, Any]) -> AgentAnalysis:
        """
        Analyze data using specific agent
        
        Args:
            agent_key: Agent identifier
            input_data: Input data for analysis
            
        Returns:
            AgentAnalysis result
        """
        try:
            agent_config = self.agents[agent_key]
            start_time = time.time()
            
            self.logger.info(f"{BLUE}🤖 {agent_config['name']} analyzing data...{END}")
            
            if self.gemini_model:
                # Prepare prompt
                if agent_key == "data_analyst":
                    prompt = agent_config["prompt_template"].format(
                        prospect_data=json.dumps(input_data, indent=2)
                    )
                elif agent_key == "psychologist":
                    prompt = agent_config["prompt_template"].format(
                        data_analysis=json.dumps(input_data, indent=2)
                    )
                elif agent_key == "master_negotiator":
                    prompt = agent_config["prompt_template"].format(
                        data_analysis=json.dumps(input_data.get("data_analysis", {}), indent=2),
                        psychology_analysis=json.dumps(input_data.get("psychology_analysis", {}), indent=2)
                    )
                
                # Generate response
                response = self.gemini_model.generate_content(prompt)
                result_text = response.text
                
                # Parse JSON response
                try:
                    import re
                    json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
                    if json_match:
                        result = json.loads(json_match.group())
                        confidence = result.get("confidence_score", 7.0)
                    else:
                        # Fallback parsing
                        result = {"error": "Failed to parse response", "raw_text": result_text}
                        confidence = 0.3
                    
                    # Extract insights and recommendations
                    insights = {k: v for k, v in result.items() if k not in ["confidence_score"]}
                    recommendations = self._extract_recommendations(result)
                    
                except json.JSONDecodeError:
                    self.logger.warning(f"{YELLOW}⚠️ Failed to parse {agent_key} response{END}")
                    insights = {"error": "JSON parse failed", "raw_text": result_text}
                    recommendations = ["Manual review required"]
                    confidence = 0.5
                    
            else:
                # Fallback analysis
                insights = {"fallback": "Gemini not available", "agent": agent_key}
                recommendations = ["Manual analysis required"]
                confidence = 0.3
            
            processing_time = time.time() - start_time
            
            analysis = AgentAnalysis(
                agent_name=agent_config["name"],
                analysis_type=agent_config["role"],
                insights=insights,
                recommendations=recommendations,
                confidence_score=confidence,
                processing_time=processing_time,
                created_at=datetime.now()
            )
            
            self.logger.info(f"{GREEN}✅ {agent_config['name']} analysis completed{END}")
            self.logger.debug(f"{CYAN}📊 Confidence: {confidence:.1f}, Time: {processing_time:.2f}s{END}")
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"{RED}❌ {agent_key} analysis error: {str(e)}{END}")
            return AgentAnalysis(
                agent_name=self.agents[agent_key]["name"],
                analysis_type=self.agents[agent_key]["role"],
                insights={"error": str(e)},
                recommendations=["Analysis failed - manual intervention required"],
                confidence_score=0.0,
                processing_time=0.0,
                created_at=datetime.now()
            )
    
    def _extract_recommendations(self, analysis_result: Dict[str, Any]) -> List[str]:
        """Extract recommendations from analysis result"""
        recommendations = []
        
        # Extract from different sections
        for key, value in analysis_result.items():
            if isinstance(value, dict):
                # Look for recommendation-like fields
                if "recommendation" in key.lower():
                    if isinstance(value, list):
                        recommendations.extend(value)
                    else:
                        recommendations.append(str(value))
                elif "insight" in key.lower() or "key" in key.lower():
                    if isinstance(value, list):
                        recommendations.extend([f"Insight: {item}" for item in value])
                    else:
                        recommendations.append(f"Insight: {value}")
        
        return recommendations[:10]  # Limit to 10 recommendations
    
    def is_vvip_prospect(self, prospect_data: Dict[str, Any], data_analysis: AgentAnalysis) -> bool:
        """
        Determine if prospect qualifies as VVIP
        
        Args:
            prospect_data: Raw prospect data
            data_analysis: Data analyst results
            
        Returns:
            True if VVIP prospect, False otherwise
        """
        try:
            insights = data_analysis.insights
            
            # Check financial capacity
            financial_capacity = insights.get("financial_capacity", {})
            affordability_score = financial_capacity.get("affordability_score", 0)
            
            # Check background intelligence
            background_intel = insights.get("background_intelligence", {})
            credibility_score = background_intel.get("credibility_score", 0)
            
            # Check risk assessment
            risk_assessment = insights.get("risk_assessment", {})
            overall_risk = risk_assessment.get("overall_risk_score", 10)
            
            # Check opportunity analysis
            opportunity_analysis = insights.get("opportunity_analysis", {})
            high_opportunities = sum(1 for v in opportunity_analysis.values() if v == "High")
            
            # VVIP criteria check
            vvip_score = 0
            
            if affordability_score >= self.vvip_thresholds["min_affordability_score"]:
                vvip_score += 1
                
            if credibility_score >= self.vvip_thresholds["min_credibility_score"]:
                vvip_score += 1
                
            if overall_risk <= self.vvip_thresholds["max_risk_score"]:
                vvip_score += 1
                
            if high_opportunities >= self.vvip_thresholds["required_high_opportunity"]:
                vvip_score += 1
            
            is_vvip = vvip_score >= 3  # At least 3 of 4 criteria
            
            self.logger.info(f"{CYAN}🎯 VVIP Score: {vvip_score}/4, Status: {'VVIP' if is_vvip else 'Standard'}{END}")
            
            return is_vvip
            
        except Exception as e:
            self.logger.error(f"{RED}❌ VVIP assessment error: {str(e)}{END}")
            return False
    
    async def analyze_vvip_prospect(self, lead_data: Dict[str, Any]) -> VVIPBriefing:
        """
        Complete VVIP prospect analysis using multi-agent swarm
        
        Args:
            lead_data: Lead/prospect data
            
        Returns:
            Complete VVIP briefing
        """
        try:
            start_time = time.time()
            prospect_id = f"vvip_{int(time.time())}_{hash(str(lead_data)) % 10000}"
            prospect_name = lead_data.get("name", "Unknown Prospect")
            
            self.logger.info(f"{MAGENTA}🧠 Starting VVIP analysis for {prospect_name}...{END}")
            self.logger.info(f"{BLUE}📊 Prospect ID: {prospect_id}{END}")
            
            # Step 1: Data Analyst Agent
            self.logger.info(f"{CYAN}🔍 Step 1: Data Intelligence Analysis{END}")
            data_analysis = await self.analyze_with_agent("data_analyst", lead_data)
            
            # Check if VVIP prospect
            is_vvip = self.is_vvip_prospect(lead_data, data_analysis)
            
            if not is_vvip:
                self.logger.warning(f"{YELLOW}⚠️ Prospect does not meet VVIP criteria{END}")
                # Still continue with analysis for learning purposes
            
            # Step 2: Psychologist Agent
            self.logger.info(f"{CYAN}🧠 Step 2: Psychological Analysis{END}")
            psychology_analysis = await self.analyze_with_agent(
                "psychologist", 
                data_analysis.insights
            )
            
            # Step 3: Master Negotiator Agent
            self.logger.info(f"{CYAN}🎯 Step 3: Strategic Negotiation Planning{END}")
            negotiation_analysis = await self.analyze_with_agent(
                "master_negotiator",
                {
                    "data_analysis": data_analysis.insights,
                    "psychology_analysis": psychology_analysis.insights
                }
            )
            
            # Generate executive summary
            executive_summary = self._generate_executive_summary(
                prospect_name, data_analysis, psychology_analysis, negotiation_analysis
            )
            
            # Extract tactical steps and discount limits
            tactical_steps = self._extract_tactical_steps(negotiation_analysis.insights)
            discount_limits = self._extract_discount_limits(negotiation_analysis.insights)
            
            # Calculate closing probability
            closing_probability = self._calculate_closing_probability(
                data_analysis, psychology_analysis, negotiation_analysis
            )
            
            total_processing_time = time.time() - start_time
            
            # Create VVIP briefing
            briefing = VVIPBriefing(
                prospect_id=prospect_id,
                prospect_name=prospect_name,
                prospect_data=lead_data,
                data_analysis=data_analysis,
                psychology_analysis=psychology_analysis,
                negotiation_strategy=negotiation_analysis,
                executive_summary=executive_summary,
                tactical_steps=tactical_steps,
                discount_limits=discount_limits,
                closing_probability=closing_probability,
                created_at=datetime.now(),
                total_processing_time=total_processing_time
            )
            
            # Save to database
            await self._save_vvip_briefing(briefing)
            
            # Send notification to Telegram
            await self._send_vvip_notification(briefing)
            
            self.logger.info(f"{GREEN}✅ VVIP analysis completed in {total_processing_time:.2f}s{END}")
            self.logger.info(f"{CYAN}🎯 Closing Probability: {closing_probability:.1f}%{END}")
            
            return briefing
            
        except Exception as e:
            self.logger.error(f"{RED}❌ VVIP analysis error: {str(e)}{END}")
            raise
    
    def _generate_executive_summary(self, prospect_name: str, data_analysis: AgentAnalysis, 
                                 psychology_analysis: AgentAnalysis, negotiation_analysis: AgentAnalysis) -> str:
        """Generate executive summary for VVIP briefing"""
        try:
            financial_capacity = data_analysis.insights.get("financial_capacity", {})
            affordability = financial_capacity.get("affordability_score", 0)
            
            psychological_profile = psychology_analysis.insights.get("psychological_profile", {})
            personality_type = psychological_profile.get("personality_type", "Unknown")
            
            executive_briefing = negotiation_analysis.insights.get("executive_briefing", {})
            success_prob = executive_briefing.get("success_probability", 0)
            
            summary = f"""
VVIP EXECUTIVE BRIEFING - {prospect_name}

FINANCIAL PROFILE:
- Affordability Score: {affordability}/10
- Payment Method: {financial_capacity.get('payment_method', 'Unknown')}
- Financial Risk: {financial_capacity.get('financial_risk', 'Unknown')}

PSYCHOLOGICAL PROFILE:
- Personality Type: {personality_type}
- Decision Style: {psychological_profile.get('decision_style', 'Unknown')}
- Primary Motivation: {psychological_profile.get('primary_motivation', 'Unknown')}

STRATEGIC OUTLOOK:
- Success Probability: {success_prob}%
- Recommended Approach: {executive_briefing.get('strategy_summary', 'TBD')}
- Key Risks: {', '.join(executive_briefing.get('key_risks', ['None']))}

RECOMMENDATION:
{'Proceed with VVIP treatment strategy' if success_prob >= 75 else 'Standard sales approach recommended'}
            """.strip()
            
            return summary
            
        except Exception as e:
            self.logger.error(f"{RED}❌ Executive summary generation error: {str(e)}{END}")
            return f"Executive summary for {prospect_name} - Analysis completed with some limitations"
    
    def _extract_tactical_steps(self, negotiation_insights: Dict[str, Any]) -> List[str]:
        """Extract tactical steps from negotiation analysis"""
        try:
            tactical_approach = negotiation_insights.get("tactical_approach", {})
            steps = []
            
            for step_key, step_data in tactical_approach.items():
                if isinstance(step_data, dict):
                    objective = step_data.get("objective", "")
                    method = step_data.get("method", "")
                    steps.append(f"Step {step_key.split('_')[1]}: {objective} via {method}")
            
            return steps
            
        except Exception as e:
            self.logger.error(f"{RED}❌ Tactical steps extraction error: {str(e)}{END}")
            return ["Tactical analysis incomplete"]
    
    def _extract_discount_limits(self, negotiation_insights: Dict[str, Any]) -> Dict[str, float]:
        """Extract discount limits from negotiation analysis"""
        try:
            discount_strategy = negotiation_insights.get("discount_strategy", {})
            
            return {
                "max_discount_percentage": discount_strategy.get("max_discount_percentage", 10.0),
                "recommended_discount": discount_strategy.get("max_discount_percentage", 10.0) * 0.7,
                "value_trade_off_value": 5.0  # Placeholder for value trade-offs
            }
            
        except Exception as e:
            self.logger.error(f"{RED}❌ Discount limits extraction error: {str(e)}{END}")
            return {"max_discount_percentage": 5.0, "recommended_discount": 3.0}
    
    def _calculate_closing_probability(self, data_analysis: AgentAnalysis, 
                                     psychology_analysis: AgentAnalysis, 
                                     negotiation_analysis: AgentAnalysis) -> float:
        """Calculate overall closing probability"""
        try:
            # Weight different factors
            data_weight = 0.3
            psychology_weight = 0.3
            negotiation_weight = 0.4
            
            data_score = data_analysis.confidence_score * 10  # Convert to percentage
            psychology_score = psychology_analysis.confidence_score * 10
            negotiation_score = negotiation_analysis.insights.get("executive_briefing", {}).get("success_probability", 50)
            
            closing_probability = (
                data_score * data_weight +
                psychology_score * psychology_weight +
                negotiation_score * negotiation_weight
            )
            
            return min(closing_probability, 95.0)  # Cap at 95%
            
        except Exception as e:
            self.logger.error(f"{RED}❌ Closing probability calculation error: {str(e)}{END}")
            return 50.0  # Default to 50%
    
    async def _save_vvip_briefing(self, briefing: VVIPBriefing) -> bool:
        """Save VVIP briefing to database"""
        try:
            if not self.supabase_manager:
                self.logger.warning(f"{YELLOW}⚠️ Database not available - briefing not saved{END}")
                return False
            
            briefing_data = {
                "prospect_id": briefing.prospect_id,
                "prospect_name": briefing.prospect_name,
                "prospect_data": briefing.prospect_data,
                "data_analysis": asdict(briefing.data_analysis),
                "psychology_analysis": asdict(briefing.psychology_analysis),
                "negotiation_strategy": asdict(briefing.negotiation_strategy),
                "executive_summary": briefing.executive_summary,
                "tactical_steps": briefing.tactical_steps,
                "discount_limits": briefing.discount_limits,
                "closing_probability": briefing.closing_probability,
                "created_at": briefing.created_at.isoformat(),
                "total_processing_time": briefing.total_processing_time
            }
            
            result = self.supabase_manager.insert_vvip_briefing(briefing_data)
            
            if result['success']:
                self.logger.info(f"{GREEN}✅ VVIP briefing saved: {briefing.prospect_id}{END}")
                return True
            else:
                self.logger.error(f"{RED}❌ Failed to save VVIP briefing: {result['error']}{END}")
                return False
                
        except Exception as e:
            self.logger.error(f"{RED}❌ Save VVIP briefing error: {str(e)}{END}")
            return False
    
    async def _send_vvip_notification(self, briefing: VVIPBriefing) -> bool:
        """Send VVIP notification to Telegram"""
        try:
            if not self.telegram_sender:
                self.logger.warning(f"{YELLOW}⚠️ Telegram not available - notification not sent{END}")
                return False
            
            notification_message = f"""
🧠 **VVIP PROSPECT ANALYSIS COMPLETED**

**Prospect**: {briefing.prospect_name}
**Prospect ID**: {briefing.prospect_id}
**Analysis Time**: {briefing.total_processing_time:.2f}s

📊 **FINANCIAL ASSESSMENT**
- Affordability: {briefing.data_analysis.insights.get('financial_capacity', {}).get('affordability_score', 0)}/10
- Risk Level: {briefing.data_analysis.insights.get('risk_assessment', {}).get('overall_risk_score', 0)}/10

🧠 **PSYCHOLOGICAL PROFILE**
- Personality: {briefing.psychology_analysis.insights.get('psychological_profile', {}).get('personality_type', 'Unknown')}
- Decision Style: {briefing.psychology_analysis.insights.get('psychological_profile', {}).get('decision_style', 'Unknown')}

🎯 **CLOSING STRATEGY**
- Success Probability: {briefing.closing_probability:.1f}%
- Max Discount: {briefing.discount_limits.get('max_discount_percentage', 0)}%
- Tactical Steps: {len(briefing.tactical_steps)}

📋 **EXECUTIVE SUMMARY**
{briefing.executive_summary[:200]}...

⚡ VVIP analysis completed with multi-agent intelligence
            """.strip()
            
            self.telegram_sender.send_message(notification_message)
            self.logger.info(f"{GREEN}✅ VVIP notification sent to Telegram{END}")
            return True
            
        except Exception as e:
            self.logger.error(f"{RED}❌ VVIP notification error: {str(e)}{END}")
            return False

# Global hivemind swarm instance
hivemind_swarm = HivemindSwarm()

# Main analysis function
async def analyze_vvip_prospect(lead_data: Dict[str, Any]) -> VVIPBriefing:
    """
    Main function to analyze VVIP prospect using multi-agent swarm
    
    Args:
        lead_data: Lead/prospect data
        
    Returns:
        Complete VVIP briefing
    """
    return await hivemind_swarm.analyze_vvip_prospect(lead_data)

# Test function
if __name__ == "__main__":
    print(f"{MAGENTA}{'='*80}{END}")
    print(f"{CYAN}LUMINA OS - PROJECT HIVEMIND{END}")
    print(f"{MAGENTA}{'='*80}{END}")
    
    print(f"{BLUE}🧠 Testing Hivemind Swarm system...{END}")
    
    # Test with sample VVIP prospect
    sample_prospect = {
        "name": "John Doe",
        "profession": "CEO",
        "company": "Tech Corporation",
        "income": "Rp 100 juta/bulan",
        "location": "Jakarta Selatan",
        "property_interest": "Luxury villa",
        "budget": "Rp 5 Miliar",
        "contact": "+628123456789",
        "source": "Referral"
    }
    
    async def test_hivemind():
        try:
            briefing = await analyze_vvip_prospect(sample_prospect)
            print(f"{GREEN}✅ Test VVIP analysis completed{END}")
            print(f"{CYAN}📊 Prospect: {briefing.prospect_name}{END}")
            print(f"{CYAN}🎯 Closing Probability: {briefing.closing_probability:.1f}%{END}")
            print(f"{CYAN}⏱️ Processing Time: {briefing.total_processing_time:.2f}s{END}")
        except Exception as e:
            print(f"{RED}❌ Test failed: {e}{END}")
    
    # Run test
    asyncio.run(test_hivemind())
    
    print(f"{MAGENTA}{'='*80}{END}")
