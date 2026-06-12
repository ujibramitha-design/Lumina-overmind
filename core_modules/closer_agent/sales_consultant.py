"""
Sales Consultant Agent for Lumina OS
Intelligent follow-up message generation with AI-powered personalization

Author: HUNTER_AGENT_AI_MARKETING_DIGITAL
Version: 1.0.0
"""

import logging
import os
import sys
from datetime import datetime
from typing import Dict, Any, Optional
import json

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

# Import core modules
from core_modules.analytics_engine.predictive_scoring import PredictiveScoringEngine
from core_modules.db_manager import DatabaseManager

# Configure logging
logger = logging.getLogger(__name__)

class SalesConsultant:
    """
    Intelligent Sales Consultant Agent for Lumina OS
    
    Features:
    - AI-powered follow-up message generation
    - Personalized content based on lead scoring and demographics
    - Tone adaptation based on lead category (Hot/Warm/Cold)
    - Professional Indonesian language messaging
    """
    
    def __init__(self):
        """Initialize Sales Consultant Agent"""
        self.scoring_engine = PredictiveScoringEngine()
        self.db_manager = DatabaseManager()
        self.ai_enabled = self._check_gemini_availability()
        
        # Message tone templates for different lead categories
        self.tone_templates = {
            'Hot': {
                'style': 'urgent_direct',
                'salutation': 'Halo {nama}',
                'opening': 'Saya melihat Anda sangat tertarik dengan properti kami',
                'urgency': 'Kesempatan terbatas, unit yang Anda minati sedang banyak diminati',
                'call_to_action': 'Segera hubungi saya untuk reservasi unit',
                'closing': 'Jangan sampai kehilangan kesempatan emas ini'
            },
            'Warm': {
                'style': 'educational_nurturing',
                'salutation': 'Selamat pagi/sore {nama}',
                'opening': 'Terima kasih atas minat Anda pada properti kami',
                'urgency': 'Saya ingin memberikan informasi lebih detail',
                'call_to_action': 'Mari diskusikan lebih lanjut kebutuhan Anda',
                'closing': 'Saya siap membantu menemukan rumah impian Anda'
            },
            'Cold': {
                'style': 'soft_introduction',
                'salutation': 'Halo {nama}',
                'opening': 'Perkenalkan, saya dari Lumina OS Property Intelligence',
                'urgency': 'Mungkin Anda sedang mencari informasi properti',
                'call_to_action': 'Jika ada yang bisa saya bantu, jangan ragu menghubungi',
                'closing': 'Semoga hari Anda menyenangkan'
            }
        }
    
    def _check_gemini_availability(self) -> bool:
        """
        Check if Gemini API is available for AI message generation
        
        Returns:
            bool: True if Gemini API is available, False otherwise
        """
        try:
            gemini_api_key = os.getenv('GEMINI_API_KEY')
            if not gemini_api_key:
                logger.warning("GEMINI_API_KEY not found in environment variables")
                return False
            
            # Test import google-generativeai
            import google.generativeai as genai
            
            # Configure Gemini
            genai.configure(api_key=gemini_api_key)
            
            # Test with a simple generation
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content("Test")
            
            logger.info("Gemini API is available and working")
            return True
            
        except ImportError:
            logger.warning("google-generativeai library not installed")
            return False
        except Exception as e:
            logger.error(f"Gemini API check failed: {str(e)}")
            return False
    
    def _determine_message_tone(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Determine message tone based on lead scoring and category
        
        Args:
            lead_data: Dictionary containing lead information with skor_akhir and kategori
            
        Returns:
            Dict: Tone template for the lead
        """
        category = lead_data.get('kategori', 'Cold').lower()
        
        # Map category to tone template
        if category == 'hot':
            return self.tone_templates['Hot']
        elif category == 'warm':
            return self.tone_templates['Warm']
        else:
            return self.tone_templates['Cold']
    
    def _extract_personalization_data(self, lead_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Extract personalization data from lead information
        
        Args:
            lead_data: Dictionary containing lead information
            
        Returns:
            Dict: Personalization variables
        """
        personalization = {
            'nama': lead_data.get('nama', 'Calon Pelanggan'),
            'lokasi': lead_data.get('lokasi', 'area strategis kami'),
            'pekerjaan': lead_data.get('pekerjaan', 'profesional'),
            'sumber': lead_data.get('sumber', 'platform properti'),
            'catatan': lead_data.get('catatan', ''),
            'email': lead_data.get('email', ''),
            'no_hp': lead_data.get('no_hp', '')
        }
        
        # Extract additional context from notes
        catatan = lead_data.get('catatan', '').lower()
        
        # Property type inference from notes
        if 'type 36' in catatan or '36/72' in catatan:
            personalization['tipe_properti'] = 'type 36/72'
        elif 'type 45' in catatan or '45/90' in catatan:
            personalization['tipe_properti'] = 'type 45/90'
        elif 'cluster' in catatan:
            personalization['tipe_properti'] = 'cluster'
        else:
            personalization['tipe_properti'] = 'properti'
        
        # Budget inference from notes
        if 'juta' in catatan:
            import re
            budget_match = re.search(r'(\d+)\s*juta', catatan)
            if budget_match:
                personalization['budget'] = f"{budget_match.group(1)} juta"
        
        return personalization
    
    def _generate_ai_message(self, lead_data: Dict[str, Any], tone: Dict[str, str]) -> str:
        """
        Generate AI-powered follow-up message using Gemini API
        
        Args:
            lead_data: Dictionary containing lead information
            tone: Tone template for message generation
            
        Returns:
            str: AI-generated follow-up message
        """
        try:
            import google.generativeai as genai
            
            # Extract personalization data
            personal_data = self._extract_personalization_data(lead_data)
            
            # Create detailed prompt for Gemini
            prompt = f"""
Sebagai konsultan properti profesional, buatkan pesan follow-up yang persuasif dan personal dalam Bahasa Indonesia.

Data Lead:
- Nama: {personal_data['nama']}
- Lokasi: {personal_data['lokasi']}
- Pekerjaan: {personal_data['pekerjaan']}
- Sumber: {personal_data['sumber']}
- Catatan: {personal_data['catatan']}
- Email: {personal_data['email']}
- Telepon: {personal_data['no_hp']}
- Kategori: {lead_data.get('kategori', 'Cold')}
- Skor: {lead_data.get('skor_akhir', 0)}

Gaya Pesan: {tone['style']}
- Salam: {tone['salutation']}
- Pembuka: {tone['opening']}
- Urgensi: {tone['urgency']}
- Call to Action: {tone['call_to_action']}
- Penutup: {tone['closing']}

Instruksi:
1. Buat pesan yang natural dan persuasif, bukan gaya robot
2. Personalisasi dengan data pekerjaan dan lokasi
3. Sesuaikan nada dengan kategori lead (Hot/Warm/Cold)
4. Gunakan Bahasa Indonesia yang luwes dan profesional
5. Sertakan informasi relevan dari catatan lead
6. Buat pesan yang membangun kepercayaan dan hubungan
7. Panjang pesan sekitar 3-5 paragraf

Format output:
[Pesan lengkap dalam Bahasa Indonesia]
"""
            
            # Generate message with Gemini
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            
            ai_message = response.text.strip()
            
            logger.info(f"AI message generated for lead: {personal_data['nama']}")
            return ai_message
            
        except Exception as e:
            logger.error(f"AI message generation failed: {str(e)}")
            # Fallback to template-based message
            return self._generate_template_message(lead_data, tone)
    
    def _generate_template_message(self, lead_data: Dict[str, Any], tone: Dict[str, str]) -> str:
        """
        Generate template-based follow-up message as fallback
        
        Args:
            lead_data: Dictionary containing lead information
            tone: Tone template for message generation
            
        Returns:
            str: Template-generated follow-up message
        """
        personal_data = self._extract_personalization_data(lead_data)
        
        # Build message using template
        message_parts = [
            tone['salutation'].format(nama=personal_data['nama']),
            "",
            tone['opening'],
            f"Saya melihat dari {personal_data['sumber']} bahwa Anda tertarik dengan {personal_data['tipe_properti']} di {personal_data['lokasi']}.",
            ""
        ]
        
        # Add job-specific content if available
        if personal_data['pekerjaan'] != 'profesional':
            message_parts.append(f"Sebagai {personal_data['pekerjaan']}, saya yakin properti ini sangat cocok dengan kebutuhan Anda.")
            message_parts.append("")
        
        # Add notes-based content if available
        if personal_data['catatan']:
            message_parts.append(f"Dari catatan Anda: '{personal_data['catatan']}', saya paham bahwa Anda sedang serius mencari properti yang tepat.")
            message_parts.append("")
        
        message_parts.extend([
            tone['urgency'],
            "",
            tone['call_to_action'],
            "",
            tone['closing'],
            "",
            f"Best regards,",
            f"Sales Consultant",
            f"Lumina OS Property Intelligence",
            f"📱 {personal_data['no_hp']}" if personal_data['no_hp'] else "",
            f"📧 {personal_data['email']}" if personal_data['email'] else ""
        ])
        
        # Remove empty lines and join
        message = '\n'.join(line for line in message_parts if line.strip())
        
        return message
    
    def generate_followup_message(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate personalized follow-up message for a lead
        
        Args:
            lead_data: Dictionary containing lead information
            
        Returns:
            Dict: Generated message and metadata
        """
        try:
            # Validate lead data
            if not lead_data or not isinstance(lead_data, dict):
                raise ValueError("Invalid lead data provided")
            
            # Get lead scoring information
            skor_akhir = lead_data.get('skor_akhir', 0)
            kategori = lead_data.get('kategori', 'Cold')
            
            logger.info(f"Generating follow-up message for lead: {lead_data.get('nama', 'Unknown')} (Score: {skor_akhir}, Category: {kategori})")
            
            # Determine message tone
            tone = self._determine_message_tone(lead_data)
            
            # Generate message
            if self.ai_enabled:
                message = self._generate_ai_message(lead_data, tone)
                message_source = 'AI_Gemini'
            else:
                message = self._generate_template_message(lead_data, tone)
                message_source = 'Template'
            
            # Create result
            result = {
                'success': True,
                'message': message,
                'metadata': {
                    'lead_id': lead_data.get('id'),
                    'lead_name': lead_data.get('nama'),
                    'skor_akhir': skor_akhir,
                    'kategori': kategori,
                    'tone_style': tone['style'],
                    'message_source': message_source,
                    'generated_at': datetime.now().isoformat(),
                    'personalization': self._extract_personalization_data(lead_data)
                }
            }
            
            logger.info(f"Follow-up message generated successfully for {lead_data.get('nama', 'Unknown')}")
            return result
            
        except Exception as e:
            logger.error(f"Error generating follow-up message: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'message': None,
                'metadata': None
            }
    
    def batch_generate_messages(self, leads_data: list[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate follow-up messages for multiple leads
        
        Args:
            leads_data: List of lead dictionaries
            
        Returns:
            Dict: Batch generation results
        """
        results = []
        successful = 0
        failed = 0
        
        for lead in leads_data:
            result = self.generate_followup_message(lead)
            
            if result['success']:
                successful += 1
                results.append({
                    'lead_id': lead.get('id'),
                    'lead_name': lead.get('nama'),
                    'message': result['message'],
                    'metadata': result['metadata']
                })
            else:
                failed += 1
                results.append({
                    'lead_id': lead.get('id'),
                    'lead_name': lead.get('nama'),
                    'error': result['error'],
                    'message': None,
                    'metadata': None
                })
        
        return {
            'success': True,
            'total_processed': len(leads_data),
            'successful': successful,
            'failed': failed,
            'results': results,
            'generated_at': datetime.now().isoformat()
        }
    
    def get_agent_status(self) -> Dict[str, Any]:
        """
        Get current agent status and capabilities
        
        Returns:
            Dict: Agent status information
        """
        return {
            'agent_name': 'SalesConsultant',
            'ai_enabled': self.ai_enabled,
            'ai_provider': 'Google Gemini' if self.ai_enabled else None,
            'supported_categories': ['Hot', 'Warm', 'Cold'],
            'tone_styles': ['urgent_direct', 'educational_nurturing', 'soft_introduction'],
            'capabilities': [
                'Personalized messaging',
                'AI-powered content generation',
                'Tone adaptation',
                'Batch processing',
                'Template fallback'
            ],
            'status': 'operational',
            'checked_at': datetime.now().isoformat()
        }

# Export for easy import
__all__ = ['SalesConsultant']
