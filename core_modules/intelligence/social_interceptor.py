"""
LUMINA OS - PROJECT HIJACKER
====================================

Competitor Social Interception System
Black Ops Intelligence Module untuk Social Media Interception

Features:
- Social Listening & Comment Analysis
- Competitor Comment Interception
- AI-Powered Intent Detection
- Secret DM Generation
- Telegram Approval Workflow
- Anti-Ban Protection
"""

import os
import sys
import json
import time
import logging
import asyncio
import requests
from typing import Dict, Any, Optional, List
from datetime import datetime
from dataclasses import dataclass
from pathlib import Path

# Add root directory to Python path
root_dir = Path(__file__).parent.parent.parent.parent
sys.path.append(str(root_dir))

# Import required modules
try:
    import google.generativeai as genai
    from core_modules.db_manager_supabase import get_supabase_manager
    from core_modules.notifications.telegram_sender import get_telegram_sender
except ImportError as e:
    print(f"❌ Import error: {e}")
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
class CompetitorComment:
    """Data structure for competitor comments"""
    username: str
    comment: str
    competitor_name: str
    platform: str
    post_url: str
    timestamp: datetime
    comment_id: str

@dataclass
class InterceptedLead:
    """Data structure for intercepted leads"""
    original_comment: CompetitorComment
    intent_score: float
    intent_type: str
    secret_dm_draft: str
    lead_id: Optional[str] = None
    approval_status: str = "pending"  # pending, approved, rejected

class SocialInterceptor:
    """
    Project Hijacker - Social Media Interception System
    Black Ops Intelligence untuk competitor comment interception
    """
    
    def __init__(self):
        """Initialize Social Interceptor"""
        self.logger = logging.getLogger(__name__)
        
        # Initialize Gemini AI
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.gemini_model = genai.GenerativeModel('gemini-pro')
            self.logger.info(f"{GREEN}✅ Gemini AI initialized for social interception{END}")
        else:
            self.gemini_model = None
            self.logger.warning(f"{YELLOW}⚠️ Gemini API key not found - using fallback logic{END}")
        
        # Initialize database
        try:
            self.supabase_manager = get_supabase_manager()
            self.logger.info(f"{GREEN}✅ Database connected for social interception{END}")
        except Exception as e:
            self.supabase_manager = None
            self.logger.error(f"{RED}❌ Database connection failed: {e}{END}")
        
        # Initialize Telegram sender
        try:
            self.telegram_sender = get_telegram_sender()
            self.logger.info(f"{GREEN}✅ Telegram sender initialized for approval workflow{END}")
        except Exception as e:
            self.telegram_sender = None
            self.logger.error(f"{RED}❌ Telegram sender failed: {e}{END}")
        
        # Competitor monitoring list
        self.competitors = [
            "Perumahan A",
            "Perumahan B", 
            "Cluster X",
            "Griya Y",
            "Residence Z"
        ]
        
        # Intent detection patterns
        self.buying_intent_patterns = [
            "minat", "mau", "cari", "butuh", "harga", "cicilan", "dp", "kpr",
            "booking", "survey", "cek lokasi", "info", "spek", "fasilitas",
            "lokasi", "tipe", "unit", "stok", "available", "promo", "diskon"
        ]
        
        # Statistics
        self.stats = {
            'total_comments_processed': 0,
            'leads_intercepted': 0,
            'dm_drafts_generated': 0,
            'telegrams_sent': 0,
            'approved_interceptions': 0,
            'rejected_interceptions': 0,
            'last_reset': datetime.now().isoformat()
        }
        
        self.logger.info(f"{MAGENTA}🏴‍☠️ PROJECT HIJACKER: Social Interceptor initialized{END}")
        self.logger.info(f"{CYAN}🎯 Monitoring {len(self.competitors)} competitors{END}")
        self.logger.info(f"{GREEN}✅ Ready for Black Ops social interception{END}")
    
    def analyze_buying_intent(self, comment: str) -> Dict[str, Any]:
        """
        Analyze comment for buying intent using Gemini AI
        
        Args:
            comment: Comment text to analyze
            
        Returns:
            Dict with intent analysis results
        """
        try:
            if self.gemini_model:
                # Use Gemini AI for advanced analysis
                prompt = f"""
                Analisis komentar media sosial berikut untuk mendeteksi niat beli properti:
                
                Komentar: "{comment}"
                
                Evaluasi:
                1. Apakah komentar ini menunjukkan niat beli yang serius? (iya/tidak)
                2. Seberapa serius niat beli tersebut? (skala 1-10)
                3. Jenis niat apa yang terdeteksi? (Informasi, Harga, Cicilan, Survey, Booking)
                4. Kata kunci apa yang menunjukkan niat beli?
                
                Return dalam format JSON:
                {{
                    "has_buying_intent": true/false,
                    "intent_score": 1-10,
                    "intent_type": "Informational/Price/Cicilan/Survey/Booking",
                    "keywords": ["keyword1", "keyword2"],
                    "confidence": 0.0-1.0
                }}
                """
                
                response = self.gemini_model.generate_content(prompt)
                result_text = response.text
                
                # Parse JSON response
                try:
                    result = json.loads(result_text)
                    self.logger.debug(f"{CYAN}🧠 Gemini AI analysis: {result}{END}")
                    return result
                except json.JSONDecodeError:
                    self.logger.warning(f"{YELLOW}⚠️ Failed to parse Gemini response, using fallback{END}")
                    return self._fallback_intent_analysis(comment)
            else:
                # Fallback to pattern matching
                return self._fallback_intent_analysis(comment)
                
        except Exception as e:
            self.logger.error(f"{RED}❌ Intent analysis error: {str(e)}{END}")
            return self._fallback_intent_analysis(comment)
    
    def _fallback_intent_analysis(self, comment: str) -> Dict[str, Any]:
        """
        Fallback intent analysis using pattern matching
        
        Args:
            comment: Comment text to analyze
            
        Returns:
            Dict with basic intent analysis
        """
        comment_lower = comment.lower()
        
        # Check for buying intent keywords
        found_keywords = [pattern for pattern in self.buying_intent_patterns if pattern in comment_lower]
        
        has_intent = len(found_keywords) > 0
        intent_score = min(len(found_keywords) * 2, 10)  # Scale to 1-10
        
        # Determine intent type
        intent_type = "Informational"
        if any(word in comment_lower for word in ["harga", "rp", "juta", "miliar"]):
            intent_type = "Price"
        elif any(word in comment_lower for word in ["cicilan", "angsuran", "kpr"]):
            intent_type = "Cicilan"
        elif any(word in comment_lower for word in ["survey", "cek", "lokasi", "kunjungan"]):
            intent_type = "Survey"
        elif any(word in comment_lower for word in ["booking", "book", "pesan", "amankan"]):
            intent_type = "Booking"
        
        return {
            "has_buying_intent": has_intent,
            "intent_score": intent_score,
            "intent_type": intent_type,
            "keywords": found_keywords,
            "confidence": 0.7 if has_intent else 0.3
        }
    
    def generate_secret_dm_draft(self, comment_data: CompetitorComment, intent_analysis: Dict[str, Any]) -> str:
        """
        Generate secret DM draft using Gemini AI
        
        Args:
            comment_data: Original comment data
            intent_analysis: Intent analysis results
            
        Returns:
            Secret DM draft message
        """
        try:
            if self.gemini_model:
                prompt = f"""
                Buatkan draf DM rahasia yang persuasif untuk mengalihkan prospek dari kompetitor:
                
                Konteks:
                - Nama kompetitor: {comment_data.competitor_name}
                - Komentar prospek: "{comment_data.comment}"
                - Niat beli: {intent_analysis.get('intent_type', 'Unknown')}
                - Skor niat: {intent_analysis.get('intent_score', 0)}/10
                
                Instruksi:
                1. Buat DM yang personal dan tidak terlihat seperti spam
                2. Acknowledge bahwa mereka sedang melihat kompetitor
                3. Tawarkan value proposition yang lebih baik
                4. Sertakan call-to-action yang lembut
                5. Gunakan tone yang friendly dan helpful
                6. Max 160 karakter untuk platform limitations
                
                Contoh style: "Halo, saya liat Anda cari info di [Kompetitor]. Kami punya opsi lebih baik dengan cicilan lebih ringan. Mau dibantu?"
                """
                
                response = self.gemini_model.generate_content(prompt)
                dm_draft = response.text.strip()
                
                # Limit to 160 characters
                if len(dm_draft) > 160:
                    dm_draft = dm_draft[:157] + "..."
                
                self.logger.debug(f"{CYAN}📝 Secret DM generated: {dm_draft}{END}")
                return dm_draft
            else:
                # Fallback DM template
                return f"Halo, saya lihat Anda cari info di {comment_data.competitor_name}. Kami punya opsi lebih baik. Mau dibantu?"
                
        except Exception as e:
            self.logger.error(f"{RED}❌ DM generation error: {str(e)}{END}")
            return f"Halo, info properti lebih baik tersedia. Dibantu?"
    
    def save_intercepted_lead(self, comment_data: CompetitorComment, intent_analysis: Dict[str, Any], dm_draft: str) -> Optional[str]:
        """
        Save intercepted lead to database
        
        Args:
            comment_data: Original comment data
            intent_analysis: Intent analysis results
            dm_draft: Generated DM draft
            
        Returns:
            Lead ID if successful, None otherwise
        """
        try:
            if not self.supabase_manager:
                self.logger.error(f"{RED}❌ Database not available{END}")
                return None
            
            # Prepare lead data
            lead_data = {
                'business_name': f"Intercepted from {comment_data.competitor_name}",
                'contact': f"@{comment_data.username}",
                'url': comment_data.post_url,
                'keywords': ','.join(intent_analysis.get('keywords', [])),
                'source': 'Competitor_Intercept',
                'score': intent_analysis.get('intent_score', 0),
                'status': 'Intercepted',
                'location': 'Social Media',
                'date_found': comment_data.timestamp.isoformat(),
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(),
                'intercept_data': {
                    'original_comment': comment_data.comment,
                    'competitor': comment_data.competitor_name,
                    'platform': comment_data.platform,
                    'username': comment_data.username,
                    'intent_type': intent_analysis.get('intent_type'),
                    'dm_draft': dm_draft,
                    'intercept_timestamp': datetime.now().isoformat()
                }
            }
            
            # Insert to database
            result = self.supabase_manager.insert_lead(lead_data)
            
            if result['success']:
                lead_id = result['data']['id']
                self.logger.info(f"{GREEN}✅ Intercepted lead saved: {lead_id}{END}")
                return lead_id
            else:
                self.logger.error(f"{RED}❌ Failed to save intercepted lead: {result['error']}{END}")
                return None
                
        except Exception as e:
            self.logger.error(f"{RED}❌ Save intercepted lead error: {str(e)}{END}")
            return None
    
    def send_approval_notification(self, intercepted_lead: InterceptedLead) -> bool:
        """
        Send Telegram notification for approval
        
        Args:
            intercepted_lead: Intercepted lead data
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.telegram_sender:
                self.logger.error(f"{RED}❌ Telegram sender not available{END}")
                return False
            
            # Create approval message
            approval_message = f"""
🏴‍☠️ **BLACK OPS - LEAD INTERCEPTED**

🎯 **Target**: @{intercepted_lead.original_comment.username}
🏢 **Competitor**: {intercepted_lead.original_comment.competitor_name}
📱 **Platform**: {intercepted_lead.original_comment.platform}
⚡ **Intent Score**: {intercepted_lead.intent_score}/10
🎪 **Intent Type**: {intercepted_lead.intent_type}

💬 **Original Comment**:
"{intercepted_lead.original_comment.comment}"

📝 **Secret DM Draft**:
"{intercepted_lead.secret_dm_draft}"

🔗 **Post URL**: {intercepted_lead.original_comment.post_url}

---
**ACTION REQUIRED**:
[✅ Approve & Send DM] - [❌ Reject Interception]

Lead ID: {intercepted_lead.lead_id}
Intercepted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """.strip()
            
            result = self.telegram_sender.send_message(approval_message)
            
            if result:
                self.logger.info(f"{GREEN}✅ Approval notification sent for lead {intercepted_lead.lead_id}{END}")
                return True
            else:
                self.logger.error(f"{RED}❌ Failed to send approval notification{END}")
                return False
                
        except Exception as e:
            self.logger.error(f"{RED}❌ Approval notification error: {str(e)}{END}")
            return False
    
    def process_competitor_comment(self, username: str, comment: str, competitor_name: str, 
                                  platform: str = "Instagram", post_url: str = "") -> Dict[str, Any]:
        """
        Main function to process competitor comment
        
        Args:
            username: Commenter username
            comment: Comment text
            competitor_name: Competitor name
            platform: Social media platform
            post_url: Post URL
            
        Returns:
            Dict with processing results
        """
        try:
            self.logger.info(f"{CYAN}🎯 Processing competitor comment from @{username}{END}")
            self.stats['total_comments_processed'] += 1
            
            # Create comment data object
            comment_data = CompetitorComment(
                username=username,
                comment=comment,
                competitor_name=competitor_name,
                platform=platform,
                post_url=post_url,
                timestamp=datetime.now(),
                comment_id=f"{platform}_{username}_{int(time.time())}"
            )
            
            # Step 1: Analyze buying intent
            self.logger.info(f"{BLUE}🧠 Analyzing buying intent...{END}")
            intent_analysis = self.analyze_buying_intent(comment)
            
            if not intent_analysis.get('has_buying_intent', False):
                self.logger.info(f"{YELLOW}⚠️ No buying intent detected - ignoring comment{END}")
                return {
                    "status": "ignored",
                    "reason": "no_buying_intent",
                    "intent_score": intent_analysis.get('intent_score', 0)
                }
            
            # Step 2: Generate secret DM draft
            self.logger.info(f"{BLUE}📝 Generating secret DM draft...{END}")
            dm_draft = self.generate_secret_dm_draft(comment_data, intent_analysis)
            self.stats['dm_drafts_generated'] += 1
            
            # Step 3: Save intercepted lead
            self.logger.info(f"{BLUE}💾 Saving intercepted lead...{END}")
            lead_id = self.save_intercepted_lead(comment_data, intent_analysis, dm_draft)
            
            if not lead_id:
                return {
                    "status": "error",
                    "reason": "failed_to_save_lead"
                }
            
            self.stats['leads_intercepted'] += 1
            
            # Step 4: Create intercepted lead object
            intercepted_lead = InterceptedLead(
                original_comment=comment_data,
                intent_score=intent_analysis.get('intent_score', 0),
                intent_type=intent_analysis.get('intent_type', 'Unknown'),
                secret_dm_draft=dm_draft,
                lead_id=lead_id,
                approval_status="pending"
            )
            
            # Step 5: Send approval notification (no auto-send to avoid ban)
            self.logger.info(f"{BLUE}📤 Sending approval notification...{END}")
            notification_sent = self.send_approval_notification(intercepted_lead)
            
            if notification_sent:
                self.stats['telegrams_sent'] += 1
                self.logger.info(f"{GREEN}✅ Lead intercepted and notification sent{END}")
            else:
                self.logger.warning(f"{YELLOW}⚠️ Lead intercepted but notification failed{END}")
            
            return {
                "status": "intercepted",
                "lead_id": lead_id,
                "intent_score": intent_analysis.get('intent_score', 0),
                "intent_type": intent_analysis.get('intent_type', 'Unknown'),
                "dm_draft": dm_draft,
                "notification_sent": notification_sent,
                "approval_status": "pending"
            }
            
        except Exception as e:
            self.logger.error(f"{RED}❌ Process competitor comment error: {str(e)}{END}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def approve_interception(self, lead_id: str) -> Dict[str, Any]:
        """
        Approve interception and mark for manual DM sending
        
        Args:
            lead_id: Lead ID to approve
            
        Returns:
            Dict with approval result
        """
        try:
            if not self.supabase_manager:
                return {"status": "error", "error": "Database not available"}
            
            # Update lead status
            update_data = {
                'status': 'Approved_For_DM',
                'updated_at': datetime.now().isoformat(),
                'approval_timestamp': datetime.now().isoformat()
            }
            
            result = self.supabase_manager.update_lead(lead_id, update_data)
            
            if result['success']:
                self.stats['approved_interceptions'] += 1
                self.logger.info(f"{GREEN}✅ Interception approved for lead {lead_id}{END}")
                
                # Send confirmation to Telegram
                confirmation_message = f"✅ **APPROVED** - Lead {lead_id} ready for DM sending"
                self.telegram_sender.send_message(confirmation_message)
                
                return {
                    "status": "approved",
                    "lead_id": lead_id,
                    "message": "Interception approved - DM can be sent manually"
                }
            else:
                self.logger.error(f"{RED}❌ Failed to approve interception: {result['error']}{END}")
                return {
                    "status": "error",
                    "error": result['error']
                }
                
        except Exception as e:
            self.logger.error(f"{RED}❌ Approve interception error: {str(e)}{END}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def reject_interception(self, lead_id: str, reason: str = "Not qualified") -> Dict[str, Any]:
        """
        Reject interception
        
        Args:
            lead_id: Lead ID to reject
            reason: Rejection reason
            
        Returns:
            Dict with rejection result
        """
        try:
            if not self.supabase_manager:
                return {"status": "error", "error": "Database not available"}
            
            # Update lead status
            update_data = {
                'status': 'Rejected',
                'updated_at': datetime.now().isoformat(),
                'rejection_reason': reason,
                'rejection_timestamp': datetime.now().isoformat()
            }
            
            result = self.supabase_manager.update_lead(lead_id, update_data)
            
            if result['success']:
                self.stats['rejected_interceptions'] += 1
                self.logger.info(f"{YELLOW}⚠️ Interception rejected for lead {lead_id}: {reason}{END}")
                
                # Send confirmation to Telegram
                confirmation_message = f"❌ **REJECTED** - Lead {lead_id}: {reason}"
                self.telegram_sender.send_message(confirmation_message)
                
                return {
                    "status": "rejected",
                    "lead_id": lead_id,
                    "reason": reason
                }
            else:
                self.logger.error(f"{RED}❌ Failed to reject interception: {result['error']}{END}")
                return {
                    "status": "error",
                    "error": result['error']
                }
                
        except Exception as e:
            self.logger.error(f"{RED}❌ Reject interception error: {str(e)}{END}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get interception statistics"""
        return {
            **self.stats,
            "interception_rate": (self.stats['leads_intercepted'] / max(self.stats['total_comments_processed'], 1)) * 100,
            "approval_rate": (self.stats['approved_interceptions'] / max(self.stats['leads_intercepted'], 1)) * 100,
            "timestamp": datetime.now().isoformat()
        }
    
    def reset_statistics(self) -> None:
        """Reset statistics counters"""
        self.stats = {
            'total_comments_processed': 0,
            'leads_intercepted': 0,
            'dm_drafts_generated': 0,
            'telegrams_sent': 0,
            'approved_interceptions': 0,
            'rejected_interceptions': 0,
            'last_reset': datetime.now().isoformat()
        }
        self.logger.info(f"{YELLOW}🔄 Social Interceptor statistics reset{END}")

# Global social interceptor instance
social_interceptor = SocialInterceptor()

# Convenience functions
def process_competitor_comment(username: str, comment: str, competitor_name: str, 
                             platform: str = "Instagram", post_url: str = "") -> Dict[str, Any]:
    """
    Convenience function to process competitor comment
    
    Args:
        username: Commenter username
        comment: Comment text
        competitor_name: Competitor name
        platform: Social media platform
        post_url: Post URL
        
    Returns:
        Dict with processing results
    """
    return social_interceptor.process_competitor_comment(username, comment, competitor_name, platform, post_url)

def approve_interception(lead_id: str) -> Dict[str, Any]:
    """Convenience function to approve interception"""
    return social_interceptor.approve_interception(lead_id)

def reject_interception(lead_id: str, reason: str = "Not qualified") -> Dict[str, Any]:
    """Convenience function to reject interception"""
    return social_interceptor.reject_interception(lead_id, reason)

def get_interception_stats() -> Dict[str, Any]:
    """Convenience function to get interception statistics"""
    return social_interceptor.get_statistics()

# Test function
if __name__ == "__main__":
    print(f"{MAGENTA}{'='*80}{END}")
    print(f"{CYAN}LUMINA OS - PROJECT HIJACKER{END}")
    print(f"{MAGENTA}{'='*80}{END}")
    
    # Test comment processing
    print(f"{BLUE}🎯 Testing competitor comment processing...{END}")
    
    test_comment = "Minat untuk cluster A ini, cicilan per bulan berapa ya? DP berapa?"
    test_result = process_competitor_comment(
        username="prospect_user123",
        comment=test_comment,
        competitor_name="Perumahan A",
        platform="Instagram",
        post_url="https://instagram.com/p/example"
    )
    
    print(f"{GREEN}✅ Test result:{END}")
    for key, value in test_result.items():
        print(f"  {key}: {value}")
    
    # Show statistics
    stats = get_interception_stats()
    print(f"{CYAN}📊 Interception Statistics:{END}")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print(f"{MAGENTA}{'='*80}{END}")
