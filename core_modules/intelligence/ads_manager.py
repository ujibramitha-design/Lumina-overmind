"""
Twin-Dragon Engine - AI Chief Marketing Officer (CMO)
Advanced AI-powered advertising proposal generation and management
"""

import asyncio
import json
import logging
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ANSI color codes for terminal output
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
CYAN = '\033[96m'
END = '\033[0m'

# Import database client
try:
    from prisma import PrismaClient
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False
    print("Warning: Prisma client not available, database operations disabled")

# Import LLM providers
try:
    import google.generativeai as genai
    import openai
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False
    print("Warning: LLM providers not available, AI operations disabled")

class AdStrategy(Enum):
    """Advertising strategy types"""
    AGRESIF = "Agresif"
    SEIMBANG = "Seimbang"
    HEMAT = "Hemat"

@dataclass
class AdProposal:
    """Ad proposal data structure"""
    opsi_strategi: str
    target_audience: str
    copywriting: str
    estimasi_budget: int
    channel_rekomendasi: List[str]
    kpi_utama: List[str]
    durasi_kampanye: str

class AIChiefMarketingOfficer:
    """
    AI Chief Marketing Officer - Advanced advertising proposal generation
    """
    
    def __init__(self, llm_provider: str = "openai"):
        self.llm_provider = llm_provider
        self.llm_client = None
        self.logger = logger
        
        # Initialize LLM client
        self._initialize_llm()
        
        # Strategy templates
        self.strategy_templates = {
            AdStrategy.AGRESIF: {
                "target_audience": "High-intent buyers with strong purchasing power",
                "tone": "Bold, urgent, and compelling",
                "budget_multiplier": 1.5,
                "channels": ["Google Ads", "Facebook Ads", "Instagram Ads"],
                "kpi": ["Conversion Rate", "Cost Per Acquisition", "Return on Ad Spend"],
                "duration": "2-4 weeks intensive campaign"
            },
            AdStrategy.SEIMBANG: {
                "target_audience": "General property seekers with moderate interest",
                "tone": "Professional, informative, and trustworthy",
                "budget_multiplier": 1.0,
                "channels": ["Google Ads", "Facebook Ads", "Content Marketing"],
                "kpi": ["Click Through Rate", "Lead Quality", "Cost Per Lead"],
                "duration": "4-6 weeks sustained campaign"
            },
            AdStrategy.HEMAT: {
                "target_audience": "Budget-conscious first-time homebuyers",
                "tone": "Friendly, helpful, and value-focused",
                "budget_multiplier": 0.7,
                "channels": ["Facebook Ads", "Instagram Ads", "WhatsApp Marketing"],
                "kpi": ["Cost Per Lead", "Lead Quality", "Engagement Rate"],
                "duration": "6-8 weeks nurturing campaign"
            }
        }
        
        # Copywriting templates by project type
        self.copywriting_templates = {
            "KOMERSIL": {
                "focus": ["Investment", "Prestige", "Luxury", "Business Opportunity"],
                "keywords": ["properti komersial", "investasi properti", "usaha", "bisnis"],
                "call_to_action": ["Hubungi Kami Sekarang", "Dapatkan Penawaran Terbaik", "Investasi Cerdas"]
            },
            "SUBSIDI": {
                "focus": ["Affordable", "Family", "Comfort", "Government Support"],
                "keywords": ["rumah subsidi", "KPR FLPP", "cicilan ringan", "keluarga"],
                "call_to_action": ["Dapatkan Rumah Impian", "Cicilan Ringan", "Promo Pemerintah"]
            }
        }
        
        self.logger.info(f"{CYAN}📢 AI CMO: Initialized with {llm_provider} provider{END}")
    
    def _initialize_llm(self):
        """Initialize LLM client based on provider"""
        if not LLM_AVAILABLE:
            self.logger.warning(f"{YELLOW}⚠️ LLM providers not available{END}")
            return
        
        try:
            if self.llm_provider == "openai":
                # Initialize OpenAI client
                self.llm_client = openai.OpenAI()
                self.logger.info(f"{GREEN}✅ OpenAI client initialized{END}")
            elif self.llm_provider == "gemini":
                # Initialize Gemini client
                genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
                self.llm_client = genai.GenerativeModel('gemini-pro')
                self.logger.info(f"{GREEN}✅ Gemini client initialized{END}")
            else:
                self.logger.warning(f"{YELLOW}⚠️ Unknown LLM provider: {self.llm_provider}{END}")
                
        except Exception as e:
            self.logger.error(f"{RED}❌ Failed to initialize LLM client: {str(e)}{END}")
            self.llm_client = None
    
    async def generate_ad_proposals(project_data: Dict[str, Any]) -> List[AdProposal]:
        """
        Generate 3 ad proposals for different strategies with full context awareness
        
        Args:
            project_data: Complete project data including type, location, price, leads, etc.
            
        Returns:
            List of 3 AdProposal objects
        """
        try:
            self.logger.info(f"{CYAN}📢 AI CMO: Generating ad proposals for {project_data.get('namaProyek', 'Unknown')}{END}")
            
            if not self.llm_client:
                self.logger.error(f"{RED}❌ LLM client not available{END}")
                return self._generate_fallback_proposals(project_data)
            
            # Build comprehensive context-aware prompt for all strategies
            prompt = self._build_comprehensive_prompt(project_data)
            
            # Generate all 3 proposals in single LLM call
            self.logger.info(f"{BLUE}🤖 Calling LLM for comprehensive proposal generation{END}")
            response = await self._call_llm_comprehensive(prompt)
            
            # Parse response and create proposals
            proposals = self._parse_comprehensive_response(response, project_data)
            
            self.logger.info(f"{GREEN}✅ Generated {len(proposals)} context-aware proposals{END}")
            
            # Save proposals to database
            if DB_AVAILABLE:
                await self._save_proposals_to_database(project_data, proposals)
            
            self.logger.info(f"{GREEN}✅ Generated {len(propososals)} ad proposals{END}")
            return proposals
            
        except Exception as e:
            self.logger.error(f"{RED}❌ Error generating ad proposals: {str(e)}{END}")
            return self._generate_fallback_proposals(project_data)
    
    async def _generate_single_proposal(self, project_data: Dict[str, Any], strategy: AdStrategy) -> AdProposal:
        """Generate single ad proposal using LLM"""
        
        # Extract project information
        project_name = project_data.get('namaProyek', 'Unknown Project')
        project_type = project_data.get('tipeProyek', 'KOMERSIL')
        location = project_data.get('lokasi', 'Unknown Location')
        price_start = project_data.get('hargaStart', 0)
        target_market = project_data.get('targetMarket', 'General Market')
        
        # Get strategy template
        strategy_template = self.strategy_templates[strategy]
        
        # Get copywriting template
        copy_template = self.copywriting_templates.get(project_type, self.copywriting_templates["KOMERSIL"])
        
        # Calculate budget estimation
        base_budget = self._calculate_base_budget(project_data, strategy)
        
        # Build prompt for LLM
        prompt = self._build_ad_proposal_prompt(
            project_name=project_name,
            project_type=project_type,
            location=location,
            price_start=price_start,
            target_market=target_market,
            strategy=strategy,
            strategy_template=strategy_template,
            copy_template=copy_template,
            base_budget=base_budget
        )
        
        # Generate proposal using LLM
        proposal_data = await self._call_llm(prompt)
        
        # Parse and create AdProposal object
        return self._parse_proposal_response(proposal_data, strategy, base_budget)
    
    def _build_ad_proposal_prompt(self, project_data: Dict[str, Any], strategy: AdStrategy, strategy_template: Dict, copy_template: Dict, base_budget: int) -> str:
        """Build comprehensive context-aware prompt for LLM"""
        
        # Extract context from project data
        project_name = project_data.get('namaProyek', 'Unknown Project')
        project_type = project_data.get('tipeProyek', 'KOMERSIL')
        location = project_data.get('lokasi', 'Unknown Location')
        price_start = project_data.get('hargaStart', 0)
        target_market = project_data.get('targetMarket', 'General Market')
        
        # Location data
        latitude = project_data.get('latitude')
        longitude = project_data.get('longitude')
        radius_km = project_data.get('radiusKm', 5)
        nama_wilayah = project_data.get('namaWilayah', '')
        
        # Performance data
        leads_count = project_data.get('leadsCount', 0)
        hot_leads_count = project_data.get('hotLeadsCount', 0)
        conversion_rate = project_data.get('conversionRate', 0.0)
        
        # Existing leads context
        existing_leads = project_data.get('existingLeads', {})
        leads_total = existing_leads.get('total', 0)
        leads_status_dist = existing_leads.get('statusDistribution', {})
        
        # Scout mode and targeting data
        scout_mode = project_data.get('scoutMode', 'API_OFFICIAL')
        dorking_targets = project_data.get('dorkingTargets', [])
        
        prompt = f"""
Anda adalah Chief Marketing Officer AI yang ahli dalam menghasilkan proposal iklan properti.

PROJECT CONTEXT - DATA LENGKAP PROYEK:
- Nama Proyek: {project_name}
- Tipe Proyek: {project_type}
- Lokasi: {location}
- Koordinat: {latitude}, {longitude} (jika tersedia)
- Radius Area: {radius_km} km
- Wilayah: {nama_wilayah}
- Harga Mulai: Rp {price_start:,}
- Target Market: {target_market}
- Scout Mode: {scout_mode}
- Dorking Targets: {', '.join(dorking_targets) if dorking_targets else 'Tidak ada'}

PERFORMANCE DATA:
- Total Leads: {leads_count}
- Hot Leads: {hot_leads_count}
- Conversion Rate: {conversion_rate:.2%}
- Existing Leads for Analysis: {leads_total}

LEADS STATUS DISTRIBUTION:
- SCOUTED: {leads_status_dist.get('SCOUTED', 0)}
- CONTACTED: {leads_status_dist.get('CONTACTED', 0)}
- INTERESTED: {leads_status_dist.get('INTERESTED', 0)}
- CONVERTED: {leads_status_dist.get('CONVERTED', 0)}

STRATEGY YANG AKAN DIGUNAKAN: {strategy.value}
- Target Audience: {strategy_template['target_audience']}
- Tone: {strategy_template['tone']}
- Budget Multiplier: {strategy_template['budget_multiplier']}
- Recommended Channels: {', '.join(strategy_template['channels'])}
- KPI Focus: {', '.join(strategy_template['kpi'])}
- Campaign Duration: {strategy_template['duration']}

COPYWRITING FOCUS UNTUK {project_type}:
- Keywords: {', '.join(copy_template['keywords'])}
- Focus Areas: {', '.join(copy_template['focus'])}
- Call to Action: {', '.join(copy_template['call_to_action'])}

BASE BUDGET ESTIMATION: Rp {base_budget:,}

ANALISIS KONTEK LOKAL:
Lokasi: {location} adalah area dengan {leads_count} leads yang sudah ada dan conversion rate {conversion_rate:.2%}. 
{"Performa leads baik, tingkat konversi tinggi" if conversion_rate > 5 else "Perlu optimasi konversi" if conversion_rate > 2 else "Perlu strategi awareness yang lebih agresif"}.

TASK UTAMA:
Buat 3 opsi draf iklan (Agresif, Seimbang, Hemat) yang SANGAT SPESIFIK dengan mempertimbangkan:
1. Data lokasi dan harga proyek yang sebenarnya
2. Performa leads yang sudah ada di area tersebut
3. Karakteristik target market yang sesuai
4. Strategi channel yang optimal untuk area {location}

Generate proposal untuk strategy {strategy.value} dengan format JSON:
{{
  "opsi_strategi": "Deskripsi strategi yang spesifik untuk {location}",
  "target_audience": "Deskripsi target audience yang detail dengan konteks {location}",
  "copywriting": "Copy iklan yang compelling (3-5 kalimat) dengan menyebutkan nama proyek dan lokasi",
  "estimasi_budget": "Budget dalam IDR (angka saja)",
  "channel_rekomendasi": ["channel1", "channel2", "channel3"],
  "kpi_utama": ["kpi1", "kpi2", "kpi3"],
  "durasi_kampanye": "Deskripsi durasi kampanye"
}}

GUIDELINES KRITIS:
1. Copywriting WAJIB menyebutkan nama proyek "{project_name}" dan lokasi "{location}"
2. Budget harus realistis untuk market {location} berdasarkan harga Rp {price_start:,}
3. Channel recommendations harus optimal untuk area {location}
4. KPI harus relevant dengan performa leads yang ada (conversion rate: {conversion_rate:.2%})
5. Tone harus sesuai dengan strategy template dan project type {project_type}
6. Pertimbangkan jumlah leads yang ada ({leads_count}) dalam strategi targeting

RESPONSE FORMAT:
Return valid JSON array untuk 3 proposal (Agresif, Seimbang, Hemat) dalam format:
[{{proposal1}}, {{proposal2}}, {{proposal3}}]

HANYA return JSON, tanpa teks tambahan.
"""
        
        return prompt
    
    async def _call_llm(self, prompt: str) -> Dict[str, Any]:
        """Call LLM and parse response"""
        try:
            if self.llm_provider == "openai":
                response = self.llm_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are an expert Chief Marketing Officer AI. Always respond with valid JSON format."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=500,
                    temperature=0.7
                )
                content = response.choices[0].message.content
                
            elif self.llm_provider == "gemini":
                response = self.llm_client.generate_content(prompt)
                content = response.text
            
            else:
                raise ValueError(f"Unknown LLM provider: {self.llm_provider}")
            
            # Parse JSON response
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                # Clean up response and try again
                content = content.strip()
                if content.startswith('```json'):
                    content = content[7:]
                if content.endswith('```'):
                    content = content[:-3]
                return json.loads(content)
                
        except Exception as e:
            self.logger.error(f"LLM call failed: {str(e)}")
            raise
    
    def _parse_proposal_response(self, proposal_data: Dict[str, Any], strategy: AdStrategy, base_budget: int) -> AdProposal:
        """Parse LLM response into AdProposal object"""
        
        return AdProposal(
            opsi_strategi=proposal_data.get('opsi_strategi', f'{strategy.value} Strategy'),
            target_audience=proposal_data.get('target_audience', 'General audience'),
            copywriting=proposal_data.get('copywriting', 'Compelling ad copy'),
            estimasi_budget=proposal_data.get('estimasi_budget', base_budget),
            channel_rekomendasi=proposal_data.get('channel_rekomendasi', ['Facebook Ads']),
            kpi_utama=proposal_data.get('kpi_utama', ['Conversion Rate']),
            durasi_kampanye=proposal_data.get('durasi_kampanye', '4 weeks')
        )
    
    def _build_comprehensive_prompt(self, project_data: Dict[str, Any]) -> str:
        """Build comprehensive prompt for all 3 strategies"""
        
        # Extract context from project data
        project_name = project_data.get('namaProyek', 'Unknown Project')
        project_type = project_data.get('tipeProyek', 'KOMERSIL')
        location = project_data.get('lokasi', 'Unknown Location')
        price_start = project_data.get('hargaStart', 0)
        target_market = project_data.get('targetMarket', 'General Market')
        
        # Location data
        latitude = project_data.get('latitude')
        longitude = project_data.get('longitude')
        radius_km = project_data.get('radiusKm', 5)
        nama_wilayah = project_data.get('namaWilayah', '')
        
        # Performance data
        leads_count = project_data.get('leadsCount', 0)
        hot_leads_count = project_data.get('hotLeadsCount', 0)
        conversion_rate = project_data.get('conversionRate', 0.0)
        
        # Existing leads context
        existing_leads = project_data.get('existingLeads', {})
        leads_total = existing_leads.get('total', 0)
        leads_status_dist = existing_leads.get('statusDistribution', {})
        
        # Scout mode and targeting data
        scout_mode = project_data.get('scoutMode', 'API_OFFICIAL')
        dorking_targets = project_data.get('dorkingTargets', [])
        
        prompt = f"""
Anda adalah Chief Marketing Officer AI yang ahli dalam menghasilkan proposal iklan properti.

PROJECT CONTEXT - DATA LENGKAP PROYEK:
- Nama Proyek: {project_name}
- Tipe Proyek: {project_type}
- Lokasi: {location}
- Koordinat: {latitude}, {longitude} (jika tersedia)
- Radius Area: {radius_km} km
- Wilayah: {nama_wilayah}
- Harga Mulai: Rp {price_start:,}
- Target Market: {target_market}
- Scout Mode: {scout_mode}
- Dorking Targets: {', '.join(dorking_targets) if dorking_targets else 'Tidak ada'}

PERFORMANCE DATA:
- Total Leads: {leads_count}
- Hot Leads: {hot_leads_count}
- Conversion Rate: {conversion_rate:.2%}
- Existing Leads for Analysis: {leads_total}

LEADS STATUS DISTRIBUTION:
- SCOUTED: {leads_status_dist.get('SCOUTED', 0)}
- CONTACTED: {leads_status_dist.get('CONTACTED', 0)}
- INTERESTED: {leads_status_dist.get('INTERESTED', 0)}
- CONVERTED: {leads_status_dist.get('CONVERTED', 0)}

ANALISIS KONTEK LOKAL:
Lokasi: {location} adalah area dengan {leads_count} leads yang sudah ada dan conversion rate {conversion_rate:.2%}. 
{"Performa leads baik, tingkat konversi tinggi" if conversion_rate > 5 else "Perlu optimasi konversi" if conversion_rate > 2 else "Perlu strategi awareness yang lebih agresif"}.

TASK UTAMA:
Buat 3 opsi draf iklan (Agresif, Seimbang, Hemat) yang SANGAT SPESIFIK dengan mempertimbangkan:
1. Data lokasi dan harga proyek yang sebenarnya
2. Performa leads yang sudah ada di area tersebut
3. Karakteristik target market yang sesuai
4. Strategi channel yang optimal untuk area {location}

STRATEGY DEFINITIONS:
- AGRESIF: Target high-intent buyers, budget 1.5x, bold tone, 2-4 weeks intensive
- SEIMBANG: Target general seekers, budget 1.0x, professional tone, 4-6 weeks sustained
- HEMAT: Target budget-conscious buyers, budget 0.7x, friendly tone, 6-8 weeks nurturing

Generate 3 proposal dalam format JSON array:
[
  {{
    "opsi_strategi": "Deskripsi strategi Agresif untuk {location}",
    "target_audience": "Deskripsi target audience yang detail dengan konteks {location}",
    "copywriting": "Copy iklan yang compelling (3-5 kalimat) dengan menyebutkan nama proyek dan lokasi",
    "estimasi_budget": "Budget dalam IDR (angka saja)",
    "channel_rekomendasi": ["channel1", "channel2", "channel3"],
    "kpi_utama": ["kpi1", "kpi2", "kpi3"],
    "durasi_kampanye": "Deskripsi durasi kampanye"
  }},
  {{
    "opsi_strategi": "Deskripsi strategi Seimbang untuk {location}",
    "target_audience": "Deskripsi target audience yang detail dengan konteks {location}",
    "copywriting": "Copy iklan yang compelling (3-5 kalimat) dengan menyebutkan nama proyek dan lokasi",
    "estimasi_budget": "Budget dalam IDR (angka saja)",
    "channel_rekomendasi": ["channel1", "channel2", "channel3"],
    "kpi_utama": ["kpi1", "kpi2", "kpi3"],
    "durasi_kampanye": "Deskripsi durasi kampanye"
  }},
  {{
    "opsi_strategi": "Deskripsi strategi Hemat untuk {location}",
    "target_audience": "Deskripsi target audience yang detail dengan konteks {location}",
    "copywriting": "Copy iklan yang compelling (3-5 kalimat) dengan menyebutkan nama proyek dan lokasi",
    "estimasi_budget": "Budget dalam IDR (angka saja)",
    "channel_rekomendasi": ["channel1", "channel2", "channel3"],
    "kpi_utama": ["kpi1", "kpi2", "kpi3"],
    "durasi_kampanye": "Deskripsi durasi kampanye"
  }}
]

GUIDELINES KRITIS:
1. Copywriting WAJIB menyebutkan nama proyek "{project_name}" dan lokasi "{location}"
2. Budget harus realistis untuk market {location} berdasarkan harga Rp {price_start:,}
3. Channel recommendations harus optimal untuk area {location}
4. KPI harus relevant dengan performa leads yang ada (conversion rate: {conversion_rate:.2%})
5. Tone harus sesuai dengan project type {project_type}
6. Pertimbangkan jumlah leads yang ada ({leads_count}) dalam strategi targeting

RESPONSE FORMAT:
Return valid JSON array HANYA, tanpa teks tambahan.
"""
        
        return prompt
    
    async def _call_llm_comprehensive(self, prompt: str) -> List[Dict[str, Any]]:
        """Call LLM for comprehensive proposal generation"""
        try:
            if self.llm_provider == "openai":
                response = self.llm_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are an expert Chief Marketing Officer AI. Always respond with valid JSON format only."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=1000,
                    temperature=0.7
                )
                content = response.choices[0].message.content
                
            elif self.llm_provider == "gemini":
                response = self.llm_client.generate_content(prompt)
                content = response.text
            
            else:
                raise ValueError(f"Unknown LLM provider: {self.llm_provider}")
            
            # Parse JSON response
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                # Clean up response and try again
                content = content.strip()
                if content.startswith('```json'):
                    content = content[7:]
                if content.endswith('```'):
                    content = content[:-3]
                return json.loads(content)
                
        except Exception as e:
            self.logger.error(f"LLM call failed: {str(e)}")
            raise
    
    def _parse_comprehensive_response(self, response_data: List[Dict[str, Any]], project_data: Dict[str, Any]) -> List[AdProposal]:
        """Parse comprehensive LLM response into AdProposal objects"""
        
        proposals = []
        base_budget = self._calculate_base_budget(project_data, AdStrategy.SEIMBANG)
        
        for i, proposal_data in enumerate(response_data):
            strategy = list(AdStrategy)[i] if i < len(AdStrategy) else AdStrategy.SEIMBANG
            
            proposal = AdProposal(
                opsi_strategi=proposal_data.get('opsi_strategi', f'{strategy.value} Strategy'),
                target_audience=proposal_data.get('target_audience', 'General audience'),
                copywriting=proposal_data.get('copywriting', 'Compelling ad copy'),
                estimasi_budget=proposal_data.get('estimasi_budget', base_budget),
                channel_rekomendasi=proposal_data.get('channel_rekomendasi', ['Facebook Ads']),
                kpi_utama=proposal_data.get('kpi_utama', ['Conversion Rate']),
                durasi_kampanye=proposal_data.get('durasi_kampanye', '4 weeks')
            )
            proposals.append(proposal)
        
        return proposals
    
    def _calculate_base_budget(self, project_data: Dict[str, Any], strategy: AdStrategy) -> int:
        """Calculate base budget estimation"""
        
        price_start = project_data.get('hargaStart', 0)
        strategy_multiplier = self.strategy_templates[strategy]['budget_multiplier']
        
        # Base budget calculation (1% of property price, adjusted by strategy)
        base_budget = int(price_start * 0.01 * strategy_multiplier)
        
        # Minimum budget of 10 million IDR
        min_budget = 10000000
        
        return max(base_budget, min_budget)
    
    async def _save_proposals_to_database(self, project_data: Dict[str, Any], proposals: List[AdProposal]):
        """Save proposals to database"""
        if not DB_AVAILABLE:
            return
        
        try:
            db = PrismaClient()
            
            for proposal in proposals:
                await db.adproposal.create({
                    'projectId': project_data.get('id'),
                    'opsiStrategi': proposal.opsi_strategi,
                    'targetAudience': proposal.target_audience,
                    'copywriting': proposal.copywriting,
                    'estimasiBudget': proposal.estimasi_budget,
                    'status': 'PENDING'
                })
            
            db.disconnect()
            self.logger.info(f"{GREEN}✅ Saved {len(propososals)} proposals to database{END}")
            
        except Exception as e:
            self.logger.error(f"{RED}❌ Failed to save proposals to database: {str(e)}{END}")
    
    def _generate_fallback_proposals(self, project_data: Dict[str, Any]) -> List[AdProposal]:
        """Generate fallback proposals when LLM is not available"""
        
        project_name = project_data.get('namaProyek', 'Unknown Project')
        project_type = project_data.get('tipeProyek', 'KOMERSIL')
        location = project_data.get('lokasi', 'Unknown Location')
        
        fallback_proposals = [
            AdProposal(
                opsi_strategi="Agresif Strategy",
                target_audience="High-intent buyers with strong purchasing power",
                copywriting=f"Investasi properti {project_name} di {location}. Dapatkan penawaran terbaik sekarang!",
                estimasi_budget=15000000,
                channel_rekomendasi=["Google Ads", "Facebook Ads", "Instagram Ads"],
                kpi_utama=["Conversion Rate", "Cost Per Acquisition"],
                durasi_kampanye="2-4 weeks intensive campaign"
            ),
            AdProposal(
                opsi_strategi="Seimbang Strategy",
                target_audience="General property seekers with moderate interest",
                copywriting=f"Temukan properti impian Anda di {project_name}, {location}. Hubungi kami untuk info lengkap.",
                estimasi_budget=10000000,
                channel_rekomendasi=["Google Ads", "Facebook Ads", "Content Marketing"],
                kpi_utama=["Click Through Rate", "Lead Quality"],
                durasi_kampanye="4-6 weeks sustained campaign"
            ),
            AdProposal(
                opsi_strategi="Hemat Strategy",
                target_audience="Budget-conscious first-time homebuyers",
                copywriting=f"Rumah {project_name} di {location} dengan cicilan ringan. Dapatkan rumah impian Anda!",
                estimasi_budget=7000000,
                channel_rekomendasi=["Facebook Ads", "Instagram Ads", "WhatsApp Marketing"],
                kpi_utama=["Cost Per Lead", "Engagement Rate"],
                durasi_kampanye="6-8 weeks nurturing campaign"
            )
        ]
        
        self.logger.info(f"{YELLOW}⚠️ Generated {len(fallback_proposals)} fallback proposals{END}")
        return fallback_proposals
    
    async def revise_proposal(self, proposal_id: str, revision_instructions: str) -> Optional[AdProposal]:
        """
        Revise existing proposal based on feedback
        
        Args:
            proposal_id: ID of the proposal to revise
            revision_instructions: Instructions for revision
            
        Returns:
            Revised AdProposal or None if not found
        """
        try:
            self.logger.info(f"{CYAN}📢 AI CMO: Revising proposal {proposal_id}{END}")
            
            if not DB_AVAILABLE:
                self.logger.error(f"{RED}❌ Database not available{END}")
                return None
            
            # Get existing proposal
            db = PrismaClient()
            proposal = await db.adproposal.find_unique(where={'id': proposal_id})
            db.disconnect()
            
            if not proposal:
                self.logger.error(f"{RED}❌ Proposal not found: {proposal_id}{END}")
                return None
            
            # Get project data
            project = await db.project.find_unique(where={'id': proposal.projectId})
            db.disconnect()
            
            if not project:
                self.logger.error(f"{RED}❌ Project not found: {proposal.projectId}{END}")
                return None
            
            # Build revision prompt
            prompt = f"""
Revise the following ad proposal based on the feedback:

CURRENT PROPOSAL:
- Strategy: {proposal.opsiStrategi}
- Target Audience: {proposal.targetAudience}
- Copywriting: {proposal.copywriting}
- Budget: Rp {proposal.estimasiBudget:,}

REVISION INSTRUCTIONS:
{revision_instructions}

PROJECT INFORMATION:
- Name: {project.namaProyek}
- Type: {project.tipeProyek}
- Location: {project.lokasi}
- Price: Rp {project.hargaStart:,}

TASK:
Generate revised proposal in the same JSON format:
{{
  "opsi_strategi": "Updated strategy description",
  "target_audience": "Updated target audience",
  "copywriting": "Revised ad copy",
  "estimasi_budget": "Updated budget (number only)",
  "channel_rekomendasi": ["channel1", "channel2", "channel3"],
  "kpi_utama": ["kpi1", "kpi2", "kpi3"],
  "durasi_kampanye": "Updated duration"
}}

Return valid JSON only.
"""
            
            # Generate revised proposal
            revised_data = await self._call_llm(prompt)
            
            # Parse and create revised proposal
            revised_proposal = self._parse_proposal_response(
                revised_data, 
                AdStrategy.AGRESIF,  # Default strategy
                proposal.estimasiBudget
            )
            
            # Update database
            db = PrismaClient()
            await db.adproposal.update({
                'where': {'id': proposal_id},
                'data': {
                    'opsiStrategi': revised_proposal.opsi_strategi,
                    'targetAudience': revised_proposal.target_audience,
                    'copywriting': revised_proposal.copywriting,
                    'estimasiBudget': revised_proposal.estimasi_budget,
                    'updatedAt': datetime.now()
                }
            })
            db.disconnect()
            
            self.logger.info(f"{GREEN}✅ Revised proposal {proposal_id}{END}")
            return revised_proposal
            
        except Exception as e:
            self.logger.error(f"{RED}❌ Error revising proposal: {str(e)}{END}")
            return None

# Global AI CMO instance
ai_cmo = AIChiefMarketingOfficer()

# Convenience functions
async def generate_ad_proposals(project_data: Dict[str, Any]) -> List[AdProposal]:
    """Generate ad proposals for a project"""
    return await ai_cmo.generate_ad_proposals(project_data)

async def revise_proposal(proposal_id: str, revision_instructions: str) -> Optional[AdProposal]:
    """Revise existing proposal"""
    return await ai_cmo.revise_proposal(proposal_id, revision_instructions)

# Example usage
async def main():
    """Example usage of AI CMO"""
    print("📢 Twin-Dragon AI Chief Marketing Officer Example")
    print("=" * 60)
    
    # Example project data
    project_data = {
        'id': 'project_123',
        'namaProyek': 'Grand Serang Residence',
        'tipeProyek': 'KOMERSIL',
        'lokasi': 'Serang',
        'hargaStart': 500000000,
        'targetMarket': 'Middle to Upper Class'
    }
    
    # Generate proposals
    proposals = await generate_ad_proposals(project_data)
    
    print(f"\n📊 Generated {len(propososals)} Ad Proposals:")
    for i, proposal in enumerate(proposals, 1):
        print(f"\n{i}. {proposal.opsi_strategi}")
        print(f"   Target: {proposal.target_audience}")
        print(f"   Budget: Rp {proposal.estimasi_budget:,}")
        print(f"   Copy: {proposal.copywriting}")
        print(f"   Channels: {', '.join(proposal.channel_rekomendasi)}")
        print(f"   KPI: {', '.join(proposal.kpi_utama)}")
        print(f"   Duration: {proposal.durasi_kampanye}")

if __name__ == "__main__":
    asyncio.run(main())
