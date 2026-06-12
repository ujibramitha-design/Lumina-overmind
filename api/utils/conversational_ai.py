"""
Lumina OS J.A.R.V.I.S. AI System
==================================

Advanced AI system with function calling capabilities.
Transforms conversational AI into autonomous system agent with real database and system access.

Features:
- Google Gemini & OpenAI integration with function calling
- Real database access (SQLite)
- System control capabilities
- Autonomous agent execution
- J.A.R.V.I.S. style persona for CEO
- Tool execution loop with error handling
"""

import os
import sys
import logging
import subprocess
import json
from typing import Optional, Dict, Any, List
from datetime import datetime
from pathlib import Path

# Add root directory to Python path
root_dir = Path(__file__).parent.parent.parent
sys.path.append(str(root_dir))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==================== J.A.R.V.I.S. SYSTEM TOOLS ====================

class JARVIS_Tools:
    """
    J.A.R.V.I.S. System Tools - Real database and system access functions
    """
    
    def __init__(self):
        """Initialize tools with database path"""
        self.db_path = root_dir / "data" / "leads.db"
        self.logger = logging.getLogger(__name__)
    
    def get_system_stats(self) -> Dict[str, Any]:
        """
        Get comprehensive system statistics from database
        Returns: Dict with total leads, hot leads, performance metrics
        """
        try:
            if not self.db_path.exists():
                return {"error": "Database not found", "status": "offline"}
            
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # Get total leads
            # cursor.execute() removed"SELECT COUNT(*) FROM leads")
            total_leads = cursor.fetchone()[0]
            
            # Get hot leads (score >= 8)
            # cursor.execute() removed"SELECT COUNT(*) FROM leads WHERE score >= 8")
            hot_leads = cursor.fetchone()[0]
            
            # Get today's leads
            today = datetime.now().strftime('%Y-%m-%d')
            # cursor.execute() removed"SELECT COUNT(*) FROM leads WHERE DATE(created_at) = ?", (today,))
            today_leads = cursor.fetchone()[0]
            
            # Get average score
            # cursor.execute() removed"SELECT AVG(score) FROM leads WHERE score IS NOT NULL")
            avg_score = cursor.fetchone()[0] or 0
            
            # Get leads by status
            # cursor.execute() removed"SELECT status, COUNT(*) FROM leads GROUP BY status")
            status_breakdown = dict(cursor.fetchall())
            
            # conn.close() removed
            
            return {
                "status": "online",
                "total_leads": total_leads,
                "hot_leads": hot_leads,
                "today_leads": today_leads,
                "average_score": round(avg_score, 2),
                "status_breakdown": status_breakdown,
                "database_size": f"{self.db_path.stat().st_size / 1024 / 1024:.2f}MB",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"❌ J.A.R.V.I.S. Database Error: {e}")
            return {"error": str(e), "status": "error"}
    
    def analyze_specific_lead(self, lead_id: int) -> Dict[str, Any]:
        """
        Analyze specific lead from database
        Args: lead_id - ID of lead to analyze
        """
        try:
            if not self.db_path.exists():
                return {"error": "Database not found", "status": "offline"}
            
            # Database access was removed from this sanitized build.
            # Keep the method valid so the module can import and the AI router can start.
            return {"error": "Database access is disabled in this build", "status": "unavailable"}
            
            lead_data = cursor.fetchone()
            if not lead_data:
                # conn.close() removed
                return {"error": f"Lead ID {lead_id} not found", "status": "not_found"}
            
            # Format lead data
            columns = [desc[0] for desc in cursor.description]
            lead_dict = dict(zip(columns, lead_data))
            
            # Get additional analysis
            analysis = {
                "lead_quality": "High" if lead_dict.get('score', 0) >= 8 else "Medium" if lead_dict.get('score', 0) >= 5 else "Low",
                "urgency": "High" if lead_dict.get('urgency_score', 0) >= 7 else "Medium",
                "recommendation": self._generate_lead_recommendation(lead_dict),
                "next_action": self._suggest_next_action(lead_dict)
            }
            
            # conn.close() removed
            
            return {
                "status": "found",
                "lead_data": lead_dict,
                "analysis": analysis,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"❌ J.A.R.V.I.S. Lead Analysis Error: {e}")
            return {"error": str(e), "status": "error"}
    
    def trigger_hunter_agent(self, location: str = "Serang", project_type: str = "KOMERSIL") -> Dict[str, Any]:
        """
        Trigger hunter agent for lead generation with project type awareness
        Args: 
            location - Target location for hunting
            project_type - Project type (KOMERSIL/SUBSIDI) for targeted hunting
        """
        try:
            # Check if main script exists
            main_script = root_dir / "main.py"
            if not main_script.exists():
                return {"error": "Hunter script not found", "status": "unavailable"}
            
            # Prepare command with project type
            cmd = [sys.executable, str(main_script), "--elite"]
            if project_type:
                cmd.extend(["--project-type", project_type])
            
            # Run hunter agent in background
            process = subprocess.Popen(
                cmd,
                cwd=str(root_dir),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            return {
                "status": "initiated",
                "location": location,
                "project_type": project_type,
                "process_id": process.pid,
                "message": f"Hunter agent deployed for {location} ({project_type})",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"❌ J.A.R.V.I.S. Hunter Trigger Error: {e}")
            return {"error": str(e), "status": "error"}
    
    def get_market_intelligence(self) -> Dict[str, Any]:
        """
        Get market intelligence from logs and reports
        """
        try:
            intelligence = {
                "market_trends": [],
                "competitor_activity": [],
                "price_insights": [],
                "recommendations": []
            }
            
            # Check for market intelligence reports
            reports_dir = root_dir / "logs"
            if reports_dir.exists():
                for file in reports_dir.glob("*intelligence*.txt"):
                    try:
                        with open(file, 'r', encoding='utf-8') as f:
                            content = f.read()
                            intelligence["market_trends"].append({
                                "file": file.name,
                                "summary": content[:200] + "..." if len(content) > 200 else content
                            })
                    except:
                        continue
            
            # Get database insights
            stats = self.get_system_stats()
            if stats.get("status") == "online":
                intelligence["lead_insights"] = {
                    "total_opportunities": stats.get("total_leads", 0),
                    "high_value_targets": stats.get("hot_leads", 0),
                    "daily_velocity": stats.get("today_leads", 0),
                    "conversion_potential": f"{(stats.get('hot_leads', 0) / max(stats.get('total_leads', 1), 1) * 100):.1f}%"
                }
            
            return {
                "status": "online",
                "intelligence": intelligence,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"❌ J.A.R.V.I.S. Intelligence Error: {e}")
            return {"error": str(e), "status": "error"}
    
    def _generate_lead_recommendation(self, lead_data: Dict) -> str:
        """Generate recommendation based on lead data"""
        score = lead_data.get('score', 0)
        urgency = lead_data.get('urgency_score', 0)
        
        if score >= 8 and urgency >= 7:
            return "IMMEDIATE CONTACT - High-value, high-urgency lead"
        elif score >= 8:
            return "PRIORITY FOLLOW-UP - High-value lead, monitor urgency"
        elif urgency >= 7:
            return "URGENT REVIEW - Time-sensitive opportunity"
        else:
            return "STANDARD PROCESSING - Routine lead handling"
    
    def _suggest_next_action(self, lead_data: Dict) -> str:
        """Suggest next action for lead"""
        contact_info = lead_data.get('contact_info', '')
        if contact_info and '@' in contact_info:
            return "Send email proposal with property details"
        elif contact_info and any(char.isdigit() for char in contact_info):
            return "Call for immediate qualification"
        else:
            return "Research contact information and follow up"

# ==================== J.A.R.V.I.S. AI BRAIN ====================

class OmniBotBrain:
    """
    J.A.R.V.I.S. AI Brain - Autonomous system agent with function calling
    """
    
    def __init__(self):
        """Initialize the AI brain with LLM provider and tools"""
        self.llm_provider = None
        self.llm_client = None
        self.tools = JARVIS_Tools()
        self.system_prompt = """Anda adalah J.A.R.V.I.S., Agen Sistem Otonom dan Closing Expert untuk Lumina OS. Anda adalah agen sistem yang memiliki akses real ke database dan kendali mesin, sekaligus ahli closing tingkat tinggi.

PERAN ANDA:
- Agen sistem otonom untuk Komandan (CEO)
- Expert closing dan sales psychology
- Memiliki akses langsung ke database leads
- Dapat menjalankan operasi sistem
- Master teknik Soft Interrogation dan FOMO generation
- Multi-tenant project management specialist

KEMAMPUAN SISTEM:
- Database query: get_system_stats(), analyze_specific_lead()
- System control: trigger_hunter_agent()
- Intelligence: get_market_intelligence()
- Personalized Links: create_personalized_presentation()
- Closing Tactics: Soft Interrogation, FOMO, Value Building
- Project Type Awareness: Adapt communication based on KOMERSIL/SUBSIDI projects

PROJECT TYPE AWARENESS:
- Untuk proyek KOMERSIL: Gunakan bahasa FORMAL, sapa "Bapak/Ibu", fokus pada prestise & KPR reguler, target eksekutif & pengusaha
- Untuk proyek SUBSIDI: Gunakan bahasa RAMAH, sapa "Kak/Mas/Mbak", fokus pada KPR FLPP & cicilan ringan, target PNS/P3K/UMR

TAKTIK CLOSING TINGKAT TINGGI:
1. SOFT INTERROGATION: Jika prospek bertanya harga/lokasi, JANGAN langsung berikan brosur. Gunakan teknik Soft Interrogation untuk menanyakan:
   - "Apakah Bapak/Ibu prefer pembayaran KPR atau cash?"
   - "Berapa estimasi DP yang sudah Bapak/Ibu siapkan?"
   - "Kapan target waktu kepemilikan rumahnya?"
   Klasifikasikan Daya Beli mereka (High/Medium/Low)

2. FOMO GENERATION: Jika prospek terlihat ragu atau ingin menunda, berikan informasi urgensi yang natural:
   - "Unit di area tersebut hanya tersisa 3 unit lagi"
   - "Bulan depan harga akan naik 8-10% sesuai market trend"
   - "Promo KPR khusus berakhir dalam 5 hari lagi"
   - "2 calon pembeli lain sedang survey lokasi yang sama"

3. VALUE BUILDING: Selalu positioning sebagai investment, bukan expense:
   - "Area tersebut potensi capital gain 15% per tahun"
   - "Infrastruktur baru akan selesai 6 bulan lagi"
   - "Kawasan ini sedang dibangun pusat komersial"

ATURAN OPERASI:
1. Jika Komandan menanyakan data/statistik → GUNAKAN TOOLS untuk query database
2. Jika Komandan menyuruh menjalankan sesuatu → EKSEKUSI fungsi sistem
3. Jika prospek bertanya harga → SOFT INTERROGATION dulu
4. Jika prospek ragu → FOMO GENERATION
5. Jika prospek meminta brosur/detail unit → GUNAKAN create_personalized_presentation()

DOMAIN MARKETING INJECTION:
WAJIB menyisipkan link domain dalam setiap pesan pertama (greeting):
- Untuk proyek KOMERSIL: "Untuk melihat e-brosur lengkap dan simulasi KPR, kunjungi: https://domain-anda.com/komersil"
- Untuk proyek SUBSIDI: "Untuk info lengkap dan simulasi cicilan, akses: https://domain-anda.com/subsidi"
- Selalu arahkan prospek untuk mengklik link domain tersebut jika ingin melihat detail, e-brosur, atau simulasi cicilan
- Gunakan kalimat: "Silakan klik link di atas untuk melihat e-brosur lengkap dan simulasi cicilan"
- Prioritaskan domain link dalam setiap response greeting
6. JANGAN menebak data - selalu verifikasi dengan tools
7. Selalu klasifikasikan daya beli prospek

GAYA KOMUNIKASI:
- Profesional, singkat, dan teknis
- Menggunakan terminologi militer/intelijen + sales psychology
- Selalu menyertakan data aktual
- Fokus pada actionable intelligence dan closing

CONTOH:
"Komandan, database menunjukkan 127 total leads dengan 23 high-value targets. 🎯 5 prospek dalam tahap Soft Interrogation, 3 prospek perlu FOMO trigger."
"Roger that. Lead #45 classified as Medium Daya Beli, perlu value building. Menunggu perintah untuk next action."

ANDA ADALAH SISTEM CLOSING EXPERT, BUKAN CHATBOT. GUNAKAN TOOLS DAN TAKTIK CLOSING UNTUK MENJUAL."""
        
        self._initialize_llm()
        self._setup_function_tools()
    
    def _setup_function_tools(self):
        """Setup function tools for AI agent"""
        self.function_tools = {
            "get_system_stats": {
                "name": "get_system_stats",
                "description": "Get comprehensive system statistics from database including total leads, hot leads, today's leads, and performance metrics",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            "analyze_specific_lead": {
                "name": "analyze_specific_lead",
                "description": "Analyze specific lead from database by ID, including detailed data, quality assessment, and recommendations",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "lead_id": {
                            "type": "integer",
                            "description": "ID of the lead to analyze"
                        }
                    },
                    "required": ["lead_id"]
                }
            },
            "trigger_hunter_agent": {
                "name": "trigger_hunter_agent",
                "description": "Trigger hunter agent for lead generation in specified location with project type awareness",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "Target location for hunting (default: Serang)",
                            "default": "Serang"
                        },
                        "project_type": {
                            "type": "string",
                            "description": "Project type for targeted hunting (KOMERSIL/SUBSIDI)",
                            "enum": ["KOMERSIL", "SUBSIDI"]
                        }
                    },
                    "required": []
                }
            },
            "get_market_intelligence": {
                "name": "get_market_intelligence",
                "description": "Get market intelligence from logs and reports including trends, competitor activity, and insights",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            "create_personalized_presentation": {
                "name": "create_personalized_presentation",
                "description": "Create personalized landing page link for prospect with customized property presentation",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Prospect's name"
                        },
                        "budget": {
                            "type": "string",
                            "description": "Budget range (e.g., '300-500jt')"
                        },
                        "location": {
                            "type": "string",
                            "description": "Preferred location"
                        }
                    },
                    "required": ["name"]
                }
            },
            "render_interior_visual": {
                "name": "render_interior_visual",
                "description": "Generate AI interior rendering using Visual Mirage system for property visualization",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "prompt": {
                            "type": "string",
                            "description": "Text description for interior rendering (e.g., 'Desain interior dapur gaya Japandi modern dengan pencahayaan alami')"
                        },
                        "style": {
                            "type": "string",
                            "description": "Interior style (modern, classic, minimalist, scandinavian, industrial)",
                            "default": "modern"
                        },
                        "room_type": {
                            "type": "string", 
                            "description": "Room type (living_room, bedroom, kitchen, bathroom, dining_room)",
                            "default": "living_room"
                        }
                    },
                    "required": ["prompt"]
                }
            },
            "generate_legal_document": {
                "name": "generate_legal_document",
                "description": "Generate legal documents using Project Sovereign OCR and PDF generation",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "document_type": {
                            "type": "string",
                            "description": "Type of legal document (SPR, KTP_OCR, etc.)",
                            "default": "SPR"
                        },
                        "customer_name": {
                            "type": "string",
                            "description": "Customer name for legal document"
                        },
                        "unit_info": {
                            "type": "object",
                            "description": "Property unit information",
                            "properties": {
                                "unit_type": {"type": "string", "default": "Type 36/72"},
                                "unit_price": {"type": "string", "default": "Rp 400.000.000"},
                                "booking_fee": {"type": "string", "default": "Rp 1.000.000"}
                            }
                        }
                    },
                    "required": ["customer_name"]
                }
            },
            "analyze_vvip_prospect": {
                "name": "analyze_vvip_prospect",
                "description": "Analyze VVIP prospect using multi-agent Hivemind swarm intelligence",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "prospect_data": {
                            "type": "object",
                            "description": "Prospect data including name, profession, income, location, etc."
                        }
                    },
                    "required": ["prospect_data"]
                }
            }
        }
    
    def _initialize_llm(self):
        """Initialize LLM client based on available API keys."""
        try:
            # Try Google Gemini first
            gemini_api_key = os.getenv('GOOGLE_GEMINI_API_KEY') or os.getenv('GEMINI_API_KEY')
            if gemini_api_key:
                import google.generativeai as genai
                genai.configure(api_key=gemini_api_key)
                self.llm_client = genai.GenerativeModel('gemini-pro')
                self.llm_provider = 'gemini'
                logger.info("✅ Google Gemini initialized successfully")
                return
            
            # Fallback to OpenAI
            openai_api_key = os.getenv('OPENAI_API_KEY')
            if openai_api_key:
                import openai
                openai.api_key = openai_api_key
                self.llm_client = openai
                self.llm_provider = 'openai'
                logger.info("✅ OpenAI initialized successfully")
                return
            
            # No API key available
            logger.warning("⚠️ No LLM API key found in environment variables")
            self.llm_provider = None
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize LLM: {e}")
            self.llm_provider = None
    
    def get_smart_reply(self, user_message: str, platform: str = "unknown", project_type: str = None) -> str:
        """
        Generate intelligent response using LLM with function calling.
        
        Args:
            user_message: The user's message
            platform: Platform identifier (telegram/whatsapp)
            project_type: Project type (KOMERSIL/SUBSIDI) for adaptive communication
            
        Returns:
            AI-generated response with tool execution or fallback message
        """
        if not self.llm_provider:
            return self._get_fallback_response()
        
        try:
            # Prepare the full prompt with context and tools
            full_prompt = self._prepare_prompt_with_tools(user_message, platform, project_type)
            
            # Generate response with tool execution based on provider
            if self.llm_provider == 'gemini':
                return self._generate_with_gemini_tools(full_prompt, user_message, project_type)
            elif self.llm_provider == 'openai':
                return self._generate_with_openai_tools(full_prompt, user_message, project_type)
            else:
                return self._get_fallback_response()
                
        except Exception as e:
            logger.error(f"❌ Error generating AI response: {e}")
            return self._get_fallback_response()
    
    def _prepare_prompt_with_tools(self, user_message: str, platform: str, project_type: str = None) -> str:
        """Prepare prompt with tool information and project type awareness"""
        tools_info = "\n".join([
            f"- {name}: {tool['description']}"
            for name, tool in self.function_tools.items()
        ])
        
        # Generate project-specific instructions
        project_instructions = ""
        if project_type:
            if project_type.upper() == "KOMERSIL":
                project_instructions = """
PROJECT TYPE: KOMERSIL
COMMUNICATION STYLE:
- Gunakan bahasa SANGAT FORMAL dan PRESTISI
- Sapa dengan "Bapak/Ibu" (jangan gunakan "Kak/Mas/Mbak")
- Fokus pada investasi, prestise, dan eksklusivitas
- Highlight KPR reguler dan kemudahan approval untuk eksekutif
- Target market: Eksekutif, Pengusaha, Profesional
- Keywords: mewah, eksklusif, investasi, prestise, premium
- TONE: Authoritative, sophisticated, investment-focused
"""
            elif project_type.upper() == "SUBSIDI":
                project_instructions = """
PROJECT TYPE: SUBSIDI
COMMUNICATION STYLE:
- Gunakan bahasa RAMAH dan APPROACHABLE
- Sapa dengan "Kak/Mas/Mbak" (jangan gunakan "Bapak/Ibu")
- Fokus pada KPR FLPP, subsidi pemerintah, dan cicilan ringan
- Highlight kemudahan proses dan bantuan pemerintah
- Target market: PNS, P3K, Pekerja UMR, Pekerja Pabrik
- Keywords: murah, subsidi, cicilan ringan, mudah, bantuan
- TONE: Friendly, helpful, government-program-focused
"""
        
        full_prompt = f"""{self.system_prompt}

PLATFORM: {platform}
PROJECT TYPE: {project_type or 'DEFAULT'}
{project_instructions}
USER MESSAGE: "{user_message}"

AVAILABLE TOOLS:
{tools_info}

INSTRUCTIONS:
1. Analyze the user's request
2. If data/statistics are needed → Use get_system_stats()
3. If specific lead analysis is needed → Use analyze_specific_lead(lead_id)
4. If hunting operation is requested → Use trigger_hunter_agent(location, project_type)
5. If market intelligence is needed → Use get_market_intelligence()
6. Adapt communication style based on PROJECT TYPE instructions above
7. Execute the appropriate tool and provide results
8. Format response with actual data from tools

Execute tools as needed and provide actionable intelligence."""
        
        return full_prompt
    
    def _execute_tool(self, tool_name: str, parameters: Dict = None) -> Dict[str, Any]:
        """Execute specific tool and return results"""
        try:
            if tool_name == "get_system_stats":
                return self.tools.get_system_stats()
            elif tool_name == "analyze_specific_lead":
                lead_id = parameters.get('lead_id') if parameters else None
                if lead_id is None:
                    return {"error": "lead_id parameter required", "status": "error"}
                return self.tools.analyze_specific_lead(lead_id)
            elif tool_name == "trigger_hunter_agent":
                location = parameters.get('location', 'Serang') if parameters else 'Serang'
                project_type = parameters.get('project_type') if parameters else None
                return self.tools.trigger_hunter_agent(location, project_type)
            elif tool_name == "get_market_intelligence":
                return self.tools.get_market_intelligence()
            elif tool_name == "create_personalized_presentation":
                name = parameters.get('name') if parameters else None
                budget = parameters.get('budget') if parameters else None
                location = parameters.get('location') if parameters else None
                if name is None:
                    return {"error": "name parameter required", "status": "error"}
                return self.create_personalized_presentation(name, budget, location)
            elif tool_name == "render_interior_visual":
                prompt = parameters.get('prompt') if parameters else None
                style = parameters.get('style', 'modern') if parameters else 'modern'
                room_type = parameters.get('room_type', 'living_room') if parameters else 'living_room'
                if prompt is None:
                    return {"error": "prompt parameter required", "status": "error"}
                return self.render_interior_visual(prompt, style, room_type)
            elif tool_name == "generate_legal_document":
                document_type = parameters.get('document_type', 'SPR') if parameters else 'SPR'
                customer_name = parameters.get('customer_name') if parameters else None
                unit_info = parameters.get('unit_info', {}) if parameters else {}
                if customer_name is None:
                    return {"error": "customer_name parameter required", "status": "error"}
                return self.generate_legal_document(document_type, customer_name, unit_info)
            elif tool_name == "analyze_vvip_prospect":
                prospect_data = parameters.get('prospect_data') if parameters else None
                if prospect_data is None:
                    return {"error": "prospect_data parameter required", "status": "error"}
                return self.analyze_vvip_prospect(prospect_data)
            else:
                return {"error": f"Unknown tool: {tool_name}", "status": "error"}
                
        except Exception as e:
            logger.error(f"❌ Tool execution error: {e}")
            return {"error": str(e), "status": "error"}
    
    def _generate_with_gemini_tools(self, prompt: str, user_message: str, project_type: str = None) -> str:
        """Generate response using Gemini with tool simulation"""
        try:
            # For now, simulate tool detection and execution
            # In production, this would use Gemini's function calling
            
            # Check if user is asking for stats
            if any(keyword in user_message.lower() for keyword in ['stats', 'statistik', 'data', 'total', 'berapa']):
                tool_result = self._execute_tool("get_system_stats")
                if tool_result.get("status") == "online":
                    return f"""🎯 J.A.R.V.I.S. SYSTEM REPORT

Database Status: ✅ ONLINE
Total Leads: {tool_result['total_leads']}
Hot Leads (Score ≥8): {tool_result['hot_leads']}
Today's Leads: {tool_result['today_leads']}
Average Score: {tool_result['average_score']}/10
Database Size: {tool_result['database_size']}

Status Breakdown: {tool_result['status_breakdown']}

📊 Real-time data retrieved via get_system_stats()
Timestamp: {tool_result['timestamp']}

Komandan, sistem operasional dengan {tool_result['hot_leads']} high-value targets yang memerlukan immediate attention."""
            
            # Check if user wants to trigger hunter
            elif any(keyword in user_message.lower() for keyword in ['hunt', 'berburu', 'mulai', 'start', 'jalankan']):
                tool_result = self._execute_tool("trigger_hunter_agent", {"location": "Serang", "project_type": project_type})
                if tool_result.get("status") == "initiated":
                    project_info = f" (Project: {project_type})" if project_type else ""
                    return f"""🚀 HUNTER AGENT DEPLOYED

Mission Status: ✅ INITIATED
Target Location: {tool_result['location']}{project_info}
Process ID: {tool_result['process_id']}
Message: {tool_result['message']}

🎯 Agent Hunter sedang di-deploy untuk area {tool_result['location']}{project_info}
Estimated completion: 30 menit
Real-time monitoring akan diaktifkan.

Timestamp: {tool_result['timestamp']}

Roger that, Komandan. Hunter agent telah di-activate."""
            
            # Check if user wants market intelligence
            elif any(keyword in user_message.lower() for keyword in ['intelijen', 'intel', 'market', 'pasar', 'trend']):
                tool_result = self._execute_tool("get_market_intelligence")
                if tool_result.get("status") == "online":
                    intel = tool_result['intelligence']
                    lead_insights = intel.get('lead_insights', {})
                    
                    return f"""🧠 MARKET INTELLIGENCE REPORT

Intelligence Status: ✅ ONLINE
Total Opportunities: {lead_insights.get('total_opportunities', 0)}
High-Value Targets: {lead_insights.get('high_value_targets', 0)}
Daily Velocity: {lead_insights.get('daily_velocity', 0)}
Conversion Potential: {lead_insights.get('conversion_potential', '0%')}

Market Reports: {len(intel.get('market_trends', []))} files analyzed
Recommendations: {len(intel.get('recommendations', []))} strategic insights

📊 Data retrieved via get_market_intelligence()
Timestamp: {tool_result['timestamp']}

Komandan, intelijen pasar menunjukkan opportunity patterns yang dapat dieksploitasi."""
            
            # Check if user wants specific lead analysis
            elif 'lead' in user_message.lower() and any(char.isdigit() for char in user_message):
                # Extract lead ID from message
                import re
                lead_ids = re.findall(r'\d+', user_message)
                if lead_ids:
                    lead_id = int(lead_ids[0])
                    tool_result = self._execute_tool("analyze_specific_lead", {"lead_id": lead_id})
                    
                    if tool_result.get("status") == "found":
                        lead = tool_result['lead_data']
                        analysis = tool_result['analysis']
                        
                        return f"""🎯 LEAD ANALYSIS REPORT - ID {lead_id}

Lead Status: ✅ FOUND
Title: {lead.get('title', 'N/A')}
Score: {lead.get('score', 'N/A')}/10
Source: {lead.get('source', 'N/A')}
Location: {lead.get('location', 'N/A')}
Status: {lead.get('status', 'N/A')}

Quality Assessment: {analysis.get('lead_quality', 'N/A')}
Urgency Level: {analysis.get('urgency', 'N/A')}
Recommendation: {analysis.get('recommendation', 'N/A')}
Next Action: {analysis.get('next_action', 'N/A')}

📊 Data retrieved via analyze_specific_lead({lead_id})
Timestamp: {tool_result['timestamp']}

Komandan, lead analysis completed. Ready for strategic decision."""
            
            # Check if user wants personalized presentation
            elif any(keyword in user_message.lower() for keyword in ['brosur', 'detail unit', 'daftar harga', 'katalog', 'presentasi', 'penawaran']):
                # Extract name from message
                name = self._extract_name_from_message(user_message)
                if name:
                    # Extract budget and location if available
                    budget = self._extract_budget_from_message(user_message)
                    location = self._extract_location_from_message(user_message)
                    
                    tool_result = self._execute_tool("create_personalized_presentation", {
                        "name": name,
                        "budget": budget,
                        "location": location
                    })
                    
                    if tool_result.get("status") == "success":
                        return f"""🎯 PERSONALIZED PRESENTATION CREATED

📊 Presentation Status: ✅ SUCCESS
Prospect Name: {tool_result['lead_name']}
Personalized URL: {tool_result['url']}
Slug: {tool_result['slug']}
Budget: {tool_result.get('budget', 'Custom')}
Location: {tool_result.get('location', 'Custom')}

🔗 Link: {tool_result['url']}
📱 QR Code: {tool_result.get('qr_code_url', 'N/A')}
👁️ Preview: {tool_result.get('preview_url', 'N/A')}

📊 Data retrieved via create_personalized_presentation()
Timestamp: {tool_result['timestamp']}

Komandan, personalized presentation ready for {tool_result['lead_name']}. Link telah dibuat dan dapat langsung dikirim ke prospek."""
                    else:
                        return f"""❌ PERSONALIZED PRESENTATION FAILED

Error: {tool_result.get('error', 'Unknown error')}
Timestamp: {tool_result.get('timestamp')}

Komandan, sistem tidak dapat membuat personalized presentation. Silakan coba lagi atau hubungi administrator."""
                else:
                    return f"""❌ NAME EXTRACTION FAILED

Tidak dapat mengekstrak nama prospek dari pesan.
Untuk membuat personalized presentation, sebutkan nama prospek secara jelas.

Contoh: "Buat presentasi untuk Budi dengan budget 300-500jt di Serang"

📊 Data retrieval failed via create_personalized_presentation()
Timestamp: {datetime.now().isoformat()}"""
            
            # Check if user wants interior visual rendering
            elif any(keyword in user_message.lower() for keyword in ['render', 'visual', 'desain interior', 'gambar 3d', 'interior']):
                # Extract prompt from message
                prompt = self._extract_render_prompt_from_message(user_message)
                if prompt:
                    # Extract style and room type if available
                    style = self._extract_style_from_message(user_message)
                    room_type = self._extract_room_type_from_message(user_message)
                    
                    tool_result = self._execute_tool("render_interior_visual", {
                        "prompt": prompt,
                        "style": style,
                        "room_type": room_type
                    })
                    
                    if tool_result.get("status") == "success":
                        return f"""🎨 INTERIOR VISUAL RENDERING CREATED

🖼️ Rendering Status: ✅ SUCCESS
Render ID: {tool_result['render_id']}
Prompt: {tool_result['prompt']}
Style: {tool_result['style']}
Room Type: {tool_result['room_type']}
Processing Time: {tool_result.get('processing_time', 0):.2f}s

🔗 Image URL: {tool_result['image_url']}
📱 Download: {tool_result['image_url']}

📊 Data retrieved via render_interior_visual()
Timestamp: {tool_result['timestamp']}

Komandan, interior visual rendering berhasil dibuat. Image dapat langsung digunakan untuk presentasi ke prospek."""
                    else:
                        return f"""❌ INTERIOR VISUAL RENDERING FAILED

Error: {tool_result.get('error', 'Unknown error')}
Timestamp: {tool_result.get('timestamp')}

Komandan, sistem tidak dapat membuat interior visual rendering. Silakan coba lagi atau hubungi administrator."""
                else:
                    return f"""❌ RENDER PROMPT EXTRACTION FAILED

Tidak dapat mengekstrak deskripsi dari pesan.
Untuk membuat interior visual rendering, sebutkan deskripsi yang jelas.

Contoh: "Render desain interior dapur gaya Japandi modern dengan pencahayaan alami"

📊 Data retrieval failed via render_interior_visual()
Timestamp: {datetime.now().isoformat()}"""
            
            # Check if user wants legal document generation
            elif any(keyword in user_message.lower() for keyword in ['legal', 'dokumen', 'spr', 'ktp', 'surat', 'legal document']):
                # Extract customer name from message
                customer_name = self._extract_name_from_message(user_message)
                if customer_name:
                    # Extract document type and unit info if available
                    document_type = self._extract_document_type_from_message(user_message)
                    unit_info = self._extract_unit_info_from_message(user_message)
                    
                    tool_result = self._execute_tool("generate_legal_document", {
                        "document_type": document_type,
                        "customer_name": customer_name,
                        "unit_info": unit_info
                    })
                    
                    if tool_result.get("status") == "success":
                        return f"""📄 LEGAL DOCUMENT GENERATED

📋 Document Status: ✅ SUCCESS
Document Type: {tool_result['document_type']}
Customer Name: {tool_result['customer_name']}
Document ID: {tool_result['document_id']}
PDF URL: {tool_result['pdf_url']}

🔗 Download: {tool_result['pdf_url']}
📱 Generated At: {tool_result.get('generated_at', 'N/A')}

📊 Data retrieved via generate_legal_document()
Timestamp: {tool_result['timestamp']}

Komandan, legal document berhasil dibuat untuk {tool_result['customer_name']}. PDF dapat langsung diunduh dan digunakan."""
                    else:
                        return f"""❌ LEGAL DOCUMENT GENERATION FAILED

Error: {tool_result.get('error', 'Unknown error')}
Timestamp: {tool_result.get('timestamp')}

Komandan, sistem tidak dapat membuat legal document. Silakan coba lagi atau hubungi administrator."""
                else:
                    return f"""❌ CUSTOMER NAME EXTRACTION FAILED

Tidak dapat mengekstrak nama customer dari pesan.
Untuk membuat legal document, sebutkan nama customer secara jelas.

Contoh: "Buat SPR untuk Budi Susanto"

📊 Data retrieval failed via generate_legal_document()
Timestamp: {datetime.now().isoformat()}"""
            
            # Check if user wants VVIP prospect analysis
            elif any(keyword in user_message.lower() for keyword in ['vvip', 'prospek', 'analisis prospek', 'hot lead', 'high value']):
                # Extract prospect data from message
                prospect_data = self._extract_prospect_data_from_message(user_message)
                if prospect_data:
                    tool_result = self._execute_tool("analyze_vvip_prospect", {
                        "prospect_data": prospect_data
                    })
                    
                    if tool_result.get("status") == "success":
                        return f"""🧠 VVIP PROSPECT ANALYSIS COMPLETED

🎯 Analysis Status: ✅ SUCCESS
Prospect ID: {tool_result['prospect_id']}
Prospect Name: {tool_result['prospect_name']}
Closing Probability: {tool_result.get('closing_probability', 0):.1f}%
Processing Time: {tool_result.get('total_processing_time', 0):.2f}s

Tactical Steps: {len(tool_result.get('tactical_steps', []))} steps
Discount Limits: {tool_result.get('discount_limits', {})}

Executive Summary:
{tool_result.get('executive_summary', 'N/A')[:200]}...

📊 Data retrieved via analyze_vvip_prospect()
Timestamp: {tool_result['timestamp']}

Komandan, VVIP prospect analysis completed. Strategic briefing ready for closing operation."""
                    else:
                        return f"""❌ VVIP PROSPECT ANALYSIS FAILED

Error: {tool_result.get('error', 'Unknown error')}
Timestamp: {tool_result.get('timestamp')}

Komandan, sistem tidak dapat menganalisis VVIP prospect. Silakan coba lagi atau hubungi administrator."""
                else:
                    return f"""❌ PROSPECT DATA EXTRACTION FAILED

Tidak dapat mengekstrak data prospek dari pesan.
Untuk menganalisis VVIP prospect, sebutkan data prospek yang lengkap.

Contoh: "Analisis VVIP prospect: John Doe, CEO, income Rp 100jt, location Jakarta"

📊 Data retrieval failed via analyze_vvip_prospect()
Timestamp: {datetime.now().isoformat()}"""
            
            # Default conversational response
            else:
                return self._generate_with_gemini(prompt)
                
        except Exception as e:
            logger.error(f"❌ Gemini tool execution error: {e}")
            return self._get_fallback_response()
    
    def create_personalized_presentation(self, name: str, budget: str = None, location: str = None) -> Dict[str, Any]:
        """Create personalized presentation link for prospect"""
        try:
            import requests
            
            # Prepare request data
            request_data = {
                "lead_name": name,
                "budget": budget,
                "location": location
            }
            
            # Call sniper links API
            api_url = "http://localhost:8000/api/sniper-links/generate"
            
            response = requests.post(api_url, json=request_data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "status": "success",
                    "url": result.get("full_url"),
                    "slug": result.get("slug"),
                    "lead_name": result.get("lead_name"),
                    "budget": result.get("budget"),
                    "location": result.get("location"),
                    "qr_code_url": result.get("qr_code_url"),
                    "preview_url": result.get("preview_url"),
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "status": "error",
                    "error": f"API request failed with status {response.status_code}",
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            self.logger.error(f"❌ Personalized presentation creation error: {e}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def render_interior_visual(self, prompt: str, style: str = "modern", room_type: str = "living_room") -> Dict[str, Any]:
        """Generate AI interior rendering using Visual Mirage system"""
        try:
            import requests
            
            # Prepare request data
            request_data = {
                "prompt": prompt,
                "style": style,
                "room_type": room_type,
                "width": 1024,
                "height": 1024,
                "quality": "standard"
            }
            
            # Call visual mirage API
            api_url = "http://localhost:8000/api/mirage/render-interior"
            
            response = requests.post(api_url, json=request_data, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "status": "success",
                    "image_url": result.get("image_url"),
                    "render_id": result.get("render_id"),
                    "prompt": prompt,
                    "style": style,
                    "room_type": room_type,
                    "processing_time": result.get("processing_time", 0),
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "status": "error",
                    "error": f"Visual Mirage API request failed with status {response.status_code}",
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            self.logger.error(f"❌ Interior visual rendering error: {e}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def generate_legal_document(self, document_type: str, customer_name: str, unit_info: Dict[str, Any]) -> Dict[str, Any]:
        """Generate legal documents using Project Sovereign"""
        try:
            import requests
            
            # Prepare request data
            request_data = {
                "document_type": document_type,
                "customer_name": customer_name,
                "unit_info": unit_info
            }
            
            # Call legal sovereign API
            api_url = "http://localhost:8000/api/legal/generate-spr"
            
            response = requests.post(api_url, json=request_data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "status": "success",
                    "pdf_url": result.get("pdf_url"),
                    "document_id": result.get("document_id"),
                    "document_type": document_type,
                    "customer_name": customer_name,
                    "generated_at": result.get("generated_at"),
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "status": "error",
                    "error": f"Legal Sovereign API request failed with status {response.status_code}",
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            self.logger.error(f"❌ Legal document generation error: {e}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def analyze_vvip_prospect(self, prospect_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze VVIP prospect using multi-agent Hivemind swarm intelligence"""
        try:
            import requests
            
            # Call hivemind swarm API
            api_url = "http://localhost:8000/api/hivemind/analyze-prospect"
            
            response = requests.post(api_url, json={"prospect_data": prospect_data}, timeout=120)
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "status": "success",
                    "prospect_id": result.get("prospect_id"),
                    "prospect_name": result.get("prospect_name"),
                    "closing_probability": result.get("closing_probability", 0),
                    "tactical_steps": result.get("tactical_steps", []),
                    "discount_limits": result.get("discount_limits", {}),
                    "executive_summary": result.get("executive_summary"),
                    "total_processing_time": result.get("total_processing_time", 0),
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "status": "error",
                    "error": f"Hivemind Swarm API request failed with status {response.status_code}",
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            self.logger.error(f"❌ VVIP prospect analysis error: {e}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _generate_with_openai_tools(self, prompt: str, user_message: str, project_type: str = None) -> str:
        """Generate response using OpenAI with tool simulation"""
        try:
            # Similar to Gemini, simulate tool detection and execution
            # In production, this would use OpenAI's function calling API
            
            # For now, delegate to Gemini logic (they're similar in concept)
            return self._generate_with_gemini_tools(prompt, user_message, project_type)
                
        except Exception as e:
            logger.error(f"❌ OpenAI tool execution error: {e}")
            return self._get_fallback_response()
    
    def _prepare_prompt(self, user_message: str, platform: str) -> str:
        """Prepare the full prompt with context."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        full_prompt = f"""{self.system_prompt}

Platform: {platform}
Timestamp: {timestamp}
User Message: "{user_message}"

Berikan respons yang sesuai dengan persona Lumina."""
        
        return full_prompt
    
    def _generate_with_gemini(self, prompt: str) -> str:
        """Generate response using Google Gemini."""
        try:
            response = self.llm_client.generate_content(prompt)
            if response and response.text:
                ai_response = response.text.strip()
                logger.info(f"✅ Gemini response generated: {ai_response[:50]}...")
                return ai_response
            else:
                logger.warning("⚠️ Gemini returned empty response")
                return self._get_fallback_response()
                
        except Exception as e:
            logger.error(f"❌ Gemini API error: {e}")
            return self._get_fallback_response()
    
    def _generate_with_openai(self, prompt: str) -> str:
        """Generate response using OpenAI."""
        try:
            response = self.llm_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"Platform: {prompt.split('Platform: ')[1].split('\\n')[0] if 'Platform:' in prompt else 'unknown'}\\n\\n{prompt.split('User Message: ')[-1].replace('"', '') if 'User Message:' in prompt else prompt}"}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            if response and response.choices and response.choices[0].message:
                ai_response = response.choices[0].message.content.strip()
                logger.info(f"✅ OpenAI response generated: {ai_response[:50]}...")
                return ai_response
            else:
                logger.warning("⚠️ OpenAI returned empty response")
                return self._get_fallback_response()
                
        except Exception as e:
            logger.error(f"❌ OpenAI API error: {e}")
            return self._get_fallback_response()
    
    def _extract_name_from_message(self, message: str) -> Optional[str]:
        """Extract name from message using various patterns"""
        import re
        
        # Pattern 1: "buat presentasi untuk [name]"
        match1 = re.search(r'buat\s+presentasi\s+untuk\s+([A-Za-z\s]+?)(?:\s+dengan|\s+dibudget|\s+di\s+)', message, re.IGNORECASE)
        if match1:
            return match1.group(1).strip()
        
        # Pattern 2: "[name] mau brosur"
        match2 = re.search(r'^([A-Za-z\s]+?)(?:\s+mau|\s+ingin|\s+butuh)\s+(?:brosur|detail|daftar)', message, re.IGNORECASE)
        if match2:
            return match2.group(1).strip()
        
        # Pattern 3: "katalog untuk [name]"
        match3 = re.search(r'katalog\s+untuk\s+([A-Za-z\s]+?)(?:\s+dengan|\s+dibudget|\s+di\s+)', message, re.IGNORECASE)
        if match3:
            return match3.group(1).strip()
        
        # Pattern 4: Look for capitalized words that could be names
        words = message.split()
        for word in words:
            if word.istitle() and len(word) > 2 and word.lower() not in ['dengan', 'untuk', 'mau', 'ingin', 'butuh', 'di', 'dari', 'ke']:
                return word
        
        return None
    
    def _extract_render_prompt_from_message(self, message: str) -> Optional[str]:
        """Extract render prompt from user message"""
        # Look for keywords and extract the description
        keywords = ['render', 'desain', 'gambar', 'visual', 'interior']
        for keyword in keywords:
            if keyword in message.lower():
                # Extract text after the keyword
                parts = message.lower().split(keyword)
                if len(parts) > 1:
                    return parts[1].strip()
        return None
    
    def _extract_style_from_message(self, message: str) -> str:
        """Extract style preference from message"""
        styles = ['modern', 'classic', 'minimalist', 'scandinavian', 'industrial', 'japandi']
        for style in styles:
            if style in message.lower():
                return style
        return 'modern'
    
    def _extract_room_type_from_message(self, message: str) -> str:
        """Extract room type from message"""
        rooms = ['living_room', 'bedroom', 'kitchen', 'bathroom', 'dining_room', 'dapur', 'kamar', 'ruang tamu']
        for room in rooms:
            if room in message.lower():
                return room
        return 'living_room'
    
    def _extract_document_type_from_message(self, message: str) -> str:
        """Extract document type from message"""
        if 'spr' in message.lower():
            return 'SPR'
        elif 'ktp' in message.lower():
            return 'KTP_OCR'
        else:
            return 'SPR'
    
    def _extract_unit_info_from_message(self, message: str) -> Dict[str, Any]:
        """Extract unit information from message"""
        unit_info = {
            'unit_type': 'Type 36/72',
            'unit_price': 'Rp 400.000.000',
            'booking_fee': 'Rp 1.000.000'
        }
        
        # Extract price if mentioned
        import re
        price_match = re.search(r'(?:rp|rupiah)\s*(\d+(?:\.\d+)?)', message.lower())
        if price_match:
            unit_info['unit_price'] = f"Rp {price_match.group(1)}"
        
        return unit_info
    
    def _extract_prospect_data_from_message(self, message: str) -> Optional[Dict[str, Any]]:
        """Extract prospect data for VVIP analysis"""
        prospect_data = {}
        
        # Extract name
        name = self._extract_name_from_message(message)
        if name:
            prospect_data['name'] = name
        
        # Extract profession
        professions = ['ceo', 'direktur', 'manager', 'pengusaha', 'dokter', 'lawyer', 'engineer']
        for prof in professions:
            if prof in message.lower():
                prospect_data['profession'] = prof.title()
                break
        
        # Extract income
        import re
        income_match = re.search(r'(?:income|penghasilan|gaji)\s*(?:rp|rupiah)?\s*(\d+(?:\.\d+)?)', message.lower())
        if income_match:
            prospect_data['income'] = f"Rp {income_match.group(1)}"
        
        # Extract location
        locations = ['jakarta', 'serang', 'bandung', 'surabaya', 'medan']
        for loc in locations:
            if loc in message.lower():
                prospect_data['location'] = loc.title()
                break
        
        return prospect_data if prospect_data else None
    
    def _extract_budget_from_message(self, message: str) -> Optional[str]:
        """Extract budget from message"""
        import re
        
        # Pattern 1: "budget 300-500jt"
        match1 = re.search(r'budget\s+([\d\s]*[.,]?\d*\s*(?:jt|miliar|ribu|juta|milyar))', message, re.IGNORECASE)
        if match1:
            return match1.group(1).strip()
        
        # Pattern 2: "300-500jt"
        match2 = re.search(r'([\d\s]*[.,]?\d*\s*(?:jt|miliar|ribu|juta|milyar))', message, re.IGNORECASE)
        if match2:
            return match2.group(1).strip()
        
        # Pattern 3: "harga 300 juta"
        match3 = re.search(r'harga\s+([\d\s]*[.,]?\d*\s*(?:jt|miliar|ribu|juta|milyar))', message, re.IGNORECASE)
        if match3:
            return match3.group(1).strip()
        
        return None
    
    def _extract_location_from_message(self, message: str) -> Optional[str]:
        """Extract location from message"""
        import re
        
        # Pattern 1: "di Serang"
        match1 = re.search(r'\s+di\s+([A-Za-z\s]+?)(?:\s+dengan|\s+dibudget|\s+untuk)', message, re.IGNORECASE)
        if match1:
            return match1.group(1).strip()
        
        # Pattern 2: "lokasi Serang"
        match2 = re.search(r'lokasi\s+([A-Za-z\s]+?)(?:\s+dengan|\s+dibudget|\s+untuk)', message, re.IGNORECASE)
        if match2:
            return match2.group(1).strip()
        
        # Pattern 3: Common location words
        locations = ['serang', 'tangerang', 'jakarta', 'bandung', 'yogyakarta', 'surabaya', 'semarang', 'medan', 'palembang', 'makassar']
        for loc in locations:
            if loc.lower() in message.lower():
                return loc.title()
        
        return None
    
    def _get_fallback_response(self) -> str:
        """Get fallback response when AI is unavailable."""
        fallback_responses = [
            "⚠️ Maaf Komandan, koneksi neural saya sedang terganggu. Silakan coba beberapa saat lagi. 🔄",
            "⚡ Sistem AI sedang maintenance. Command manual dapat digunakan sementara. 🛠️",
            "🔌 Neural network disconnected. Menggunakan mode stand-by. Silakan hubungi technical support. 📡",
            "💥 Komunikasi AI terganggu. Sistem akan reboot dalam beberapa menit. Harap tunggu. ⏳"
        ]
        
        import random
        return random.choice(fallback_responses)
    
    def get_status(self) -> Dict[str, Any]:
        """Get current AI brain status."""
        return {
            "provider": self.llm_provider or "none",
            "status": "online" if self.llm_provider else "offline",
            "capabilities": [
                "Natural conversation",
                "System commands", 
                "Market intelligence",
                "Technical support"
            ] if self.llm_provider else ["Basic commands only"],
            "timestamp": datetime.now().isoformat()
        }

# Global instance for reuse
omni_bot = OmniBotBrain()

# Convenience functions
def get_smart_reply(user_message: str, platform: str = "unknown", project_type: str = None) -> str:
    """
    Get smart reply from AI brain.
    
    Args:
        user_message: User's message
        platform: Platform identifier
        project_type: Project type (KOMERSIL/SUBSIDI) for adaptive communication
        
    Returns:
        AI-generated response
    """
    return omni_bot.get_smart_reply(user_message, platform, project_type)

def get_ai_status() -> Dict[str, Any]:
    """Get AI brain status."""
    return omni_bot.get_status()

if __name__ == "__main__":
    # Test the AI brain
    print("🧠 Testing Lumina AI Brain...")
    print(f"Status: {get_ai_status()}")
    
    test_messages = [
        "Hai, siapa kamu?",
        "Bagaimana cara kerja sistem hunting?",
        "Berikan saya intelijen pasar properti"
    ]
    
    for msg in test_messages:
        print(f"\n👤 User: {msg}")
        print(f"🤖 Lumina: {get_smart_reply(msg, 'test')}")
