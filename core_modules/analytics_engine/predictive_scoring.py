"""
Predictive Scoring Engine - Analytics Engine

This module provides a hybrid scoring system that combines rule-based scoring
with AI sentiment analysis using Google Gemini API. It offers comprehensive
lead evaluation with fallback mechanisms and robust error handling.

Author: HUNTER_AGENT_AI_MARKETING_DIGITAL
Version: 1.0.0
"""

import os
import logging
import sys
import re
import json
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging with colored output for warnings/errors
class ColoredFormatter(logging.Formatter):
    """Custom formatter with colored output for warnings and errors"""
    
    COLORS = {
        'WARNING': '\033[93m',  # Yellow
        'ERROR': '\033[91m',   # Red
        'CRITICAL': '\033[91m', # Red
        'INFO': '\033[94m',    # Blue
        'DEBUG': '\033[92m',   # Green
        'RESET': '\033[0m'      # Reset
    }
    
    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        reset_color = self.COLORS['RESET']
        
        # Format the message
        formatted = super().format(record)
        
        # Add color to the entire message
        return f"{log_color}{formatted}{reset_color}"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/system_logs/predictive_scoring.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

# Apply colored formatter to console handler
for handler in logging.root.handlers:
    if isinstance(handler, logging.StreamHandler):
        handler.setFormatter(ColoredFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

logger = logging.getLogger(__name__)

class PredictiveScoringEngine:
    """
    Hybrid Predictive Scoring Engine
    
    Combines rule-based scoring with AI sentiment analysis to provide
    comprehensive lead evaluation with fallback mechanisms.
    """
    
    def __init__(self):
        """
        Initialize the Predictive Scoring Engine with pre-check system
        
        Performs pre-check for Gemini API key availability and sets up
        scoring configuration with graceful fallback.
        """
        self.logger = logging.getLogger(__name__)
        
        # Scoring configuration
        self.rule_based_weight = 0.6  # 60% weight for rule-based scoring
        self.ai_sentiment_weight = 0.4  # 40% weight for AI sentiment scoring
        
        # Rule-based scoring factors
        self.scoring_factors = {
            'phone_number': 20,      # Has phone number
            'job_pns_bumn': 30,      # PNS/BUMN job
            'location_banten_jakarta': 20,  # Prime location
            'email_present': 10,     # Has email
            'complete_data': 15,     # Data completeness
            'property_intent': 25     # Clear property intent
        }
        
        # AI sentiment configuration
        self.ai_enabled = True
        self.gemini_api_key = os.getenv('GEMINI_API_KEY', '')
        
        # Module status flag
        self.module_active = True
        
        # PRE-CHECK: Verify Gemini API key
        if not self._precheck_gemini():
            self.ai_enabled = False
            self.rule_based_weight = 1.0  # Use 100% rule-based scoring
            self.logger.info("[INFO] AI sentiment scoring disabled. Using rule-based scoring only.")
        
        self.logger.info("Predictive Scoring Engine initialized successfully")
    
    def _precheck_gemini(self) -> bool:
        """
        Pre-check system for Gemini API key availability
        
        Returns:
            bool: True if Gemini API key is available and valid, False otherwise
        """
        try:
            # Check if Gemini API key exists
            if not self.gemini_api_key:
                # Display colored warning message
                warning_msg = "[WARNING] GEMINI_API_KEY tidak ditemukan di environment variables."
                self.logger.warning(warning_msg)
                
                # Additional helpful information
                info_msg = "[INFO] AI Sentiment Scoring dinonaktifkan sementara."
                self.logger.info(info_msg)
                
                setup_msg = "[INFO] Untuk mengaktifkan AI scoring:"
                self.logger.info(setup_msg)
                self.logger.info("[INFO] 1. Dapatkan API key dari Google AI Studio")
                self.logger.info("[INFO] 2. Set environment variable: GEMINI_API_KEY=your_api_key_here")
                self.logger.info("[INFO] 3. Restart aplikasi untuk mengaktifkan AI scoring")
                
                return False
            
            # Basic API key format validation
            if len(self.gemini_api_key) < 20:
                error_msg = "[ERROR] GEMINI_API_KEY format tidak valid (terlalu pendek)."
                self.logger.error(error_msg)
                return False
            
            # Try to import and test google-generativeai
            try:
                import google.generativeai as genai
                
                # Test API key with minimal request
                genai.configure(api_key=self.gemini_api_key)
                model = genai.GenerativeModel('gemini-pro')
                
                # Quick test with a simple prompt
                response = model.generate_content("Test")
                
                if response and hasattr(response, 'text'):
                    success_msg = "[SUCCESS] Gemini API key valid dan terhubung."
                    self.logger.info(success_msg)
                    return True
                else:
                    error_msg = "[ERROR] Gemini API test gagal - response tidak valid."
                    self.logger.error(error_msg)
                    return False
                    
            except ImportError:
                error_msg = "[ERROR] Library 'google-generativeai' tidak terinstall."
                self.logger.error(error_msg)
                self.logger.info("[INFO] Install dengan: pip install google-generativeai")
                return False
                
            except Exception as e:
                error_msg = f"[ERROR] Gemini API connection error: {str(e)}"
                self.logger.error(error_msg)
                return False
                
        except Exception as e:
            error_msg = f"[ERROR] Error saat mengecek Gemini API: {str(e)}"
            self.logger.error(error_msg)
            return False
    
    def _rule_based_score(self, lead_data: Dict) -> int:
        """
        Calculate rule-based score based on data completeness and quality
        
        Args:
            lead_data: Dictionary containing lead information
            
        Returns:
            int: Rule-based score (0-100)
        """
        try:
            score = 0
            
            # Phone number scoring
            phone = lead_data.get('no_hp', '').strip()
            if phone and len(phone) >= 10:
                if phone.startswith('+62') or phone.startswith('08'):
                    score += self.scoring_factors['phone_number']
                    self.logger.debug(f"Phone score: +{self.scoring_factors['phone_number']}")
            
            # Job scoring (PNS/BUMN preference)
            catatan = lead_data.get('catatan', '').lower()
            nama = lead_data.get('nama', '').lower()
            job_keywords = ['pns', 'bumn', 'pegawai negeri', 'swasta', 'karyawan', 'guru', 'polri', 'tni']
            
            for keyword in job_keywords:
                if keyword in catatan or keyword in nama:
                    score += self.scoring_factors['job_pns_bumn']
                    self.logger.debug(f"Job score: +{self.scoring_factors['job_pns_bumn']} (keyword: {keyword})")
                    break
            
            # Location scoring (Banten/Jakarta preference)
            lokasi = lead_data.get('lokasi', '').lower()
            location_keywords = ['banten', 'jakarta', 'tangerang', 'serang', 'cilegon', 'tangerang selatan']
            
            for keyword in location_keywords:
                if keyword in lokasi:
                    score += self.scoring_factors['location_banten_jakarta']
                    self.logger.debug(f"Location score: +{self.scoring_factors['location_banten_jakarta']} (keyword: {keyword})")
                    break
            
            # Email scoring
            email = lead_data.get('email', '').strip()
            if email and '@' in email and '.' in email:
                score += self.scoring_factors['email_present']
                self.logger.debug(f"Email score: +{self.scoring_factors['email_present']}")
            
            # Data completeness scoring
            required_fields = ['nama', 'no_hp']
            optional_fields = ['email', 'lokasi', 'catatan', 'sumber']
            
            completeness = 0
            for field in required_fields:
                if lead_data.get(field, '').strip():
                    completeness += 2
            
            for field in optional_fields:
                if lead_data.get(field, '').strip():
                    completeness += 1
            
            if completeness >= 7:
                score += self.scoring_factors['complete_data']
                self.logger.debug(f"Completeness score: +{self.scoring_factors['complete_data']}")
            
            # Property intent scoring
            property_keywords = ['rumah', 'properti', 'beli', 'cari', 'kpr', 'cicilan', 'dp', 'uang muka', 'investasi']
            intent_text = f"{catatan} {nama}".lower()
            
            intent_count = sum(1 for keyword in property_keywords if keyword in intent_text)
            if intent_count >= 3:
                score += self.scoring_factors['property_intent']
                self.logger.debug(f"Property intent score: +{self.scoring_factors['property_intent']} (count: {intent_count})")
            
            # Ensure score is within bounds
            final_score = min(max(score, 0), 100)
            
            self.logger.info(f"Rule-based scoring completed: {final_score}/100")
            return final_score
            
        except Exception as e:
            self.logger.error(f"Error in rule-based scoring: {e}")
            return 50  # Return neutral score on error
    
    def _ai_sentiment_score(self, lead_data: Dict) -> int:
        """
        Calculate AI sentiment score using Google Gemini API
        
        Args:
            lead_data: Dictionary containing lead information
            
        Returns:
            int: AI sentiment score (0-100)
        """
        try:
            if not self.ai_enabled:
                self.logger.debug("AI sentiment scoring disabled, returning neutral score")
                return 50
            
            # Import google-generativeai
            import google.generativeai as genai
            
            # Configure API
            genai.configure(api_key=self.gemini_api_key)
            model = genai.GenerativeModel('gemini-pro')
            
            # Prepare text for sentiment analysis
            text_to_analyze = self._prepare_text_for_analysis(lead_data)
            
            # Create prompt for sentiment analysis
            prompt = f"""
            Analisis sentimen dari data lead properti berikut dan berikan skor 1-100:
            
            Data Lead:
            Nama: {lead_data.get('nama', 'Unknown')}
            No HP: {lead_data.get('no_hp', 'Unknown')}
            Email: {lead_data.get('email', 'Unknown')}
            Lokasi: {lead_data.get('lokasi', 'Unknown')}
            Sumber: {lead_data.get('sumber', 'Unknown')}
            Catatan: {lead_data.get('catatan', 'Tidak ada')}
            
            Text untuk analisis: {text_to_analyze}
            
            Berikan respons dalam format JSON:
            {{
                "sentiment_score": 85,
                "sentiment_label": "positive",
                "confidence": 90,
                "key_indicators": ["tertarik properti", "siap beli", "lokasi strategis"],
                "analysis": "Lead menunjukkan minat tinggi dengan indikasi pembelian"
            }}
            
            Skor sentimen:
            - 90-100: Sangat Positif (Hot Lead)
            - 70-89: Positif (Warm Lead)
            - 50-69: Netral (Cold Lead)
            - 30-49: Negatif (Very Cold Lead)
            - 1-29: Sangat Negatif (Not Interested)
            """
            
            # Generate response
            response = model.generate_content(prompt)
            
            if not response or not hasattr(response, 'text'):
                self.logger.error("Invalid Gemini API response")
                return 50
            
            # Parse JSON response
            response_text = response.text.strip()
            
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if not json_match:
                self.logger.error("No JSON found in Gemini response")
                return 50
            
            json_str = json_match.group(0)
            result = json.loads(json_str)
            
            sentiment_score = result.get('sentiment_score', 50)
            sentiment_label = result.get('sentiment_label', 'neutral')
            confidence = result.get('confidence', 50)
            key_indicators = result.get('key_indicators', [])
            analysis = result.get('analysis', '')
            
            # Validate score range
            sentiment_score = min(max(sentiment_score, 1), 100)
            
            self.logger.info(f"AI sentiment scoring completed: {sentiment_score}/100 ({sentiment_label})")
            self.logger.debug(f"Confidence: {confidence}%, Indicators: {key_indicators}")
            self.logger.debug(f"Analysis: {analysis}")
            
            return sentiment_score
            
        except ImportError:
            self.logger.error("google-generativeai library not available")
            return 50
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse Gemini JSON response: {e}")
            return 50
            
        except Exception as e:
            self.logger.error(f"Error in AI sentiment scoring: {e}")
            return 50  # Return neutral score on error
    
    def _prepare_text_for_analysis(self, lead_data: Dict) -> str:
        """
        Prepare text data for AI sentiment analysis
        
        Args:
            lead_data: Dictionary containing lead information
            
        Returns:
            str: Combined text for analysis
        """
        text_parts = []
        
        # Add name
        if lead_data.get('nama'):
            text_parts.append(f"Nama: {lead_data['nama']}")
        
        # Add contact info
        if lead_data.get('no_hp'):
            text_parts.append(f"Kontak: {lead_data['no_hp']}")
        
        if lead_data.get('email'):
            text_parts.append(f"Email: {lead_data['email']}")
        
        # Add location
        if lead_data.get('lokasi'):
            text_parts.append(f"Lokasi: {lead_data['lokasi']}")
        
        # Add source
        if lead_data.get('sumber'):
            text_parts.append(f"Sumber: {lead_data['sumber']}")
        
        # Add notes (most important for sentiment)
        if lead_data.get('catatan'):
            text_parts.append(f"Catatan: {lead_data['catatan']}")
        
        return " | ".join(text_parts)
    
    def calculate_final_score(self, lead_data: Dict) -> Dict[str, Any]:
        """
        Calculate final hybrid score combining rule-based and AI sentiment scoring
        
        Args:
            lead_data: Dictionary containing lead information
            
        Returns:
            Dict: Comprehensive scoring result with final score, category, and reasoning
        """
        try:
            self.logger.info(f"Starting hybrid scoring for lead: {lead_data.get('nama', 'Unknown')}")
            
            # Calculate rule-based score
            rule_score = self._rule_based_score(lead_data)
            
            # Calculate AI sentiment score (if enabled)
            if self.ai_enabled:
                ai_score = self._ai_sentiment_score(lead_data)
            else:
                ai_score = 50  # Neutral score when AI is disabled
            
            # Calculate weighted final score
            final_score = (rule_score * self.rule_based_weight) + (ai_score * self.ai_sentiment_weight)
            final_score = round(min(max(final_score, 0), 100), 2)
            
            # Determine category
            category = self._determine_category(final_score)
            
            # Generate scoring reasons
            reasons = self._generate_scoring_reasons(rule_score, ai_score, lead_data)
            
            # Create comprehensive result
            result = {
                'lead_id': lead_data.get('id', 'unknown'),
                'lead_name': lead_data.get('nama', 'Unknown'),
                'skor_akhir': final_score,
                'kategori': category,
                'alasan_skor': reasons,
                'scoring_breakdown': {
                    'rule_based_score': rule_score,
                    'ai_sentiment_score': ai_score,
                    'rule_weight': self.rule_based_weight,
                    'ai_weight': self.ai_sentiment_weight,
                    'ai_enabled': self.ai_enabled
                },
                'timestamp': datetime.now().isoformat(),
                'recommendations': self._generate_recommendations(final_score, category),
                'next_action': self._suggest_next_action(final_score, category)
            }
            
            self.logger.info(f"Hybrid scoring completed: {final_score}/100 ({category})")
            return result
            
        except Exception as e:
            self.logger.error(f"Error in calculate_final_score: {e}")
            return {
                'lead_id': lead_data.get('id', 'unknown'),
                'lead_name': lead_data.get('nama', 'Unknown'),
                'skor_akhir': 50,
                'kategori': 'Cold',
                'alasan_skor': f'Error occurred during scoring: {str(e)}',
                'scoring_breakdown': {
                    'rule_based_score': 50,
                    'ai_sentiment_score': 50,
                    'rule_weight': 1.0,
                    'ai_weight': 0.0,
                    'ai_enabled': False
                },
                'timestamp': datetime.now().isoformat(),
                'recommendations': ['Review lead data manually'],
                'next_action': 'Manual review required'
            }
    
    def _determine_category(self, score: float) -> str:
        """
        Determine lead category based on score
        
        Args:
            score: Final score (0-100)
            
        Returns:
            str: Category (Cold/Warm/Hot)
        """
        if score >= 80:
            return 'Hot'
        elif score >= 60:
            return 'Warm'
        else:
            return 'Cold'
    
    def _generate_scoring_reasons(self, rule_score: int, ai_score: int, lead_data: Dict) -> List[str]:
        """
        Generate detailed scoring reasons
        
        Args:
            rule_score: Rule-based score
            ai_score: AI sentiment score
            lead_data: Lead data
            
        Returns:
            List[str]: List of scoring reasons
        """
        reasons = []
        
        # Rule-based reasons
        if rule_score >= 70:
            reasons.append("Data lead sangat lengkap dan berkualitas")
        elif rule_score >= 50:
            reasons.append("Data lead cukup lengkap")
        else:
            reasons.append("Data lead perlu dilengkapi")
        
        # Specific rule-based factors
        if lead_data.get('no_hp'):
            reasons.append("✅ Memiliki nomor telepon valid")
        
        if lead_data.get('email'):
            reasons.append("✅ Memiliki alamat email")
        
        lokasi = lead_data.get('lokasi', '').lower()
        if any(keyword in lokasi for keyword in ['banten', 'jakarta', 'tangerang']):
            reasons.append("✅ Lokasi strategis (Banten/Jakarta)")
        
        catatan = lead_data.get('catatan', '').lower()
        if any(keyword in catatan for keyword in ['pns', 'bumn', 'pegawai negeri']):
            reasons.append("✅ Profil pekerjaan stabil (PNS/BUMN)")
        
        # AI sentiment reasons
        if self.ai_enabled:
            if ai_score >= 80:
                reasons.append("🤖 AI: Sentimen sangat positif, menunjukkan minat tinggi")
            elif ai_score >= 60:
                reasons.append("🤖 AI: Sentimen positif, ada minat yang jelas")
            elif ai_score >= 40:
                reasons.append("🤖 AI: Sentimen netral, perlu follow-up lebih lanjut")
            else:
                reasons.append("🤖 AI: Sentimen negatif, minat rendah")
        else:
            reasons.append("🤖 AI: Scoring dinonaktifkan, menggunakan rule-based saja")
        
        return reasons
    
    def _generate_recommendations(self, score: float, category: str) -> List[str]:
        """
        Generate recommendations based on score and category
        
        Args:
            score: Final score
            category: Lead category
            
        Returns:
            List[str]: List of recommendations
        """
        recommendations = []
        
        if category == 'Hot':
            recommendations.extend([
                "🔥 Prioritaskan untuk follow-up segera (maksimal 2 jam)",
                "📞 Hubungi langsung via telepon",
                "🏠 Siapkan jadwal viewing properti",
                "📋 Assign ke sales senior terbaik"
            ])
        elif category == 'Warm':
            recommendations.extend([
                "📧 Kirim email personal dalam 24 jam",
                "📱 Follow-up via WhatsApp dalam 2 hari",
                "📊 Kirim portfolio properti relevan",
                "🔄 Monitor engagement rate"
            ])
        else:  # Cold
            recommendations.extend([
                "📨 Tambahkan ke nurturing campaign",
                "📚 Kirim content edukasi properti",
                "⏰ Follow-up dalam 1 minggu",
                "📈 Monitor perubahan minat"
            ])
        
        # Score-specific recommendations
        if score >= 90:
            recommendations.append("⭐ Lead premium - berikan penawaran khusus")
        elif score <= 30:
            recommendations.append("⚠️ Low priority - batasi resource allocation")
        
        return recommendations
    
    def _suggest_next_action(self, score: float, category: str) -> str:
        """
        Suggest next best action based on score and category
        
        Args:
            score: Final score
            category: Lead category
            
        Returns:
            str: Next action suggestion
        """
        if category == 'Hot':
            return "🚀 Immediate Action: Hubungi sekarang juga dan jadwalkan meeting!"
        elif category == 'Warm':
            return "📈 Engage: Kirim informasi detail dan follow-up dalam 24 jam"
        else:
            return "🔄 Nurture: Tambahkan ke campaign dan monitor perkembangan"
    
    def get_scoring_status(self) -> Dict[str, Any]:
        """
        Get current scoring engine status and configuration
        
        Returns:
            Dict: Status information
        """
        return {
            'engine_version': '1.0.0',
            'ai_enabled': self.ai_enabled,
            'rule_based_weight': self.rule_based_weight,
            'ai_sentiment_weight': self.ai_sentiment_weight,
            'gemini_api_configured': bool(self.gemini_api_key),
            'scoring_factors': self.scoring_factors,
            'module_active': self.module_active,
            'timestamp': datetime.now().isoformat()
        }
    
    def batch_score_leads(self, leads_data: List[Dict]) -> List[Dict[str, Any]]:
        """
        Score multiple leads in batch
        
        Args:
            leads_data: List of lead dictionaries
            
        Returns:
            List[Dict]: List of scoring results
        """
        results = []
        
        self.logger.info(f"Starting batch scoring for {len(leads_data)} leads")
        
        for i, lead_data in enumerate(leads_data):
            try:
                result = self.calculate_final_score(lead_data)
                results.append(result)
                
                # Log progress every 10 leads
                if (i + 1) % 10 == 0:
                    self.logger.info(f"Processed {i + 1}/{len(leads_data)} leads")
                    
            except Exception as e:
                self.logger.error(f"Error scoring lead {i + 1}: {e}")
                # Add error result
                error_result = {
                    'lead_id': lead_data.get('id', f'lead_{i}'),
                    'lead_name': lead_data.get('nama', 'Unknown'),
                    'skor_akhir': 0,
                    'kategori': 'Error',
                    'alasan_skor': f'Scoring error: {str(e)}',
                    'timestamp': datetime.now().isoformat()
                }
                results.append(error_result)
        
        self.logger.info(f"Batch scoring completed: {len(results)} results")
        return results

# Main function for testing
def main():
    """
    Test the Predictive Scoring Engine with sample data
    """
    print("🧠 Testing Predictive Scoring Engine")
    print("=" * 50)
    
    # Initialize engine
    engine = PredictiveScoringEngine()
    
    # Show status
    status = engine.get_scoring_status()
    print(f"Engine Status: {status}")
    print()
    
    # Test with sample leads
    test_leads = [
        {
            'id': 1,
            'nama': 'Budi Santoso PNS',
            'no_hp': '+62812345678',
            'email': 'budi@gmail.com',
            'lokasi': 'Serang, Banten',
            'sumber': 'Website',
            'catatan': 'Saya PNS di Kementerian Pendidikan, cari rumah KPR di Serang dengan DP 20%'
        },
        {
            'id': 2,
            'nama': 'Siti Aminah',
            'no_hp': '08234567890',
            'email': '',
            'lokasi': 'Jakarta Selatan',
            'sumber': 'Facebook',
            'catatan': 'Cari apartemen studio untuk investasi'
        },
        {
            'id': 3,
            'nama': 'Ahmad',
            'no_hp': '08123456789',
            'lokasi': 'Bandung',
            'sumber': 'WhatsApp',
            'catatan': 'Tanya-tanya harga rumah'
        }
    ]
    
    # Score each lead
    for lead in test_leads:
        print(f"\n📊 Scoring Lead: {lead['nama']}")
        print("-" * 30)
        
        result = engine.calculate_final_score(lead)
        
        print(f"Final Score: {result['skor_akhir']}/100")
        print(f"Category: {result['kategori']}")
        print(f"Reasons: {len(result['alasan_skor'])} factors")
        print(f"Next Action: {result['next_action']}")
        
        # Show breakdown
        breakdown = result['scoring_breakdown']
        print(f"Rule-based: {breakdown['rule_based_score']}")
        print(f"AI Sentiment: {breakdown['ai_sentiment_score']}")
    
    print(f"\n✅ Testing completed!")

if __name__ == "__main__":
    main()
