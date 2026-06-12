"""
LUMINA OS - Data Sanitizer & Standardization Module
Enterprise-grade data cleansing and standardization for lead management
"""

import os
import logging
import re
import json
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataQuality(Enum):
    """Data quality levels"""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    INVALID = "invalid"

class PhoneNumberType(Enum):
    """Phone number type classification"""
    MOBILE = "mobile"
    LANDLINE = "landline"
    TOLL_FREE = "toll_free"
    PREMIUM = "premium"
    UNKNOWN = "unknown"

@dataclass
class SanitizationResult:
    """Data sanitization result"""
    original_data: Dict[str, Any]
    sanitized_data: Dict[str, Any]
    quality_score: float
    quality_level: DataQuality
    issues_found: List[str]
    fixes_applied: List[str]
    warnings: List[str]
    processing_time: float
    timestamp: datetime

@dataclass
class PhoneNumberInfo:
    """Phone number analysis result"""
    original: str
    standardized: str
    international: str
    national: str
    type: PhoneNumberType
    country_code: str
    is_valid: bool
    carrier: Optional[str]
    region: Optional[str]

class DataSanitizer:
    """
    Enterprise-grade data sanitization and standardization
    Ensures data quality and consistency across the system
    """
    
    def __init__(self):
        """Initialize data sanitizer"""
        self.logger = logging.getLogger(__name__)
        
        # Phone number patterns
        self.phone_patterns = self._initialize_phone_patterns()
        
        # Email patterns
        self.email_pattern = re.compile(
            r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        )
        
        # Name patterns
        self.name_patterns = self._initialize_name_patterns()
        
        # Address patterns
        self.address_patterns = self._initialize_address_patterns()
        
        # Common data issues
        self.data_issues = self._initialize_data_issues()
        
        self.logger.info("🧹 Data Sanitizer initialized")
        self.logger.info(f"📞 Phone patterns loaded: {len(self.phone_patterns)}")
    
    def _initialize_phone_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Initialize Indonesian phone number patterns"""
        return {
            'indonesia_mobile': {
                'pattern': re.compile(r'^(?:\+62|62|0)?8[1-9][0-9]{6,11}$'),
                'country_code': '62',
                'type': PhoneNumberType.MOBILE,
                'format_international': '+62{number}',
                'format_national': '0{number}'
            },
            'indonesia_landline': {
                'pattern': re.compile(r'^(?:\+62|62|0)?[2-9][0-9]{6,9}$'),
                'country_code': '62',
                'type': PhoneNumberType.LANDLINE,
                'format_international': '+62{number}',
                'format_national': '0{number}'
            },
            'indonesia_toll_free': {
                'pattern': re.compile(r'^(?:\+62|62|0)?800[0-9]{5,7}$'),
                'country_code': '62',
                'type': PhoneNumberType.TOLL_FREE,
                'format_international': '+62{number}',
                'format_national': '0{number}'
            }
        }
    
    def _initialize_name_patterns(self) -> Dict[str, re.Pattern]:
        """Initialize name validation patterns"""
        return {
            'invalid_chars': re.compile(r'[0-9!@#$%^&*()_+=\[\]{};:"\\|,.<>/?]'),
            'multiple_spaces': re.compile(r'\s+'),
            'title_case': re.compile(r'^[A-Z][a-z]+(?:\s[A-Z][a-z]+)*$'),
            'indonesian_prefixes': re.compile(r'^(?:Bapak|Ibu|Saudara|Tn|Ny|Sdr)\s+', re.IGNORECASE)
        }
    
    def _initialize_address_patterns(self) -> Dict[str, re.Pattern]:
        """Initialize address validation patterns"""
        return {
            'street_number': re.compile(r'^[A-Za-z\s]+\s+[0-9]+'),
            'postal_code': re.compile(r'^[0-9]{5}$'),
            'indonesian_province': re.compile(
                r'(?:Aceh|Sumatera|Jawa|Kalimantan|Sulawesi|Bali|Nusa|Papua|Maluku)'
            ),
            'address_separators': re.compile(r'[,\n;]')
        }
    
    def _initialize_data_issues(self) -> Dict[str, Dict[str, Any]]:
        """Initialize common data issue patterns"""
        return {
            'duplicate_spaces': {
                'pattern': re.compile(r'\s+'),
                'fix': ' ',
                'description': 'Multiple spaces'
            },
            'trailing_spaces': {
                'pattern': re.compile(r'\s+$'),
                'fix': '',
                'description': 'Trailing spaces'
            },
            'leading_spaces': {
                'pattern': re.compile(r'^\s+'),
                'fix': '',
                'description': 'Leading spaces'
            },
            'empty_fields': {
                'pattern': re.compile(r'^\s*$'),
                'fix': None,
                'description': 'Empty fields'
            },
            'invalid_emails': {
                'pattern': re.compile(r'^[^@]+@[^@]+\.[^@]+$'),
                'fix': None,
                'description': 'Invalid email format'
            }
        }
    
    async def sanitize_lead_data(self, raw_data: Dict[str, Any]) -> SanitizationResult:
        """
        Sanitize and standardize lead data
        
        Args:
            raw_data: Raw lead data from various sources
            
        Returns:
            SanitizationResult with cleaned data and quality metrics
        """
        try:
            start_time = datetime.now()
            
            sanitized_data = raw_data.copy()
            issues_found = []
            fixes_applied = []
            warnings = []
            
            # Sanitize phone numbers
            if 'phone' in sanitized_data or 'nomorHp' in sanitized_data:
                phone_key = 'phone' if 'phone' in sanitized_data else 'nomorHp'
                phone_result = self._sanitize_phone_number(sanitized_data[phone_key])
                
                if phone_result:
                    sanitized_data[phone_key] = phone_result.standardized
                    sanitized_data[f'{phone_key}_international'] = phone_result.international
                    sanitized_data[f'{phone_key}_type'] = phone_result.type.value
                    
                    if not phone_result.is_valid:
                        issues_found.append(f"Invalid phone number: {phone_result.original}")
                    
                    if phone_result.original != phone_result.standardized:
                        fixes_applied.append(f"Phone standardized: {phone_result.original} → {phone_result.standardized}")
            
            # Sanitize email
            if 'email' in sanitized_data:
                email_result = self._sanitize_email(sanitized_data['email'])
                sanitized_data['email'] = email_result
                
                if not self._is_valid_email(email_result):
                    issues_found.append(f"Invalid email: {sanitized_data['email']}")
            
            # Sanitize name
            if 'name' in sanitized_data or 'nama' in sanitized_data:
                name_key = 'name' if 'name' in sanitized_data else 'nama'
                name_result = self._sanitize_name(sanitized_data[name_key])
                sanitized_data[name_key] = name_result
                
                if sanitized_data[name_key] != raw_data[name_key]:
                    fixes_applied.append(f"Name cleaned: {raw_data[name_key]} → {sanitized_data[name_key]}")
            
            # Sanitize address
            if 'address' in sanitized_data or 'alamat' in sanitized_data:
                address_key = 'address' if 'address' in sanitized_data else 'alamat'
                address_result = self._sanitize_address(sanitized_data[address_key])
                sanitized_data[address_key] = address_result
                
                if sanitized_data[address_key] != raw_data[address_key]:
                    fixes_applied.append(f"Address cleaned: {raw_data[address_key]} → {sanitized_data[address_key]}")
            
            # Sanitize other text fields
            text_fields = ['notes', 'keterangan', 'source', 'sumber']
            for field in text_fields:
                if field in sanitized_data:
                    cleaned_text = self._sanitize_text(sanitized_data[field])
                    if cleaned_text != sanitized_data[field]:
                        sanitized_data[field] = cleaned_text
                        fixes_applied.append(f"Text field cleaned: {field}")
            
            # Calculate quality score
            quality_score = self._calculate_quality_score(raw_data, sanitized_data, issues_found)
            quality_level = self._get_quality_level(quality_score)
            
            # Add metadata
            sanitized_data['sanitized_at'] = datetime.now().isoformat()
            sanitized_data['quality_score'] = quality_score
            sanitized_data['quality_level'] = quality_level.value
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            result = SanitizationResult(
                original_data=raw_data,
                sanitized_data=sanitized_data,
                quality_score=quality_score,
                quality_level=quality_level,
                issues_found=issues_found,
                fixes_applied=fixes_applied,
                warnings=warnings,
                processing_time=processing_time,
                timestamp=datetime.now()
            )
            
            self.logger.info(f"🧹 Data sanitized: Quality {quality_score:.1f} ({quality_level.value})")
            self.logger.info(f"🔧 Fixes applied: {len(fixes_applied)}")
            self.logger.info(f"⚠️ Issues found: {len(issues_found)}")
            
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Data sanitization failed: {e}")
            return SanitizationResult(
                original_data=raw_data,
                sanitized_data=raw_data,
                quality_score=0.0,
                quality_level=DataQuality.INVALID,
                issues_found=[f"Sanitization error: {str(e)}"],
                fixes_applied=[],
                warnings=[],
                processing_time=0.0,
                timestamp=datetime.now()
            )
    
    def _sanitize_phone_number(self, phone: str) -> Optional[PhoneNumberInfo]:
        """Sanitize and standardize phone number"""
        try:
            if not phone:
                return None
            
            # Remove all non-digit characters
            clean_phone = re.sub(r'[^\d+]', '', phone)
            
            # Check Indonesian patterns
            for pattern_name, pattern_info in self.phone_patterns.items():
                pattern = pattern_info['pattern']
                
                # Extract the number part
                match = pattern.match(clean_phone)
                if match:
                    number = match.group(0)
                    
                    # Remove country code and leading zero
                    if number.startswith('+62'):
                        number = number[3:]
                    elif number.startswith('62'):
                        number = number[2:]
                    elif number.startswith('0'):
                        number = number[1:]
                    
                    # Create standardized formats
                    international = pattern_info['format_international'].format(number=number)
                    national = pattern_info['format_national'].format(number=number)
                    standardized = international  # Use international as standard
                    
                    return PhoneNumberInfo(
                        original=phone,
                        standardized=standardized,
                        international=international,
                        national=national,
                        type=pattern_info['type'],
                        country_code=pattern_info['country_code'],
                        is_valid=True,
                        carrier=None,  # Could be enhanced with carrier lookup
                        region=None     # Could be enhanced with region lookup
                    )
            
            # If no pattern matches, return invalid
            return PhoneNumberInfo(
                original=phone,
                standardized=phone,
                international=phone,
                national=phone,
                type=PhoneNumberType.UNKNOWN,
                country_code='62',
                is_valid=False,
                carrier=None,
                region=None
            )
            
        except Exception as e:
            self.logger.error(f"❌ Phone sanitization failed: {e}")
            return None
    
    def _sanitize_email(self, email: str) -> str:
        """Sanitize email address"""
        try:
            if not email:
                return ""
            
            # Convert to lowercase
            email = email.lower().strip()
            
            # Remove invalid characters
            email = re.sub(r'[^\w.@-]', '', email)
            
            return email
            
        except Exception as e:
            self.logger.error(f"❌ Email sanitization failed: {e}")
            return ""
    
    def _sanitize_name(self, name: str) -> str:
        """Sanitize person name"""
        try:
            if not name:
                return ""
            
            # Remove Indonesian prefixes
            name = self.name_patterns['indonesian_prefixes'].sub('', name)
            
            # Remove invalid characters
            name = self.name_patterns['invalid_chars'].sub('', name)
            
            # Normalize spaces
            name = self.name_patterns['multiple_spaces'].sub(' ', name)
            
            # Remove leading/trailing spaces
            name = name.strip()
            
            # Title case
            name = name.title()
            
            return name
            
        except Exception as e:
            self.logger.error(f"❌ Name sanitization failed: {e}")
            return name
    
    def _sanitize_address(self, address: str) -> str:
        """Sanitize address"""
        try:
            if not address:
                return ""
            
            # Normalize separators
            address = self.address_patterns['address_separators'].sub(', ', address)
            
            # Remove multiple spaces
            address = re.sub(r'\s+', ' ', address)
            
            # Title case
            address = address.title()
            
            # Remove leading/trailing spaces and commas
            address = address.strip(' ,')
            
            return address
            
        except Exception as e:
            self.logger.error(f"❌ Address sanitization failed: {e}")
            return address
    
    def _sanitize_text(self, text: str) -> str:
        """Sanitize general text fields"""
        try:
            if not text:
                return ""
            
            # Remove multiple spaces
            text = re.sub(r'\s+', ' ', text)
            
            # Remove leading/trailing spaces
            text = text.strip()
            
            return text
            
        except Exception as e:
            self.logger.error(f"❌ Text sanitization failed: {e}")
            return text
    
    def _is_valid_email(self, email: str) -> bool:
        """Check if email is valid"""
        try:
            if not email:
                return False
            return bool(self.email_pattern.match(email))
        except:
            return False
    
    def _calculate_quality_score(self, original: Dict[str, Any], 
                               sanitized: Dict[str, Any], 
                               issues: List[str]) -> float:
        """Calculate data quality score"""
        try:
            score = 100.0
            
            # Deduct points for issues
            score -= len(issues) * 10
            
            # Deduct points for missing required fields
            required_fields = ['phone', 'nomorHp', 'email', 'name', 'nama']
            missing_required = sum(1 for field in required_fields 
                                 if field not in original or not original[field])
            score -= missing_required * 5
            
            # Bonus for complete data
            if len(issues) == 0 and missing_required == 0:
                score += 10
            
            # Ensure score is within bounds
            score = max(0, min(100, score))
            
            return score
            
        except Exception as e:
            self.logger.error(f"❌ Quality score calculation failed: {e}")
            return 0.0
    
    def _get_quality_level(self, score: float) -> DataQuality:
        """Get quality level from score"""
        if score >= 90:
            return DataQuality.EXCELLENT
        elif score >= 75:
            return DataQuality.GOOD
        elif score >= 60:
            return DataQuality.FAIR
        elif score >= 40:
            return DataQuality.POOR
        else:
            return DataQuality.INVALID
    
    def get_sanitization_stats(self, results: List[SanitizationResult]) -> Dict[str, Any]:
        """Get sanitization statistics"""
        try:
            if not results:
                return {}
            
            total = len(results)
            quality_counts = {}
            issue_counts = {}
            fix_counts = {}
            
            for result in results:
                # Quality distribution
                quality = result.quality_level.value
                quality_counts[quality] = quality_counts.get(quality, 0) + 1
                
                # Issue analysis
                for issue in result.issues_found:
                    issue_type = issue.split(':')[0] if ':' in issue else 'general'
                    issue_counts[issue_type] = issue_counts.get(issue_type, 0) + 1
                
                # Fix analysis
                for fix in result.fixes_applied:
                    fix_type = fix.split(':')[0] if ':' in fix else 'general'
                    fix_counts[fix_type] = fix_counts.get(fix_type, 0) + 1
            
            avg_quality = sum(r.quality_score for r in results) / total
            avg_processing_time = sum(r.processing_time for r in results) / total
            
            return {
                'total_processed': total,
                'average_quality_score': avg_quality,
                'average_processing_time': avg_processing_time,
                'quality_distribution': quality_counts,
                'common_issues': issue_counts,
                'common_fixes': fix_counts
            }
            
        except Exception as e:
            self.logger.error(f"❌ Sanitization stats failed: {e}")
            return {}

# Global data sanitizer instance
data_sanitizer = DataSanitizer()
