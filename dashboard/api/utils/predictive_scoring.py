"""
LUMINA OS - Predictive Scoring Utility

Lead scoring system for evaluating lead quality based on content analysis.
Uses keyword-based scoring to determine lead temperature and priority.
"""

import re
from typing import Dict, List, Set
from dataclasses import dataclass


@dataclass
class ScoringResult:
    """Result of lead scoring calculation"""
    score: int
    status: str
    keywords_found: List[str]
    breakdown: Dict[str, int]
    intent_category: str
    intent_score: int
    intent_confidence: str


class LeadScorer:
    """
    Advanced lead scoring system with intent classification for evaluating lead quality.
    
    Executive Blueprint Lumina OS - Intent Classification System
    
    Scoring Logic:
    - Base score: 40 points
    - Intent Classification: Priority-based scoring
    - Hot keywords: +30 points each
    - Warm keywords: +15 points each
    - Negative keywords: -20 points each
    - Final score: 0-100 scale
    
    Intent Classification (Priority-based):
    - Transactional: Priority 1 (+40 points) - beli, cari, butuh, survey, dp, kpr
    - Pain-Point: Priority 2 (+20 points) - khawatir, sulit, bingung, mahal
    - Comparison: Priority 3 (+15 points) - bandingkan, mana, lebih baik
    - Informational: Priority 4 (+10 points) - tanya, info, detail, lokasi
    
    Status Classification:
    - Hot: score >= 80
    - Warm: score 60-79
    - Cold: score < 60
    """
    
    # Intent classification keywords with priority-based scoring
    TRANSACTIONAL_KEYWORDS = {
        # High-intent transactional keywords
        'beli': 40, 'cari': 40, 'butuh': 40, 'survey': 40, 'dp': 40, 'kpr': 40,
        'booking': 40, 'deal': 40, 'offer': 40, 'tunai': 40, 'cash': 40,
        'investasi': 40, 'dibeli': 40, 'dicari': 40, 'dibutuhkan': 40,
        'survei': 40, 'angsur': 40, 'cicilan': 40, 'kredit': 40,
        'pinjam': 40, 'bayar': 40, 'harga': 40, 'promo': 40,
        'diskon': 40, 'murah': 40, 'dijual': 40, 'penawaran': 40
    }
    
    PAIN_POINT_KEYWORDS = {
        # Pain point and concern keywords
        'khawatir': 20, 'sulit': 20, 'bingung': 20, 'mahal': 20,
        'banyak': 20, 'terlalu': 20, 'sulitnya': 20, 'keluhan': 20,
        'masalah': 20, 'kendala': 20, 'hambatan': 20, 'kesulitan': 20,
        'rumit': 20, 'kompleks': 20, 'proses': 20, 'waktu': 20,
        'lama': 20, 'kecewa': 20, 'buruk': 20, 'jelek': 20,
        'tidak sesuai': 20, 'kurang': 20, 'cacat': 20, 'kritik': 20
    }
    
    COMPARISON_KEYWORDS = {
        # Comparison and evaluation keywords
        'bandingkan': 15, 'banding': 15, 'mana': 15, 'lebih': 15, 'lebih baik': 15,
        'pilihan': 15, 'opsi': 15, 'alternatif': 15, 'bandingkan dengan': 15,
        'dibandingkan': 15, 'perbanding': 15, 'versus': 15, 'atau': 15,
        'antara': 15, 'dengan': 15, 'dari': 15, 'lain': 15,
        'rekomendasi': 15, 'saran': 15, 'preferensi': 15, 'pilihan terbaik': 15
    }
    
    INFORMATIONAL_KEYWORDS = {
        # Information seeking keywords
        'tanya': 10, 'info': 10, 'informasi': 10, 'detail': 10, 'lokasi': 10,
        'alamat': 10, 'alamatnya': 10, 'dimana': 10, 'kapan': 10,
        'bagaimana': 10, 'berapa': 10, 'berapa banyak': 10, 'berapa harga': 10,
        'spesifikasi': 10, 'spek': 10, 'fasilitas': 10, 'fitur': 10,
        'gambar': 10, 'foto': 10, 'video': 10, 'contoh': 10,
        'demo': 10, 'sample': 10, 'katalog': 10, 'brochure': 10
    }
    
    # Legacy keyword categories for backward compatibility
    HOT_KEYWORDS = {
        'jual': 30, 'promo': 30, 'diskon': 30, 'murah': 30,
        'ready stock': 30, 'dijual': 30, 'investasi': 30,
        'penawaran': 30
    }
    
    WARM_KEYWORDS = {
        'perumahan': 15, 'cluster': 15, 'apartemen': 15, 'properti': 15,
        'rumah': 15, 'tanah': 15, 'ruko': 15, 'kavling': 15,
        'type': 15, 'tipe': 15, 'unit': 15, 'bangun': 15,
        'developer': 15, 'pengembang': 15, 'proyek': 15,
        'area': 15, 'wilayah': 15, 'kota': 15
    }
    
    NEGATIVE_KEYWORDS = {
        'penipuan': -20, 'berita': -20, 'komplain': -20, 'kasus': -20,
        'penipu': -20, 'scam': -20, 'hoax': -20, 'palsu': -20,
        'tipu': -20, 'gagal': -20, 'batal': -20, 'tidak': -20,
        'bukan': -20, 'error': -20, 'salah': -20, 'jelek': -20
    }
    
    # Base score for all leads
    BASE_SCORE = 40
    
    def __init__(self):
        """Initialize the LeadScorer with compiled regex patterns"""
        self._compile_patterns()
    
    def _compile_patterns(self):
        """Pre-compile regex patterns for better performance"""
        self.hot_patterns = self._compile_keyword_patterns(self.HOT_KEYWORDS)
        self.warm_patterns = self._compile_keyword_patterns(self.WARM_KEYWORDS)
        self.negative_patterns = self._compile_keyword_patterns(self.NEGATIVE_KEYWORDS)
        
        # Intent classification patterns
        self.transactional_patterns = self._compile_keyword_patterns(self.TRANSACTIONAL_KEYWORDS)
        self.pain_point_patterns = self._compile_keyword_patterns(self.PAIN_POINT_KEYWORDS)
        self.comparison_patterns = self._compile_keyword_patterns(self.COMPARISON_KEYWORDS)
        self.informational_patterns = self._compile_keyword_patterns(self.INFORMATIONAL_KEYWORDS)
    
    def _compile_keyword_patterns(self, keywords: Dict[str, int]) -> List[tuple]:
        """
        Compile regex patterns for keywords
        
        Args:
            keywords: Dictionary of keywords and their scores
            
        Returns:
            List of (pattern, score, keyword) tuples
        """
        patterns = []
        for keyword, score in keywords.items():
            # Create case-insensitive regex pattern
            pattern = re.compile(r'\b' + re.escape(keyword) + r'\b', re.IGNORECASE)
            patterns.append((pattern, score, keyword))
        return patterns
    
    def _find_keywords(self, text: str, patterns: List[tuple]) -> List[tuple]:
        """
        Find keywords in text using compiled patterns
        
        Args:
            text: Text to search in
            patterns: List of (pattern, score, keyword) tuples
            
        Returns:
            List of (keyword, score) tuples found
        """
        found = []
        for pattern, score, keyword in patterns:
            if pattern.search(text):
                found.append((keyword, score))
        return found
    
    def _calculate_status(self, score: int) -> str:
        """
        Determine lead status based on score
        
        Args:
            score: Calculated score (0-100)
            
        Returns:
            Status string: 'Hot', 'Warm', or 'Cold'
        """
        if score >= 80:
            return 'Hot'
        elif score >= 60:
            return 'Warm'
        else:
            return 'Cold'
    
    def _classify_intent(self, text: str) -> Dict[str, Any]:
        """
        Classify user intent based on keyword analysis
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with intent classification results
        """
        intent_scores = {
            'transactional': 0,
            'pain_point': 0,
            'comparison': 0,
            'informational': 0
        }
        
        intent_keywords = {
            'transactional': [],
            'pain_point': [],
            'comparison': [],
            'informational': []
        }
        
        # Find intent keywords
        transactional_keywords = self._find_keywords(text, self.transactional_patterns)
        for keyword, score in transactional_keywords:
            intent_scores['transactional'] += score
            intent_keywords['transactional'].append(keyword)
        
        pain_point_keywords = self._find_keywords(text, self.pain_point_patterns)
        for keyword, score in pain_point_keywords:
            intent_scores['pain_point'] += score
            intent_keywords['pain_point'].append(keyword)
        
        comparison_keywords = self._find_keywords(text, self.comparison_patterns)
        for keyword, score in comparison_keywords:
            intent_scores['comparison'] += score
            intent_keywords['comparison'].append(keyword)
        
        informational_keywords = self._find_keywords(text, self.informational_patterns)
        for keyword, score in informational_keywords:
            intent_scores['informational'] += score
            intent_keywords['informational'].append(keyword)
        
        # Determine dominant intent
        max_score = max(intent_scores.values())
        dominant_intent = max(intent_scores, key=intent_scores.get)
        
        # Calculate confidence level
        total_keywords = sum(len(keywords) for keywords in intent_keywords.values())
        if total_keywords >= 3:
            confidence = 'high'
        elif total_keywords >= 2:
            confidence = 'medium'
        elif total_keywords >= 1:
            confidence = 'low'
        else:
            confidence = 'none'
        
        return {
            'dominant_intent': dominant_intent,
            'intent_scores': intent_scores,
            'intent_keywords': intent_keywords,
            'max_score': max_score,
            'total_keywords': total_keywords,
            'confidence': confidence
        }
    
    def _get_intent_category(self, dominant_intent: str) -> str:
        """
        Get human-readable intent category name
        
        Args:
            dominant_intent: Intent identifier
            
        Returns:
            Human-readable intent category
        """
        intent_mapping = {
            'transactional': 'Transactional',
            'pain_point': 'Pain-Point',
            'comparison': 'Comparison',
            'informational': 'Informational'
        }
        return intent_mapping.get(dominant_intent, 'Unknown')
    
    def _normalize_text(self, text: str) -> str:
        """
        Normalize text for consistent processing
        
        Args:
            text: Input text
            
        Returns:
            Normalized text
        """
        if not text:
            return ""
        
        # Convert to lowercase and remove extra whitespace
        normalized = text.lower().strip()
        
        # Remove common punctuation that might interfere with keyword matching
        normalized = re.sub(r'[^\w\s]', ' ', normalized)
        
        # Replace multiple spaces with single space
        normalized = re.sub(r'\s+', ' ', normalized)
        
        return normalized
    
    def calculate_score(self, title: str, description: str, source: str = "") -> ScoringResult:
        """
        Calculate lead score based on title, description, and source with intent classification
        
        Args:
            title: Lead title or subject
            description: Lead description or content
            source: Source of the lead (optional)
            
        Returns:
            ScoringResult object with score, status, keywords found, and intent classification
        """
        # Combine all text for analysis
        combined_text = f"{title} {description} {source}"
        normalized_text = self._normalize_text(combined_text)
        
        # Initialize scoring variables
        total_score = self.BASE_SCORE
        keywords_found = []
        breakdown = {'base_score': self.BASE_SCORE}
        
        # Find hot keywords
        hot_keywords = self._find_keywords(normalized_text, self.hot_patterns)
        for keyword, score in hot_keywords:
            total_score += score
            keywords_found.append(keyword)
            breakdown[f'hot_{keyword}'] = score
        
        # Find warm keywords
        warm_keywords = self._find_keywords(normalized_text, self.warm_patterns)
        for keyword, score in warm_keywords:
            total_score += score
            keywords_found.append(keyword)
            breakdown[f'warm_{keyword}'] = score
        
        # Find negative keywords
        negative_keywords = self._find_keywords(normalized_text, self.negative_patterns)
        for keyword, score in negative_keywords:
            total_score += score  # Note: negative scores are already negative
            keywords_found.append(keyword)
            breakdown[f'negative_{keyword}'] = score
        
        # Intent Classification (Executive Blueprint)
        intent_result = self._classify_intent(normalized_text)
        
        # Add intent-based scoring
        intent_score = intent_result['max_score']
        total_score += intent_score
        
        # Add intent keywords to found keywords
        for intent_type, keywords in intent_result['intent_keywords'].items():
            keywords_found.extend(keywords)
            breakdown[f'intent_{intent_type}'] = intent_result['intent_scores'][intent_type]
        
        # Ensure score stays within 0-100 range
        total_score = max(0, min(100, total_score))
        
        # Determine status
        status = self._calculate_status(total_score)
        
        # Get intent category and confidence
        intent_category = self._get_intent_category(intent_result['dominant_intent'])
        intent_confidence = intent_result['confidence'].title()
        
        # Create result object with intent classification
        result = ScoringResult(
            score=total_score,
            status=status,
            keywords_found=keywords_found,
            breakdown=breakdown,
            intent_category=intent_category,
            intent_score=intent_score,
            intent_confidence=intent_confidence
        )
        
        return result
    
    def batch_score(self, leads: List[Dict[str, str]]) -> List[ScoringResult]:
        """
        Score multiple leads in batch
        
        Args:
            leads: List of lead dictionaries with 'title', 'description', and 'source' keys
            
        Returns:
            List of ScoringResult objects
        """
        results = []
        for lead in leads:
            result = self.calculate_score(
                title=lead.get('title', ''),
                description=lead.get('description', ''),
                source=lead.get('source', '')
            )
            results.append(result)
        return results
    
    def get_keyword_stats(self) -> Dict[str, Dict[str, int]]:
        """
        Get statistics about keyword categories
        
        Returns:
            Dictionary with keyword statistics
        """
        return {
            'hot_keywords': {
                'count': len(self.HOT_KEYWORDS),
                'score_range': [min(self.HOT_KEYWORDS.values()), max(self.HOT_KEYWORDS.values())],
                'keywords': list(self.HOT_KEYWORDS.keys())
            },
            'warm_keywords': {
                'count': len(self.WARM_KEYWORDS),
                'score_range': [min(self.WARM_KEYWORDS.values()), max(self.WARM_KEYWORDS.values())],
                'keywords': list(self.WARM_KEYWORDS.keys())
            },
            'negative_keywords': {
                'count': len(self.NEGATIVE_KEYWORDS),
                'score_range': [min(self.NEGATIVE_KEYWORDS.values()), max(self.NEGATIVE_KEYWORDS.values())],
                'keywords': list(self.NEGATIVE_KEYWORDS.keys())
            }
        }
    
    def add_custom_keyword(self, category: str, keyword: str, score: int) -> bool:
        """
        Add a custom keyword to a specific category
        
        Args:
            category: 'hot', 'warm', or 'negative'
            keyword: Keyword to add
            score: Score value for the keyword
            
        Returns:
            True if successful, False if category is invalid
        """
        category = category.lower()
        
        if category == 'hot':
            self.HOT_KEYWORDS[keyword.lower()] = score
        elif category == 'warm':
            self.WARM_KEYWORDS[keyword.lower()] = score
        elif category == 'negative':
            self.NEGATIVE_KEYWORDS[keyword.lower()] = score
        else:
            return False
        
        # Re-compile patterns with new keyword
        self._compile_patterns()
        return True
    
    def remove_keyword(self, category: str, keyword: str) -> bool:
        """
        Remove a keyword from a specific category
        
        Args:
            category: 'hot', 'warm', or 'negative'
            keyword: Keyword to remove
            
        Returns:
            True if successful, False if keyword not found
        """
        category = category.lower()
        keyword = keyword.lower()
        
        removed = False
        if category == 'hot' and keyword in self.HOT_KEYWORDS:
            del self.HOT_KEYWORDS[keyword]
            removed = True
        elif category == 'warm' and keyword in self.WARM_KEYWORDS:
            del self.WARM_KEYWORDS[keyword]
            removed = True
        elif category == 'negative' and keyword in self.NEGATIVE_KEYWORDS:
            del self.NEGATIVE_KEYWORDS[keyword]
            removed = True
        
        if removed:
            # Re-compile patterns
            self._compile_patterns()
        
        return removed


# Example usage and testing
if __name__ == "__main__":
    # Initialize the scorer
    scorer = LeadScorer()
    
    # Test examples
    test_cases = [
        {
            'title': 'JUAL CEPAT Rumah Mewah',
            'description': 'Properti dengan harga promo, ready stock dan KPR mudah',
            'source': 'website'
        },
        {
            'title': 'Perumahan Cluster Baru',
            'description': 'Lokasi strategis dengan fasilitas lengkap',
            'source': 'properti_portal'
        },
        {
            'title': 'Berita Penipuan Properti',
            'description': 'Kasus penipuan investasi properti palsu',
            'source': 'social_media'
        }
    ]
    
    # Test single scoring
    print("=== Single Lead Scoring Test ===")
    for i, test_case in enumerate(test_cases, 1):
        result = scorer.calculate_score(
            title=test_case['title'],
            description=test_case['description'],
            source=test_case['source']
        )
        
        print(f"\nTest Case {i}:")
        print(f"Title: {test_case['title']}")
        print(f"Score: {result.score}")
        print(f"Status: {result.status}")
        print(f"Keywords Found: {result.keywords_found}")
        print(f"Breakdown: {result.breakdown}")
    
    # Test batch scoring
    print("\n\n=== Batch Scoring Test ===")
    batch_results = scorer.batch_score(test_cases)
    
    for i, result in enumerate(batch_results, 1):
        print(f"Lead {i}: Score {result.score} ({result.status})")
    
    # Test keyword stats
    print("\n\n=== Keyword Statistics ===")
    stats = scorer.get_keyword_stats()
    for category, info in stats.items():
        print(f"{category.upper()}:")
        print(f"  Count: {info['count']}")
        print(f"  Score Range: {info['score_range']}")
        print(f"  Sample Keywords: {info['keywords'][:5]}...")
    
    # Test custom keyword addition
    print("\n\n=== Custom Keyword Test ===")
    scorer.add_custom_keyword('hot', 'urgent', 25)
    
    custom_result = scorer.calculate_score(
        title="URGENT Sale Available",
        description="Urgent property sale with good price",
        source="direct"
    )
    
    print(f"Custom Test Result:")
    print(f"Score: {custom_result.score}")
    print(f"Status: {custom_result.status}")
    print(f"Keywords Found: {custom_result.keywords_found}")
    
    # Test intent classification
    print("\n\n=== INTENT CLASSIFICATION TEST ===")
    intent_test_cases = [
        {
            'title': 'BELI CEPAT Rumah Type 36',
            'description': 'Butuh rumah segera, siap DP dan KPR',
            'source': 'web_form',
            'expected_intent': 'Transactional'
        },
        {
            'title': 'Khawatir Harga Properti Mahal',
            'description': 'Sulit untuk beli rumah dengan harga yang tinggi',
            'source': 'forum',
            'expected_intent': 'Pain-Point'
        },
        {
            'title': 'Bandingkan Perumahan A vs B',
            'description': 'Mana yang lebih baik untuk investasi?',
            'source': 'comparison_site',
            'expected_intent': 'Comparison'
        },
        {
            'title': 'Tanya Info Lokasi Cluster',
            'description': 'Detail spesifikasi dan fasilitas cluster baru',
            'source': 'inquiry',
            'expected_intent': 'Informational'
        }
    ]
    
    for i, test_case in enumerate(intent_test_cases, 1):
        print(f"\nIntent Test {i}: {test_case['title']}")
        print(f"Expected Intent: {test_case['expected_intent']}")
        print("-" * 40)
        
        result = scorer.calculate_score(
            test_case['title'], 
            test_case['description'], 
            test_case['source']
        )
        
        print(f"Score: {result.score}")
        print(f"Status: {result.status}")
        print(f"Intent Category: {result.intent_category}")
        print(f"Intent Score: {result.intent_score}")
        print(f"Intent Confidence: {result.intent_confidence}")
        print(f"Keywords Found: {result.keywords_found}")
        
        # Check if intent matches expectation
        if result.intent_category == test_case['expected_intent']:
            print(f"✅ Intent Classification: CORRECT")
        else:
            print(f"❌ Intent Classification: INCORRECT (Expected: {test_case['expected_intent']})")
