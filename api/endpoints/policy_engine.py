"""
Policy Engine & Compliance Reporting API Endpoints
Policy evaluation, compliance monitoring, and audit reporting
"""

import os
import sys
import logging
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime, timedelta

# Add root directory to Python path
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(root_dir)

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/policy", tags=["Policy Engine"])

# Pydantic models
class PolicyDefinition(BaseModel):
    id: str
    name: str
    description: str
    category: str  # 'security', 'privacy', 'access', 'data', 'compliance'
    severity: str  # 'low', 'medium', 'high', 'critical'
    enabled: bool
    rules: List[Dict[str, Any]]
    remediation: str

class PolicyEvaluationRequest(BaseModel):
    policy_id: str
    context: Dict[str, Any]
    user_id: Optional[str] = None
    resource_id: Optional[str] = None

class PolicyEvaluationResponse(BaseModel):
    policy_id: str
    result: str  # 'pass', 'fail', 'warning'
    violations: List[Dict[str, Any]]
    score: float
    timestamp: str

class ComplianceReportRequest(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    category: Optional[str] = None
    severity: Optional[str] = None

class ComplianceReportResponse(BaseModel):
    period: Dict[str, str]
    total_policies: int
    passed_policies: int
    failed_policies: int
    warning_policies: int
    compliance_score: float
    violations: List[Dict[str, Any]]
    recommendations: List[str]
    timestamp: str

class PolicyViolation(BaseModel):
    id: str
    policy_id: str
    policy_name: str
    severity: str
    description: str
    context: Dict[str, Any]
    detected_at: str
    status: str  # 'open', 'in_progress', 'resolved'
    remediation: str

# Mock policy definitions
POLICY_DEFINITIONS = [
    {
        'id': 'POL-001',
        'name': 'Data Encryption at Rest',
        'description': 'All sensitive data must be encrypted at rest',
        'category': 'security',
        'severity': 'critical',
        'enabled': True,
        'rules': [
            {'field': 'data.sensitive', 'operator': 'equals', 'value': True, 'action': 'require_encryption'}
        ],
        'remediation': 'Enable encryption for all sensitive data fields'
    },
    {
        'id': 'POL-002',
        'name': 'Access Control Minimum',
        'description': 'All resources must have access control defined',
        'category': 'access',
        'severity': 'high',
        'enabled': True,
        'rules': [
            {'field': 'resource.access_control', 'operator': 'exists', 'value': True}
        ],
        'remediation': 'Define access control for all resources'
    },
    {
        'id': 'POL-003',
        'name': 'Data Retention Policy',
        'description': 'Data must not be retained longer than required',
        'category': 'privacy',
        'severity': 'medium',
        'enabled': True,
        'rules': [
            {'field': 'data.retention_days', 'operator': 'less_than', 'value': 365}
        ],
        'remediation': 'Implement data retention and deletion policies'
    },
    {
        'id': 'POL-004',
        'name': 'Audit Trail Logging',
        'description': 'All critical operations must be logged',
        'category': 'compliance',
        'severity': 'high',
        'enabled': True,
        'rules': [
            {'field': 'operation.critical', 'operator': 'equals', 'value': True, 'action': 'require_logging'}
        ],
        'remediation': 'Enable audit logging for all critical operations'
    },
    {
        'id': 'POL-005',
        'name': 'Password Policy',
        'description': 'Passwords must meet minimum complexity requirements',
        'category': 'security',
        'severity': 'high',
        'enabled': True,
        'rules': [
            {'field': 'password.length', 'operator': 'greater_than', 'value': 8},
            {'field': 'password.complexity', 'operator': 'equals', 'value': True}
        ],
        'remediation': 'Enforce password complexity requirements'
    },
    {
        'id': 'POL-006',
        'name': 'Data Privacy Consent',
        'description': 'User consent must be obtained before data collection',
        'category': 'privacy',
        'severity': 'critical',
        'enabled': True,
        'rules': [
            {'field': 'data.collection', 'operator': 'equals', 'value': True, 'action': 'require_consent'}
        ],
        'remediation': 'Implement consent management system'
    },
    {
        'id': 'POL-007',
        'name': 'API Rate Limiting',
        'description': 'All API endpoints must have rate limiting',
        'category': 'security',
        'severity': 'medium',
        'enabled': True,
        'rules': [
            {'field': 'endpoint.rate_limit', 'operator': 'exists', 'value': True}
        ],
        'remediation': 'Configure rate limiting for all API endpoints'
    },
    {
        'id': 'POL-008',
        'name': 'Data Backup Policy',
        'description': 'Critical data must be backed up regularly',
        'category': 'data',
        'severity': 'high',
        'enabled': True,
        'rules': [
            {'field': 'data.critical', 'operator': 'equals', 'value': True, 'action': 'require_backup'}
        ],
        'remediation': 'Implement automated backup system'
    }
]

# Mock violations database
POLICY_VIOLATIONS = []

@router.get("/policies")
async def get_policies(
    category: Optional[str] = None,
    severity: Optional[str] = None,
    enabled: Optional[bool] = None
):
    """
    Get all policy definitions with optional filters
    """
    try:
        policies = POLICY_DEFINITIONS
        
        if category:
            policies = [p for p in policies if p['category'] == category]
        if severity:
            policies = [p for p in policies if p['severity'] == severity]
        if enabled is not None:
            policies = [p for p in policies if p['enabled'] == enabled]
        
        return {
            'policies': policies,
            'total': len(policies),
            'timestamp': datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Error getting policies: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get policies: {str(e)}")

@router.post("/evaluate", response_model=PolicyEvaluationResponse)
async def evaluate_policy(request: PolicyEvaluationRequest):
    """
    Evaluate a policy against given context
    """
    try:
        policy = next((p for p in POLICY_DEFINITIONS if p['id'] == request.policy_id), None)
        
        if not policy:
            raise HTTPException(status_code=404, detail=f"Policy {request.policy_id} not found")
        
        if not policy['enabled']:
            return PolicyEvaluationResponse(
                policy_id=request.policy_id,
                result='pass',
                violations=[],
                score=100.0,
                timestamp=datetime.utcnow().isoformat()
            )
        
        violations = []
        score = 100.0
        
        # Evaluate each rule
        for rule in policy['rules']:
            field = rule['field']
            operator = rule['operator']
            expected_value = rule['value']
            
            # Get actual value from context
            actual_value = request.context
            for key in field.split('.'):
                if isinstance(actual_value, dict) and key in actual_value:
                    actual_value = actual_value[key]
                else:
                    actual_value = None
                    break
            
            # Evaluate rule
            passed = False
            if operator == 'equals':
                passed = actual_value == expected_value
            elif operator == 'not_equals':
                passed = actual_value != expected_value
            elif operator == 'greater_than':
                passed = actual_value > expected_value if actual_value is not None else False
            elif operator == 'less_than':
                passed = actual_value < expected_value if actual_value is not None else False
            elif operator == 'exists':
                passed = actual_value is not None
            elif operator == 'not_exists':
                passed = actual_value is None
            
            if not passed:
                violations.append({
                    'rule': rule,
                    'expected': expected_value,
                    'actual': actual_value
                })
                score -= 10.0  # Deduct score for each violation
        
        # Determine result
        result = 'pass'
        if violations:
            if policy['severity'] == 'critical':
                result = 'fail'
            elif policy['severity'] == 'high':
                result = 'fail'
            else:
                result = 'warning'
        
        # Log violation if any
        if violations:
            violation = PolicyViolation(
                id=f"VIOL-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
                policy_id=policy['id'],
                policy_name=policy['name'],
                severity=policy['severity'],
                description=f"Policy violation detected: {policy['name']}",
                context=request.context,
                detected_at=datetime.utcnow().isoformat(),
                status='open',
                remediation=policy['remediation']
            )
            POLICY_VIOLATIONS.append(violation)
        
        return PolicyEvaluationResponse(
            policy_id=request.policy_id,
            result=result,
            violations=violations,
            score=max(0, score),
            timestamp=datetime.utcnow().isoformat()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error evaluating policy: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Policy evaluation failed: {str(e)}")

@router.post("/compliance-report", response_model=ComplianceReportResponse)
async def generate_compliance_report(request: ComplianceReportRequest):
    """
    Generate comprehensive compliance report
    """
    try:
        # Parse dates or use defaults
        if not request.end_date:
            end_date = datetime.utcnow()
        else:
            end_date = parseISO(request.end_date)
        
        if not request.start_date:
            start_date = end_date - timedelta(days=30)
        else:
            start_date = parseISO(request.start_date)
        
        # Filter policies
        policies = POLICY_DEFINITIONS
        if request.category:
            policies = [p for p in policies if p['category'] == request.category]
        if request.severity:
            policies = [p for p in policies if p['severity'] == request.severity]
        
        # Evaluate all policies (mock evaluation)
        passed_policies = 0
        failed_policies = 0
        warning_policies = 0
        violations = []
        
        for policy in policies:
            if not policy['enabled']:
                continue
            
            # Mock evaluation - assume 80% pass rate
            import random
            if random.random() < 0.8:
                passed_policies += 1
            else:
                if policy['severity'] in ['critical', 'high']:
                    failed_policies += 1
                    violations.append({
                        'policy_id': policy['id'],
                        'policy_name': policy['name'],
                        'severity': policy['severity'],
                        'remediation': policy['remediation']
                    })
                else:
                    warning_policies += 1
        
        # Calculate compliance score
        total_evaluated = passed_policies + failed_policies + warning_policies
        compliance_score = (passed_policies / total_evaluated * 100) if total_evaluated > 0 else 100.0
        
        # Generate recommendations
        recommendations = []
        if failed_policies > 0:
            recommendations.append(f"Address {failed_policies} critical/high policy violations immediately")
        if warning_policies > 0:
            recommendations.append(f"Review {warning_policies} medium/low policy warnings")
        if compliance_score < 80:
            recommendations.append("Overall compliance score below 80% - requires attention")
        else:
            recommendations.append("Maintain current compliance practices")
        
        return ComplianceReportResponse(
            period={
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat()
            },
            total_policies=len(policies),
            passed_policies=passed_policies,
            failed_policies=failed_policies,
            warning_policies=warning_policies,
            compliance_score=compliance_score,
            violations=violations,
            recommendations=recommendations,
            timestamp=datetime.utcnow().isoformat()
        )
    
    except Exception as e:
        logger.error(f"Error generating compliance report: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Compliance report generation failed: {str(e)}")

@router.get("/violations")
async def get_violations(
    status: Optional[str] = None,
    severity: Optional[str] = None,
    limit: int = 50
):
    """
    Get policy violations with optional filters
    """
    try:
        violations = POLICY_VIOLATIONS
        
        if status:
            violations = [v for v in violations if v.status == status]
        if severity:
            violations = [v for v in violations if v.severity == severity]
        
        return {
            'violations': violations[:limit],
            'total': len(violations),
            'timestamp': datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Error getting violations: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get violations: {str(e)}")

@router.put("/violations/{violation_id}")
async def update_violation(
    violation_id: str,
    status: str
):
    """
    Update violation status
    """
    try:
        violation = next((v for v in POLICY_VIOLATIONS if v.id == violation_id), None)
        
        if not violation:
            raise HTTPException(status_code=404, detail=f"Violation {violation_id} not found")
        
        violation.status = status
        
        return {
            'violation_id': violation_id,
            'status': status,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating violation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update violation: {str(e)}")

@router.get("/summary")
async def get_policy_summary():
    """
    Get policy engine summary
    """
    try:
        total_policies = len(POLICY_DEFINITIONS)
        enabled_policies = len([p for p in POLICY_DEFINITIONS if p['enabled']])
        open_violations = len([v for v in POLICY_VIOLATIONS if v.status == 'open'])
        
        # Category breakdown
        category_breakdown = {}
        for policy in POLICY_DEFINITIONS:
            category = policy['category']
            if category not in category_breakdown:
                category_breakdown[category] = 0
            category_breakdown[category] += 1
        
        # Severity breakdown
        severity_breakdown = {}
        for policy in POLICY_DEFINITIONS:
            severity = policy['severity']
            if severity not in severity_breakdown:
                severity_breakdown[severity] = 0
            severity_breakdown[severity] += 1
        
        return {
            'total_policies': total_policies,
            'enabled_policies': enabled_policies,
            'disabled_policies': total_policies - enabled_policies,
            'open_violations': open_violations,
            'category_breakdown': category_breakdown,
            'severity_breakdown': severity_breakdown,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Error getting policy summary: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get policy summary: {str(e)}")
