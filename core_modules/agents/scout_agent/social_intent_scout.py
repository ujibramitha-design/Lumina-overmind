"""
Social Intent Scout - Social Listening Agent
Scans social media, forums, and online platforms for property buying intent

Author: HUNTER_AGENT_AI_MARKETING_DIGITAL
Version: 1.0.0
"""

import os
import sys
import json
import random
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import re

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import core modules
from core_modules.db_manager import DatabaseManager

# Configure logging
logger = logging.getLogger(__name__)

class SocialIntentScout:
    """Social Listening Agent for Property Buying Intent Detection"""
    
    def __init__(self):
        self.name = "Social Intent Scout"
        self.version = "2.0.0"  # Enhanced with Deep Comment Analysis
        self.db_manager = DatabaseManager()
        
        # API Credentials (Blueprint for future integration)
        self.api_credentials = {
            'facebook_access_token': os.getenv('FB_ACCESS_TOKEN', ''),
            'tiktok_api_key': os.getenv('TIKTOK_API_KEY', ''),
            'apify_token': os.getenv('APIFY_TOKEN', ''),
            'instagram_access_token': os.getenv('INSTAGRAM_ACCESS_TOKEN', ''),
            'twitter_bearer_token': os.getenv('TWITTER_BEARER_TOKEN', '')
        }
        
        # Comment analysis patterns
        self.urgency_patterns = [
            r'butuh\s+sekarang', r'urgent', r'buruan', r'segera', r'minggu\s+ini',
            r'bulan\s+ini', r'cepat', r'lagi\s+cari', r'sedang\s+cari',
            r'butuh\s+banget', r'mau\s+segera', r'cari\s+urgent'
        ]
        
        self.budget_patterns = [
            r'budget\s+(\d+(?:\.\d+)?)\s*(?:juta|miliar|jt|m)', 
            r'harga\s+(\d+(?:\.\d+)?)\s*(?:juta|miliar|jt|m)',
            r'cicilan\s+(\d+(?:\.\d+)?)\s*(?:juta|jt)',
            r'dp\s+(\d+(?:\.\d+)?)\s*(?:juta|jt)',
            r'uang\s+muka\s+(\d+(?:\.\d+)?)\s*(?:juta|jt)',
            r'kisaran\s+(\d+(?:\.\d+)?)\s*(?:juta|miliar|jt|m)'
        ]
        
        self.pain_point_patterns = [
            r'susah\s+acc', r'ditolak\s+bank', r'ACC\s+ditolak', r'bank\s+tolak',
            r'dp\s+0', r'tanpa\s+dp', r'0\s+dp', r'dp\s+nol',
            r'bunga\s+tinggi', r'cicilan\s+berat', r'beban\s+cicilan',
            r'proses\s+lama', r'persyaratan\s+rumit', r'dokumen\s+ribet',
            r'lokasi\s+jauh', r'akses\s+sulit', r'fasilitas\s+kurang'
        ]
        
        # Platform configurations
        self.platforms = [
            'Facebook', 'Instagram', 'Twitter', 'LinkedIn', 
            'Reddit', 'Kaskus', 'Forum Properti', 'WhatsApp Group',
            'Telegram Channel', 'TikTok', 'YouTube Comments'
        ]
        
        # Realistic Indonesian usernames
        self.usernames = [
            'budi_setiawan', 'susi_wati88', 'ahmad_property', 'dewi_rumah',
            'eko_investor', 'rina_kpr', 'joko_developer', 'sari_milik',
            'hendrak_property', 'fitri_hunian', 'anton_propertindo', 'maya_rumahku',
            'bambang_invest', 'diana_kpr', 'fajar_property', 'lisa_hunian',
            'chris_developer', 'siti_rumah', 'doni_property', 'nina_investasi'
        ]
        
        # Realistic post templates
        self.post_templates = [
            "Lagi cari rumah di {location}, budget {budget}, ada yang punya info?",
            "Butuh KPR murah {location}, gaji {salary}, bantu ya teman2",
            "Overkredit rumah {location}, cicilan {installment}, minat?",
            "Cari rumah untuk keluarga kecil {location}, {bedroom} KT, {bathroom} KM",
            "Pengen punya rumah {location} tapi DP kurang, ada solusi?",
            "Dijual rumah cepat {location}, butuh uang segera, harga nego",
            "Cari kontrakan {location} budget {budget}, {duration} bulan",
            "Ada yang tau developer {location} yang bagus dan terpercaya?",
            "Mau beli rumah {location} tapi masih bingung proses KPR-nya",
            "Cari rumah second {location}, kondisi bagus, bisa KPR",
            "Butuh info rumah subsidi {location}, syarat apa aja ya?",
            "Selling rumah {location}, {size}m², harga {price}, nego sampai deal",
            "Cari kavling siap bangun {location}, budget {budget}",
            "Ada yang punya referensi bank untuk KPR {location}? Bunga ringan?",
            "Mau jual rumah {location} karena pindah kerja, butuh cepat terjual"
        ]
        
        # Location variations
        self.locations = [
            'Serang', 'Cipocok Jaya', 'Kasemen', 'Walantaka', 'Curug',
            'Taktakan', 'Pontang', 'Kramatwatu', 'Pabuaran', 'Mancak',
            'Cikande', 'Jawilan', 'Kopo', 'Ciruas', 'Bojong',
            'Bandung', 'Jakarta', 'Tangerang', 'Bekasi', 'Depok'
        ]
        
        # Budget ranges
        self.budgets = [
            '100-150 juta', '150-200 juta', '200-300 juta', '300-400 juta',
            '400-500 juta', '500-700 juta', '700-1 M', '1-1.5 M', '1.5-2 M'
        ]
        
        # Salary ranges for KPR context
        self.salaries = [
            '5 juta', '7 juta', '10 juta', '15 juta', '20 juta', '25 juta'
        ]
        
        # Installment ranges
        self.installments = [
            '3 juta/bulan', '4 juta/bulan', '5 juta/bulan', '6 juta/bulan',
            '7 juta/bulan', '8 juta/bulan', '10 juta/bulan'
        ]
        
        # Room specifications
        self.bedrooms = ['1 KT', '2 KT', '3 KT', '4 KT']
        self.bathrooms = ['1 KM', '2 KM', '3 KM']
        
        # Property sizes
        self.sizes = ['30m²', '36m²', '45m²', '60m²', '72m²', '90m²', '120m²']
        
        # Prices
        self.prices = [
            '250 juta', '300 juta', '350 juta', '400 juta', '450 juta',
            '500 juta', '600 juta', '750 juta', '1 M', '1.2 M'
        ]
        
        # Durations
        self.durations = ['6', '12', '24', '36']
        
        logger.info(f"🎯 {self.name} v{self.version} initialized")
        logger.info(f"📱 Monitoring {len(self.platforms)} platforms for property intent")
        logger.info(f"🔍 Deep Comment Analysis enabled with {len(self.urgency_patterns)} urgency patterns")
        logger.info(f"🧠 AI Simulation ready for prospect deep profiling")
    
    def _generate_realistic_post(self, keyword: str) -> Dict[str, Any]:
        """Generate realistic social media post based on keyword"""
        
        # Select random platform
        platform = random.choice(self.platforms)
        username = random.choice(self.usernames)
        
        # Generate post content based on keyword
        if 'butuh rumah' in keyword.lower():
            template = random.choice([
                "Lagi butuh rumah {location}, budget {budget}, ada yang punya info?",
                "Butuh rumah untuk keluarga {location}, {bedroom} KT, {bathroom} KM",
                "Sedang cari rumah {location}, butuh segera, mohon bantuannya"
            ])
        elif 'cari kpr murah' in keyword.lower():
            template = random.choice([
                "Cari KPR murah {location}, gaji {salary}, ada yang bisa bantu?",
                "Butuh KPR murah {location}, DP rendah, ada rekomendasi?",
                "Mau ajukan KPR {location} tapi cari yang bunga rendah, info ya"
            ])
        elif 'overkredit rumah' in keyword.lower():
            template = random.choice([
                "Overkredit rumah {location}, cicilan {installment}, serius minat?",
                "Dari overkredit rumah {location}, cicilan ringan {installment}",
                "Cari overkredit rumah {location}, budget cicilan {installment}"
            ])
        else:
            template = random.choice(self.post_templates)
        
        # Fill template with realistic data
        post_content = template.format(
            location=random.choice(self.locations),
            budget=random.choice(self.budgets),
            salary=random.choice(self.salaries),
            installment=random.choice(self.installments),
            bedroom=random.choice(self.bedrooms),
            bathroom=random.choice(self.bathrooms),
            size=random.choice(self.sizes),
            price=random.choice(self.prices),
            duration=random.choice(self.durations)
        )
        
        # Calculate intent score based on content analysis
        intent_score = self._calculate_intent_score(post_content, keyword)
        
        # Generate timestamp (within last 24 hours)
        hours_ago = random.randint(0, 23)
        timestamp = datetime.now() - timedelta(hours=hours_ago)
        
        return {
            'username': username,
            'platform': platform,
            'post_content': post_content,
            'intent_score': intent_score,
            'keyword_matched': keyword,
            'timestamp': timestamp.isoformat(),
            'post_url': f"https://{platform.lower().replace(' ', '')}.com/post/{random.randint(100000, 999999)}",
            'engagement': {
                'likes': random.randint(0, 50),
                'comments': random.randint(0, 20),
                'shares': random.randint(0, 10)
            },
            'user_profile': {
                'followers': random.randint(100, 5000),
                'verified': random.choice([True, False]),
                'account_type': random.choice(['Personal', 'Business', 'Developer'])
            }
        }
    
    def _calculate_intent_score(self, content: str, keyword: str) -> int:
        """Calculate intent score based on content analysis"""
        
        base_score = 50  # Base score
        
        # High intent keywords
        high_intent_keywords = [
            'butuh', 'cari', 'mau beli', 'minat', 'serius', 'segera',
            'buruan', 'butuh sekali', 'cari rumah', 'mau punya rumah'
        ]
        
        # Medium intent keywords
        medium_intent_keywords = [
            'info', 'bantu', 'referensi', 'rekomendasi', 'tau tidak',
            'ada yang', 'mohon info', 'cari tahu'
        ]
        
        # Low intent keywords
        low_intent_keywords = [
            'tanya', 'info aja', 'lihat-lihat', 'survey', 'belum minat',
            'cari tahu dulu', 'belum siap'
        ]
        
        # Urgency indicators
        urgency_keywords = [
            'segera', 'buruan', 'cepat', 'butuh sekali', 'urgent',
            'minggu ini', 'bulan ini', 'sekarang'
        ]
        
        # Budget indicators (higher score if specific budget mentioned)
        budget_keywords = [
            'budget', 'cicilan', 'dp', 'harga', 'juta', 'miliar'
        ]
        
        # Location specificity (higher score if specific location)
        location_keywords = [
            'serang', 'cipocok', 'kasemen', 'walantaka', 'jakarta',
            'bandung', 'tangerang', 'bekasi', 'depok'
        ]
        
        # Calculate score
        for word in high_intent_keywords:
            if word.lower() in content.lower():
                base_score += 20
        
        for word in medium_intent_keywords:
            if word.lower() in content.lower():
                base_score += 10
        
        for word in low_intent_keywords:
            if word.lower() in content.lower():
                base_score -= 10
        
        for word in urgency_keywords:
            if word.lower() in content.lower():
                base_score += 15
        
        for word in budget_keywords:
            if word.lower() in content.lower():
                base_score += 8
        
        for word in location_keywords:
            if word.lower() in content.lower():
                base_score += 5
        
        # Keyword match bonus
        if keyword.lower() in content.lower():
            base_score += 10
        
        # Ensure score is within 0-100 range
        intent_score = max(0, min(100, base_score))
        
        return intent_score
    
    def analyze_comments(self, post_id: str) -> Dict[str, Any]:
        """
        Analyze comments from a viral post to extract deep prospect insights
        
        Args:
            post_id: ID of the post to analyze comments from
            
        Returns:
            Dict containing comment analysis results and high-intent prospects
        """
        
        logger.info(f"🔍 Starting deep comment analysis for post: {post_id}")
        logger.info(f"📱 Simulating extraction of hundreds of comments...")
        
        # Simulate comment extraction (in real implementation, this would use APIs)
        comment_count = random.randint(50, 200)
        logger.info(f"📊 Found {comment_count} comments to analyze")
        
        # Generate realistic comments
        comments = self._generate_realistic_comments(comment_count, post_id)
        
        # Analyze each comment for intent and extract prospect data
        high_intent_prospects = []
        comment_analysis = {
            'post_id': post_id,
            'total_comments': comment_count,
            'analyzed_comments': len(comments),
            'high_intent_prospects': [],
            'comment_sentiment': {
                'positive': 0,
                'neutral': 0,
                'negative': 0
            },
            'common_themes': {},
            'urgency_indicators': [],
            'budget_mentions': [],
            'pain_points': []
        }
        
        for comment in comments:
            # Calculate intent score for comment
            intent_score = self._calculate_comment_intent_score(comment['text'])
            
            # Extract sentiment
            sentiment = self._analyze_comment_sentiment(comment['text'])
            comment_analysis['comment_sentiment'][sentiment] += 1
            
            # If high intent, perform deep profiling
            if intent_score >= 75:
                try:
                    # Deep profile the prospect
                    deep_profile = self.deep_profile_prospect(comment['user'], comment['text'])
                    
                    prospect = {
                        'comment_id': comment['id'],
                        'post_id': post_id,
                        'username': comment['user']['username'],
                        'platform': comment['platform'],
                        'comment_text': comment['text'],
                        'intent_score': intent_score,
                        'deep_profile': deep_profile,
                        'timestamp': comment['timestamp'],
                        'engagement': comment.get('engagement', {})
                    }
                    
                    high_intent_prospects.append(prospect)
                    comment_analysis['high_intent_prospects'].append(prospect)
                    
                    # Extract insights
                    if deep_profile.get('urgency'):
                        comment_analysis['urgency_indicators'].append({
                            'username': comment['user']['username'],
                            'urgency': deep_profile['urgency']
                        })
                    
                    if deep_profile.get('budget'):
                        comment_analysis['budget_mentions'].append({
                            'username': comment['user']['username'],
                            'budget': deep_profile['budget']
                        })
                    
                    if deep_profile.get('pain_points'):
                        comment_analysis['pain_points'].extend(deep_profile['pain_points'])
                    
                except Exception as e:
                    logger.error(f"Error deep profiling prospect {comment['user']['username']}: {e}")
        
        # Analyze common themes
        comment_analysis['common_themes'] = self._extract_common_themes(comments)
        
        logger.info(f"✅ Comment analysis completed")
        logger.info(f"🎯 Found {len(high_intent_prospects)} high-intent prospects from {comment_count} comments")
        logger.info(f"🔥 Urgency indicators: {len(comment_analysis['urgency_indicators'])}")
        logger.info(f"💰 Budget mentions: {len(comment_analysis['budget_mentions'])}")
        logger.info(f"😣 Pain points identified: {len(comment_analysis['pain_points'])}")
        
        return comment_analysis
    
    def deep_profile_prospect(self, user_data: Dict, comment_text: str) -> Dict[str, Any]:
        """
        Perform deep profiling of prospect using simulated Gemini AI analysis
        
        Args:
            user_data: User information from social media
            comment_text: The comment text to analyze
            
        Returns:
            Dict containing deep profile insights (urgency, budget, pain points)
        """
        
        try:
            # Simulate Gemini AI analysis (in real implementation, this would call Gemini API)
            logger.debug(f"🧠 Performing AI deep profiling for: {user_data.get('username', 'unknown')}")
            
            # Extract urgency from comment
            urgency = self._extract_urgency_from_comment(comment_text)
            
            # Extract budget from comment
            budget = self._extract_budget_from_comment(comment_text)
            
            # Extract pain points from comment
            pain_points = self._extract_pain_points_from_comment(comment_text)
            
            # Simulate AI insights
            ai_insights = self._simulate_ai_analysis(user_data, comment_text, urgency, budget, pain_points)
            
            deep_profile = {
                'urgency': urgency,
                'budget': budget,
                'pain_points': pain_points,
                'ai_insights': ai_insights,
                'confidence_score': random.randint(70, 95),
                'profiling_timestamp': datetime.now().isoformat(),
                'analysis_method': 'Gemini AI Simulation'
            }
            
            logger.debug(f"🎯 Deep profile completed: Urgency={urgency}, Budget={budget}, Pain Points={len(pain_points)}")
            
            return deep_profile
            
        except Exception as e:
            logger.error(f"Error in deep profiling: {e}")
            return {
                'urgency': 'Unknown',
                'budget': 'Unknown',
                'pain_points': [],
                'ai_insights': {'error': str(e)},
                'confidence_score': 0,
                'profiling_timestamp': datetime.now().isoformat(),
                'analysis_method': 'Fallback'
            }
    
    def _extract_urgency_from_comment(self, comment_text: str) -> str:
        """Extract urgency level from comment text"""
        
        comment_lower = comment_text.lower()
        
        # High urgency indicators
        high_urgency = ['butuh sekarang', 'urgent', 'buruan', 'segera', 'minggu ini']
        medium_urgency = ['bulan ini', 'cepat', 'lagi cari', 'sedang cari']
        low_urgency = ['cari-cari', 'lihat dulu', 'masih survey']
        
        for pattern in high_urgency:
            if pattern in comment_lower:
                return 'High (Immediate)'
        
        for pattern in medium_urgency:
            if pattern in comment_lower:
                return 'Medium (This Month)'
        
        for pattern in low_urgency:
            if pattern in comment_lower:
                return 'Low (Research Phase)'
        
        return 'Unknown'
    
    def _extract_budget_from_comment(self, comment_text: str) -> str:
        """Extract budget information from comment text"""
        
        for pattern in self.budget_patterns:
            matches = re.findall(pattern, comment_text, re.IGNORECASE)
            if matches:
                budget_value = matches[0]
                # Determine unit (juta/miliar)
                if 'miliar' in comment_text.lower() or 'm' in comment_text.lower():
                    return f"{budget_value} Miliar"
                else:
                    return f"{budget_value} Juta"
        
        return 'Not Mentioned'
    
    def _extract_pain_points_from_comment(self, comment_text: str) -> List[str]:
        """Extract pain points from comment text"""
        
        pain_points = []
        comment_lower = comment_text.lower()
        
        pain_point_mapping = {
            'susah acc': 'ACC Bank Issues',
            'ditolak bank': 'Bank Rejection',
            'dp 0': 'Down Payment Issues',
            'tanpa dp': 'No Down Payment',
            'bunga tinggi': 'High Interest Rates',
            'cicilan berat': 'Heavy Installments',
            'proses lama': 'Long Processing Time',
            'persyaratan rumit': 'Complex Requirements',
            'lokasi jauh': 'Location Issues',
            'akses sulit': 'Access Problems'
        }
        
        for key, value in pain_point_mapping.items():
            if key in comment_lower:
                pain_points.append(value)
        
        return pain_points
    
    def _simulate_ai_analysis(self, user_data: Dict, comment_text: str, urgency: str, budget: str, pain_points: List[str]) -> Dict[str, Any]:
        """Simulate Gemini AI analysis insights"""
        
        # Generate realistic AI insights based on extracted data
        insights = {
            'buyer_persona': self._determine_buyer_persona(user_data, comment_text),
            'purchase_probability': self._calculate_purchase_probability(urgency, budget, pain_points),
            'recommended_approach': self._recommend_approach(urgency, pain_points),
            'estimated_timeline': self._estimate_timeline(urgency),
            'concerns': pain_points,
            'motivation_factors': self._extract_motivation_factors(comment_text)
        }
        
        return insights
    
    def _determine_buyer_persona(self, user_data: Dict, comment_text: str) -> str:
        """Determine buyer persona based on user data and comment"""
        
        comment_lower = comment_text.lower()
        
        if any(word in comment_lower for word in ['keluarga', 'anak', 'istri', 'suami']):
            return 'Family Seeker'
        elif any(word in comment_lower for word in ['investasi', 'untung', 'cuan']):
            return 'Investor'
        elif any(word in comment_lower for word in ['pertama', 'baru', 'nikah']):
            return 'First Home Buyer'
        elif any(word in comment_lower for word in ['pindah', 'kerja', 'kantor']):
            return 'Relocator'
        else:
            return 'General Buyer'
    
    def _calculate_purchase_probability(self, urgency: str, budget: str, pain_points: List[str]) -> int:
        """Calculate purchase probability (0-100%)"""
        
        base_probability = 50
        
        # Urgency factor
        if urgency == 'High (Immediate)':
            base_probability += 30
        elif urgency == 'Medium (This Month)':
            base_probability += 15
        elif urgency == 'Low (Research Phase)':
            base_probability += 5
        
        # Budget factor
        if budget != 'Not Mentioned':
            base_probability += 10
        
        # Pain points factor (more pain points = lower probability)
        base_probability -= len(pain_points) * 5
        
        return max(0, min(100, base_probability))
    
    def _recommend_approach(self, urgency: str, pain_points: List[str]) -> str:
        """Recommended approach for the prospect"""
        
        if urgency == 'High (Immediate)':
            if 'ACC Bank Issues' in pain_points:
                return 'Immediate follow-up with alternative financing options'
            elif 'Down Payment Issues' in pain_points:
                return 'Urgent contact with DP 0 programs'
            else:
                return 'Priority contact with available units'
        
        elif urgency == 'Medium (This Month)':
            return 'Schedule property viewing within 3 days'
        
        else:
            return 'Add to nurturing campaign with educational content'
    
    def _estimate_timeline(self, urgency: str) -> str:
        """Estimate purchase timeline"""
        
        timeline_mapping = {
            'High (Immediate)': '1-2 weeks',
            'Medium (This Month)': '2-4 weeks',
            'Low (Research Phase)': '1-3 months'
        }
        
        return timeline_mapping.get(urgency, 'Unknown')
    
    def _extract_motivation_factors(self, comment_text: str) -> List[str]:
        """Extract motivation factors from comment"""
        
        motivations = []
        comment_lower = comment_text.lower()
        
        motivation_keywords = {
            'lokasi': 'Location Priority',
            'harga': 'Price Sensitive',
            'fasilitas': 'Amenities Focus',
            'sekolah': 'Education Priority',
            'akses': 'Accessibility Important',
            'investasi': 'Investment Motivation',
            'nyaman': 'Comfort Seeking',
            'aman': 'Security Concern'
        }
        
        for keyword, motivation in motivation_keywords.items():
            if keyword in comment_lower:
                motivations.append(motivation)
        
        return motivations
    
    def _generate_realistic_comments(self, count: int, post_id: str) -> List[Dict[str, Any]]:
        """Generate realistic comments for simulation"""
        
        # Realistic comment templates
        comment_templates = [
            "Masih ada unitnya? Saya butuh sekarang untuk keluarga",
            "Budget 300 juta, bisa KPR tanpa DP?",
            "Susah ACC bank, ada solusi lain?",
            "Lokasi dekat sekolah ga?",
            "Cicilan berapa ya per bulannya?",
            "Saya urgent butuh rumah bulan ini",
            "Ada promo bulan ini?",
            "Proses KPR nya berapa lama?",
            "DP 0 beneran bisa?",
            "Unit tipe 36 masih ada?",
            "Bisa bantu ACC yang ditolak bank?",
            "Lokasi strategis dekat mana aja?",
            "Ada cluster khusus untuk keluarga?",
            "Berapa cicilan untuk 15 tahun?",
            "Saya cari yang cicilan ringan",
            "Masih ada yang view bagus?",
            "Proses cepat ga perlu ribet?",
            "Ada unit siap huni?",
            "Bisa KPR bank mana aja?",
            "Lokasi dekat akses tol?"
        ]
        
        comments = []
        for i in range(count):
            username = random.choice(self.usernames)
            template = random.choice(comment_templates)
            
            # Add some variation
            if random.random() > 0.7:
                template += f" 🙏"
            
            comment = {
                'id': f"comment_{post_id}_{i+1}",
                'user': {
                    'username': username,
                    'verified': random.choice([True, False]),
                    'followers': random.randint(100, 5000)
                },
                'text': template,
                'platform': random.choice(['Facebook', 'Instagram', 'YouTube']),
                'timestamp': datetime.now() - timedelta(hours=random.randint(0, 24)),
                'engagement': {
                    'likes': random.randint(0, 50),
                    'replies': random.randint(0, 10)
                }
            }
            
            comments.append(comment)
        
        return comments
    
    def _calculate_comment_intent_score(self, comment_text: str) -> int:
        """Calculate intent score specifically for comments"""
        
        base_score = 50
        
        # Urgency indicators (higher weight for comments)
        for pattern in self.urgency_patterns:
            if re.search(pattern, comment_text, re.IGNORECASE):
                base_score += 25
        
        # Budget mentions
        for pattern in self.budget_patterns:
            if re.search(pattern, comment_text, re.IGNORECASE):
                base_score += 15
        
        # Pain points (indicates serious consideration)
        for pattern in self.pain_point_patterns:
            if re.search(pattern, comment_text, re.IGNORECASE):
                base_score += 10
        
        # Question indicators (shows engagement)
        if '?' in comment_text:
            base_score += 5
        
        # Direct property mentions
        property_keywords = ['unit', 'rumah', 'tipe', 'cluster', 'kavling']
        for keyword in property_keywords:
            if keyword.lower() in comment_text.lower():
                base_score += 3
                break
        
        return max(0, min(100, base_score))
    
    def _analyze_comment_sentiment(self, comment_text: str) -> str:
        """Analyze sentiment of comment"""
        
        positive_words = ['bagus', 'ok', 'siap', 'minat', 'mau', 'butuh', 'cari']
        negative_words = ['mahal', 'jauh', 'susah', 'ribet', 'lama', 'ditolak']
        
        comment_lower = comment_text.lower()
        
        positive_count = sum(1 for word in positive_words if word in comment_lower)
        negative_count = sum(1 for word in negative_words if word in comment_lower)
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'
    
    def _extract_common_themes(self, comments: List[Dict]) -> Dict[str, int]:
        """Extract common themes from comments"""
        
        themes = {}
        
        for comment in comments:
            text = comment['text'].lower()
            
            # Count common keywords
            keywords = ['budget', 'kpr', 'dp', 'lokasi', 'cicilan', 'unit', 'proses']
            for keyword in keywords:
                if keyword in text:
                    themes[keyword] = themes.get(keyword, 0) + 1
        
        return themes
    
    def scan_social_intent(self, keywords: List[str]) -> Dict[str, Any]:
        """
        Scan social media platforms for property buying intent
        
        Args:
            keywords: List of keywords to search for
            
        Returns:
            Dict containing scan results and statistics
        """
        
        logger.info(f"🔍 Starting social intent scan for keywords: {keywords}")
        logger.info(f"📱 Scanning {len(self.platforms)} platforms...")
        
        scan_results = {
            'scan_id': f"social_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'keywords_used': keywords,
            'platforms_scanned': self.platforms,
            'start_time': datetime.now().isoformat(),
            'posts_found': [],
            'high_intent_prospects': [],
            'statistics': {
                'total_posts': 0,
                'high_intent_posts': 0,
                'medium_intent_posts': 0,
                'low_intent_posts': 0,
                'platforms_with_posts': []
            },
            'end_time': None,
            'duration_seconds': 0
        }
        
        # Generate posts for each keyword
        for keyword in keywords:
            # Generate 5-10 posts per keyword
            posts_per_keyword = random.randint(5, 10)
            
            for _ in range(posts_per_keyword):
                post = self._generate_realistic_post(keyword)
                scan_results['posts_found'].append(post)
                scan_results['statistics']['total_posts'] += 1
                
                # Categorize by intent score
                if post['intent_score'] >= 70:
                    scan_results['high_intent_prospects'].append(post)
                    scan_results['statistics']['high_intent_posts'] += 1
                elif post['intent_score'] >= 40:
                    scan_results['statistics']['medium_intent_posts'] += 1
                else:
                    scan_results['statistics']['low_intent_posts'] += 1
                
                # Track platforms with posts
                if post['platform'] not in scan_results['statistics']['platforms_with_posts']:
                    scan_results['statistics']['platforms_with_posts'].append(post['platform'])
        
        # Sort posts by intent score (highest first)
        scan_results['posts_found'].sort(key=lambda x: x['intent_score'], reverse=True)
        scan_results['high_intent_prospects'].sort(key=lambda x: x['intent_score'], reverse=True)
        
        # Calculate duration
        scan_results['end_time'] = datetime.now().isoformat()
        start_dt = datetime.fromisoformat(scan_results['start_time'])
        end_dt = datetime.fromisoformat(scan_results['end_time'])
        scan_results['duration_seconds'] = (end_dt - start_dt).total_seconds()
        
        logger.info(f"✅ Social intent scan completed in {scan_results['duration_seconds']:.2f} seconds")
        logger.info(f"📊 Found {scan_results['statistics']['total_posts']} posts total")
        logger.info(f"🎯 High-intent prospects: {scan_results['statistics']['high_intent_posts']}")
        
        return scan_results
    
    def integrate_high_intent_prospects(self, scan_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Integrate high-intent prospects into database as leads
        
        Args:
            scan_results: Results from scan_social_intent
            
        Returns:
            Dict containing integration results
        """
        
        high_intent_prospects = scan_results.get('high_intent_prospects', [])
        
        if not high_intent_prospects:
            logger.info("ℹ️ No high-intent prospects to integrate")
            return {
                'integrated_count': 0,
                'success': True,
                'message': 'No high-intent prospects found'
            }
        
        logger.info(f"🔄 Integrating {len(high_intent_prospects)} high-intent prospects into database...")
        
        integration_results = {
            'integrated_count': 0,
            'failed_count': 0,
            'success': True,
            'integration_details': [],
            'errors': []
        }
        
        for prospect in high_intent_prospects:
            try:
                # Prepare lead data with enhanced deep profiling
                lead_data = {
                    'url': prospect.get('post_url', ''),
                    'title': f"Social Intent: {prospect['username']} on {prospect['platform']}",
                    'content_snippet': prospect['post_content'],
                    'score': prospect['intent_score'],
                    'source': 'Social Intent Scout',
                    'status': 'new',
                    'lead_type': 'Social Media',
                    'location': self._extract_location_from_content(prospect['post_content']),
                    'query_used': prospect.get('keyword_matched', ''),
                    'contact_info': json.dumps({
                        'username': prospect['username'],
                        'platform': prospect['platform']
                    }),
                    'urgency_score': prospect['intent_score'],
                    'potential_value': self._estimate_potential_value(prospect),
                    'data_quality_score': 85,  # High quality from social intent
                    'metadata': json.dumps({
                        'social_intent_data': prospect,
                        'engagement': prospect.get('engagement', {}),
                        'user_profile': prospect.get('user_profile', {}),
                        'scan_id': scan_results.get('scan_id', ''),
                        'extraction_method': 'social_listening',
                        'deep_profile': prospect.get('deep_profile', {}),  # Enhanced with deep profiling
                        'comment_analysis': {
                            'urgency': prospect.get('deep_profile', {}).get('urgency', 'Unknown'),
                            'budget': prospect.get('deep_profile', {}).get('budget', 'Not Mentioned'),
                            'pain_points': prospect.get('deep_profile', {}).get('pain_points', []),
                            'buyer_persona': prospect.get('deep_profile', {}).get('ai_insights', {}).get('buyer_persona', 'Unknown'),
                            'purchase_probability': prospect.get('deep_profile', {}).get('ai_insights', {}).get('purchase_probability', 0),
                            'recommended_approach': prospect.get('deep_profile', {}).get('ai_insights', {}).get('recommended_approach', 'Standard')
                        }
                    }),
                    'behavioral_signals': json.dumps({
                        'intent_signals': {
                            'explicit_need': self._has_explicit_need(prospect['post_content']),
                            'urgency_level': self._get_urgency_level(prospect['post_content']),
                            'budget_mentioned': self._has_budget_mention(prospect['post_content']),
                            'location_specific': self._is_location_specific(prospect['post_content']),
                            'deep_profile_confidence': prospect.get('deep_profile', {}).get('confidence_score', 0)
                        },
                        'engagement_signals': {
                            'likes': prospect.get('engagement', {}).get('likes', 0),
                            'comments': prospect.get('engagement', {}).get('comments', 0),
                            'shares': prospect.get('engagement', {}).get('shares', 0)
                        },
                        'ai_insights': prospect.get('deep_profile', {}).get('ai_insights', {})
                    }),
                    'system_info': json.dumps({
                        'agent': self.name,
                        'version': self.version,
                        'processing_time': scan_results.get('duration_seconds', 0),
                        'confidence_score': prospect['intent_score'],
                        'analysis_method': 'Deep Comment Analysis v2.0'
                    })
                }
                
                # Insert into database
                lead_id = self.db_manager.insert_lead(lead_data)
                
                integration_results['integrated_count'] += 1
                integration_results['integration_details'].append({
                    'lead_id': lead_id,
                    'username': prospect['username'],
                    'platform': prospect['platform'],
                    'intent_score': prospect['intent_score'],
                    'urgency': prospect.get('deep_profile', {}).get('urgency', 'Unknown'),
                    'budget': prospect.get('deep_profile', {}).get('budget', 'Not Mentioned'),
                    'pain_points_count': len(prospect.get('deep_profile', {}).get('pain_points', [])),
                    'status': 'success'
                })
                
                logger.info(f"✅ Integrated prospect: {prospect['username']} (Score: {prospect['intent_score']})")
                logger.info(f"   🧠 Deep Profile: Urgency={prospect.get('deep_profile', {}).get('urgency', 'Unknown')}, Budget={prospect.get('deep_profile', {}).get('budget', 'Not Mentioned')}")
                
            except Exception as e:
                integration_results['failed_count'] += 1
                error_msg = f"Failed to integrate prospect {prospect['username']}: {str(e)}"
                integration_results['errors'].append(error_msg)
                logger.error(error_msg)
        
        logger.info(f"🎯 Integration completed: {integration_results['integrated_count']} successful, {integration_results['failed_count']} failed")
        
        return integration_results
    
    def integrate_comment_prospects(self, comment_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Integrate high-intent prospects from comment analysis into database
        
        Args:
            comment_analysis: Results from analyze_comments
            
        Returns:
            Dict containing integration results
        """
        
        high_intent_prospects = comment_analysis.get('high_intent_prospects', [])
        
        if not high_intent_prospects:
            logger.info("ℹ️ No high-intent comment prospects to integrate")
            return {
                'integrated_count': 0,
                'success': True,
                'message': 'No high-intent comment prospects found'
            }
        
        logger.info(f"🔄 Integrating {len(high_intent_prospects)} high-intent comment prospects into database...")
        
        integration_results = {
            'integrated_count': 0,
            'failed_count': 0,
            'success': True,
            'integration_details': [],
            'errors': []
        }
        
        for prospect in high_intent_prospects:
            try:
                # Enhanced lead data with deep comment profiling
                deep_profile = prospect.get('deep_profile', {})
                ai_insights = deep_profile.get('ai_insights', {})
                
                lead_data = {
                    'url': f"https://{prospect['platform'].lower()}.com/post/{prospect['post_id']}",
                    'title': f"Comment Intent: {prospect['username']} on {prospect['platform']}",
                    'content_snippet': prospect['comment_text'],
                    'score': prospect['intent_score'],
                    'source': 'Social Comment Analysis',
                    'status': 'hot',  # Comment prospects are typically high-intent
                    'lead_type': 'Social Comment',
                    'location': self._extract_location_from_content(prospect['comment_text']),
                    'query_used': f"comment_analysis_{prospect['post_id']}",
                    'contact_info': json.dumps({
                        'username': prospect['username'],
                        'platform': prospect['platform'],
                        'comment_id': prospect['comment_id']
                    }),
                    'urgency_score': prospect['intent_score'],
                    'potential_value': self._estimate_potential_value_from_comment(prospect),
                    'data_quality_score': 95,  # Very high quality from deep comment analysis
                    'metadata': json.dumps({
                        'comment_analysis_data': prospect,
                        'deep_profile': deep_profile,
                        'ai_insights': ai_insights,
                        'post_id': prospect['post_id'],
                        'comment_id': prospect['comment_id'],
                        'extraction_method': 'deep_comment_analysis',
                        'analysis_version': '2.0'
                    }),
                    'behavioral_signals': json.dumps({
                        'intent_signals': {
                            'explicit_need': True,  # Comments show explicit need
                            'urgency_level': deep_profile.get('urgency', 'Unknown'),
                            'budget_mentioned': deep_profile.get('budget') != 'Not Mentioned',
                            'location_specific': self._is_location_specific(prospect['comment_text']),
                            'deep_profile_confidence': deep_profile.get('confidence_score', 0),
                            'purchase_probability': ai_insights.get('purchase_probability', 0)
                        },
                        'engagement_signals': {
                            'likes': prospect.get('engagement', {}).get('likes', 0),
                            'replies': prospect.get('engagement', {}).get('replies', 0),
                            'comment_engagement': True
                        },
                        'ai_insights': ai_insights
                    }),
                    'system_info': json.dumps({
                        'agent': self.name,
                        'version': self.version,
                        'analysis_method': 'Deep Comment Analysis',
                        'confidence_score': deep_profile.get('confidence_score', 0),
                        'profiling_timestamp': deep_profile.get('profiling_timestamp', '')
                    })
                }
                
                # Insert into database
                lead_id = self.db_manager.insert_lead(lead_data)
                
                integration_results['integrated_count'] += 1
                integration_results['integration_details'].append({
                    'lead_id': lead_id,
                    'username': prospect['username'],
                    'platform': prospect['platform'],
                    'intent_score': prospect['intent_score'],
                    'urgency': deep_profile.get('urgency', 'Unknown'),
                    'budget': deep_profile.get('budget', 'Not Mentioned'),
                    'pain_points_count': len(deep_profile.get('pain_points', [])),
                    'buyer_persona': ai_insights.get('buyer_persona', 'Unknown'),
                    'purchase_probability': ai_insights.get('purchase_probability', 0),
                    'status': 'success'
                })
                
                logger.info(f"✅ Integrated comment prospect: {prospect['username']} (Score: {prospect['intent_score']})")
                logger.info(f"   🧠 Deep Profile: {ai_insights.get('buyer_persona', 'Unknown')} - {deep_profile.get('urgency', 'Unknown')}")
                logger.info(f"   💰 Budget: {deep_profile.get('budget', 'Not Mentioned')}")
                logger.info(f"   😣 Pain Points: {len(deep_profile.get('pain_points', []))}")
                
            except Exception as e:
                integration_results['failed_count'] += 1
                error_msg = f"Failed to integrate comment prospect {prospect['username']}: {str(e)}"
                integration_results['errors'].append(error_msg)
                logger.error(error_msg)
        
        logger.info(f"🎯 Comment integration completed: {integration_results['integrated_count']} successful, {integration_results['failed_count']} failed")
        
        return integration_results
    
    def _extract_location_from_content(self, content: str) -> str:
        """Extract location from post content"""
        for location in self.locations:
            if location.lower() in content.lower():
                return location
        return 'Unknown'
    
    def _estimate_potential_value(self, prospect: Dict[str, Any]) -> str:
        """Estimate potential value based on content"""
        content = prospect['post_content'].lower()
        
        if any(word in content for word in ['1 m', '1m', 'miliar']):
            return 'High (>1M)'
        elif any(word in content for word in ['500 juta', '600 juta', '700 juta', '800 juta', '900 juta']):
            return 'Medium-High (500M-1M)'
        elif any(word in content for word in ['300 juta', '400 juta']):
            return 'Medium (300M-500M)'
        else:
            return 'Low-Medium (<300M)'
    
    def _estimate_potential_value_from_comment(self, prospect: Dict[str, Any]) -> str:
        """Estimate potential value based on comment analysis"""
        deep_profile = prospect.get('deep_profile', {})
        ai_insights = deep_profile.get('ai_insights', {})
        budget = deep_profile.get('budget', 'Not Mentioned')
        buyer_persona = ai_insights.get('buyer_persona', 'Unknown')
        
        # Enhanced value estimation based on deep profiling
        if buyer_persona == 'Investor':
            return 'High (>800M)'
        elif buyer_persona == 'Family Seeker':
            return 'Medium-High (500M-800M)'
        elif buyer_persona == 'First Home Buyer':
            return 'Medium (300M-500M)'
        elif budget != 'Not Mentioned':
            if 'Miliar' in budget:
                return 'Very High (>1M)'
            elif '500' in budget or '600' in budget or '700' in budget:
                return 'High (600M-1M)'
            elif '300' in budget or '400' in budget:
                return 'Medium (300M-600M)'
            else:
                return 'Low-Medium (<300M)'
        else:
            return 'Medium (300M-500M)'
    
    def _has_explicit_need(self, content: str) -> bool:
        """Check if content has explicit buying need"""
        explicit_words = ['butuh', 'cari', 'mau beli', 'minat', 'serius', 'segera']
        return any(word in content.lower() for word in explicit_words)
    
    def _get_urgency_level(self, content: str) -> str:
        """Determine urgency level from content"""
        if any(word in content.lower() for word in ['segera', 'buruan', 'cepat', 'urgent']):
            return 'High'
        elif any(word in content.lower() for word in ['minggu ini', 'bulan ini']):
            return 'Medium'
        else:
            return 'Low'
    
    def _has_budget_mention(self, content: str) -> bool:
        """Check if content mentions budget"""
        budget_words = ['budget', 'cicilan', 'dp', 'harga', 'juta', 'miliar']
        return any(word in content.lower() for word in budget_words)
    
    def _is_location_specific(self, content: str) -> bool:
        """Check if content is location specific"""
        return any(location.lower() in content.lower() for location in self.locations)
    
    def run_social_intent_analysis(self, keywords: List[str]) -> Dict[str, Any]:
        """
        Run complete social intent analysis workflow with enhanced comment analysis
        
        Args:
            keywords: List of keywords to search for
            
        Returns:
            Dict containing complete analysis results
        """
        
        logger.info("🚀 Starting complete Social Intent Analysis workflow v2.0...")
        logger.info("🔍 Enhanced with Deep Comment Analysis capabilities")
        
        # Step 1: Scan social intent
        scan_results = self.scan_social_intent(keywords)
        
        # Step 2: Analyze comments from viral posts (NEW)
        comment_analysis_results = []
        if scan_results['high_intent_prospects']:
            # Select top posts for comment analysis
            top_posts = scan_results['high_intent_prospects'][:3]  # Analyze top 3 posts
            for post in top_posts:
                post_id = f"post_{random.randint(10000, 99999)}"
                logger.info(f"🔍 Analyzing comments for post: {post_id}")
                comment_result = self.analyze_comments(post_id)
                comment_analysis_results.append(comment_result)
        
        # Step 3: Integrate high-intent prospects from posts
        integration_results = self.integrate_high_intent_prospects(scan_results)
        
        # Step 4: Integrate high-intent prospects from comments (NEW)
        comment_integration_results = []
        for comment_result in comment_analysis_results:
            result = self.integrate_comment_prospects(comment_result)
            comment_integration_results.append(result)
        
        # Step 5: Generate enhanced summary report
        total_comment_prospects = sum(result['integrated_count'] for result in comment_integration_results)
        
        summary_report = {
            'workflow_id': f"social_workflow_v2_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'keywords_analyzed': keywords,
            'scan_summary': {
                'total_posts_found': scan_results['statistics']['total_posts'],
                'high_intent_prospects': scan_results['statistics']['high_intent_posts'],
                'platforms_covered': len(scan_results['statistics']['platforms_with_posts']),
                'scan_duration': scan_results['duration_seconds']
            },
            'comment_analysis_summary': {
                'posts_analyzed': len(comment_analysis_results),
                'total_comments_analyzed': sum(result['total_comments'] for result in comment_analysis_results),
                'high_intent_comment_prospects': sum(len(result['high_intent_prospects']) for result in comment_analysis_results),
                'urgency_indicators': sum(len(result['urgency_indicators']) for result in comment_analysis_results),
                'budget_mentions': sum(len(result['budget_mentions']) for result in comment_analysis_results),
                'pain_points_identified': sum(len(result['pain_points']) for result in comment_analysis_results)
            },
            'integration_summary': {
                'post_prospects_integrated': integration_results['integrated_count'],
                'comment_prospects_integrated': total_comment_prospects,
                'total_prospects_integrated': integration_results['integrated_count'] + total_comment_prospects,
                'integration_success_rate': (integration_results['integrated_count'] / len(scan_results['high_intent_prospects']) * 100) if scan_results['high_intent_prospects'] else 0,
                'integration_errors': integration_results['failed_count']
            },
            'top_prospects': scan_results['high_intent_prospects'][:5],  # Top 5 prospects from posts
            'top_comment_prospects': self._get_top_comment_prospects(comment_analysis_results),
            'platform_performance': self._analyze_platform_performance(scan_results['posts_found']),
            'deep_insights': self._generate_deep_insights(comment_analysis_results),
            'recommendations': self._generate_enhanced_recommendations(scan_results, integration_results, comment_analysis_results),
            'execution_time': scan_results['duration_seconds'],
            'timestamp': datetime.now().isoformat(),
            'version': '2.0'
        }
        
        logger.info("🎉 Enhanced Social Intent Analysis workflow completed successfully!")
        logger.info(f"📊 Summary: {summary_report['scan_summary']['total_posts_found']} posts, {summary_report['integration_summary']['post_prospects_integrated']} post prospects, {summary_report['integration_summary']['comment_prospects_integrated']} comment prospects")
        logger.info(f"🧠 Deep Insights: {summary_report['comment_analysis_summary']['urgency_indicators']} urgency indicators, {summary_report['comment_analysis_summary']['budget_mentions']} budget mentions")
        
        return summary_report
    
    def _get_top_comment_prospects(self, comment_analysis_results: List[Dict]) -> List[Dict]:
        """Get top prospects from comment analysis"""
        all_prospects = []
        for result in comment_analysis_results:
            all_prospects.extend(result['high_intent_prospects'])
        
        # Sort by intent score
        all_prospects.sort(key=lambda x: x['intent_score'], reverse=True)
        return all_prospects[:5]  # Top 5 comment prospects
    
    def _generate_deep_insights(self, comment_analysis_results: List[Dict]) -> Dict[str, Any]:
        """Generate deep insights from comment analysis"""
        
        if not comment_analysis_results:
            return {'message': 'No comment analysis data available'}
        
        # Aggregate all data
        all_urgency_indicators = []
        all_budget_mentions = []
        all_pain_points = []
        all_buyer_personas = []
        all_purchase_probabilities = []
        
        for result in comment_analysis_results:
            all_urgency_indicators.extend(result['urgency_indicators'])
            all_budget_mentions.extend(result['budget_mentions'])
            all_pain_points.extend(result['pain_points'])
            
            for prospect in result['high_intent_prospects']:
                ai_insights = prospect.get('deep_profile', {}).get('ai_insights', {})
                if ai_insights.get('buyer_persona'):
                    all_buyer_personas.append(ai_insights['buyer_persona'])
                if ai_insights.get('purchase_probability'):
                    all_purchase_probabilities.append(ai_insights['purchase_probability'])
        
        # Analyze urgency distribution
        urgency_distribution = {}
        for indicator in all_urgency_indicators:
            urgency = indicator['urgency']
            urgency_distribution[urgency] = urgency_distribution.get(urgency, 0) + 1
        
        # Analyze budget ranges
        budget_ranges = {}
        for mention in all_budget_mentions:
            budget = mention['budget']
            budget_ranges[budget] = budget_ranges.get(budget, 0) + 1
        
        # Analyze pain points
        pain_point_frequency = {}
        for pain_point in all_pain_points:
            pain_point_frequency[pain_point] = pain_point_frequency.get(pain_point, 0) + 1
        
        # Analyze buyer personas
        persona_distribution = {}
        for persona in all_buyer_personas:
            persona_distribution[persona] = persona_distribution.get(persona, 0) + 1
        
        # Calculate average purchase probability
        avg_purchase_probability = sum(all_purchase_probabilities) / len(all_purchase_probabilities) if all_purchase_probabilities else 0
        
        return {
            'urgency_distribution': urgency_distribution,
            'budget_ranges': budget_ranges,
            'top_pain_points': sorted(pain_point_frequency.items(), key=lambda x: x[1], reverse=True)[:5],
            'buyer_persona_distribution': persona_distribution,
            'average_purchase_probability': round(avg_purchase_probability, 1),
            'total_prospects_analyzed': len(all_urgency_indicators),
            'insights_confidence': 'High' if len(all_urgency_indicators) > 10 else 'Medium'
        }
    
    def _generate_enhanced_recommendations(self, scan_results: Dict, integration_results: Dict, comment_analysis_results: List[Dict]) -> List[str]:
        """Generate enhanced recommendations based on deep comment analysis"""
        
        recommendations = []
        
        # Base recommendations
        platform_performance = self._analyze_platform_performance(scan_results['posts_found'])
        best_platform = max(platform_performance.items(), key=lambda x: x[1]['high_intent_percentage'])
        recommendations.append(f"Focus on {best_platform[0]} - highest high-intent percentage ({best_platform[1]['high_intent_percentage']:.1f}%)")
        
        # Enhanced recommendations from comment analysis
        if comment_analysis_results:
            deep_insights = self._generate_deep_insights(comment_analysis_results)
            
            # Urgency-based recommendations
            urgency_dist = deep_insights.get('urgency_distribution', {})
            if urgency_dist.get('High (Immediate)', 0) > 5:
                recommendations.append("High urgency detected - Prepare immediate response team and fast-track processing")
            
            # Budget-based recommendations
            budget_ranges = deep_insights.get('budget_ranges', {})
            if budget_ranges:
                top_budget = max(budget_ranges.items(), key=lambda x: x[1])
                recommendations.append(f"Most common budget range: {top_budget[0]} - Tailor financing options accordingly")
            
            # Pain point-based recommendations
            top_pain_points = deep_insights.get('top_pain_points', [])
            if top_pain_points:
                top_pain = top_pain_points[0][0]
                if 'ACC' in top_pain:
                    recommendations.append("ACC issues prevalent - Prepare alternative financing solutions")
                elif 'DP' in top_pain:
                    recommendations.append("Down payment concerns - Highlight DP 0 programs and low down payment options")
            
            # Persona-based recommendations
            persona_dist = deep_insights.get('buyer_persona_distribution', {})
            if persona_dist:
                top_persona = max(persona_dist.items(), key=lambda x: x[1])
                recommendations.append(f"Primary buyer persona: {top_persona[0]} - Customize marketing approach")
            
            # Purchase probability insights
            avg_prob = deep_insights.get('average_purchase_probability', 0)
            if avg_prob > 70:
                recommendations.append("High purchase probability detected - Prioritize immediate follow-up")
            elif avg_prob > 50:
                recommendations.append("Moderate purchase probability - Schedule property viewings")
        
        # Integration recommendations
        total_prospects = integration_results['integrated_count']
        if total_prospects > 20:
            recommendations.append("High prospect volume - Consider automated follow-up sequences")
        elif total_prospects > 10:
            recommendations.append("Moderate prospect volume - Balance automated and personal outreach")
        
        return recommendations
    
    def _analyze_platform_performance(self, posts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze which platforms perform best"""
        platform_stats = {}
        
        for post in posts:
            platform = post['platform']
            if platform not in platform_stats:
                platform_stats[platform] = {
                    'post_count': 0,
                    'total_intent_score': 0,
                    'high_intent_count': 0
                }
            
            platform_stats[platform]['post_count'] += 1
            platform_stats[platform]['total_intent_score'] += post['intent_score']
            
            if post['intent_score'] >= 70:
                platform_stats[platform]['high_intent_count'] += 1
        
        # Calculate averages
        for platform, stats in platform_stats.items():
            stats['average_intent_score'] = stats['total_intent_score'] / stats['post_count']
            stats['high_intent_percentage'] = (stats['high_intent_count'] / stats['post_count']) * 100
        
        return platform_stats
    
    def _generate_recommendations(self, scan_results: Dict[str, Any], integration_results: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations based on analysis"""
        recommendations = []
        
        # Platform recommendations
        platform_performance = self._analyze_platform_performance(scan_results['posts_found'])
        best_platform = max(platform_performance.items(), key=lambda x: x[1]['high_intent_percentage'])
        recommendations.append(f"Focus on {best_platform[0]} - highest high-intent percentage ({best_platform[1]['high_intent_percentage']:.1f}%)")
        
        # Keyword recommendations
        keyword_performance = {}
        for keyword in scan_results['keywords_used']:
            keyword_posts = [p for p in scan_results['posts_found'] if keyword in p.get('keyword_matched', '')]
            high_intent_keyword = [p for p in keyword_posts if p['intent_score'] >= 70]
            keyword_performance[keyword] = {
                'total': len(keyword_posts),
                'high_intent': len(high_intent_keyword),
                'percentage': (len(high_intent_keyword) / len(keyword_posts) * 100) if keyword_posts else 0
            }
        
        best_keyword = max(keyword_performance.items(), key=lambda x: x[1]['percentage'])
        recommendations.append(f"Prioritize '{best_keyword[0]}' keyword - {best_keyword[1]['percentage']:.1f}% high-intent rate")
        
        # Timing recommendations
        if scan_results['statistics']['high_intent_posts'] > 5:
            recommendations.append("High-intent volume detected - consider immediate follow-up campaign")
        else:
            recommendations.append("Moderate intent volume - continue monitoring and engage with top prospects")
        
        # Integration recommendations
        if integration_results['failed_count'] > 0:
            recommendations.append(f"Review integration errors - {integration_results['failed_count']} prospects failed to integrate")
        
        return recommendations


# Convenience functions for external usage
def run_social_intent_scan(keywords: List[str]) -> Dict[str, Any]:
    """
    Convenience function to run social intent scan
    
    Args:
        keywords: List of keywords to search for
        
    Returns:
        Dict containing scan results
    """
    scout = SocialIntentScout()
    return scout.scan_social_intent(keywords)


def run_complete_social_analysis(keywords: List[str]) -> Dict[str, Any]:
    """
    Convenience function to run complete social intent analysis
    
    Args:
        keywords: List of keywords to search for
        
    Returns:
        Dict containing complete analysis results
    """
    scout = SocialIntentScout()
    return scout.run_social_intent_analysis(keywords)


if __name__ == "__main__":
    # Example usage
    keywords = ['butuh rumah', 'cari KPR murah', 'overkredit rumah']
    
    print("🎯 Social Intent Scout - Example Usage")
    print(f"🔍 Keywords: {keywords}")
    print("=" * 50)
    
    # Run complete analysis
    results = run_complete_social_analysis(keywords)
    
    print(f"\n📊 Analysis Results:")
    print(f"Total Posts Found: {results['scan_summary']['total_posts_found']}")
    print(f"High-Intent Prospects: {results['scan_summary']['high_intent_prospects']}")
    print(f"Prospects Integrated: {results['integration_summary']['prospects_integrated']}")
    print(f"Execution Time: {results['execution_time']:.2f} seconds")
    
    print(f"\n🎯 Top 3 Prospects:")
    for i, prospect in enumerate(results['top_prospects'][:3], 1):
        print(f"{i}. {prospect['username']} ({prospect['platform']}) - Score: {prospect['intent_score']}")
        print(f"   Content: {prospect['post_content'][:100]}...")
    
    print(f"\n💡 Recommendations:")
    for rec in results['recommendations']:
        print(f"- {rec}")
