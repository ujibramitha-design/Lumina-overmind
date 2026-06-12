"""
LUMINA OS Property Intelligence System - Flask Application
Advanced Analytics & Strategic Insights Dashboard

Author: HUNTER_AGENT_AI_MARKETING_DIGITAL
Version: 1.0.0
"""

import os
import sys
from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__, 
                template_folder='src',
                static_folder='src/assets')
    
    # Configure CORS
    CORS(app)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'lumina-os-secret-key-2026')
    app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    return app

# Create Flask app
app = create_app()

# Database path
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'leads.db (SQLite - removed))

def get_db_connection():
    """Get database connection"""
    conn = # SQLite connection removed
    conn.row_factory = sqlite3.Row
    return conn

def get_daily_trends(days=7):
    """Get daily lead trends"""
    try:
        conn = get_db_connection()
        
        # Calculate date range
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days-1)
        
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
        
        results = conn.execute(query, (start_date,)).fetchall()
        
        # Convert to list of dictionaries
        trends = []
        for row in results:
            trends.append({
                'date': row['date'],
                'total_leads': row['lead_count'],
                'hot_leads': row['hot_leads'],
                'warm_leads': row['warm_leads'],
                'cold_leads': row['cold_leads']
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
        
        # conn.close() removed
        return filled_trends
        
    except Exception as e:
        print(f"Error getting daily trends: {e}")
        return []

def get_category_distribution():
    """Get lead category distribution"""
    try:
        conn = get_db_connection()
        
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
        
        results = conn.execute(query).fetchall()
        
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
            category = row['kategori']
            labels.append(f"{category} ({row['percentage']}%)")
            data.append(row['count'])
            colors.append(color_map.get(category, '#6b7280'))
        
        # conn.close() removed
        
        if not labels:
            return {
                'labels': ['No Data'],
                'data': [1],
                'colors': ['#6b7280']
            }
        
        return {
            'labels': labels,
            'data': data,
            'colors': colors
        }
        
    except Exception as e:
        print(f"Error getting category distribution: {e}")
        return {
            'labels': ['No Data'],
            'data': [1],
            'colors': ['#6b7280']
        }

def get_conversion_forecast():
    """Calculate conversion forecast based on hot leads"""
    try:
        conn = get_db_connection()
        
        # Get hot leads from last 30 days
        query = """
        SELECT 
            COUNT(*) as hot_leads_30d,
            AVG(skor_akhir) as avg_score
        FROM leads 
        WHERE kategori = 'Hot' 
        AND DATE(created_at) >= DATE('now', '-30 days')
        """
        
        result = conn.execute(query).fetchone()
        
        if not result:
            return {
                'hot_leads_30d': 0,
                'avg_score': 0,
                'conversion_rate': 0,
                'estimated_conversions': 0,
                'forecast_revenue': 0
            }
        
        hot_leads_30d = result['hot_leads_30d']
        avg_score = result['avg_score'] if result['avg_score'] else 0
        
        # Conversion rate estimation
        base_conversion_rate = 0.25
        score_multiplier = avg_score / 100
        
        conversion_rate = min(base_conversion_rate * score_multiplier, 0.5)
        estimated_conversions = int(hot_leads_30d * conversion_rate)
        
        # Estimate revenue
        avg_property_value = 400000000  # 400 juta
        commission_rate = 0.02  # 2% commission
        forecast_revenue = estimated_conversions * avg_property_value * commission_rate
        
        # conn.close() removed
        
        return {
            'hot_leads_30d': hot_leads_30d,
            'avg_score': round(avg_score, 1),
            'conversion_rate': round(conversion_rate * 100, 1),
            'estimated_conversions': estimated_conversions,
            'forecast_revenue': forecast_revenue
        }
        
    except Exception as e:
        print(f"Error calculating conversion forecast: {e}")
        return {
            'hot_leads_30d': 0,
            'avg_score': 0,
            'conversion_rate': 0,
            'estimated_conversions': 0,
            'forecast_revenue': 0
        }

def get_performance_metrics():
    """Get overall performance metrics"""
    try:
        conn = get_db_connection()
        
        # Get overall statistics
        stats = conn.execute('SELECT COUNT(*) as total_leads FROM leads').fetchone()
        
        # Get recent activity (last 24 hours)
        result_24h = conn.execute("""
            SELECT COUNT(*) as leads_24h
            FROM leads 
            WHERE created_at >= DATETIME('now', '-1 day')
        """).fetchone()
        
        leads_24h = result_24h['leads_24h'] if result_24h else 0
        
        # Get follow-up metrics
        result_followup = conn.execute("""
            SELECT 
                COUNT(*) as total_followups,
                COUNT(CASE WHEN catatan_followup IS NOT NULL AND catatan_followup != '' THEN 1 END) as completed_followups
            FROM leads 
            WHERE status = 'Follow Up'
        """).fetchone()
        
        total_followups = result_followup['total_followups'] if result_followup else 0
        completed_followups = result_followup['completed_followups'] if result_followup else 0
        
        followup_rate = (completed_followups / total_followups * 100) if total_followups > 0 else 0
        
        # conn.close() removed
        
        return {
            'total_leads': stats['total_leads'],
            'leads_24h': leads_24h,
            'by_status': {'New': leads_24h, 'Follow Up': total_followups},
            'total_followups': total_followups,
            'completed_followups': completed_followups,
            'followup_rate': round(followup_rate, 1),
            'last_updated': datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"Error getting performance metrics: {e}")
        return {
            'total_leads': 0,
            'leads_24h': 0,
            'by_status': {},
            'total_followups': 0,
            'completed_followups': 0,
            'followup_rate': 0,
            'last_updated': datetime.now().isoformat()
        }

@app.route('/')
def dashboard():
    """Serve main dashboard"""
    return render_template('dashboard.html')

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'app': 'LUMINA OS Property Intelligence',
        'version': '1.0.0'
    })

@app.route('/api/test')
def api_test():
    """Test API endpoint"""
    return jsonify({
        'success': True,
        'message': 'LUMINA OS API is working',
        'endpoints': [
            '/api/analytics/summary',
            '/api/analytics/trends',
            '/api/analytics/categories',
            '/api/analytics/forecast',
            '/api/analytics/performance'
        ]
    })

@app.route('/api/analytics/summary', methods=['GET'])
def get_analytics_summary():
    """Get comprehensive analytics summary for dashboard"""
    try:
        # Get all analytics data
        daily_trends = get_daily_trends(days=7)
        category_distribution = get_category_distribution()
        conversion_forecast = get_conversion_forecast()
        performance_metrics = get_performance_metrics()
        
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
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'generated_at': datetime.now().isoformat()
        }), 500

@app.route('/api/analytics/trends', methods=['GET'])
def get_trends_data():
    """Get daily trends data"""
    try:
        days = 7  # Default to 7 days
        daily_trends = get_daily_trends(days=days)
        
        response = {
            'success': True,
            'data': daily_trends,
            'days_analyzed': days,
            'generated_at': datetime.now().isoformat()
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'generated_at': datetime.now().isoformat()
        }), 500

@app.route('/api/analytics/categories', methods=['GET'])
def get_categories_data():
    """Get category distribution data"""
    try:
        category_distribution = get_category_distribution()
        
        response = {
            'success': True,
            'data': category_distribution,
            'generated_at': datetime.now().isoformat()
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'generated_at': datetime.now().isoformat()
        }), 500

@app.route('/api/analytics/forecast', methods=['GET'])
def get_forecast_data():
    """Get conversion forecast data"""
    try:
        conversion_forecast = get_conversion_forecast()
        
        response = {
            'success': True,
            'data': conversion_forecast,
            'generated_at': datetime.now().isoformat()
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'generated_at': datetime.now().isoformat()
        }), 500

@app.route('/api/analytics/performance', methods=['GET'])
def get_performance_data():
    """Get performance metrics data"""
    try:
        performance_metrics = get_performance_metrics()
        
        response = {
            'success': True,
            'data': performance_metrics,
            'generated_at': datetime.now().isoformat()
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'generated_at': datetime.now().isoformat()
        }), 500

@app.route('/api/leads/update/<int:lead_id>', methods=['POST'])
def update_lead(lead_id):
    """Update lead data - Manual Override"""
    try:
        # Get update data from request
        update_data = request.get_json()
        
        if not update_data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Connect to database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if lead exists
        # cursor.execute() removed'SELECT id FROM leads WHERE id = ?', (lead_id,))
        if not cursor.fetchone():
            # conn.close() removed
            return jsonify({
                'success': False,
                'error': 'Lead not found'
            }), 404
        
        # Update lead data
        update_query = """
        UPDATE leads 
        SET nama = ?, email = ?, skor_akhir = ?, kategori = ?, 
            status = ?, sumber = ?, catatan = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """
        
        # cursor.execute() removedupdate_query, (
            update_data.get('nama'),
            update_data.get('email'),
            update_data.get('skor_akhir'),
            update_data.get('kategori'),
            update_data.get('status'),
            update_data.get('sumber'),
            update_data.get('catatan'),
            lead_id
        ))
        
        # conn.commit() removed
        
        # Get updated lead data
        # cursor.execute() removed'SELECT * FROM leads WHERE id = ?', (lead_id,))
        updated_lead = cursor.fetchone()
        
        # conn.close() removed
        
        if updated_lead:
            # Convert to dictionary
            lead_dict = dict(updated_lead)
            
            return jsonify({
                'success': True,
                'message': 'Lead updated successfully',
                'data': lead_dict
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to retrieve updated lead'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/leads/recent', methods=['GET'])
def get_recent_leads():
    """Get recent leads for dashboard"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get recent leads
        # cursor.execute() removed'''
            SELECT id, nama, email, skor_akhir, kategori, status, sumber, catatan, created_at
            FROM leads 
            ORDER BY created_at DESC 
            LIMIT 50
        ''')
        
        leads = []
        for row in cursor.fetchall():
            leads.append({
                'id': row['id'],
                'nama': row['nama'],
                'email': row['email'],
                'skor_akhir': row['skor_akhir'],
                'kategori': row['kategori'],
                'status': row['status'],
                'sumber': row['sumber'],
                'catatan': row['catatan'],
                'created_at': row['created_at']
            })
        
        # conn.close() removed
        
        return jsonify({
            'success': True,
            'data': leads,
            'count': len(leads)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Development server
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '127.0.0.1')
    
    print(f"""
🚀 LUMINA OS Property Intelligence System
📊 Advanced Analytics & Strategic Insights
🌐 Server: http://{host}:{port}
📈 Dashboard: http://{host}:{port}/
🔧 API Test: http://{host}:{port}/api/test
    """)
    
    app.run(host=host, port=port, debug=app.config['DEBUG'])
