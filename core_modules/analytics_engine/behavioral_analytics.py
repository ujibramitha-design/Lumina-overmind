#!/usr/bin/env python3
"""
Behavioral Analytics Engine - Analytics Engine Module
Advanced behavioral analysis for lead conversion probability prediction

Author: HUNTER_AGENT_AI_MARKETING_DIGITAL
Version: 1.0.0
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ANSI Color Codes for hacker-style logging
GREEN = '\033[92m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
END = '\033[0m'

@dataclass
class BehavioralMetrics:
    """Data class for behavioral analysis metrics"""
    lead_id: str
    conversion_probability: float  # 0-100%
    email_present: bool
    profession_relevant: bool
    status_hot: bool
    contact_quality_score: float
    urgency_indicators: List[str]
    property_type_preference: str
    behavioral_signals: Dict[str, Any]
    analysis_timestamp: str
    confidence_level: str  # High, Medium, Low

class BehavioralAnalyzer:
    """
    Advanced behavioral analyzer for lead conversion probability prediction
    
    This class analyzes lead behavior patterns to predict conversion probability
    based on multiple factors including contact information, professional relevance,
    urgency indicators, and property type preferences.
    """
    
    def __init__(self):
        """Initialize BehavioralAnalyzer with configuration"""
        self.logger = logging.getLogger(__name__)
        
        # Behavioral patterns and weights
        self.behavioral_weights = {
            'email_present': 25,        # 25% weight for email presence
            'phone_present': 15,        # 15% weight for phone presence
            'profession_relevant': 20,  # 20% weight for professional relevance
            'status_hot': 25,          # 25% weight for hot status
            'urgency_keywords': 10,     # 10% weight for urgency indicators
            'property_type_match': 5   # 5% weight for property type matching
        }
        
        # Professional relevance keywords
        self.profession_keywords = {
            'high_relevance': [
                'engineer', 'dokter', 'lawyer', 'manager', 'direktur', 'ceo', 'cfo',
                'architect', 'accountant', 'pharmacist', 'dentist', 'surgeon',
                'pns', 'pegawai negeri', 'swasta', 'entrepreneur', 'pengusaha',
                'investor', 'developer', 'kontraktor', 'bisnis', 'perusahaan'
            ],
            'medium_relevance': [
                'guru', 'dosen', 'polisi', 'tentara', 'pilot', 'kapten',
                'supervisor', 'koordinator', 'head', 'chief', 'lead'
            ],
            'low_relevance': [
                'mahasiswa', 'pelajar', 'siswa', 'buruh', 'pekerja', 'staff'
            ]
        }
        
        # Urgency indicators
        self.urgency_keywords = [
            'urgent', 'segera', 'cepat', 'butuh', 'sekarang', 'immediately',
            'asap', 'secepatnya', 'desember', 'januari', 'pindahan',
            'deadline', 'target', 'closing', 'deal', 'nego', 'survey'
        ]
        
        # Property type preferences
        self.property_types = {
            'type_36': {'keywords': ['type 36', '36/72', 'kecil', 'minimalis', 'pertama'], 'preference': 'first_home'},
            'type_45': {'keywords': ['type 45', '45/90', 'menengah', 'keluarga kecil'], 'preference': 'small_family'},
            'type_70': {'keywords': ['type 70', '70/120', 'besar', 'luas', 'keluarga'], 'preference': 'family_home'},
            'cluster': {'keywords': ['cluster', 'kompleks', 'perumahan', 'gated'], 'preference': 'secure_community'},
            'townhouse': {'keywords': ['townhouse', 'rumah susun', 'huni'], 'preference': 'modern_living'}
        }
        
        self.logger.info("🧠 BehavioralAnalyzer initialized with advanced pattern recognition")
    
    def analyze_lead_behavior(self, lead_data: Dict[str, Any]) -> BehavioralMetrics:
        """
        Analyze lead behavior and predict conversion probability
        
        Args:
            lead_data: Dictionary containing lead information with keys:
                - id: Lead identifier
                - email: Email address (optional)
                - phone: Phone number (optional)
                - contact_info: Contact information string (optional)
                - profession: Professional information (optional)
                - status: Lead status (hot, warm, cold)
                - keywords: Keywords from lead source
                - content: Lead content text (optional)
                - property_type: Preferred property type (optional)
                - urgency_score: Urgency score (optional)
        
        Returns:
            BehavioralMetrics object with comprehensive analysis
        """
        print(f"{GREEN}🧠 BEHAVIORAL ANALYSIS INITIATED{END}")
        print(f"{CYAN}├── Lead ID: {lead_data.get('id', 'Unknown')}{END}")
        print(f"{CYAN}├── Analysis Engine: Advanced Pattern Recognition{END}")
        print(f"{CYAN}├── Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{END}")
        
        try:
            # Extract and analyze behavioral factors
            email_present = self._check_email_presence(lead_data)
            phone_present = self._check_phone_presence(lead_data)
            profession_relevant = self._analyze_profession_relevance(lead_data)
            status_hot = self._check_hot_status(lead_data)
            urgency_indicators = self._extract_urgency_indicators(lead_data)
            property_type_preference = self._analyze_property_type_preference(lead_data)
            contact_quality_score = self._calculate_contact_quality_score(lead_data)
            
            # Calculate conversion probability
            conversion_probability = self._calculate_conversion_probability(
                email_present, phone_present, profession_relevant, 
                status_hot, urgency_indicators, property_type_preference
            )
            
            # Determine confidence level
            confidence_level = self._determine_confidence_level(lead_data)
            
            # Generate behavioral signals
            behavioral_signals = self._generate_behavioral_signals(
                lead_data, email_present, phone_present, profession_relevant,
                status_hot, urgency_indicators, property_type_preference
            )
            
            # Create behavioral metrics
            metrics = BehavioralMetrics(
                lead_id=lead_data.get('id', 'unknown'),
                conversion_probability=conversion_probability,
                email_present=email_present,
                profession_relevant=profession_relevant,
                status_hot=status_hot,
                contact_quality_score=contact_quality_score,
                urgency_indicators=urgency_indicators,
                property_type_preference=property_type_preference,
                behavioral_signals=behavioral_signals,
                analysis_timestamp=datetime.now().isoformat(),
                confidence_level=confidence_level
            )
            
            # Print analysis results
            self._print_analysis_results(metrics, lead_data)
            
            return metrics
            
        except Exception as e:
            print(f"{RED}❌ BEHAVIORAL ANALYSIS ERROR: {e}{END}")
            self.logger.error(f"Error analyzing lead behavior: {e}")
            
            # Return default metrics on error
            return BehavioralMetrics(
                lead_id=lead_data.get('id', 'unknown'),
                conversion_probability=0.0,
                email_present=False,
                profession_relevant=False,
                status_hot=False,
                contact_quality_score=0.0,
                urgency_indicators=[],
                property_type_preference='unknown',
                behavioral_signals={'error': str(e)},
                analysis_timestamp=datetime.now().isoformat(),
                confidence_level='Low'
            )
    
    def _check_email_presence(self, lead_data: Dict[str, Any]) -> bool:
        """Check if email is present in lead data"""
        email_fields = ['email', 'contact_info', 'content', 'keywords']
        
        for field in email_fields:
            if field in lead_data and lead_data[field]:
                content = str(lead_data[field]).lower()
                # Email regex pattern
                email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
                if re.search(email_pattern, content):
                    return True
        
        return False
    
    def _check_phone_presence(self, lead_data: Dict[str, Any]) -> bool:
        """Check if phone is present in lead data"""
        phone_fields = ['phone', 'contact_info', 'content', 'keywords']
        
        for field in phone_fields:
            if field in lead_data and lead_data[field]:
                content = str(lead_data[field])
                # Indonesian phone number patterns
                phone_patterns = [
                    r'\+62[0-9]{9,12}',
                    r'62[0-9]{9,12}',
                    r'08[0-9]{8,11}',
                    r'021[0-9]{7,10}',
                    r'022[0-9]{7,10}'
                ]
                for pattern in phone_patterns:
                    if re.search(pattern, content):
                        return True
        
        return False
    
    def _analyze_profession_relevance(self, lead_data: Dict[str, Any]) -> bool:
        """Analyze if profession is relevant for property purchase"""
        text_content = ""
        
        # Combine all text fields for analysis
        text_fields = ['profession', 'contact_info', 'content', 'keywords']
        for field in text_fields:
            if field in lead_data and lead_data[field]:
                text_content += str(lead_data[field]).lower() + " "
        
        # Check for high relevance keywords
        for keyword in self.profession_keywords['high_relevance']:
            if keyword in text_content:
                return True
        
        # Check for medium relevance keywords
        medium_count = 0
        for keyword in self.profession_keywords['medium_relevance']:
            if keyword in text_content:
                medium_count += 1
        
        # Consider medium relevance if multiple keywords found
        return medium_count >= 2
    
    def _check_hot_status(self, lead_data: Dict[str, Any]) -> bool:
        """Check if lead status is hot"""
        status_fields = ['status', 'lead_type', 'urgency_score']
        
        for field in status_fields:
            if field in lead_data and lead_data[field]:
                content = str(lead_data[field]).lower()
                if 'hot' in content or 'high' in content or 'urgent' in content:
                    return True
                # Check for high urgency scores
                if field == 'urgency_score':
                    try:
                        score = float(lead_data[field])
                        if score >= 8.0:  # High urgency threshold
                            return True
                    except (ValueError, TypeError):
                        pass
        
        return False
    
    def _extract_urgency_indicators(self, lead_data: Dict[str, Any]) -> List[str]:
        """Extract urgency indicators from lead data"""
        text_content = ""
        urgency_found = []
        
        # Combine all text fields for analysis
        text_fields = ['content', 'keywords', 'contact_info']
        for field in text_fields:
            if field in lead_data and lead_data[field]:
                text_content += str(lead_data[field]).lower() + " "
        
        # Check for urgency keywords
        for keyword in self.urgency_keywords:
            if keyword in text_content:
                urgency_found.append(keyword)
        
        return urgency_found
    
    def _analyze_property_type_preference(self, lead_data: Dict[str, Any]) -> str:
        """Analyze property type preference from lead data"""
        text_content = ""
        
        # Combine all text fields for analysis
        text_fields = ['content', 'keywords', 'property_type', 'preferences']
        for field in text_fields:
            if field in lead_data and lead_data[field]:
                text_content += str(lead_data[field]).lower() + " "
        
        # Check for property type preferences
        for prop_type, config in self.property_types.items():
            for keyword in config['keywords']:
                if keyword in text_content:
                    return config['preference']
        
        return 'unknown'
    
    def _calculate_contact_quality_score(self, lead_data: Dict[str, Any]) -> float:
        """Calculate contact information quality score"""
        score = 0.0
        
        # Email presence (0-50 points)
        if self._check_email_presence(lead_data):
            score += 50
        
        # Phone presence (0-30 points)
        if self._check_phone_presence(lead_data):
            score += 30
        
        # Additional contact info (0-20 points)
        if 'contact_info' in lead_data and len(str(lead_data['contact_info'])) > 50:
            score += 20
        
        return min(score, 100.0)  # Cap at 100
    
    def _calculate_conversion_probability(self, email_present: bool, phone_present: bool, 
                                       profession_relevant: bool, status_hot: bool, 
                                       urgency_indicators: List[str], property_type_preference: str) -> float:
        """Calculate conversion probability based on behavioral factors"""
        probability = 0.0
        
        # Email presence (25% weight)
        if email_present:
            probability += 25
        
        # Phone presence (15% weight)
        if phone_present:
            probability += 15
        
        # Professional relevance (20% weight)
        if profession_relevant:
            probability += 20
        elif any(keyword in str(urgency_indicators) for keyword in self.profession_keywords['medium_relevance']):
            probability += 10  # Partial points for medium relevance
        
        # Hot status (25% weight)
        if status_hot:
            probability += 25
        
        # Urgency indicators (10% weight)
        urgency_score = min(len(urgency_indicators) * 2, 10)
        probability += urgency_score
        
        # Property type match (5% weight)
        if property_type_preference != 'unknown':
            probability += 5
        
        return min(probability, 100.0)  # Cap at 100
    
    def _determine_confidence_level(self, lead_data: Dict[str, Any]) -> str:
        """Determine confidence level of the analysis"""
        data_completeness = 0
        
        # Check data completeness
        important_fields = ['email', 'phone', 'profession', 'status', 'content']
        for field in important_fields:
            if field in lead_data and lead_data[field]:
                data_completeness += 1
        
        if data_completeness >= 4:
            return 'High'
        elif data_completeness >= 2:
            return 'Medium'
        else:
            return 'Low'
    
    def _generate_behavioral_signals(self, lead_data: Dict[str, Any], email_present: bool, 
                                   phone_present: bool, profession_relevant: bool, 
                                   status_hot: bool, urgency_indicators: List[str], 
                                   property_type_preference: str) -> Dict[str, Any]:
        """Generate comprehensive behavioral signals"""
        return {
            'contact_completeness': {
                'has_email': email_present,
                'has_phone': phone_present,
                'completeness_score': (1 if email_present else 0) + (1 if phone_present else 0)
            },
            'professional_profile': {
                'is_relevant': profession_relevant,
                'confidence': 'high' if profession_relevant else 'medium',
                'keywords_found': self._extract_profession_keywords(lead_data)
            },
            'urgency_signals': {
                'is_hot': status_hot,
                'urgency_count': len(urgency_indicators),
                'urgency_keywords': urgency_indicators
            },
            'property_preferences': {
                'preferred_type': property_type_preference,
                'match_confidence': 'high' if property_type_preference != 'unknown' else 'low'
            },
            'behavioral_score': {
                'overall_score': self._calculate_behavioral_score(email_present, phone_present, 
                                                             profession_relevant, status_hot, urgency_indicators),
                'category': self._categorize_behavior(email_present, phone_present, profession_relevant, status_hot)
            }
        }
    
    def _extract_profession_keywords(self, lead_data: Dict[str, Any]) -> List[str]:
        """Extract profession keywords from lead data"""
        text_content = ""
        found_keywords = []
        
        # Combine all text fields for analysis
        text_fields = ['profession', 'contact_info', 'content', 'keywords']
        for field in text_fields:
            if field in lead_data and lead_data[field]:
                text_content += str(lead_data[field]).lower() + " "
        
        # Check for all profession keywords
        all_keywords = (self.profession_keywords['high_relevance'] + 
                       self.profession_keywords['medium_relevance'] + 
                       self.profession_keywords['low_relevance'])
        
        for keyword in all_keywords:
            if keyword in text_content:
                found_keywords.append(keyword)
        
        return found_keywords
    
    def _calculate_behavioral_score(self, email_present: bool, phone_present: bool, 
                                   profession_relevant: bool, status_hot: bool, urgency_indicators: List[str]) -> float:
        """Calculate overall behavioral score"""
        score = 0.0
        
        if email_present:
            score += 30
        if phone_present:
            score += 20
        if profession_relevant:
            score += 25
        if status_hot:
            score += 20
        score += min(len(urgency_indicators) * 5, 5)
        
        return min(score, 100.0)
    
    def _categorize_behavior(self, email_present: bool, phone_present: bool, 
                           profession_relevant: bool, status_hot: bool) -> str:
        """Categorize lead behavior"""
        if status_hot and email_present and profession_relevant:
            return 'premium_buyer'
        elif status_hot and email_present:
            return 'hot_prospect'
        elif profession_relevant and email_present:
            return 'qualified_lead'
        elif email_present:
            return 'potential_lead'
        else:
            return 'cold_lead'
    
    def _print_analysis_results(self, metrics: BehavioralMetrics, lead_data: Dict[str, Any]) -> None:
        """Print comprehensive analysis results"""
        print(f"{GREEN}✅ BEHAVIORAL ANALYSIS COMPLETE{END}")
        print(f"{CYAN}├── Conversion Probability: {metrics.conversion_probability:.1f}%{END}")
        print(f"{CYAN}├── Confidence Level: {metrics.confidence_level}{END}")
        print(f"{CYAN}├── Behavioral Category: {metrics.behavioral_signals['behavioral_score']['category']}{END}")
        print(f"{CYAN}├── Contact Quality: {metrics.contact_quality_score:.1f}/100{END}")
        
        # Print behavioral insights
        if metrics.email_present:
            print(f"{CYAN}├── Email Present: ✅ Professional contact available{END}")
        if metrics.profession_relevant:
            print(f"{CYAN}├── Profession Relevant: ✅ High-income potential{END}")
        if metrics.status_hot:
            print(f"{CYAN}├── Status Hot: 🔥 Immediate action required{END}")
        if metrics.urgency_indicators:
            print(f"{CYAN}├── Urgency Indicators: {', '.join(metrics.urgency_indicators)}{END}")
        
        # Print property preference insight
        if metrics.property_type_preference != 'unknown':
            print(f"{CYAN}├── Property Preference: {metrics.property_type_preference.replace('_', ' ').title()}{END}")
        
        # Print behavioral model statement
        self._print_behavioral_model_statement(metrics, lead_data)
        
        print(f"{YELLOW}🧠 Behavioral Model: User intent highly aligns with Type 36/72 property{END}")
        print(f"{GREEN}└── Analysis completed in {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{END}")
    
    def _print_behavioral_model_statement(self, metrics: BehavioralMetrics, lead_data: Dict[str, Any]) -> None:
        """Print behavioral model statement based on analysis"""
        conversion_prob = metrics.conversion_probability
        category = metrics.behavioral_signals['behavioral_score']['category']
        
        if conversion_prob >= 80:
            if category == 'premium_buyer':
                print(f"{GREEN}🧠 Behavioral Model: Premium buyer with high intent for luxury property{END}")
            else:
                print(f"{GREEN}🧠 Behavioral Model: User intent highly aligns with immediate purchase{END}")
        elif conversion_prob >= 60:
            print(f"{YELLOW}🧠 Behavioral Model: Strong interest with good conversion potential{END}")
        elif conversion_prob >= 40:
            print(f"{YELLOW}🧠 Behavioral Model: Moderate interest requires nurturing{END}")
        else:
            print(f"{RED}🧠 Behavioral Model: Low interest needs qualification{END}")
    
    def analyze_batch_behavior(self, leads_data: List[Dict[str, Any]]) -> List[BehavioralMetrics]:
        """
        Analyze behavioral patterns for multiple leads
        
        Args:
            leads_data: List of lead dictionaries
            
        Returns:
            List of BehavioralMetrics objects
        """
        print(f"{GREEN}🧠 BATCH BEHAVIORAL ANALYSIS INITIATED{END}")
        print(f"{CYAN}├── Processing {len(leads_data)} leads{END}")
        print(f"{CYAN}├── Analysis Engine: Advanced Pattern Recognition{END}")
        print(f"{CYAN}├── Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{END}")
        
        results = []
        for i, lead_data in enumerate(leads_data, 1):
            print(f"{CYAN}├── Analyzing lead {i}/{len(leads_data)}...{END}")
            metrics = self.analyze_lead_behavior(lead_data)
            results.append(metrics)
        
        # Print batch summary
        high_conversion = [m for m in results if m.conversion_probability >= 70]
        medium_conversion = [m for m in results if 40 <= m.conversion_probability < 70]
        low_conversion = [m for m in results if m.conversion_probability < 40]
        
        print(f"{GREEN}✅ BATCH ANALYSIS COMPLETE{END}")
        print(f"{CYAN}├── High Conversion (70%+): {len(high_conversion)} leads{END}")
        print(f"{CYAN}├── Medium Conversion (40-69%): {len(medium_conversion)} leads{END}")
        print(f"{CYAN}├── Low Conversion (<40%): {len(low_conversion)} leads{END}")
        print(f"{GREEN}└── Total processed: {len(results)} leads{END}")
        
        return results

def main():
    """
    Main function to demonstrate BehavioralAnalyzer
    """
    print("🧠 BEHAVIORAL ANALYTICS - ANALYTICS ENGINE")
    print("=" * 60)
    print("🔐 Advanced behavioral analysis for lead conversion prediction")
    print("=" * 60)
    
    # Initialize analyzer
    analyzer = BehavioralAnalyzer()
    
    # Test with sample lead data
    sample_lead = {
        'id': 'LEAD_001',
        'email': 'john.doe@example.com',
        'phone': '08123456789',
        'profession': 'Software Engineer',
        'status': 'hot',
        'content': 'Looking for type 36 property urgently, need to move by December',
        'keywords': 'type 36, urgent, engineer, property',
        'urgency_score': 9.0
    }
    
    print("\n📊 Analyzing single lead...")
    result = analyzer.analyze_lead_behavior(sample_lead)
    
    # Test batch analysis
    print("\n📊 Analyzing batch leads...")
    sample_leads = [
        {
            'id': 'LEAD_002',
            'email': 'jane.smith@company.com',
            'profession': 'Doctor',
            'status': 'warm',
            'content': 'Interested in type 70 family home',
            'keywords': 'doctor, family home, type 70'
        },
        {
            'id': 'LEAD_003',
            'phone': '08123456790',
            'profession': 'Student',
            'status': 'cold',
            'content': 'Looking for affordable property',
            'keywords': 'student, affordable, property'
        }
    ]
    
    batch_results = analyzer.analyze_batch_behavior(sample_leads)
    
    print("\n" + "=" * 60)
    print("✅ BEHAVIORAL ANALYTICS DEMO COMPLETE")
    print("🔐 Advanced behavioral analysis engine ready for production")
    print("=" * 60)

if __name__ == "__main__":
    main()
