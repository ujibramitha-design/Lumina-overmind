"""
Analytics API Endpoint for LUMINA OS Property Intelligence
Provides strategic insights and data visualization endpoints

Author: HUNTER_AGENT_AI_MARKETING_DIGITAL
Version: 1.0.0
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List
from flask import Blueprint, jsonify

# Import core modules
from core_modules.db_manager import DatabaseManager

# Configure logging
logger = logging.getLogger(__name__)

# Create analytics blueprint
analytics_bp = Blueprint('analytics', __name__)

def get_daily_trends(db_manager: DatabaseManager, days: int = 7) -> List[Dict[str, Any]]:
    """
    Get daily lead trends for the last N days
    
    Args:
        db_manager: Database manager instance
        days: Number of days to analyze
        
    Returns:
        List: Daily trend data
    """
    try:
        # Calculate date range
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days-1)
        
        # Query daily lead counts
        query = """
        SELECT 
            DATE(created_at) as date,
            COUNT(*) as lead_count,
            COUNT(CASE WHEN skor_akhir >= 80 THEN 1 END) as hot_leads,
            COUNT(CASE WHEN skor_akhir >= 60 AND skor_akhir < 80 THEN 1 END) as warm_leads,
            COUNT(CASE WHEN skor_akhir < 60 THEN 1 END) as cold_leads
        FROM leads 
        WHERE DATE(created_at) >= ?
        GROUP BY DATE(created_at)
        ORDER BY DATE(created_at)
        """
        
        results = db_manager.execute_query(query, (start_date,))
        
        # Convert to list of dictionaries
        trends = []
        for row in results:
            trends.append({
                'date': row[0].strftime('%Y-%m-%d'),
                'total_leads': row[1],
                'hot_leads': row[2],
                'warm_leads': row[3],
                'cold_leads': row[4]
            })
        
        # Fill missing dates with zero values
        current_date = start_date
        filled_trends = []
        
        while current_date <= end_date:
            date_str = current_date.strftime('%Y-%m-%d')
            
            # Find existing data for this date
            existing_data = next((t for t in trends if t['date'] == date_str), None)
            
            if existing_data:
                filled_trends.append(existing_data)
            else:
                filled_trends.append({
                    'date': date_str,
                    'total_leads': 0,
                    'hot_leads': 0,
                    'warm_leads': 0,
                    'cold_leads': 0
                })
            
            current_date += timedelta(days=1)
        
        return filled_trends
        
    except Exception as e:
        logger.error(f"Error getting daily trends: {str(e)}")
        return []

def get_category_distribution(db_manager: DatabaseManager) -> Dict[str, Any]:
    """
    Get lead category distribution
    
    Args:
        db_manager: Database manager instance
        
    Returns:
        Dict: Category distribution data
    """
    try:
        # Query category distribution
        query = """
        SELECT 
            kategori,
            COUNT(*) as count,
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM leads), 2) as percentage
        FROM leads 
        WHERE kategori IS NOT NULL AND kategori != ''
        GROUP BY kategori
        ORDER BY COUNT(*) DESC
        """
        
        results = db_manager.execute_query(query)
        
        # Prepare data for doughnut chart
        labels = []
        data = []
        colors = []
        
        color_map = {
            'Hot': '#10b981',      # Emerald
            'Warm': '#f59e0b',     # Amber
            'Cold': '#3b82f6',     # Blue
            'Unknown': '#6b7280'   # Gray
        }
        
        for row in results:
            category = row[0]
            labels.append(f"{category} ({row[2]}%)")
            data.append(row[1])
            colors.append(color_map.get(category, '#6b7280'))
        
        return {
            'labels': labels,
            'data': data,
            'colors': colors
        }
        
    except Exception as e:
        logger.error(f"Error getting category distribution: {str(e)}")
        return {
            'labels': ['No Data'],
            'data': [1],
            'colors': ['#6b7280']
        }

def get_conversion_forecast(db_manager: DatabaseManager) -> Dict[str, Any]:
    """
    Calculate conversion forecast based on hot leads
    
    Args:
        db_manager: Database manager instance
        
    Returns:
        Dict: Conversion forecast data
    """
    try:
        # Get hot leads from last 30 days
        query = """
        SELECT 
            COUNT(*) as hot_leads_30d,
            AVG(skor_akhir) as avg_score
        FROM leads 
        WHERE kategori = 'Hot' 
        AND DATE(created_at) >= DATE('now', '-30 days')
        """
        
        result = db_manager.execute_query(query)
        
        if not result:
            return {
                'hot_leads_30d': 0,
                'avg_score': 0,
                'conversion_rate': 0,
                'estimated_conversions': 0,
                'forecast_revenue': 0
            }
        
        hot_leads_30d = result[0][0]
        avg_score = result[0][1] if result[0][1] else 0
        
        # Conversion rate estimation (based on industry standards)
        # Hot leads typically have 20-30% conversion rate
        base_conversion_rate = 0.25
        score_multiplier = avg_score / 100  # Higher scores = higher conversion
        
        conversion_rate = min(base_conversion_rate * score_multiplier, 0.5)  # Cap at 50%
        estimated_conversions = int(hot_leads_30d * conversion_rate)
        
        # Estimate revenue (assuming average property value of 400M)
        avg_property_value = 400000000  # 400 juta
        commission_rate = 0.02  # 2% commission
        forecast_revenue = estimated_conversions * avg_property_value * commission_rate
        
        return {
            'hot_leads_30d': hot_leads_30d,
            'avg_score': round(avg_score, 1),
            'conversion_rate': round(conversion_rate * 100, 1),
            'estimated_conversions': estimated_conversions,
            'forecast_revenue': forecast_revenue
        }
        
    except Exception as e:
        logger.error(f"Error calculating conversion forecast: {str(e)}")
        return {
            'hot_leads_30d': 0,
            'avg_score': 0,
            'conversion_rate': 0,
            'estimated_conversions': 0,
            'forecast_revenue': 0
        }

def get_performance_metrics(db_manager: DatabaseManager) -> Dict[str, Any]:
    """
    Get overall performance metrics
    
    Args:
        db_manager: Database manager instance
        
    Returns:
        Dict: Performance metrics
    """
    try:
        # Get overall statistics
        stats = db_manager.get_statistics()
        
        # Get recent activity (last 24 hours)
        query_24h = """
        SELECT COUNT(*) as leads_24h
        FROM leads 
        WHERE created_at >= DATETIME('now', '-1 day')
        """
        
        result_24h = db_manager.execute_query(query_24h)
        leads_24h = result_24h[0][0] if result_24h else 0
        
        # Get follow-up metrics
        query_followup = """
        SELECT 
            COUNT(*) as total_followups,
            COUNT(CASE WHEN catatan_followup IS NOT NULL AND catatan_followup != '' THEN 1 END) as completed_followups
        FROM leads 
        WHERE status = 'Follow Up'
        """
        
        result_followup = db_manager.execute_query(query_followup)
        total_followups = result_followup[0][0] if result_followup else 0
        completed_followups = result_followup[0][1] if result_followup else 0
        
        followup_rate = (completed_followups / total_followups * 100) if total_followups > 0 else 0
        
        return {
            'total_leads': stats.get('total_leads', 0),
            'leads_24h': leads_24h,
            'by_status': stats.get('by_status', {}),
            'total_followups': total_followups,
            'completed_followups': completed_followups,
            'followup_rate': round(followup_rate, 1),
            'last_updated': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting performance metrics: {str(e)}")
        return {
            'total_leads': 0,
            'leads_24h': 0,
            'by_status': {},
            'total_followups': 0,
            'completed_followups': 0,
            'followup_rate': 0,
            'last_updated': datetime.now().isoformat()
        }

@analytics_bp.route('/analytics/summary', methods=['GET'])
def get_analytics_summary():
    """
    Get comprehensive analytics summary for dashboard
    """
    try:
        db_manager = DatabaseManager()
        
        # Get all analytics data
        daily_trends = get_daily_trends(db_manager, days=7)
        category_distribution = get_category_distribution(db_manager)
        conversion_forecast = get_conversion_forecast(db_manager)
        performance_metrics = get_performance_metrics(db_manager)
        
        response = {
            'success': True,
            'data': {
                'daily_trends': daily_trends,
                'category_distribution': category_distribution,
                'conversion_forecast': conversion_forecast,
                'performance_metrics': performance_metrics
            },
            'generated_at': datetime.now().isoformat()
        }
        
        logger.info("Analytics summary generated successfully")
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error generating analytics summary: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'generated_at': datetime.now().isoformat()
        }), 500

@analytics_bp.route('/analytics/trends', methods=['GET'])
def get_trends_data():
    """
    Get daily trends data
    """
    try:
        db_manager = DatabaseManager()
        
        # Get query parameter for days
        from flask import request
        days = request.args.get('days', 7, type=int)
        days = min(max(days, 1), 30)  # Limit between 1-30 days
        
        daily_trends = get_daily_trends(db_manager, days=days)
        
        response = {
            'success': True,
            'data': daily_trends,
            'days_analyzed': days,
            'generated_at': datetime.now().isoformat()
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error getting trends data: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'generated_at': datetime.now().isoformat()
        }), 500

@analytics_bp.route('/analytics/categories', methods=['GET'])
def get_categories_data():
    """
    Get category distribution data
    """
    try:
        db_manager = DatabaseManager()
        category_distribution = get_category_distribution(db_manager)
        
        response = {
            'success': True,
            'data': category_distribution,
            'generated_at': datetime.now().isoformat()
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error getting categories data: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'generated_at': datetime.now().isoformat()
        }), 500

@analytics_bp.route('/analytics/forecast', methods=['GET'])
def get_forecast_data():
    """
    Get conversion forecast data
    """
    try:
        db_manager = DatabaseManager()
        conversion_forecast = get_conversion_forecast(db_manager)
        
        response = {
            'success': True,
            'data': conversion_forecast,
            'generated_at': datetime.now().isoformat()
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error getting forecast data: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'generated_at': datetime.now().isoformat()
        }), 500

@analytics_bp.route('/analytics/performance', methods=['GET'])
def get_performance_data():
    """
    Get performance metrics data
    """
    try:
        db_manager = DatabaseManager()
        performance_metrics = get_performance_metrics(db_manager)
        
        response = {
            'success': True,
            'data': performance_metrics,
            'generated_at': datetime.now().isoformat()
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error getting performance data: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'generated_at': datetime.now().isoformat()
        }), 500

@analytics_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for analytics service
    """
    try:
        db_manager = DatabaseManager()
        
        # Test database connection
        stats = db_manager.get_statistics()
        
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'total_leads': stats.get('total_leads', 0),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Analytics health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500
