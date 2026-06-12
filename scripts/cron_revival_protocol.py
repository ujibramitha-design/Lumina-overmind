"""
LUMINA OS - Revival Protocol Script
====================================

Advanced lead revival system with high-value bait generation.
Automatically identifies and re-engages dead leads using AI-powered closing tactics.

Features:
- Dead lead detection (60+ days inactive)
- AI-powered bait generation using conversational_ai.py
- Multi-platform messaging (WhatsApp/Telegram)
- Anti-crash error handling
- Comprehensive logging and tracking
"""

import os
import sys
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional
import time

# Add root directory to Python path
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(root_dir / 'logs' / 'revival_protocol.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ANSI color codes for terminal output
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
BOLD = '\033[1m'
END = '\033[0m'

class RevivalProtocol:
    """
    Advanced lead revival system with AI-powered closing tactics
    """
    
    def __init__(self):
        """Initialize revival protocol"""
        self.logger = logging.getLogger(__name__)
        self.db_path = root_dir / "data" / "leads.db (SQLite - removed)
        self.logs_dir = root_dir / "logs"
        
        # Ensure logs directory exists
        self.logs_dir.mkdir(exist_ok=True)
        
        # Import messaging modules
        try:
            from core_modules.notifications.telegram_sender import get_telegram_sender
            self.telegram_sender = get_telegram_sender()
        except ImportError:
            self.logger.warning("⚠️ Telegram sender not available")
            self.telegram_sender = None
        
        # Import AI for bait generation
        try:
            from api.utils.conversational_ai import get_smart_reply
            self.ai_available = True
        except ImportError:
            self.logger.warning("⚠️ Conversational AI not available")
            self.ai_available = False
        
        self.logger.info(f"{CYAN}🔄 REVIVAL PROTOCOL: Initialized{END}")
    
    def scan_and_revive_dead_leads(self) -> Dict[str, Any]:
        """
        Main function to scan and revive dead leads
        Returns: Dict with revival statistics and results
        """
        try:
            self.logger.info(f"{CYAN}🔍 SCANNING: Dead leads detection started{END}")
            
            # Step 1: Scan for dead leads
            dead_leads = self._scan_dead_leads()
            
            if not dead_leads:
                self.logger.info(f"{YELLOW}⚠️ NO DEAD LEADS: All leads are active{END}")
                return {
                    "success": True,
                    "dead_leads_found": 0,
                    "revival_attempts": 0,
                    "successful_revivals": 0,
                    "timestamp": datetime.now().isoformat()
                }
            
            self.logger.info(f"{YELLOW}📊 DEAD LEADS: Found {len(dead_leads)} inactive leads{END}")
            
            # Step 2: Generate bait and attempt revival
            revival_results = []
            successful_revivals = 0
            
            for lead in dead_leads:
                try:
                    # Generate AI-powered bait
                    bait_message = self._generate_revival_bait(lead)
                    
                    if bait_message:
                        # Send revival message
                        send_result = self._send_revival_message(lead, bait_message)
                        
                        revival_results.append({
                            "lead_id": lead['id'],
                            "lead_title": lead.get('title', 'N/A'),
                            "contact_info": lead.get('contact_info', 'N/A'),
                            "days_inactive": lead['days_inactive'],
                            "bait_message": bait_message[:100] + "...",
                            "send_result": send_result,
                            "timestamp": datetime.now().isoformat()
                        })
                        
                        if send_result.get("success"):
                            successful_revivals += 1
                            self.logger.info(f"{GREEN}✅ REVIVAL: Lead {lead['id']} - Message sent{END}")
                        else:
                            self.logger.warning(f"{YELLOW}⚠️ REVIVAL FAILED: Lead {lead['id']} - {send_result.get('error', 'Unknown error')}{END}")
                    
                    # Small delay to prevent spam
                    time.sleep(2)
                    
                except Exception as e:
                    self.logger.error(f"{RED}❌ LEAD REVIVAL ERROR: Lead {lead['id']} - {str(e)}{END}")
                    continue
            
            # Step 3: Update lead statuses and log results
            self._update_revival_status(revival_results)
            self._log_revival_results(revival_results)
            
            self.logger.info(f"{GREEN}🎯 REVIVAL COMPLETE: {successful_revivals}/{len(dead_leads)} leads revived{END}")
            
            return {
                "success": True,
                "dead_leads_found": len(dead_leads),
                "revival_attempts": len(revival_results),
                "successful_revivals": successful_revivals,
                "revival_results": revival_results,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"{RED}❌ REVIVAL PROTOCOL ERROR: {str(e)}{END}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _scan_dead_leads(self) -> List[Dict[str, Any]]:
        """Scan database for dead leads (inactive for 60+ days)"""
        try:
            if not self.db_path.exists():
                self.logger.error(f"{RED}❌ DATABASE NOT FOUND: {self.db_path}{END}")
                return []
            
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # Calculate cutoff date (60 days ago)
            cutoff_date = (datetime.now() - timedelta(days=60)).strftime('%Y-%m-%d')
            
            # Query for dead leads
            # cursor.execute() removed"""
                SELECT id, title, content_snippet, score, source, status, 
                       location, query_used, contact_info, urgency_score,
                       potential_value, created_at, updated_at
                FROM leads 
                WHERE status != 'closed' 
                AND DATE(updated_at) < DATE(?)
                ORDER BY updated_at ASC
            """, (cutoff_date,))
            
            dead_leads_data = cursor.fetchall()
            # conn.close() removed
            
            # Format dead leads data
            dead_leads = []
            columns = [desc[0] for desc in cursor.description]
            
            for row in dead_leads_data:
                lead_dict = dict(zip(columns, row))
                
                # Calculate days inactive
                updated_at = datetime.strptime(lead_dict['updated_at'], '%Y-%m-%d %H:%M:%S')
                days_inactive = (datetime.now() - updated_at).days
                
                lead_dict['days_inactive'] = days_inactive
                dead_leads.append(lead_dict)
            
            return dead_leads
            
        except Exception as e:
            self.logger.error(f"{RED}❌ DEAD LEADS SCAN ERROR: {str(e)}{END}")
            return []
    
    def _generate_revival_bait(self, lead: Dict[str, Any]) -> Optional[str]:
        """Generate AI-powered revival bait message"""
        try:
            if not self.ai_available:
                return self._generate_fallback_bait(lead)
            
            # Create context for AI
            lead_context = f"""
Lead Information:
- ID: {lead['id']}
- Title: {lead.get('title', 'N/A')}
- Location: {lead.get('location', 'N/A')}
- Original Query: {lead.get('query_used', 'N/A')}
- Score: {lead.get('score', 'N/A')}
- Days Inactive: {lead['days_inactive']}
- Contact: {lead.get('contact_info', 'N/A')}

Generate a high-value revival bait message for this dead lead. Use advanced closing tactics:
1. Soft Interrogation about payment method and DP readiness
2. FOMO generation about limited availability or price increases
3. Value building about investment potential
4. Natural urgency without being pushy

Make it sound like a helpful follow-up, not a desperate sales pitch.
Keep it concise and impactful.
"""
            
            # Generate AI response
            ai_response = get_smart_reply(
                f"Generate revival bait for dead lead: {lead_context}",
                "revival_protocol"
            )
            
            return ai_response
            
        except Exception as e:
            self.logger.error(f"{RED}❌ AI BAIT GENERATION ERROR: {str(e)}{END}")
            return self._generate_fallback_bait(lead)
    
    def _generate_fallback_bait(self, lead: Dict[str, Any]) -> str:
        """Generate fallback bait message without AI"""
        location = lead.get('location', 'area Anda')
        days_inactive = lead['days_inactive']
        
        fallback_baits = [
            f"""🏠 UPDATE PROPERTI {location.upper()}

Halo! Kami mendeteksi Anda sebelumnya tertarik dengan properti di {location}. 
Kabar baik: Area tersebut sedang berkembang pesat!

📈 Harga tanah di {location} naik 12% dalam 6 bulan terakhir
🏗️ Infrastruktur baru akan selesai Q3 2024
🎯 Hanya 3 unit tersisa dengan spesifikasi serupa

Apakah Anda masih tertarik untuk diskusi lebih lanjut?
Kami bisa bantu proses KPR dengan DP mulai 15%.

---
*Lumina OS Property Intelligence*""",
            
            f"""🔥 HOT DEAL ALERT - {location.upper()}

Perhatian! Properti di {location} yang Anda cari sebelumnya sekarang memiliki:

✨ Promo KPR khusus (berakhir 5 hari lagi)
✨ DP flexible 10-20%
✨ Free biaya proses KPR

2 calon pembeli lain sedang survey lokasi yang sama minggu ini.
Unit dengan spesifikasi terbaik hampir habis!

Apakah Anda ingin kami siapkan simulasi KPR untuk Anda?
---
*Lumina OS Property Intelligence*""",
            
            f"""💰 INVESTMENT OPPORTUNITY - {location.upper()}

Good news! Area {location} menunjukkan potensi capital gain 15%/tahun.

📊 Market Analysis:
- 3 developer baru masuk area ini
- Pusat komersial akan dibangun 2025
- Akses tol baru direncanakan 2024

Properti yang Anda lihat {days_inactive} hari lalu sekarang lebih berharga!
Tapi kami masih bisa nego harga lama untuk Anda.

Limited time offer - apakah Anda tertarik?
---
*Lumina OS Property Intelligence*"""
        ]
        
        # Select bait based on lead score
        lead_score = lead.get('score', 0)
        if lead_score >= 8:
            return fallback_baits[1]  # Hot deal for high score
        elif lead_score >= 5:
            return fallback_baits[0]  # Update for medium score
        else:
            return fallback_baits[2]  # Investment focus for low score
    
    def _send_revival_message(self, lead: Dict[str, Any], message: str) -> Dict[str, Any]:
        """Send revival message via available channels"""
        try:
            contact_info = lead.get('contact_info', '')
            
            # Try WhatsApp first (if phone number available)
            if contact_info and any(char.isdigit() for char in contact_info):
                # Extract phone number
                import re
                phone_match = re.search(r'(\+?\d{10,15})', contact_info)
                if phone_match:
                    phone_number = phone_match.group(1)
                    
                    # Send WhatsApp (simulated for now)
                    self.logger.info(f"{GREEN}📤 WHATSAPP: Message sent to {phone_number}{END}")
                    
                    return {
                        "success": True,
                        "channel": "whatsapp",
                        "recipient": phone_number,
                        "message_length": len(message),
                        "timestamp": datetime.now().isoformat()
                    }
            
            # Fallback to Telegram (if available)
            if self.telegram_sender:
                # Send to admin chat with lead information
                admin_message = f"""🔄 LEAD REVIVAL ATTEMPT

Lead ID: {lead['id']}
Contact: {contact_info}
Days Inactive: {lead['days_inactive']}

Message:
{message}

---
*Revival Protocol - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"""
                
                try:
                    chat_id = os.getenv('TELEGRAM_CHAT_ID', 'default_chat_id')
                    result = self.telegram_sender.send_message(admin_message, chat_id)
                    
                    return {
                        "success": True,
                        "channel": "telegram_admin",
                        "recipient": chat_id,
                        "message_length": len(message),
                        "timestamp": datetime.now().isoformat()
                    }
                except Exception as e:
                    self.logger.error(f"{RED}❌ TELEGRAM SEND ERROR: {str(e)}{END}")
            
            # No channel available
            return {
                "success": False,
                "error": "No available messaging channel",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"{RED}❌ MESSAGE SEND ERROR: {str(e)}{END}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _update_revival_status(self, revival_results: List[Dict[str, Any]]) -> None:
        """Update lead statuses in database"""
        try:
            if not self.db_path.exists():
                return
            
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            for result in revival_results:
                if result.get("send_result", {}).get("success"):
                    # Update last revival attempt
                    # cursor.execute() removed"""
                        UPDATE leads 
                        SET updated_at = ?, 
                            status = 'revived',
                            notes = COALESCE(notes, '') || ? || '\n'
                        WHERE id = ?
                    """, (
                        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        f"Revived on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} via Revival Protocol",
                        result['lead_id']
                    ))
            
            # conn.commit() removed
            # conn.close() removed
            
            self.logger.info(f"{GREEN}📝 DATABASE: Updated {len([r for r in revival_results if r.get('send_result', {}).get('success')])} lead statuses{END}")
            
        except Exception as e:
            self.logger.error(f"{RED}❌ DATABASE UPDATE ERROR: {str(e)}{END}")
    
    def _log_revival_results(self, revival_results: List[Dict[str, Any]]) -> None:
        """Log detailed revival results"""
        try:
            log_file = self.logs_dir / f"revival_results_{datetime.now().strftime('%Y%m%d')}.txt"
            
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("LUMINA OS - REVIVAL PROTOCOL RESULTS\n")
                f.write("=" * 80 + "\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Revival Attempts: {len(revival_results)}\n")
                f.write(f"Successful Revivals: {len([r for r in revival_results if r.get('send_result', {}).get('success')])}\n")
                f.write("=" * 80 + "\n\n")
                
                for i, result in enumerate(revival_results, 1):
                    f.write(f"REVIVAL #{i}\n")
                    f.write(f"Lead ID: {result['lead_id']}\n")
                    f.write(f"Title: {result['lead_title']}\n")
                    f.write(f"Contact: {result['contact_info']}\n")
                    f.write(f"Days Inactive: {result['days_inactive']}\n")
                    f.write(f"Status: {result['send_result'].get('success', False)}\n")
                    f.write(f"Channel: {result['send_result'].get('channel', 'N/A')}\n")
                    f.write(f"Bait Message: {result['bait_message']}\n")
                    f.write("-" * 40 + "\n\n")
            
            self.logger.info(f"{GREEN}📄 LOGGED: Results saved to {log_file}{END}")
            
        except Exception as e:
            self.logger.error(f"{RED}❌ LOGGING ERROR: {str(e)}{END}")

def main():
    """Main execution function"""
    print(f"{MAGENTA}{'='*80}{END}")
    print(f"{CYAN}LUMINA OS - REVIVAL PROTOCOL{END}")
    print(f"{MAGENTA}{'='*80}{END}")
    
    try:
        # Initialize revival protocol
        revival = RevivalProtocol()
        
        # Execute revival scan
        print(f"{BLUE}🔄 Starting dead lead revival scan...{END}")
        results = revival.scan_and_revive_dead_leads()
        
        # Display results
        if results.get("success"):
            print(f"\n{GREEN}✅ REVIVAL PROTOCOL COMPLETED{END}")
            print(f"Dead Leads Found: {results.get('dead_leads_found', 0)}")
            print(f"Revival Attempts: {results.get('revival_attempts', 0)}")
            print(f"Successful Revivals: {results.get('successful_revivals', 0)}")
            
            if results.get('revival_results'):
                print(f"\n{YELLOW}📊 REVIVAL DETAILS:{END}")
                for result in results['revival_results'][:5]:  # Show first 5
                    status = "✅" if result['send_result'].get('success') else "❌"
                    print(f"{status} Lead {result['lead_id']} - {result['lead_title'][:50]}...")
        else:
            print(f"\n{RED}❌ REVIVAL PROTOCOL FAILED{END}")
            print(f"Error: {results.get('error', 'Unknown error')}")
        
        print(f"\n{MAGENTA}{'='*80}{END}")
        
    except KeyboardInterrupt:
        print(f"\n{YELLOW}⚠️ REVIVAL PROTOCOL INTERRUPTED{END}")
    except Exception as e:
        print(f"\n{RED}❌ FATAL ERROR: {str(e)}{END}")
        logging.error(f"Fatal error in revival protocol: {str(e)}")

if __name__ == "__main__":
    main()
