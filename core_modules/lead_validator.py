"""
Lead Validator Module
Automatic lead quality validation system untuk filtering dan gatekeeping
"""

import re
import json
import logging
from typing import Dict, Optional, Tuple
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Try to import Twilio for WhatsApp validation
try:
    from twilio.rest import Client
    from twilio.base.exceptions import TwilioRestException
    TWILIO_AVAILABLE = True
except ImportError:
    TWILIO_AVAILABLE = False

class LeadValidator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Indonesian phone number patterns
        self.phone_patterns = {
            'mobile': [
                r'^\+62[0-9]{9,12}$',  # +62xxxxxxxxx (10-13 digits)
                r'^62[0-9]{9,12}$',   # 62xxxxxxxxx (10-13 digits)
                r'^08[0-9]{8,11}$',   # 08xxxxxxxxx (9-12 digits)
            ],
            'landline': [
                r'^021[0-9]{7,10}$',  # 021xxxxxxx (8-11 digits)
                r'^022[0-9]{7,10}$',  # 022xxxxxxx (8-11 digits)
                r'^023[0-9]{7,10}$',  # 023xxxxxxx (8-11 digits)
                r'^024[0-9]{7,10}$',  # 024xxxxxxx (8-11 digits)
            ],
            'special': [
                r'^0800[0-9]{7}$',    # 0800xxxxx (7 digits)
                r'^0807[0-9]{7}$',    # 0807xxxxx (7 digits)
                r'^0808[0-9]{7}$',    # 0808xxxxx (7 digits)
                r'^0809[0-9]{7}$',    # 0809xxxxx (7 digits)
            ]
        }
        
        # WhatsApp validation configuration
        self.twilio_client = None
        self.use_whatsapp_validation = False
        
        # Initialize Twilio if available
        if TWILIO_AVAILABLE and os.getenv('TWILIO_ACCOUNT_SID') and os.getenv('TWILIO_AUTH_TOKEN'):
            try:
                self.twilio_client = Client(
                    os.getenv('TWILIO_ACCOUNT_SID'),
                    os.getenv('TWILIO_AUTH_TOKEN')
                )
                self.use_whatsapp_validation = True
                self.logger.info("Twilio client initialized for WhatsApp validation")
            except Exception as e:
                self.logger.error(f"Failed to initialize Twilio client: {e}")
                self.use_whatsapp_validation = False
        else:
            self.logger.warning("Twilio not available. WhatsApp validation disabled")
            self.use_whatsapp_validation = False
        
        # Validation thresholds
        self.validation_thresholds = {
            'min_score_for_validation': 8,
            'phone_format_required': True,
            'whatsapp_check_enabled': True
        }
    
    def validate_phone(self, phone_number: str) -> Dict:
        """
        Validate Indonesian phone number format
        
        Args:
            phone_number: Phone number to validate
            
        Returns:
            Dict with validation results
        """
        try:
            self.logger.info(f"Validating phone number: {phone_number}")
            
            # Clean phone number
            cleaned_phone = self._clean_phone_number(phone_number)
            
            if not cleaned_phone:
                return {
                    'status': 'invalid_format',
                    'phone_number': phone_number,
                    'cleaned_phone': '',
                    'phone_type': 'unknown',
                    'is_valid': False,
                    'validation_timestamp': datetime.now().isoformat(),
                    'error': 'Empty or invalid phone number'
                }
            
            # Check format patterns
            phone_type = self._determine_phone_type(cleaned_phone)
            
            if phone_type == 'invalid':
                return {
                    'status': 'invalid_format',
                    'phone_number': phone_number,
                    'cleaned_phone': cleaned_phone,
                    'phone_type': 'invalid',
                    'is_valid': False,
                    'validation_timestamp': datetime.now().isoformat(),
                    'error': 'Invalid Indonesian phone format'
                }
            
            # Additional validation checks
            validation_result = self._additional_validation_checks(cleaned_phone, phone_type)
            
            result = {
                'status': 'valid',
                'phone_number': phone_number,
                'cleaned_phone': cleaned_phone,
                'phone_type': phone_type,
                'is_valid': True,
                'validation_timestamp': datetime.now().isoformat(),
                'validation_details': validation_result
            }
            
            self.logger.info(f"Phone validation successful: {phone_type} - {cleaned_phone}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error validating phone number: {e}")
            return {
                'status': 'error',
                'phone_number': phone_number,
                'cleaned_phone': '',
                'phone_type': 'unknown',
                'is_valid': False,
                'validation_timestamp': datetime.now().isoformat(),
                'error': str(e)
            }
    
    def _clean_phone_number(self, phone_number: str) -> str:
        """
        Clean and normalize phone number
        """
        try:
            if not phone_number:
                return ''
            
            # Remove common formatting characters
            cleaned = re.sub(r'[^\d+]', '', phone_number)
            
            # Remove leading zeros for mobile numbers (except for special numbers)
            if cleaned.startswith('62') and len(cleaned) > 12:
                cleaned = cleaned.lstrip('0')
            elif cleaned.startswith('08') and len(cleaned) > 11:
                cleaned = cleaned.lstrip('0')
            
            # Add country code if missing
            if cleaned.startswith('8') and len(cleaned) >= 9:
                cleaned = '62' + cleaned
            elif cleaned.startswith('0') and not cleaned.startswith('62') and len(cleaned) >= 8:
                cleaned = '62' + cleaned
            
            return cleaned
            
        except Exception as e:
            self.logger.error(f"Error cleaning phone number: {e}")
            return ''
    
    def _determine_phone_type(self, phone_number: str) -> str:
        """
        Determine phone type based on patterns
        """
        try:
            for phone_type, patterns in self.phone_patterns.items():
                for pattern in patterns:
                    if re.match(pattern, phone_number):
                        return phone_type
            
            return 'invalid'
            
        except Exception as e:
            self.logger.error(f"Error determining phone type: {e}")
            return 'invalid'
    
    def _additional_validation_checks(self, phone_number: str, phone_type: str) -> Dict:
        """
        Additional validation checks
        """
        try:
            checks = {
                'length_check': self._check_phone_length(phone_number, phone_type),
                'prefix_check': self._check_phone_prefix(phone_number),
                'format_consistency': self._check_format_consistency(phone_number)
            }
            
            # Determine overall validation quality
            all_passed = all(check.get('passed', False) for check in checks.values())
            
            return {
                'checks': checks,
                'overall_quality': 'excellent' if all_passed else 'acceptable',
                'recommendations': self._get_validation_recommendations(checks)
            }
            
        except Exception as e:
            self.logger.error(f"Error in additional validation checks: {e}")
            return {
                'checks': {},
                'overall_quality': 'unknown',
                'recommendations': []
            }
    
    def _check_phone_length(self, phone_number: str, phone_type: str) -> Dict:
        """
        Check phone number length
        """
        try:
            length = len(phone_number)
            
            if phone_type == 'mobile':
                if 10 <= length <= 13:
                    return {'passed': True, 'message': 'Valid mobile number length'}
                else:
                    return {'passed': False, 'message': f'Invalid mobile number length: {length}'}
            elif phone_type == 'landline':
                if 8 <= length <= 11:
                    return {'passed': True, 'message': 'Valid landline number length'}
                else:
                    return {'passed': False, 'message': f'Invalid landline number length: {length}'}
            elif phone_type == 'special':
                if length == 7:
                    return {'passed': True, 'message': 'Valid special number length'}
                else:
                    return {'passed': False, 'message': f'Invalid special number length: {length}'}
            else:
                return {'passed': False, 'message': 'Unknown phone type for length check'}
                
        except Exception as e:
            self.logger.error(f"Error checking phone length: {e}")
            return {'passed': False, 'message': str(e)}
    
    def _check_phone_prefix(self, phone_number: str) -> Dict:
        """
        Check phone number prefix
        """
        try:
            # Check for valid Indonesian prefixes
            valid_prefixes = ['62', '08', '021', '022', '023', '024', '0800', '0807', '0808', '0809']
            
            for prefix in valid_prefixes:
                if phone_number.startswith(prefix):
                    return {'passed': True, 'message': f'Valid Indonesian prefix: {prefix}'}
            
            return {'passed': False, 'message': 'Invalid Indonesian prefix'}
            
        except Exception as e:
            self.logger.error(f"Error checking phone prefix: {e}")
            return {'passed': False, 'message': str(e)}
    
    def _check_format_consistency(self, phone_number: str) -> Dict:
        """
        Check format consistency
        """
        try:
            # Check for common formatting issues
            issues = []
            
            if phone_number.count(' ') > 0:
                issues.append('Contains spaces')
            
            if phone_number.count('-') > 0:
                issues.append('Contains hyphens')
            
            if phone_number.count('(') > 0 or phone_number.count(')') > 0:
                issues.append('Contains parentheses')
            
            if phone_number.count('+') > 1:
                issues.append('Multiple plus signs')
            
            if issues:
                return {'passed': False, 'message': f'Format issues: {", ".join(issues)}'}
            else:
                return {'passed': True, 'message': 'Format consistency good'}
                
        except Exception as e:
            self.logger.error(f"Error checking format consistency: {e}")
            return {'passed': False, 'message': str(e)}
    
    def _get_validation_recommendations(self, checks: Dict) -> list:
        """
        Get validation recommendations based on failed checks
        """
        try:
            recommendations = []
            
            for check_name, check_result in checks.items():
                if not check_result.get('passed', False):
                    if check_name == 'length_check':
                        recommendations.append("Verify phone number length for Indonesian standards")
                    elif check_name == 'prefix_check':
                        recommendations.append("Ensure valid Indonesian area code prefix")
                    elif check_name == 'format_consistency':
                        recommendations.append("Remove spaces, hyphens, and extra characters")
            
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Error getting validation recommendations: {e}")
            return []
    
    def check_whatsapp_existence(self, phone_number: str) -> Dict:
        """
        Check WhatsApp existence using Twilio Lookup API
        
        Args:
            phone_number: Phone number to check (cleaned format)
            
        Returns:
            Dict with WhatsApp existence results
        """
        try:
            self.logger.info(f"Checking WhatsApp existence for: {phone_number}")
            
            if not self.use_whatsapp_validation:
                return {
                    'status': 'unavailable',
                    'phone_number': phone_number,
                    'whatsapp_status': 'unknown',
                    'is_active': None,
                    'check_timestamp': datetime.now().isoformat(),
                    'message': 'WhatsApp validation not available'
                }
            
            # Ensure phone number is in E.164 format
            if not phone_number.startswith('+'):
                if phone_number.startswith('62'):
                    phone_number = '+' + phone_number
                else:
                    phone_number = '+62' + phone_number.lstrip('0')
            
            try:
                # Use Twilio Lookup API
                lookup = self.twilio_client.lookups.v2.phone_numbers(phone_number).fetch()
                
                if lookup:
                    whatsapp_status = lookup.get('carrier', {}).get('name', 'unknown')
                    is_active = lookup.get('carrier', {}).get('type') == 'mobile'
                    
                    result = {
                        'status': 'success',
                        'phone_number': phone_number,
                        'whatsapp_status': whatsapp_status,
                        'is_active': is_active,
                        'check_timestamp': datetime.now().isoformat(),
                        'lookup_data': {
                            'carrier': lookup.get('carrier', {}),
                            'country_code': lookup.get('country_code', ''),
                            'national_format': lookup.get('national_format', '')
                        }
                    }
                    
                    self.logger.info(f"WhatsApp check successful: {whatsapp_status} - Active: {is_active}")
                    return result
                else:
                    return {
                        'status': 'not_found',
                        'phone_number': phone_number,
                        'whatsapp_status': 'not_found',
                        'is_active': False,
                        'check_timestamp': datetime.now().isoformat(),
                        'message': 'Phone number not found in Twilio database'
                    }
                    
            except TwilioRestException as e:
                self.logger.error(f"Twilio API error: {e}")
                return {
                    'status': 'error',
                    'phone_number': phone_number,
                    'whatsapp_status': 'error',
                    'is_active': None,
                    'check_timestamp': datetime.now().isoformat(),
                    'error': str(e)
                }
                
        except Exception as e:
            self.logger.error(f"Error checking WhatsApp existence: {e}")
            return {
                'status': 'error',
                'phone_number': phone_number,
                'whatsapp_status': 'error',
                'is_active': None,
                'check_timestamp': datetime.now().isoformat(),
                'error': str(e)
            }
    
    def validate_lead(self, lead_data: Dict) -> Dict:
        """
        Comprehensive lead validation including phone and WhatsApp checks
        
        Args:
            lead_data: Lead data dictionary containing phone number and score
            
        Returns:
            Dict with comprehensive validation results
        """
        try:
            self.logger.info(f"Starting comprehensive lead validation")
            
            # Extract phone number from lead data
            phone_number = self._extract_phone_from_lead(lead_data)
            lead_score = lead_data.get('elite_score', 0)
            
            validation_result = {
                'lead_data': lead_data,
                'validation_timestamp': datetime.now().isoformat(),
                'validation_status': 'pending',
                'validation_details': {},
                'recommendations': []
            }
            
            # Step 1: Phone validation
            if phone_number:
                phone_validation = self.validate_phone(phone_number)
                validation_result['validation_details']['phone'] = phone_validation
                
                if phone_validation['status'] == 'invalid_format':
                    validation_result['validation_status'] = 'invalid_format'
                    validation_result['recommendations'].append('Phone number format is invalid')
                    self.logger.warning(f"Lead rejected: Invalid phone format - {phone_number}")
                    return validation_result
                
                # Step 2: WhatsApp check (if score is high enough)
                if lead_score >= self.validation_thresholds['min_score_for_validation']:
                    if self.validation_thresholds['whatsapp_check_enabled']:
                        whatsapp_check = self.check_whatsapp_existence(phone_validation['cleaned_phone'])
                        validation_result['validation_details']['whatsapp'] = whatsapp_check
                        
                        # Determine final validation status
                        validation_result['validation_status'] = self._determine_final_status(
                            phone_validation, whatsapp_check, lead_score
                        )
                        
                        # Add recommendations based on results
                        validation_result['recommendations'].extend(
                            self._get_validation_recommendations(phone_validation, whatsapp_check)
                        )
                    else:
                        validation_result['validation_status'] = 'qualified'
                        validation_result['recommendations'].append('WhatsApp check disabled - qualified based on score')
                else:
                    validation_result['validation_status'] = 'low_score'
                    validation_result['recommendations'].append(f'Lead score {lead_score} below validation threshold {self.validation_thresholds["min_score_for_validation"]}')
            else:
                validation_result['validation_status'] = 'no_phone'
                validation_result['recommendations'].append('No phone number provided for validation')
            
            self.logger.info(f"Lead validation completed: {validation_result['validation_status']}")
            return validation_result
            
        except Exception as e:
            self.logger.error(f"Error in comprehensive lead validation: {e}")
            return {
                'lead_data': lead_data,
                'validation_timestamp': datetime.now().isoformat(),
                'validation_status': 'error',
                'validation_details': {},
                'recommendations': ['Validation system error'],
                'error': str(e)
            }
    
    def _extract_phone_from_lead(self, lead_data: Dict) -> str:
        """
        Extract phone number from lead data
        """
        try:
            # Try multiple fields for phone number
            phone_fields = [
                'phone',
                'contact_info',
                'phone_number',
                'mobile',
                'whatsapp',
                'contact_phone'
            ]
            
            for field in phone_fields:
                phone = lead_data.get(field, '')
                if phone:
                    # Extract phone number from text
                    phone_match = re.search(r'(\+?\d{8,15})', str(phone))
                    if phone_match:
                        return phone_match.group(1)
            
            return ''
            
        except Exception as e:
            self.logger.error(f"Error extracting phone from lead data: {e}")
            return ''
    
    def _determine_final_status(self, phone_validation: Dict, whatsapp_check: Dict, lead_score: int) -> str:
        """
        Determine final validation status based on all checks
        """
        try:
            # Priority 1: Phone format must be valid
            if phone_validation.get('status') != 'valid':
                return 'invalid_format'
            
            # Priority 2: Check WhatsApp status if available
            if whatsapp_check.get('status') == 'success':
                if whatsapp_check.get('is_active', False):
                    return 'qualified'  # WhatsApp active
                else:
                    return 'suspected_bot'  # WhatsApp not active
            elif whatsapp_check.get('status') == 'not_found':
                return 'suspected_bot'  # Not found in WhatsApp
            elif whatsapp_check.get('status') == 'unavailable':
                return 'qualified'  # Can't check WhatsApp, but phone is valid
            elif whatsapp_check.get('status') == 'error':
                return 'qualified'  # WhatsApp check failed, but phone is valid
            
            # Default to qualified if all checks pass
            return 'qualified'
            
        except Exception as e:
            self.logger.error(f"Error determining final validation status: {e}")
            return 'error'
    
    def _get_validation_recommendations(self, phone_validation: Dict, whatsapp_check: Dict) -> list:
        """
        Get recommendations based on validation results
        """
        try:
            recommendations = []
            
            # Phone validation recommendations
            if phone_validation.get('status') == 'valid':
                phone_details = phone_validation.get('validation_details', {})
                if phone_details.get('overall_quality') == 'acceptable':
                    recommendations.extend(phone_details.get('recommendations', []))
            
            # WhatsApp check recommendations
            if whatsapp_check.get('status') == 'success':
                if not whatsapp_check.get('is_active', False):
                    recommendations.append('WhatsApp not active - potential bot or inactive number')
            elif whatsapp_check.get('status') == 'not_found':
                recommendations.append('Number not found in WhatsApp database')
            elif whatsapp_check.get('status') == 'unavailable':
                recommendations.append('WhatsApp validation not available')
            elif whatsapp_check.get('status') == 'error':
                recommendations.append('WhatsApp check failed - proceed with caution')
            
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Error getting validation recommendations: {e}")
            return []
    
    def gatekeeper_pipeline(self, lead_data: Dict, min_score: int = 8) -> Dict:
        """
        Gatekeeper pipeline for lead validation before processing
        
        Args:
            lead_data: Lead data to validate
            min_score: Minimum score required for validation
            
        Returns:
            Dict with gatekeeper decision
        """
        try:
            self.logger.info(f"Running gatekeeper pipeline for lead with score: {lead_data.get('elite_score', 0)}")
            
            # Update validation threshold
            self.validation_thresholds['min_score_for_validation'] = min_score
            
            # Run comprehensive validation
            validation_result = self.validate_lead(lead_data)
            
            # Make gatekeeper decision
            gatekeeper_decision = {
                'lead_data': lead_data,
                'validation_result': validation_result,
                'gatekeeper_decision': 'reject',
                'gatekeeper_timestamp': datetime.now().isoformat(),
                'min_score_used': min_score
            }
            
            # Determine if lead should be processed
            validation_status = validation_result.get('validation_status', '')
            
            if validation_status in ['qualified', 'low_score', 'no_phone']:
                gatekeeper_decision['gatekeeper_decision'] = 'process'
                gatekeeper_decision['reason'] = f"Lead passed validation: {validation_status}"
            elif validation_status == 'invalid_format':
                gatekeeper_decision['gatekeeper_decision'] = 'trash'
                gatekeeper_decision['reason'] = "Invalid phone format"
            elif validation_status == 'suspected_bot':
                gatekeeper_decision['gatekeeper_decision'] = 'trash'
                gatekeeper_decision['reason'] = "Suspected bot or inactive WhatsApp"
            elif validation_status == 'error':
                gatekeeper_decision['gatekeeper_decision'] = 'process'  # Allow processing on validation errors
                gatekeeper_decision['reason'] = "Validation error - proceed with caution"
            
            self.logger.info(f"Gatekeeper decision: {gatekeeper_decision['gatekeeper_decision']} - {gatekeeper_decision['reason']}")
            return gatekeeper_decision
            
        except Exception as e:
            self.logger.error(f"Error in gatekeeper pipeline: {e}")
            return {
                'lead_data': lead_data,
                'validation_result': {'status': 'error'},
                'gatekeeper_decision': 'process',  # Default to process on errors
                'gatekeeper_timestamp': datetime.now().isoformat(),
                'min_score_used': min_score,
                'reason': f"Pipeline error: {e}"
            }
    
    def get_validation_statistics(self) -> Dict:
        """
        Get validation statistics for monitoring
        """
        try:
            # This would typically query a database for validation statistics
            # For now, return mock statistics
            return {
                'total_validations': 0,
                'valid_phones': 0,
                'invalid_formats': 0,
                'whatsapp_checks': 0,
                'qualified_leads': 0,
                'rejected_leads': 0,
                'statistics_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error getting validation statistics: {e}")
            return {
                'total_validations': 0,
                'valid_phones': 0,
                'invalid_formats': 0,
                'whatsapp_checks': 0,
                'qualified_leads': 0,
                'rejected_leads': 0,
                'statistics_timestamp': datetime.now().isoformat(),
                'error': str(e)
            }

# Global lead validator instance
lead_validator = LeadValidator()

# Convenience functions
def validate_phone(phone_number: str) -> Dict:
    """Validate phone number format"""
    return lead_validator.validate_phone(phone_number)

def check_whatsapp_existence(phone_number: str) -> Dict:
    """Check WhatsApp existence"""
    return lead_validator.check_whatsapp_existence(phone_number)

def validate_lead(lead_data: Dict) -> Dict:
    """Comprehensive lead validation"""
    return lead_validator.validate_lead(lead_data)

def gatekeeper_pipeline(lead_data: Dict, min_score: int = 8) -> Dict:
    """Run gatekeeper pipeline"""
    return lead_validator.gatekeeper_pipeline(lead_data, min_score)

if __name__ == "__main__":
    # Test Lead Validator
    logging.basicConfig(level=logging.INFO)
    
    print("=== Lead Validator Test ===")
    
    # Test phone validation
    test_phones = [
        '+62812345678',  # Valid mobile
        '08123456789',  # Valid mobile
        '021123456',    # Valid landline
        '12345678',     # Invalid (no country code)
        'abc1234567',   # Invalid (letters)
        '+62123456789', # Invalid (too short)
    ]
    
    for phone in test_phones:
        result = validate_phone(phone)
        print(f"Phone: {phone} -> Status: {result['status']}, Type: {result['phone_type']}, Valid: {result['is_valid']}")
    
    # Test WhatsApp check (if available)
    if lead_validator.use_whatsapp_validation:
        print("\nTesting WhatsApp validation...")
        whatsapp_result = check_whatsapp_existence('+62812345678')
        print(f"WhatsApp Check: Status: {whatsapp_result['status']}, Active: {whatsapp_result.get('is_active', 'Unknown')}")
    
    # Test comprehensive validation
    print("\nTesting comprehensive validation...")
    test_lead = {
        'title': 'Test Lead',
        'elite_score': 9,
        'phone': '+62812345678',
        'contact_info': 'Test contact info'
    }
    
    validation_result = validate_lead(test_lead)
    print(f"Validation Status: {validation_result['validation_status']}")
    print(f"Recommendations: {validation_result['recommendations']}")
    
    # Test gatekeeper pipeline
    print("\nTesting gatekeeper pipeline...")
    gatekeeper_result = gatekeeper_pipeline(test_lead, min_score=8)
    print(f"Gatekeeper Decision: {gatekeeper_result['gatekeeper_decision']}")
    print(f"Reason: {gatekeeper_result['reason']}")
    
    print("\nLead Validator test completed!")
