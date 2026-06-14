"""
Cost Monitoring API Endpoints
Cloud cost tracking, resource optimization, and budget management
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
router = APIRouter(prefix="/api/cost", tags=["Cost Monitoring"])

# Pydantic models
class CostMetricsRequest(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    granularity: str = "daily"  # 'hourly', 'daily', 'monthly'
    service: Optional[str] = None  # 'compute', 'storage', 'database', 'network'

class CostMetricsResponse(BaseModel):
    period: Dict[str, str]
    total_cost: float
    currency: str
    breakdown: Dict[str, float]
    trends: List[Dict[str, Any]]
    recommendations: List[str]
    timestamp: str

class BudgetAlertRequest(BaseModel):
    budget_limit: float
    alert_threshold: float  # percentage (e.g., 80 for 80%)
    notification_channels: List[str] = ["email", "slack"]

class BudgetAlertResponse(BaseModel):
    budget_id: str
    budget_limit: float
    current_spend: float
    utilization_percentage: float
    alert_triggered: bool
    remaining_budget: float
    forecast: Dict[str, Any]
    timestamp: str

class ResourceOptimizationRequest(BaseModel):
    service: str
    optimization_type: str  # 'rightsizing', 'scheduling', 'cleanup'

class ResourceOptimizationResponse(BaseModel):
    service: str
    optimization_type: str
    current_cost: float
    potential_savings: float
    recommendations: List[Dict[str, Any]]
    estimated_monthly_savings: float
    timestamp: str

# Mock cost data (in production, this would come from AWS Cost Explorer, Azure Cost Management, etc.)
MOCK_COST_DATA = {
    'compute': {
        'daily': 50.0,
        'monthly': 1500.0,
        'trend': 'increasing'
    },
    'storage': {
        'daily': 20.0,
        'monthly': 600.0,
        'trend': 'stable'
    },
    'database': {
        'daily': 30.0,
        'monthly': 900.0,
        'trend': 'increasing'
    },
    'network': {
        'daily': 10.0,
        'monthly': 300.0,
        'trend': 'stable'
    }
}

@router.get("/metrics", response_model=CostMetricsResponse)
async def get_cost_metrics(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    granularity: str = "daily",
    service: Optional[str] = None
):
    """
    Get cost metrics for specified period and granularity
    """
    try:
        # Parse dates or use defaults
        if not end_date:
            end_date = datetime.utcnow().isoformat()
        if not start_date:
            start_date = (datetime.utcnow() - timedelta(days=30)).isoformat()
        
        # Calculate total cost
        if service:
            if service not in MOCK_COST_DATA:
                raise HTTPException(status_code=400, detail=f"Invalid service: {service}")
            total_cost = MOCK_COST_DATA[service]['daily'] * 30  # Assume 30 days
            breakdown = {service: MOCK_COST_DATA[service]['monthly']}
        else:
            total_cost = sum(data['monthly'] for data in MOCK_COST_DATA.values())
            breakdown = {k: v['monthly'] for k, v in MOCK_COST_DATA.items()}
        
        # Generate trend data
        trends = []
        for i in range(30):
            date = (datetime.utcnow() - timedelta(days=29-i)).strftime('%Y-%m-%d')
            daily_cost = sum(data['daily'] for data in MOCK_COST_DATA.values())
            trends.append({
                'date': date,
                'cost': daily_cost
            })
        
        # Generate recommendations
        recommendations = []
        if MOCK_COST_DATA['compute']['trend'] == 'increasing':
            recommendations.append("Consider rightsizing compute instances during off-peak hours")
        if MOCK_COST_DATA['database']['trend'] == 'increasing':
            recommendations.append("Review database query optimization and indexing")
        recommendations.append("Enable auto-scaling to reduce idle resource costs")
        recommendations.append("Review reserved instance utilization")
        
        return CostMetricsResponse(
            period={
                'start_date': start_date,
                'end_date': end_date
            },
            total_cost=total_cost,
            currency='USD',
            breakdown=breakdown,
            trends=trends,
            recommendations=recommendations,
            timestamp=datetime.utcnow().isoformat()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting cost metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get cost metrics: {str(e)}")

@router.post("/budget-alert", response_model=BudgetAlertResponse)
async def set_budget_alert(request: BudgetAlertRequest):
    """
    Set budget alert and check current utilization
    """
    try:
        budget_id = f"BUD-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        
        # Calculate current spend (mock data)
        current_spend = sum(data['daily'] for data in MOCK_COST_DATA.values()) * 30
        utilization_percentage = (current_spend / request.budget_limit) * 100
        remaining_budget = request.budget_limit - current_spend
        
        # Check if alert should be triggered
        alert_triggered = utilization_percentage >= request.alert_threshold
        
        # Generate forecast
        forecast = {
            'projected_monthly_cost': current_spend * 1.1,  # Assume 10% growth
            'budget_exceeded': utilization_percentage > 100,
            'days_until_budget_exceeded': None
        }
        
        if utilization_percentage > 100:
            # Calculate days until budget would be exceeded (if trending up)
            daily_spend = sum(data['daily'] for data in MOCK_COST_DATA.values())
            days_remaining = remaining_budget / daily_spend if daily_spend > 0 else 0
            forecast['days_until_budget_exceeded'] = max(0, int(days_remaining))
        
        return BudgetAlertResponse(
            budget_id=budget_id,
            budget_limit=request.budget_limit,
            current_spend=current_spend,
            utilization_percentage=utilization_percentage,
            alert_triggered=alert_triggered,
            remaining_budget=remaining_budget,
            forecast=forecast,
            timestamp=datetime.utcnow().isoformat()
        )
    
    except Exception as e:
        logger.error(f"Error setting budget alert: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to set budget alert: {str(e)}")

@router.post("/optimize", response_model=ResourceOptimizationResponse)
async def optimize_resources(request: ResourceOptimizationRequest):
    """
    Get resource optimization recommendations
    """
    try:
        # Get current cost for the service
        if request.service not in MOCK_COST_DATA:
            raise HTTPException(status_code=400, detail=f"Invalid service: {service}")
        
        current_cost = MOCK_COST_DATA[request.service]['monthly']
        
        # Generate optimization recommendations based on type
        recommendations = []
        potential_savings = 0.0
        
        if request.optimization_type == 'rightsizing':
            recommendations = [
                {
                    'action': 'Downsize idle instances',
                    'potential_saving': 200.0,
                    'description': 'Identify and downsize instances with <10% utilization'
                },
                {
                    'action': 'Use spot instances',
                    'potential_saving': 300.0,
                    'description': 'Replace non-critical instances with spot instances'
                }
            ]
            potential_savings = 500.0
        
        elif request.optimization_type == 'scheduling':
            recommendations = [
                {
                    'action': 'Schedule off-peak shutdown',
                    'potential_saving': 150.0,
                    'description': 'Shut down non-critical resources during off-peak hours'
                },
                {
                    'action': 'Auto-scaling optimization',
                    'potential_saving': 100.0,
                    'description': 'Configure aggressive auto-scaling policies'
                }
            ]
            potential_savings = 250.0
        
        elif request.optimization_type == 'cleanup':
            recommendations = [
                {
                    'action': 'Delete unused resources',
                    'potential_saving': 50.0,
                    'description': 'Identify and delete unused EBS volumes, snapshots, etc.'
                },
                {
                    'action': 'Clean up old logs',
                    'potential_saving': 30.0,
                    'description': 'Implement log retention policies'
                }
            ]
            potential_savings = 80.0
        
        else:
            raise HTTPException(status_code=400, detail=f"Invalid optimization type: {request.optimization_type}")
        
        estimated_monthly_savings = potential_savings
        
        return ResourceOptimizationResponse(
            service=request.service,
            optimization_type=request.optimization_type,
            current_cost=current_cost,
            potential_savings=potential_savings,
            recommendations=recommendations,
            estimated_monthly_savings=estimated_monthly_savings,
            timestamp=datetime.utcnow().isoformat()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error optimizing resources: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to optimize resources: {str(e)}")

@router.get("/summary")
async def get_cost_summary():
    """
    Get overall cost summary
    """
    try:
        total_monthly_cost = sum(data['monthly'] for data in MOCK_COST_DATA.values())
        
        return {
            'total_monthly_cost': total_monthly_cost,
            'currency': 'USD',
            'breakdown': {
                'compute': MOCK_COST_DATA['compute']['monthly'],
                'storage': MOCK_COST_DATA['storage']['monthly'],
                'database': MOCK_COST_DATA['database']['monthly'],
                'network': MOCK_COST_DATA['network']['monthly']
            },
            'trends': {
                'compute': MOCK_COST_DATA['compute']['trend'],
                'storage': MOCK_COST_DATA['storage']['trend'],
                'database': MOCK_COST_DATA['database']['trend'],
                'network': MOCK_COST_DATA['network']['trend']
            },
            'timestamp': datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Error getting cost summary: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get cost summary: {str(e)}")
