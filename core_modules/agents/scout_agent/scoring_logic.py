"""
Elite Hunter - Lead Scoring Logic Module
Sistem intelligent scoring dengan LLM integration untuk analisis lead yang lebih akurat
Enhanced dengan Property Intelligence untuk comprehensive market analysis
"""

import re
import json
import os
import random
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Try to import OpenAI, but make it optional for fallback
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    openai = None
    logging.warning("OpenAI not available. Using fallback scoring method.")

# Import alert manager for Telegram notifications
try:
    from core_modules.notifications.alert_manager import send_high_intent_alert
    TELEGRAM_ALERTS_AVAILABLE = True
    logging.info("Telegram alert system available for high-intent leads")
except ImportError:
    TELEGRAM_ALERTS_AVAILABLE = False
    logging.warning("Telegram alert system not available")

# Import Property Scout for market intelligence
try:
    from .property_scout import property_scout
    PROPERTY_SCOUT_AVAILABLE = True
    logging.info("Property scout system available for market intelligence")
except ImportError:
    PROPERTY_SCOUT_AVAILABLE = False
    logging.warning("Property scout system not available")

# Import Agency Scout for agency intelligence
try:
    from .agency_scout import agency_scout
    AGENCY_SCOUT_AVAILABLE = True
    logging.info("Agency scout system available for agency intelligence")
except ImportError:
    AGENCY_SCOUT_AVAILABLE = False
    logging.warning("Agency scout system not available")

class LeadScoringEngine:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Initialize OpenAI client if available
        self.openai_client = None
        self.use_llm = False
        
        if OPENAI_AVAILABLE and os.getenv('OPENAI_API_KEY'):
            try:
                openai.api_key = os.getenv('OPENAI_API_KEY')
                self.openai_client = openai
                self.use_llm = True
                self.logger.info("OpenAI client initialized successfully")
            except Exception as e:
                self.logger.error(f"Failed to initialize OpenAI client: {e}")
                self.use_llm = False
        else:
            self.logger.warning("OpenAI not configured. Using fallback scoring method.")
            self.use_llm = False
        
        # Initialize Property Scout if available
        self.property_scout = None
        if PROPERTY_SCOUT_AVAILABLE:
            self.property_scout = property_scout
            self.logger.info("Property scout initialized successfully")
        
        # Initialize Agency Scout if available
        self.agency_scout = None
        if AGENCY_SCOUT_AVAILABLE:
            self.agency_scout = agency_scout
            self.logger.info("Agency scout initialized successfully")
        
        # Advanced Intelligence Layer - Entity Extraction Patterns
        self.entity_patterns = {
            'price': [
                r'(\d+\s*(?:juta|miliar|ribu|jt|milyar|rb))\s*(?:rupiah|rp)',
                r'(?:rp|rupiah)\s*(\d+(?:\.\d+)?)',
                r'harga\s*(?:rp|rupiah)?\s*(\d+(?:\.\d+)?)',
                r'(\d+(?:\.\d+)?)\s*(?:juta|miliar|ribu)',
                r'cicilan\s*(?:rp|rupiah)?\s*(\d+(?:\.\d+)?)',
                r'dp\s*(?:rp|rupiah)?\s*(\d+(?:\.\d+)?)',
                r'uang\s*muka\s*(?:rp|rupiah)?\s*(\d+(?:\.\d+)?)'
            ],
            'location': [
                r'(?:di|daerah|wilayah|kawasan)\s*([a-zA-Z\s]+?)(?:[,\.]|$)',
                r'([a-zA-Z\s]+?)\s*(?:serang|tangerang|jakarta|bogor|depok|bekasi)',
                r'([a-zA-Z\s]+?)(?:serang|tangerang|jakarta|bogor|depok|bekasi)',
                r'cluster\s*([a-zA-Z0-9\s]+)',
                r'perumahan\s*([a-zA-Z0-9\s]+)',
                r'griya\s*([a-zA-Z0-9\s]+)',
                r'([a-zA-Z0-9\s]+)\s*residence'
            ],
            'bank': [
                r'(?:bank|kpr)\s*([a-zA-Z\s]+)',
                r'([a-zA-Z\s]+?)(?:bank|kpr)',
                r'kpr\s*([a-zA-Z\s]+)',
                r'btn|bni|bri|bca|mandiri|cimb|danamon|permata|panin',
                r'btn|bni|bri|bca|mandiri|cimb|danamon|permata|panin'
            ],
            'pain_point': [
                r'(?:(?:khawatir|sulit|bingung|masalah|kendala|kesulitan)\s*(?:dengan|tentang|soal))\s*([a-zA-Z\s]+)',
                r'(?:(?:belum|belum punya|tidak ada)\s*(?:dp|uang\s*muka|biaya))',
                r'(?:(?:cicilan\s*(?:terlalu|terlalu\s*(?:tinggi|besar)|sulit))',
                r'(?:(?:proses|pengajuan|persetujuan)\s*(?:lama|sulit|ribet|kompleks))',
                r'(?:(?:dokumen|syarat)\s*(?:banyak|rumit|sulit))',
                r'(?:(?:bunga|suku\s*bunga)\s*(?:tinggi|besar|mahal))',
                r'(?:(?:lokasi|posisi)\s*(?:jauh|tidak\s*strategis|kurang\s*bagus))',
                r'(?:(?:harga|biaya)\s*(?:terlalu|terlalu\s*(?:tinggi|besar)|mahal))'
            ]
        }
        
        # Intent Classification Categories
        self.intent_categories = {
            'Informational': [
                'tanya', 'info', 'informasi', 'detail', 'spek', 'fasilitas', 'lokasi', 
                'deskripsi', 'keterangan', 'gambar', 'photo', 'video', 'alamat'
            ],
            'Comparison': [
                'bandingkan', 'perbandingan', 'pilih', 'mana', 'lebih', 'bagus', 
                'cocok', 'sesuai', 'rekomendasi', 'saran', 'alternatif', 'opsi'
            ],
            'Pain-Point': [
                'khawatir', 'sulit', 'bingung', 'masalah', 'kendala', 'kesulitan',
                'belum', 'tidak', 'belum punya', 'proses lama', 'syarat rumit',
                'cicilan tinggi', 'bunga tinggi', 'dp besar', 'harga mahal'
            ],
            'Transactional': [
                'beli', 'beli rumah', 'cari rumah', 'butuh rumah', 'dicari',
                'survey', 'cek lokasi', 'nego', 'deal', 'ambil', 'booking',
                'kpr', 'pengajuan', 'ajukan', 'proses', 'siap', 'serius'
            ]
        }
        
        # Fallback keywords for traditional scoring
        self.high_intent_keywords = [
            'kpr', 'cicilan', 'survei', 'harga', 'lokasi', 'cash', 'dp',
            'booking', 'ready stock', 'indent', 'promo', 'diskon', 'harga cash',
            'kpr syariah', 'bank', 'approve', 'akad', 'notaris', 'sertifikat',
            'imb', 'pbb', 'ajb', 'balik nama', 'biaya', 'total', 'nett',
            'investasi', 'roi', 'keuntungan', 'modal', 'bunga', 'tenor'
        ]
        
        # Additional keywords for traditional scoring
        self.warm_keywords = [
            'minat', 'tanya', 'kapan', 'bagaimana', 'prosedur', 'syarat',
            'fasilitas', 'spek', 'spesifikasi', 'luas', 'dimensi', 'denah',
            'tipe', 'cluster', 'blok', 'unit', 'no', 'available', 'sold',
            'ready', 'progress', 'rencana', 'jadwal', 'target', 'waktu'
        ]
        
        self.cold_keywords = [
            'berita', 'artikel', 'info', 'pengumuman', 'press release',
            'review', 'testimoni', 'galeri', 'foto', 'video', 'virtual tour',
            'lokasi strategis', 'dekat', 'akses', 'tol', 'terminal', 'stasiun',
            'sekolah', 'rumah sakit', 'mall', 'pasar', 'supermarket'
        ]
        
        self.negative_keywords = [
            'scam', 'penipuan', 'hoax', 'spam', 'iklan', 'promosi',
            'lowongan', 'karir', 'recruitment', 'job', 'kerja'
        ]
        
        # Ensure logs directory exists
        os.makedirs('logs', exist_ok=True)
        
        # LLM configuration
        self.llm_model = os.getenv('LLM_MODEL', 'gpt-3.5-turbo')
        self.llm_temperature = float(os.getenv('LLM_TEMPERATURE', '0.1'))
        self.llm_max_tokens = int(os.getenv('LLM_MAX_TOKENS', '50'))
    
    def extract_entities(self, text: str) -> Dict[str, str]:
        """
        Extract entities dari teks menggunakan regex patterns
        Returns: {'price': str, 'location': str, 'bank': str, 'pain_point': str}
        """
        entities = {
            'price': '',
            'location': '',
            'bank': '',
            'pain_point': ''
        }
        
        if not text:
            return entities
        
        text_lower = text.lower()
        
        for entity_type, patterns in self.entity_patterns.items():
            for pattern in patterns:
                try:
                    matches = re.findall(pattern, text_lower, re.IGNORECASE)
                    if matches:
                        # Take the first match, clean it up
                        match = str(matches[0]).strip()
                        if match and len(match) > 1:
                            entities[entity_type] = match
                            break  # Take first valid match
                except Exception as e:
                    self.logger.debug(f"Error in pattern {pattern}: {e}")
                    continue
        
        # Special handling for bank names (direct match)
        if not entities['bank']:
            banks = ['btn', 'bni', 'bri', 'bca', 'mandiri', 'cimb', 'danamon', 'permata', 'panin']
            for bank in banks:
                if bank in text_lower:
                    entities['bank'] = bank.upper()
                    break
        
        # Clean up entities
        for key, value in entities.items():
            if value:
                entities[key] = value[:100]  # Limit length
        
        self.logger.debug(f"Extracted entities: {entities}")
        return entities
    
    def classify_intent(self, text: str) -> str:
        """
        Classify intent ke dalam 4 kategori: Informational, Comparison, Pain-Point, Transactional
        """
        if not text:
            return 'Informational'
        
        text_lower = text.lower()
        intent_scores = {}
        
        # Calculate score for each category
        for category, keywords in self.intent_categories.items():
            score = 0
            for keyword in keywords:
                if keyword in text_lower:
                    # Weight by keyword length (longer keywords get higher weight)
                    weight = len(keyword.split())
                    score += weight
            intent_scores[category] = score
        
        # Find category with highest score
        max_score = max(intent_scores.values())
        if max_score == 0:
            return 'Informational'  # Default
        
        # Get all categories with max score (to handle ties)
        top_categories = [cat for cat, score in intent_scores.items() if score == max_score]
        
        # Priority order for ties: Transactional > Pain-Point > Comparison > Informational
        priority_order = ['Transactional', 'Pain-Point', 'Comparison', 'Informational']
        
        for category in priority_order:
            if category in top_categories:
                self.logger.debug(f"Intent classified as: {category} (scores: {intent_scores})")
                return category
        
        return 'Informational'  # Fallback
    
    def analyze_lead_with_entities(self, lead_data: Dict) -> Dict:
        """
        Advanced analysis dengan entity extraction dan intent classification
        """
        try:
            # Combine text from title, snippet, and content
            text = f"{lead_data.get('title', '')} {lead_data.get('snippet', '')} {lead_data.get('content', '')}"
            
            # Extract entities
            entities = self.extract_entities(text)
            
            # Classify intent
            intent = self.classify_intent(text)
            
            # Get traditional score
            score_result = self.analyze_lead_intent_traditional(lead_data)
            
            # Extract score from result
            if isinstance(score_result, dict):
                score = score_result.get('score', 1)
            else:
                score = score_result
            
            # Enhanced result with entities and intent
            result = {
                'score': score,
                'elite_score': score,  # For compatibility
                'entities': entities,
                'intent_category': intent,
                'confidence': score / 10.0,  # Convert to 0-1 scale
                'analysis_method': 'advanced_intelligence_layer',
                'timestamp': datetime.now().isoformat()
            }
            
            self.logger.info(f"Advanced analysis: Score={score}, Intent={intent}, Entities={entities}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error in advanced analysis: {e}")
            # Fallback to basic scoring
            score_result = self.analyze_lead_intent_traditional(lead_data)
            
            # Extract score from result
            if isinstance(score_result, dict):
                score = score_result.get('score', 1)
            else:
                score = score_result
                
            return {
                'score': score,
                'elite_score': score,
                'entities': {'price': '', 'location': '', 'bank': '', 'pain_point': ''},
                'intent_category': 'Informational',
                'confidence': score / 10.0,
                'analysis_method': 'fallback_traditional',
                'timestamp': datetime.now().isoformat()
            }
        
        # Additional keywords for traditional scoring
        self.warm_keywords = [
            'minat', 'tanya', 'kapan', 'bagaimana', 'prosedur', 'syarat',
            'fasilitas', 'spek', 'spesifikasi', 'luas', 'dimensi', 'denah',
            'tipe', 'cluster', 'blok', 'unit', 'no', 'available', 'sold',
            'ready', 'progress', 'rencana', 'jadwal', 'target', 'waktu'
        ]
        
        self.cold_keywords = [
            'berita', 'artikel', 'info', 'pengumuman', 'press release',
            'review', 'testimoni', 'galeri', 'foto', 'video', 'virtual tour',
            'lokasi strategis', 'dekat', 'akses', 'tol', 'terminal', 'stasiun',
            'sekolah', 'rumah sakit', 'mall', 'pasar', 'supermarket'
        ]
        
        self.negative_keywords = [
            'scam', 'penipuan', 'hoax', 'spam', 'iklan', 'promosi',
            'lowongan', 'karir', 'recruitment', 'job', 'kerja'
        ]
        
        # Ensure logs directory exists
        os.makedirs('logs', exist_ok=True)
        
        # LLM configuration
        self.llm_model = os.getenv('LLM_MODEL', 'gpt-3.5-turbo')
        self.llm_temperature = float(os.getenv('LLM_TEMPERATURE', '0.1'))
        self.llm_max_tokens = int(os.getenv('LLM_MAX_TOKENS', '50'))
    
    def analyze_property_market_context(self, title: str, content: str = "") -> Dict:
        """
        Analisis lead dengan konteks market properti yang ada
        """
        try:
            # Extract entities dari lead
            entities = self.extract_entities(f"{title} {content}")
            
            # Get market intelligence
            market_context = {}
            if self.property_scout:
                # Search for properties based on extracted entities
                search_query = entities.get('location', [''])[0] if entities.get('location') else ''
                
                if search_query:
                    # Search properties in database
                    matching_properties = self.property_scout.search_properties(search_query)
                    
                    if matching_properties:
                        # Calculate market metrics
                        total_available = sum(p['available_units'] for p in matching_properties)
                        total_sold = sum(p['sold_units'] for p in matching_properties)
                        avg_price = sum(p['price_idr'] for p in matching_properties) / len(matching_properties)
                        
                        market_context = {
                            "matching_properties": len(matching_properties),
                            "total_available_units": total_available,
                            "total_sold_units": total_sold,
                            "average_price_idr": avg_price,
                            "market_activity": "high" if total_sold > 50 else "medium" if total_sold > 20 else "low",
                            "price_competitiveness": "competitive" if avg_price < 500000000 else "premium" if avg_price < 1000000000 else "luxury"
                        }
            
            return market_context
            
        except Exception as e:
            self.logger.error(f"Error analyzing property market context: {e}")
            return {}
    
    def enhance_lead_with_property_intelligence(self, lead_data: Dict) -> Dict:
        """
        Enhance lead data dengan property intelligence
        """
        try:
            enhanced_lead = lead_data.copy()
            
            # Add market context
            market_context = self.analyze_property_market_context(
                lead_data.get('title', ''),
                lead_data.get('content_snippet', '')
            )
            
            enhanced_lead['property_intelligence'] = market_context
            
            # Adjust score based on market context
            base_score = enhanced_lead.get('score', 1)
            
            if market_context:
                # Boost score if market is active
                if market_context.get('market_activity') == 'high':
                    base_score = min(10, base_score + 1)
                
                # Adjust based on price competitiveness
                price_competitive = market_context.get('price_competitiveness', '')
                if price_competitive == 'competitive':
                    base_score = min(10, base_score + 1)
                elif price_competitive == 'luxury':
                    base_score = max(1, base_score - 1)
            
            enhanced_lead['enhanced_score'] = base_score
            enhanced_lead['market_analysis_timestamp'] = datetime.now().isoformat()
            
            return enhanced_lead
            
        except Exception as e:
            self.logger.error(f"Error enhancing lead with property intelligence: {e}")
            return lead_data
    
    def analyze_agency_market_context(self, title: str, content: str = "") -> Dict:
        """
        Analisis lead dengan konteks agency marketing yang ada
        """
        try:
            # Extract entities dari lead
            entities = self.extract_entities(f"{title} {content}")
            
            # Get agency intelligence
            agency_context = {}
            if self.agency_scout:
                # Search for agencies based on extracted entities
                search_query = entities.get('location', [''])[0] if entities.get('location') else ''
                
                if search_query:
                    # Search agencies in database
                    matching_agencies = self.agency_scout.search_agencies(search_query)
                    
                    if matching_agencies:
                        # Calculate agency metrics
                        total_agencies = len(matching_agencies)
                        premium_agencies = len([a for a in matching_agencies if a.get('reputation', '').lower() in ['excellent', 'very good']])
                        digital_agencies = len([a for a in matching_agencies if 'digital' in a.get('type', '').lower()])
                        
                        agency_context = {
                            "matching_agencies": total_agencies,
                            "premium_agencies": premium_agencies,
                            "digital_agencies": digital_agencies,
                            "agency_types": list(set([a.get('type', '') for a in matching_agencies])),
                            "market_competition": "high" if total_agencies > 5 else "medium" if total_agencies > 2 else "low",
                            "digital_presence": "strong" if digital_agencies > 2 else "moderate" if digital_agencies > 0 else "weak"
                        }
            
            return agency_context
            
        except Exception as e:
            self.logger.error(f"Error analyzing agency market context: {e}")
            return {}
    
    def enhance_lead_with_agency_intelligence(self, lead_data: Dict) -> Dict:
        """
        Enhance lead data dengan agency intelligence
        """
        try:
            enhanced_lead = lead_data.copy()
            
            # Add agency context
            agency_context = self.analyze_agency_market_context(
                lead_data.get('title', ''),
                lead_data.get('content_snippet', '')
            )
            
            enhanced_lead['agency_intelligence'] = agency_context
            
            # Adjust score based on agency context
            base_score = enhanced_lead.get('score', 1)
            
            if agency_context:
                # Boost score if market is competitive
                if agency_context.get('market_competition') == 'high':
                    base_score = min(10, base_score + 1)
                
                # Adjust based on digital presence
                if agency_context.get('digital_presence') == 'strong':
                    base_score = min(10, base_score + 1)
                elif agency_context.get('digital_presence') == 'weak':
                    base_score = max(1, base_score - 1)
                
                # Premium agencies boost
                if agency_context.get('premium_agencies', 0) > 2:
                    base_score = min(10, base_score + 1)
            
            enhanced_lead['enhanced_score'] = base_score
            enhanced_lead['agency_analysis_timestamp'] = datetime.now().isoformat()
            
            return enhanced_lead
            
        except Exception as e:
            self.logger.error(f"Error enhancing lead with agency intelligence: {e}")
            return lead_data
    
    def analyze_lead_intent_llm(self, title: str, content: str = "") -> Dict:
        """
        Menganalisis intent lead menggunakan OpenAI LLM untuk scoring yang lebih akurat
        """
        if not self.use_llm:
            # Fallback to traditional method
            return self.analyze_lead_intent_traditional(title, content)
        
        try:
            # Prepare text for LLM analysis
            text_to_analyze = f"{title} {content}".strip()
            
            # Create prompt for LLM
            prompt = f"Analisis teks ini: {text_to_analyze}. Berikan skor 1-10 berdasarkan minat beli properti. Respon hanya angka saja."
            
            self.logger.info(f"Sending to LLM for analysis: {title[:50]}...")
            
            # Call OpenAI API
            response = self.openai_client.chat.completions.create(
                model=self.llm_model,
                messages=[
                    {"role": "system", "content": "You are a professional real estate lead analyst. Analyze the given text and provide a score from 1-10 based on purchase intent for property. Respond with only the number."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.llm_temperature,
                max_tokens=self.llm_max_tokens
            )
            
            # Extract score from response
            score_text = response.choices[0].message.content.strip()
            
            # Parse score (expecting just a number)
            try:
                score = int(score_text)
                score = max(1, min(10, score))  # Ensure score is within 1-10 range
                
                # Determine category based on score
                if score >= 8:
                    category = 'high_intent'
                elif score >= 4:
                    category = 'warm'
                else:
                    category = 'cold'
                
                # High confidence for LLM analysis
                confidence = 0.9
                
                self.logger.info(f"LLM analysis result: Score {score}, Category: {category}")
                
                # Send Telegram alert for high-intent leads (score >= 8)
                if score >= 8 and TELEGRAM_ALERTS_AVAILABLE:
                    lead_data = {
                        'title': title,
                        'source': 'LLM Analysis',
                        'score': score,
                        'elite_score': score,
                        'lead_type': 'high_intent',
                        'location': 'Unknown',
                        'url': '',
                        'timestamp': datetime.now().isoformat(),
                        'analysis_method': 'llm',
                        'confidence_level': confidence
                    }
                    
                    try:
                        alert_sent = send_high_intent_alert(lead_data)
                        if alert_sent:
                            self.logger.info(f"Telegram alert sent for high-intent lead (score: {score})")
                        else:
                            self.logger.warning(f"Failed to send Telegram alert for high-intent lead (score: {score})")
                    except Exception as e:
                        self.logger.error(f"Error sending Telegram alert: {e}")
                
                return {
                    'base_score': score,
                    'intent_category': category,
                    'confidence_level': confidence,
                    'analysis_method': 'llm',
                    'llm_response': score_text,
                    'analysis_timestamp': datetime.now().isoformat(),
                    'matched_keywords': [],
                    'telegram_alert_sent': score >= 8 and TELEGRAM_ALERTS_AVAILABLE
                }
                
            except (ValueError, IndexError) as e:
                self.logger.error(f"Error parsing LLM response: {e}")
                # Fallback to traditional method
                return self.analyze_lead_intent_traditional(title, content)
                
        except Exception as e:
            self.logger.error(f"Error in LLM analysis: {e}")
            # Fallback to traditional method
            return self.analyze_lead_intent_traditional(title, content)
    
    def analyze_lead_intent_traditional(self, title: str, content: str = "") -> Dict:
        """
        Fallback traditional scoring method when LLM is not available
        """
        try:
            # Combine title and content for analysis
            full_text = f"{title} {content}".lower()
            
            # Initialize scoring components
            score_analysis = {
                'base_score': 0,
                'high_intent_count': 0,
                'warm_count': 0,
                'cold_count': 0,
                'negative_count': 0,
                'intent_category': 'unknown',
                'confidence_level': 0.0,
                'matched_keywords': [],
                'analysis_timestamp': datetime.now().isoformat(),
                'analysis_method': 'traditional'
            }
            
            # Count keyword matches
            for keyword in self.high_intent_keywords:
                if keyword in full_text:
                    score_analysis['high_intent_count'] += 1
                    score_analysis['matched_keywords'].append(f"HIGH:{keyword}")
            
            for keyword in self.warm_keywords:
                if keyword in full_text:
                    score_analysis['warm_count'] += 1
                    score_analysis['matched_keywords'].append(f"WARM:{keyword}")
            
            for keyword in self.cold_keywords:
                if keyword in full_text:
                    score_analysis['cold_count'] += 1
                    score_analysis['matched_keywords'].append(f"COLD:{keyword}")
            
            for keyword in self.negative_keywords:
                if keyword in full_text:
                    score_analysis['negative_count'] += 1
                    score_analysis['matched_keywords'].append(f"NEG:{keyword}")
            
            # Calculate base score
            base_score = (score_analysis['high_intent_count'] * 3) + \
                        (score_analysis['warm_count'] * 2) + \
                        (score_analysis['cold_count'] * 1) - \
                        (score_analysis['negative_count'] * 5)
            
            # Normalize to 1-10 scale
            if score_analysis['high_intent_count'] > 0:
                score_analysis['base_score'] = min(10, max(8, base_score))
                score_analysis['intent_category'] = 'high_intent'
            elif score_analysis['warm_count'] > 0:
                score_analysis['base_score'] = min(7, max(4, base_score))
                score_analysis['intent_category'] = 'warm'
            elif score_analysis['cold_count'] > 0:
                score_analysis['base_score'] = min(3, max(1, base_score))
                score_analysis['intent_category'] = 'cold'
            else:
                score_analysis['base_score'] = 1
                score_analysis['intent_category'] = 'unknown'
            
            # Apply negative penalty
            if score_analysis['negative_count'] > 0:
                score_analysis['base_score'] = max(1, score_analysis['base_score'] - 3)
                score_analysis['intent_category'] = 'low_quality'
            
            # Calculate confidence level
            total_keywords = score_analysis['high_intent_count'] + \
                           score_analysis['warm_count'] + \
                           score_analysis['cold_count'] + \
                           score_analysis['negative_count']
            
            if total_keywords > 0:
                score_analysis['confidence_level'] = min(1.0, total_keywords / 5.0)
            else:
                score_analysis['confidence_level'] = 0.1
            
            # Add quality indicators
            score_analysis['quality_indicators'] = self._assess_quality_indicators(title, content)
            
            # Send Telegram alert for high-intent leads (score >= 8)
            if score_analysis['base_score'] >= 8 and TELEGRAM_ALERTS_AVAILABLE:
                lead_data = {
                    'title': title,
                    'source': 'Traditional Analysis',
                    'score': score_analysis['base_score'],
                    'elite_score': score_analysis['base_score'],
                    'lead_type': score_analysis['intent_category'],
                    'location': 'Unknown',
                    'url': '',
                    'timestamp': datetime.now().isoformat(),
                    'analysis_method': 'traditional',
                    'confidence_level': score_analysis['confidence_level']
                }
                
                try:
                    alert_sent = send_high_intent_alert(lead_data)
                    if alert_sent:
                        self.logger.info(f"Telegram alert sent for high-intent lead (score: {score_analysis['base_score']})")
                    else:
                        self.logger.warning(f"Failed to send Telegram alert for high-intent lead (score: {score_analysis['base_score']})")
                except Exception as e:
                    self.logger.error(f"Error sending Telegram alert: {e}")
            
            score_analysis['telegram_alert_sent'] = score_analysis['base_score'] >= 8 and TELEGRAM_ALERTS_AVAILABLE
            
            return score_analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing lead intent: {e}")
            return {
                'base_score': 1,
                'intent_category': 'error',
                'confidence_level': 0.0,
                'error': str(e)
            }
    
    def analyze_lead_intent(self, title: str, content: str = "") -> Dict:
        """
        Main method to analyze lead intent - tries LLM first, falls back to traditional
        """
        if self.use_llm:
            return self.analyze_lead_intent_llm(title, content)
        else:
            return self.analyze_lead_intent_traditional(title, content)
    
    def _assess_quality_indicators(self, title: str, content: str) -> Dict:
        """
        Menilai indikator kualitas tambahan
        """
        indicators = {
            'has_contact_info': False,
            'has_price_info': False,
            'has_location_info': False,
            'has_urgency_words': False,
            'content_length': len(content),
            'title_length': len(title)
        }
        
        text = f"{title} {content}".lower()
        
        # Contact info indicators
        contact_patterns = [
            r'\b\d{10,13}\b',  # Phone numbers
            r'\b\d{4}\s\d{4}\s\d{4}\b',  # Phone format
            r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',  # Email
            r'\bwa\b|\bwhatsapp\b|\btelegram\b'  # Messaging apps
        ]
        
        for pattern in contact_patterns:
            if re.search(pattern, text):
                indicators['has_contact_info'] = True
                break
        
        # Price info indicators
        price_patterns = [
            r'\d+\s*(juta|miliar|jt|mil)',
            r'rp\s*\d+',
            r'idr\s*\d+',
            r'harga\s*\d+'
        ]
        
        for pattern in price_patterns:
            if re.search(pattern, text):
                indicators['has_price_info'] = True
                break
        
        # Location info indicators
        location_keywords = ['cipocok', 'serang', 'banten', 'jakarta', 'tangerang']
        if any(loc in text for loc in location_keywords):
            indicators['has_location_info'] = True
        
        # Urgency indicators
        urgency_keywords = ['segera', 'buruan', 'promo', 'diskon', 'limited', 'cepat']
        if any(urg in text for urg in urgency_keywords):
            indicators['has_urgency_words'] = True
        
        return indicators
    
    def score_lead_batch(self, leads: List[Dict]) -> List[Dict]:
        """
        Melakukan scoring untuk batch leads dengan Telegram alerts untuk high-intent leads
        """
        scored_leads = []
        alerts_sent = 0
        
        for lead in leads:
            try:
                # Analyze intent
                scoring_result = self.analyze_lead_intent(
                    lead.get('title', ''),
                    lead.get('snippet', '')
                )
                
                # Add scoring to lead
                enhanced_lead = lead.copy()
                enhanced_lead['scoring'] = scoring_result
                enhanced_lead['elite_score'] = scoring_result['base_score']
                enhanced_lead['intent_category'] = scoring_result['intent_category']
                enhanced_lead['confidence_level'] = scoring_result['confidence_level']
                enhanced_lead['scoring_timestamp'] = datetime.now().isoformat()
                
                # Track if Telegram alert was sent
                if scoring_result.get('telegram_alert_sent', False):
                    alerts_sent += 1
                
                scored_leads.append(enhanced_lead)
                
                self.logger.info(f"Scored lead: {lead.get('title', 'Unknown')} - Score: {scoring_result['base_score']}/10 ({scoring_result['intent_category']})")
                
            except Exception as e:
                self.logger.error(f"Error scoring lead {lead.get('title', 'Unknown')}: {e}")
                # Add lead with error scoring
                lead['scoring'] = {'base_score': 1, 'intent_category': 'error', 'error': str(e)}
                lead['elite_score'] = 1
                scored_leads.append(lead)
        
        # Log batch summary
        if TELEGRAM_ALERTS_AVAILABLE:
            self.logger.info(f"Batch scoring completed: {len(scored_leads)} leads scored, {alerts_sent} Telegram alerts sent for high-intent leads")
        else:
            self.logger.info(f"Batch scoring completed: {len(scored_leads)} leads scored (Telegram alerts not available)")
        
        return scored_leads
    
    def filter_high_value_leads(self, scored_leads: List[Dict], min_score: int = 8) -> List[Dict]:
        """
        Filter leads dengan skor tinggi
        """
        high_value_leads = [
            lead for lead in scored_leads 
            if lead.get('elite_score', 0) >= min_score
        ]
        
        self.logger.info(f"Filtered {len(high_value_leads)} high-value leads (score >= {min_score}) from {len(scored_leads)} total leads")
        
        return high_value_leads
    
    def generate_scoring_report(self, scored_leads: List[Dict]) -> Dict:
        """
        Generate comprehensive scoring report
        """
        try:
            total_leads = len(scored_leads)
            
            if total_leads == 0:
                return {'error': 'No leads to analyze'}
            
            # Category distribution
            categories = {}
            score_distribution = {i: 0 for i in range(1, 11)}
            
            for lead in scored_leads:
                category = lead.get('intent_category', 'unknown')
                categories[category] = categories.get(category, 0) + 1
                
                score = lead.get('elite_score', 1)
                score_distribution[score] = score_distribution.get(score, 0) + 1
            
            # High-value leads analysis
            high_value = self.filter_high_value_leads(scored_leads, 8)
            medium_value = [l for l in scored_leads if 4 <= l.get('elite_score', 0) <= 7]
            low_value = [l for l in scored_leads if l.get('elite_score', 0) <= 3]
            
            report = {
                'generated_at': datetime.now().isoformat(),
                'total_leads_analyzed': total_leads,
                'category_distribution': categories,
                'score_distribution': score_distribution,
                'value_breakdown': {
                    'high_value_leads': len(high_value),
                    'medium_value_leads': len(medium_value),
                    'low_value_leads': len(low_value)
                },
                'quality_metrics': {
                    'avg_score': sum(l.get('elite_score', 0) for l in scored_leads) / total_leads,
                    'high_value_percentage': (len(high_value) / total_leads) * 100,
                    'leads_with_contact_info': len([l for l in scored_leads if l.get('scoring', {}).get('quality_indicators', {}).get('has_contact_info', False)]),
                    'leads_with_price_info': len([l for l in scored_leads if l.get('scoring', {}).get('quality_indicators', {}).get('has_price_info', False)])
                },
                'recommendations': self._generate_recommendations(high_value, medium_value, low_value)
            }
            
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating scoring report: {e}")
            return {'error': str(e)}
    
    def _generate_recommendations(self, high_value: List[Dict], medium_value: List[Dict], low_value: List[Dict]) -> List[str]:
        """
        Generate actionable recommendations based on scoring results
        """
        recommendations = []
        
        if len(high_value) > 0:
            recommendations.append(f"IMMEDIATE ACTION: Contact {len(high_value)} high-value leads (score 8-10) within 24 hours")
            recommendations.append("Priority: Focus on leads with financial keywords (KPR, cicilan, harga)")
        
        if len(medium_value) > 5:
            recommendations.append(f"WARM LEADS: Nurture {len(medium_value)} medium-value leads with follow-up sequence")
        
        if len(low_value) > len(high_value + medium_value):
            recommendations.append(f"QUALITY ISSUE: {len(low_value)} low-value leads detected - consider refining search keywords")
        
        # Analyze common patterns
        all_leads = high_value + medium_value + low_value
        contact_info_leads = [l for l in all_leads if l.get('scoring', {}).get('quality_indicators', {}).get('has_contact_info', False)]
        
        if len(contact_info_leads) < len(all_leads) * 0.3:
            recommendations.append("DATA QUALITY: Only 30% leads have contact info - improve search targeting")
        
        return recommendations
    
    def score_lead_batch_advanced(self, leads: List[Dict]) -> Dict:
        """
        Advanced batch scoring dengan entity extraction dan intent classification
        """
        try:
            results = []
            alerts_sent = 0
            
            for lead in leads:
                # Advanced analysis dengan entities dan intent
                analysis = self.analyze_lead_with_entities(lead)
                
                # Add analysis to lead data
                lead.update(analysis)
                
                # Add entity data to lead for database storage
                lead['entities'] = analysis.get('entities', {})
                lead['intent_category'] = analysis.get('intent_category', 'Informational')
                
                # Send Telegram alert for high-intent leads
                if analysis.get('score', 0) >= 8 and TELEGRAM_ALERTS_AVAILABLE:
                    try:
                        alert_sent = send_high_intent_alert(lead)
                        if alert_sent:
                            alerts_sent += 1
                    except Exception as e:
                        self.logger.error(f"Error sending Telegram alert: {e}")
                
                results.append(lead)
            
            # Generate summary statistics
            intent_distribution = {}
            entity_stats = {}
            
            for lead in results:
                intent = lead.get('intent_category', 'Informational')
                intent_distribution[intent] = intent_distribution.get(intent, 0) + 1
                
                entities = lead.get('entities', {})
                for entity_type, value in entities.items():
                    if value:
                        entity_stats[entity_type] = entity_stats.get(entity_type, 0) + 1
            
            return {
                'status': 'success',
                'leads_analyzed': len(leads),
                'high_intent_leads': len([l for l in results if l.get('score', 0) >= 8]),
                'alerts_sent': alerts_sent,
                'results': results,
                'advanced_intelligence': {
                    'intent_distribution': intent_distribution,
                    'entity_extraction_stats': entity_stats,
                    'analysis_method': 'advanced_intelligence_layer'
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error in advanced batch scoring: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'leads_analyzed': 0
            }

    def identify_values(self, content_snippet: str) -> Dict:
        """
        Psychographic Labeler - Identify customer values and motivations
        
        Args:
            content_snippet: Text content to analyze for psychographic indicators
            
        Returns:
            Dict with value classification and psychographic profile
        """
        try:
            self.logger.info(f"Analyzing psychographic values: {content_snippet[:100]}...")
            
            # Value-based keyword patterns
            value_patterns = {
                'Security-Oriented': [
                    'aman', 'amanah', 'keamanan', 'tenang', 'nyaman', 'damai', 'stabil',
                    'investasi', 'tabungan', 'masa depan', 'jaminan', 'pasti', 'terjamin',
                    'bebas banjir', 'lingkungan aman', 'keamanan 24 jam', 'one gate system'
                ],
                'Prestige-Oriented': [
                    'mewah', 'prestige', 'kelas', 'premium', 'eksklusif', 'elite',
                    'bergengsi', 'status', 'kualitas', 'mahal', 'branded', 'design',
                    'arsitektur', 'modern', 'futuristik', 'iconic', 'landmark'
                ],
                'Value-for-Money-Oriented': [
                    'murah', 'terjangkau', 'hemat', 'ekonomis', 'praktis', 'efisien',
                    'cicilan', 'dp', 'uang muka', 'promo', 'diskon', 'cashback',
                    'harga', 'budget', 'dapat', 'worth it', 'investasi balik modal'
                ],
                'Family-Oriented': [
                    'keluarga', 'anak', 'istri', 'suami', 'orang tua', 'nenek',
                    'sekolah', 'pendidikan', 'taman bermain', 'dekat sekolah',
                    'lingkungan keluarga', 'ramah anak', 'ruang keluarga'
                ],
                'Career-Oriented': [
                    'karir', 'pekerjaan', 'kantor', 'bisnis', 'usaha', 'wirausaha',
                    'akses mudah', 'strategis', 'dekat tol', 'dekat kota', 'mobilitas',
                    'koneksi', 'network', 'opportunity', 'pengembangan'
                ],
                'Lifestyle-Oriented': [
                    'lifestyle', 'gaya hidup', 'trend', 'fashion', 'liburan',
                    'rekreasi', 'hobi', 'entertainment', 'kuliner', 'shopping',
                    'hangout', 'sosialita', 'instagramable', 'spot foto'
                ]
            }
            
            # Count value indicators
            value_scores = {}
            content_lower = content_snippet.lower()
            
            for value_type, keywords in value_patterns.items():
                score = 0
                matched_keywords = []
                
                for keyword in keywords:
                    if keyword in content_lower:
                        score += 1
                        matched_keywords.append(keyword)
                
                if score > 0:
                    value_scores[value_type] = {
                        'score': score,
                        'keywords': matched_keywords,
                        'percentage': (score / len(keywords)) * 100
                    }
            
            # Determine primary value
            primary_value = None
            max_score = 0
            
            for value_type, data in value_scores.items():
                if data['score'] > max_score:
                    max_score = data['score']
                    primary_value = value_type
            
            # Secondary values (tie-breakers)
            secondary_values = []
            for value_type, data in value_scores.items():
                if value_type != primary_value and data['score'] >= max_score * 0.6:
                    secondary_values.append(value_type)
            
            # Create psychographic profile
            psychographic_profile = {
                'primary_value': primary_value,
                'secondary_values': secondary_values,
                'value_scores': value_scores,
                'content_analysis': {
                    'total_value_indicators': sum(data['score'] for data in value_scores.values()),
                    'dominant_value_percentage': max_score / len(value_patterns.get(primary_value, [])) * 100 if primary_value else 0,
                    'value_diversity': len(value_scores)
                },
                'marketing_insights': self._generate_value_insights(primary_value, secondary_values, value_scores),
                'analysis_timestamp': datetime.now().isoformat()
            }
            
            # LLM enhancement if available
            if OPENAI_AVAILABLE and primary_value:
                psychographic_profile['llm_enhancement'] = self._enhance_psychographic_with_llm(
                    content_snippet, primary_value, secondary_values
                )
            
            self.logger.info(f"Psychographic analysis complete: Primary value = {primary_value}")
            return psychographic_profile
            
        except Exception as e:
            self.logger.error(f"Error in psychographic value identification: {e}")
            return {
                'primary_value': 'Unknown',
                'secondary_values': [],
                'value_scores': {},
                'error': str(e),
                'analysis_timestamp': datetime.now().isoformat()
            }
    
    def _generate_value_insights(self, primary_value: str, secondary_values: List[str], value_scores: Dict) -> Dict:
        """
        Generate marketing insights based on psychographic values
        """
        insights = {
            'selling_points': [],
            'communication_style': '',
            'pain_points': [],
            'decision_factors': [],
            'recommended_approach': ''
        }
        
        # Value-based insights
        value_insights_map = {
            'Security-Oriented': {
                'selling_points': [
                    'One gate system dengan security 24 jam',
                    'Lokasi bebas banjir dan lingkungan aman',
                    'Investasi properti yang stabil dan menguntungkan',
                    'Legalitas lengkap dan terjamin'
                ],
                'communication_style': 'Formal, detail-oriented, focus on long-term benefits',
                'pain_points': ['Ketidakpastian investasi', 'Keamanan lingkungan', 'Legalitas tidak jelas'],
                'decision_factors': ['Keamanan', 'Stabilitas investasi', 'Jaminan hukum'],
                'recommended_approach': 'Emphasize security features, investment stability, and legal protection'
            },
            'Prestige-Oriented': {
                'selling_points': [
                    'Desain arsitektur premium dan eksklusif',
                    'Lokasi strategis di kawasan bergengsi',
                    'Fasilitas kelas atas dan modern',
                    'Status sosial dan image enhancement'
                ],
                'communication_style': 'Sophisticated, exclusive, focus on status and uniqueness',
                'pain_points': ['Kurang eksklusif', 'Tidak sesuai status', 'Kualitas standar'],
                'decision_factors': ['Status', 'Kualitas', 'Keunikan', 'Desain'],
                'recommended_approach': 'Highlight exclusivity, premium features, and social status benefits'
            },
            'Value-for-Money-Oriented': {
                'selling_points': [
                    'Harga terbaik di kelasnya',
                    'Promo dan diskon menarik',
                    'Cicilan KPR yang terjangkau',
                    'Nilai investasi yang tinggi'
                ],
                'communication_style': 'Practical, numbers-focused, emphasize savings and value',
                'pain_points': ['Harga terlalu mahal', 'Tidak worth it', 'Biaya tersembunyi'],
                'decision_factors': ['Harga', 'Promo', 'Cicilan', 'ROI'],
                'recommended_approach': 'Focus on financial benefits, promotions, and cost-effectiveness'
            },
            'Family-Oriented': {
                'selling_points': [
                    'Dekat dengan sekolah berkualitas',
                    'Lingkungan ramah anak dan aman',
                    'Ruang keluarga yang luas',
                    'Fasilitas untuk tumbuh kembang anak'
                ],
                'communication_style': 'Warm, family-focused, emphasize children benefits',
                'pain_points': ['Lingkungan tidak ramah anak', 'Jauh dari sekolah', 'Kurang aman'],
                'decision_factors': ['Keamanan anak', 'Pendidikan', 'Lingkungan', 'Ruang'],
                'recommended_approach': 'Emphasize family benefits, education access, and child-friendly features'
            },
            'Career-Oriented': {
                'selling_points': [
                    'Akses mudah ke pusat bisnis',
                    'Dekat dengan infrastruktur transportasi',
                    'Lokasi strategis untuk pengembangan karir',
                    'Koneksi dan networking opportunities'
                ],
                'communication_style': 'Professional, efficiency-focused, emphasize career benefits',
                'pain_points': ['Akses sulit', 'Macet', 'Jauh dari kantor'],
                'decision_factors': ['Aksesibilitas', 'Waktu tempuh', 'Lokasi strategis'],
                'recommended_approach': 'Highlight accessibility, time savings, and career advantages'
            },
            'Lifestyle-Oriented': {
                'selling_points': [
                    'Dekat dengan pusat hiburan dan lifestyle',
                    'Instagramable spots dan modern design',
                    'Akses mudah ke tempat hangout',
                    'Lingkungan yang vibrant dan dynamic'
                ],
                'communication_style': 'Trendy, social-focused, emphasize lifestyle benefits',
                'pain_points': ['Kurang trendy', 'Jauh dari hiburan', 'Tidak instagramable'],
                'decision_factors': ['Lifestyle', 'Social status', 'Trend', 'Entertainment'],
                'recommended_approach': 'Focus on lifestyle benefits, social aspects, and trendy features'
            }
        }
        
        # Get insights for primary value
        if primary_value in value_insights_map:
            insights.update(value_insights_map[primary_value])
        
        # Add secondary value considerations
        if secondary_values:
            insights['secondary_considerations'] = []
            for secondary in secondary_values:
                if secondary in value_insights_map:
                    insights['secondary_considerations'].append({
                        'value': secondary,
                        'additional_focus': value_insights_map[secondary]['selling_points'][:2]
                    })
        
        return insights
    
    def _enhance_psychographic_with_llm(self, content_snippet: str, primary_value: str, secondary_values: List[str]) -> Dict:
        """
        Enhance psychographic analysis with LLM
        """
        try:
            if not OPENAI_AVAILABLE:
                return {'status': 'unavailable', 'reason': 'OpenAI not available'}
            
            client = openai.OpenAI()
            
            prompt = f"""
            Analisis psikografis dari konten berikut:
            
            Konten: "{content_snippet}"
            Nilai Utama: {primary_value}
            Nilai Sekunder: {', '.join(secondary_values)}
            
            Berikan analisis mendalam dalam format JSON:
            {{
                "psychographic_profile": {{
                    "motivation_drivers": ["driver1", "driver2"],
                    "fear_factors": ["fear1", "fear2"],
                    "aspirations": ["aspiration1", "aspiration2"],
                    "decision_triggers": ["trigger1", "trigger2"]
                }},
                "communication_strategy": {{
                    "tone": "formal/casual/professional/friendly",
                    "key_messages": ["message1", "message2"],
                    "avoid_topics": ["topic1", "topic2"]
                }},
                "conversion_probability": "high/medium/low",
                "recommended_next_steps": ["step1", "step2"]
            }}
            """
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a psychographic analysis expert for real estate marketing."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.3
            )
            
            llm_response = response.choices[0].message.content
            
            # Try to parse JSON response
            try:
                enhanced_data = json.loads(llm_response)
                return {
                    'status': 'success',
                    'enhanced_profile': enhanced_data,
                    'llm_confidence': 'high'
                }
            except json.JSONDecodeError:
                return {
                    'status': 'partial',
                    'raw_response': llm_response,
                    'llm_confidence': 'medium'
                }
                
        except Exception as e:
            self.logger.error(f"Error in LLM psychographic enhancement: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'llm_confidence': 'low'
            }

if __name__ == "__main__":
    # Test the scoring engine
    logging.basicConfig(level=logging.INFO)
    
    scorer = LeadScoringEngine()
    
    # Test leads
    test_leads = [
        {
            'title': 'Cari rumah KPR di Serang',
            'snippet': 'Butuh rumah dengan cicilan KPR syariah, harga 500 juta, lokasi strategis'
        },
        {
            'title': 'Tanya properti Cipocok Jaya',
            'snippet': 'Minat tanya kapan ready stock, fasilitas cluster'
        },
        {
            'title': 'Berita properti Banten',
            'snippet': 'Artikel tentang pengembangan kawasan Serang'
        }
    ]
    
    # Score the leads
    scored = scorer.score_lead_batch(test_leads)
    
    # Generate report
    report = scorer.generate_scoring_report(scored)
    
    print("Scoring Results:")
    for lead in scored:
        print(f"Title: {lead['title']}")
        print(f"Score: {lead['elite_score']}/10 - {lead['intent_category']}")
        print(f"Keywords: {lead['scoring']['matched_keywords']}")
        print("-" * 50)
    
    print("\nScoring Report:")
    print(json.dumps(report, indent=2, ensure_ascii=False))
