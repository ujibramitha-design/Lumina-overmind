"""
HUNTER_AGENT_AI_MARKETING_DIGITAL API
Main API entry point for the web dashboard
"""

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import json
import os
from datetime import datetime, timedelta
import random

app = Flask(__name__)
CORS(app)

# Configuration
DATABASE_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'leads.db (SQLite - removed))
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def api_info():
    """API information and available endpoints"""
    return jsonify({
        'name': 'HUNTER_AGENT_AI_MARKETING_DIGITAL API',
        'version': '1.0.0',
        'description': 'API for property marketing and lead management system',
        'endpoints': {
            'dashboard': '/api/dashboard',
            'leads': '/api/leads',
            'analytics': '/api/analytics',
            'market_intelligence': '/api/market-intelligence',
            'system_status': '/api/system/status'
        }
    })

@app.route('/api/dashboard')
def dashboard_data():
    """Get dashboard metrics and KPIs"""
    try:
        # Get data from database
        conn = # SQLite connection removed
        cursor = conn.cursor()
        
        # Total leads
        # cursor.execute() removed"SELECT COUNT(*) FROM leads")
        total_leads = cursor.fetchone()[0]
        
        # New leads (last 7 days)
        seven_days_ago = datetime.now() - timedelta(days=7)
        # cursor.execute() removed"SELECT COUNT(*) FROM leads WHERE created_at >= ?", (seven_days_ago,))
        new_leads = cursor.fetchone()[0]
        
        # Conversion rate
        # cursor.execute() removed"SELECT COUNT(*) FROM leads WHERE status = 'converted'")
        converted_leads = cursor.fetchone()[0]
        conversion_rate = (converted_leads / total_leads * 100) if total_leads > 0 else 0
        
        # Average score
        # cursor.execute() removed"SELECT AVG(score) FROM leads WHERE score IS NOT NULL")
        avg_score_result = cursor.fetchone()[0]
        avg_score = round(avg_score_result, 1) if avg_score_result else 0
        
        # conn.close() removed
        
        return jsonify({
            'totalLeads': total_leads,
            'newLeads': new_leads,
            'conversionRate': round(conversion_rate, 1),
            'roi': random.randint(280, 350),  # Simulated ROI
            'satisfaction': round(random.uniform(4.2, 4.8), 1),  # Simulated satisfaction
            'averageScore': avg_score,
            'lastUpdated': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/leads')
def get_leads():
    """Get all leads with pagination and filtering"""
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 25))
        status_filter = request.args.get('status', '')
        score_filter = request.args.get('score', '')
        search = request.args.get('search', '')
        
        conn = # SQLite connection removed
        cursor = conn.cursor()
        
        # Build query
        query = "SELECT * FROM leads WHERE 1=1"
        params = []
        
        if status_filter:
            query += " AND status = ?"
            params.append(status_filter)
        
        if score_filter:
            if score_filter == 'high':
                query += " AND score >= 8"
            elif score_filter == 'medium':
                query += " AND score >= 5 AND score < 8"
            elif score_filter == 'low':
                query += " AND score < 5"
        
        if search:
            query += " AND (title LIKE ? OR content_snippet LIKE ?)"
            params.extend([f'%{search}%', f'%{search}%'])
        
        # Count total
        count_query = query.replace("SELECT *", "SELECT COUNT(*)")
        # cursor.execute() removedcount_query, params)
        total_count = cursor.fetchone()[0]
        
        # Add pagination
        offset = (page - 1) * per_page
        query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
        params.extend([per_page, offset])
        
        # cursor.execute() removedquery, params)
        columns = [description[0] for description in cursor.description]
        leads = []
        
        for row in cursor.fetchall():
            lead = dict(zip(columns, row))
            # Convert datetime to string
            if lead.get('created_at'):
                lead['created_at'] = datetime.fromisoformat(lead['created_at']).isoformat()
            if lead.get('updated_at'):
                lead['updated_at'] = datetime.fromisoformat(lead['updated_at']).isoformat()
            leads.append(lead)
        
        # conn.close() removed
        
        return jsonify({
            'leads': leads,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total_count,
                'pages': (total_count + per_page - 1) // per_page
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/leads/<int:lead_id>')
def get_lead(lead_id):
    """Get specific lead details"""
    try:
        conn = # SQLite connection removed
        cursor = conn.cursor()
        
        # cursor.execute() removed"SELECT * FROM leads WHERE id = ?", (lead_id,))
        row = cursor.fetchone()
        
        if not row:
            return jsonify({'error': 'Lead not found'}), 404
        
        columns = [description[0] for description in cursor.description]
        lead = dict(zip(columns, row))
        
        # Add mock activities
        lead['activities'] = [
            {
                'timestamp': lead.get('created_at', datetime.now().isoformat()),
                'description': 'Lead created from web scraping'
            },
            {
                'timestamp': datetime.now().isoformat(),
                'description': 'Lead scored and categorized'
            }
        ]
        
        # conn.close() removed
        
        return jsonify(lead)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/leads/<int:lead_id>', methods=['PUT'])
def update_lead(lead_id):
    """Update lead information"""
    try:
        data = request.get_json()
        
        conn = # SQLite connection removed
        cursor = conn.cursor()
        
        # Update lead
        update_fields = []
        params = []
        
        for field in ['name', 'phone', 'email', 'status', 'score', 'notes']:
            if field in data:
                update_fields.append(f"{field} = ?")
                params.append(data[field])
        
        if update_fields:
            update_fields.append("updated_at = ?")
            params.append(datetime.now().isoformat())
            params.append(lead_id)
            
            query = f"UPDATE leads SET {', '.join(update_fields)} WHERE id = ?"
            # cursor.execute() removedquery, params)
            # conn.commit() removed
        
        # conn.close() removed
        
        return jsonify({'success': True, 'message': 'Lead updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/leads/<int:lead_id>', methods=['DELETE'])
def delete_lead(lead_id):
    """Delete a lead"""
    try:
        conn = # SQLite connection removed
        cursor = conn.cursor()
        
        # cursor.execute() removed"DELETE FROM leads WHERE id = ?", (lead_id,))
        # conn.commit() removed
        
        # conn.close() removed
        
        return jsonify({'success': True, 'message': 'Lead deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics')
def get_analytics():
    """Get analytics data"""
    try:
        conn = # SQLite connection removed
        cursor = conn.cursor()
        
        # Lead trends over time
        # cursor.execute() removed"""
            SELECT DATE(created_at) as date, COUNT(*) as count 
            FROM leads 
            WHERE created_at >= date('now', '-30 days')
            GROUP BY DATE(created_at)
            ORDER BY date
        """)
        lead_trends = [{'date': row[0], 'count': row[1]} for row in cursor.fetchall()]
        
        # Lead sources
        # cursor.execute() removed"SELECT source, COUNT(*) as count FROM leads GROUP BY source")
        lead_sources = [{'source': row[0], 'count': row[1]} for row in cursor.fetchall()]
        
        # Lead scores distribution
        # cursor.execute() removed"""
            SELECT 
                CASE 
                    WHEN score >= 8 THEN 'High'
                    WHEN score >= 5 THEN 'Medium'
                    ELSE 'Low'
                END as category,
                COUNT(*) as count
            FROM leads 
            WHERE score IS NOT NULL
            GROUP BY category
        """)
        score_distribution = [{'category': row[0], 'count': row[1]} for row in cursor.fetchall()]
        
        # Conversion funnel
        # cursor.execute() removed"SELECT status, COUNT(*) as count FROM leads GROUP BY status")
        conversion_funnel = [{'status': row[0], 'count': row[1]} for row in cursor.fetchall()]
        
        # conn.close() removed
        
        return jsonify({
            'leadTrends': lead_trends,
            'leadSources': lead_sources,
            'scoreDistribution': score_distribution,
            'conversionFunnel': conversion_funnel,
            'generatedAt': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/market-intelligence')
def get_market_intelligence():
    """Get market intelligence data"""
    try:
        # Simulate market intelligence data
        intelligence = {
            'marketOverview': {
                'averagePrice': 450000000,
                'priceTrend': '+5.2%',
                'inventoryLevel': 1250,
                'marketHealth': 'Good'
            },
            'competitorAnalysis': {
                'totalCompetitors': 12,
                'averageCompetitorPrice': 465000000,
                'priceGap': '-3.2%',
                'marketShare': 8.5
            },
            'trendingKeywords': [
                'rumah subsidi serang',
                'KPR murah',
                'perumahan cicilan ringan',
                'cluster baru serang'
            ],
            'hotAreas': [
                {'name': 'Cipocok Jaya', 'growth': '+12%', 'avgPrice': 420000000},
                {'name': 'Kota Serang', 'growth': '+8%', 'avgPrice': 550000000},
                {'name': 'Serang Utara', 'growth': '+15%', 'avgPrice': 380000000}
            ],
            'recommendations': [
                'Focus on affordable housing segment',
                'Increase marketing in Cipocok Jaya area',
                'Highlight KPR assistance programs'
            ]
        }
        
        return jsonify(intelligence)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/system/status')
def system_status():
    """Get system status and health"""
    try:
        status = {
            'overall': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'components': {
                'database': {
                    'status': 'healthy',
                    'connection': 'active',
                    'size': os.path.getsize(DATABASE_PATH) if os.path.exists(DATABASE_PATH) else 0
                },
                'leadHunter': {
                    'status': 'active',
                    'lastRun': datetime.now().isoformat(),
                    'successRate': 98.5
                },
                'marketIntelligence': {
                    'status': 'active',
                    'lastUpdate': datetime.now().isoformat(),
                    'dataFreshness': 'fresh'
                },
                'analytics': {
                    'status': 'healthy',
                    'processingTime': '< 1s'
                }
            },
            'metrics': {
                'uptime': '99.9%',
                'responseTime': '120ms',
                'errorRate': '0.1%',
                'activeUsers': 3
            }
        }
        
        return jsonify(status)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export/leads')
def export_leads():
    """Export leads data"""
    try:
        format_type = request.args.get('format', 'csv')
        
        conn = # SQLite connection removed
        cursor = conn.cursor()
        
        # cursor.execute() removed"SELECT * FROM leads")
        columns = [description[0] for description in cursor.description]
        leads = cursor.fetchall()
        
        # conn.close() removed
        
        if format_type == 'csv':
            import csv
            import io
            
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(columns)
            writer.writerows(leads)
            
            output.seek(0)
            return send_file(
                io.BytesIO(output.getvalue().encode()),
                mimetype='text/csv',
                as_attachment=True,
                download_name='leads_export.csv'
            )
        elif format_type == 'json':
            leads_data = []
            for lead in leads:
                leads_data.append(dict(zip(columns, lead)))
            
            return send_file(
                io.BytesIO(json.dumps(leads_data, indent=2).encode()),
                mimetype='application/json',
                as_attachment=True,
                download_name='leads_export.json'
            )
        else:
            return jsonify({'error': 'Unsupported format'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/real-time-updates')
def real_time_updates():
    """Server-sent events for real-time updates"""
    def generate():
        try:
            while True:
                # Simulate real-time updates
                update = {
                    'type': random.choice(['new_lead', 'conversion', 'system_alert', 'milestone']),
                    'timestamp': datetime.now().isoformat(),
                    'data': {
                        'message': 'System update',
                        'value': random.randint(1, 100)
                    }
                }
                
                yield f"data: {json.dumps(update)}\n\n"
                
                # Wait before next update
                import time
                time.sleep(30)  # 30 seconds
                
        except GeneratorExit:
            pass
    
    return app.response_class(
        generate(),
        mimetype='text/event-stream'
    )

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
