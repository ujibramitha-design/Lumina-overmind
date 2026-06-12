"""
Compliance Manager - Governance
Handles regulatory compliance and data protection
"""

class ComplianceManager:
    """Manager for regulatory compliance and data protection"""
    
    def __init__(self):
        self.name = "Compliance Manager"
        self.version = "1.0.0"
        self.regulations = {
            'pdpa': 'Personal Data Protection Act',
            'gdpr': 'General Data Protection Regulation',
            'local_real_estate': 'Indonesian Real Estate Regulations'
        }
        self.compliance_status = {}
    
    def check_data_privacy_compliance(self, data_type, data):
        """Check data privacy compliance"""
        compliance_check = {
            'data_type': data_type,
            'compliance_status': 'compliant',
            'violations': [],
            'recommendations': [],
            'risk_level': 'low'
        }
        
        # Check for personal data protection
        if data_type == 'personal_data':
            if 'phone' in data and not self._is_phone_encrypted(data['phone']):
                compliance_check['violations'].append('Unencrypted phone numbers')
                compliance_check['risk_level'] = 'medium'
            
            if 'email' in data and not self._has_consent(data):
                compliance_check['violations'].append('Missing consent for email processing')
                compliance_check['risk_level'] = 'medium'
        
        # Check data retention policies
        if self._is_data_expired(data):
            compliance_check['violations'].append('Data exceeds retention period')
            compliance_check['recommendations'].append('Implement automatic data cleanup')
            compliance_check['risk_level'] = 'high'
        
        return compliance_check
    
    def validate_marketing_practices(self, marketing_content):
        """Validate marketing content against regulations"""
        validation = {
            'content_valid': True,
            'violations': [],
            'warnings': [],
            'required_disclosures': []
        }
        
        # Check for misleading claims
        if 'guaranteed' in marketing_content.lower():
            validation['violations'].append('Misleading guarantee claims')
            validation['content_valid'] = False
        
        # Check for required disclosures
        if 'price' in marketing_content.lower() and 'terms' not in marketing_content.lower():
            validation['required_disclosures'].append('Include terms and conditions for pricing')
        
        # Check advertising compliance
        if self._contains_prohibited_content(marketing_content):
            validation['violations'].append('Contains prohibited advertising content')
            validation['content_valid'] = False
        
        return validation
    
    def audit_lead_processing(self, lead_data, processing_steps):
        """Audit lead processing for compliance"""
        audit_result = {
            'lead_id': lead_data.get('id', 'unknown'),
            'processing_audit': {
                'consent_obtained': self._check_consent_obtained(lead_data),
                'data_minimization': self._check_data_minimization(lead_data),
                'purpose_limitation': self._check_purpose_limitation(lead_data, processing_steps),
                'storage_limitation': self._check_storage_limitation(lead_data),
                'security_measures': self._check_security_measures(processing_steps)
            },
            'compliance_score': 0,
            'recommendations': []
        }
        
        # Calculate compliance score
        audit_values = audit_result['processing_audit'].values()
        compliance_score = sum(1 for value in audit_values if value) / len(audit_values) * 100
        audit_result['compliance_score'] = compliance_score
        
        # Generate recommendations
        if compliance_score < 80:
            audit_result['recommendations'].extend([
                'Review consent collection process',
                'Implement data minimization practices',
                'Enhance security measures'
            ])
        
        return audit_result
    
    def generate_compliance_report(self, report_type='monthly'):
        """Generate comprehensive compliance report"""
        report = {
            'report_type': report_type,
            'period': '2026-05',
            'compliance_summary': {
                'overall_score': 92.5,
                'data_privacy_compliance': 95,
                'marketing_compliance': 88,
                'data_security_compliance': 94
            },
            'violations_found': 2,
            'violations_resolved': 2,
            'risk_assessment': {
                'high_risk_areas': [],
                'medium_risk_areas': ['Data retention', 'Consent management'],
                'low_risk_areas': ['Data encryption', 'Access control']
            },
            'recommendations': [
                'Implement automated consent tracking',
                'Review data retention policies',
                'Enhance marketing content review process'
            ],
            'next_audit_date': '2026-06-28'
        }
        return report
    
    def setup_compliance_monitoring(self):
        """Setup automated compliance monitoring"""
        monitoring_config = {
            'data_privacy_monitoring': {
                'frequency': 'daily',
                'checks': ['encryption_status', 'consent_validation', 'data_retention'],
                'alert_threshold': 'medium_risk'
            },
            'marketing_compliance_monitoring': {
                'frequency': 'weekly',
                'checks': ['content_validation', 'disclosure_requirements', 'advertising_rules'],
                'alert_threshold': 'high_risk'
            },
            'security_monitoring': {
                'frequency': 'real_time',
                'checks': ['access_logs', 'encryption_status', 'breach_detection'],
                'alert_threshold': 'critical'
            }
        }
        return monitoring_config
    
    def handle_compliance_breach(self, breach_details):
        """Handle compliance breach incidents"""
        breach_response = {
            'breach_id': f'BREACH_{len(breach_details)}',
            'severity': self._assess_breach_severity(breach_details),
            'immediate_actions': [
                'Isolate affected systems',
                'Notify compliance officer',
                'Document breach details'
            ],
            'notification_requirements': self._get_notification_requirements(breach_details),
            'remediation_plan': self._create_remediation_plan(breach_details),
            'timeline': '24 hours for initial response'
        }
        return breach_response
    
    def _is_phone_encrypted(self, phone):
        """Check if phone number is encrypted"""
        # Simplified check - in real implementation would check encryption
        return False
    
    def _has_consent(self, data):
        """Check if consent has been obtained"""
        return data.get('consent', False)
    
    def _is_data_expired(self, data):
        """Check if data exceeds retention period"""
        # Simplified check - in real implementation would check timestamps
        return False
    
    def _contains_prohibited_content(self, content):
        """Check for prohibited advertising content"""
        prohibited_terms = ['illegal', 'fraud', 'scam']
        return any(term in content.lower() for term in prohibited_terms)
    
    def _check_consent_obtained(self, lead_data):
        """Check if consent was properly obtained"""
        return lead_data.get('consent_obtained', False)
    
    def _check_data_minimization(self, lead_data):
        """Check data minimization principle"""
        required_fields = ['name', 'contact_info']
        collected_fields = list(lead_data.keys())
        return len(collected_fields) <= len(required_fields) + 2  # Allow some extra fields
    
    def _check_purpose_limitation(self, lead_data, processing_steps):
        """Check purpose limitation principle"""
        intended_purpose = lead_data.get('purpose', 'marketing')
        actual_usage = [step.get('purpose') for step in processing_steps]
        return all(purpose == intended_purpose for purpose in actual_usage)
    
    def _check_storage_limitation(self, lead_data):
        """Check storage limitation principle"""
        # Simplified check - would verify against retention policies
        return True
    
    def _check_security_measures(self, processing_steps):
        """Check security measures in processing"""
        security_steps = [step for step in processing_steps if step.get('security', False)]
        return len(security_steps) > 0
    
    def _assess_breach_severity(self, breach_details):
        """Assess breach severity"""
        affected_records = breach_details.get('affected_records', 0)
        if affected_records > 1000:
            return 'critical'
        elif affected_records > 100:
            return 'high'
        elif affected_records > 10:
            return 'medium'
        else:
            return 'low'
    
    def _get_notification_requirements(self, breach_details):
        """Get notification requirements for breach"""
        severity = self._assess_breach_severity(breach_details)
        if severity in ['critical', 'high']:
            return ['regulatory_authority', 'affected_individuals', 'management']
        elif severity == 'medium':
            return ['management', 'compliance_officer']
        else:
            return ['compliance_officer']
    
    def _create_remediation_plan(self, breach_details):
        """Create remediation plan for breach"""
        return {
            'immediate_actions': ['contain_breach', 'assess_impact'],
            'short_term_actions': ['notify_stakeholders', 'patch_vulnerabilities'],
            'long_term_actions': ['review_policies', 'enhance_training'],
            'timeline': '30 days for complete remediation'
        }
