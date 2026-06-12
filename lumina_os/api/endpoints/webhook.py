"""
Webhook Endpoint Module for Lumina OS
Handles incoming lead data from external platforms

Author: HUNTER_AGENT_AI_MARKETING_DIGITAL
Version: 1.0.0
"""

from flask import Blueprint, request, jsonify
import logging
import os
import sys
from datetime import datetime
from typing import Dict, Any

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

# Import core modules
from core_modules.analytics_engine.predictive_scoring import PredictiveScoringEngine
from core_modules.db_manager import DatabaseManager

# Create blueprint
webhook_bp = Blueprint('webhook', __name__, url_prefix='/api/webhook')

# Configure logging
logger = logging.getLogger(__name__)

# Security configuration
WEBHOOK_TOKEN = os.getenv('LUMINA_WEBHOOK_TOKEN', 'DUMMY-TOKEN-123')

def validate_webhook_request() -> bool:
    """
    Validate incoming webhook request using security token
    
    Returns:
        bool: True if request is valid, False otherwise
    """
    # Check for security token in headers
    auth_header = request.headers.get('X-Lumina-Token')
    
    if not auth_header:
        logger.warning("Webhook request missing X-Lumina-Token header")
        return False
    
    if auth_header != WEBHOOK_TOKEN:
        logger.warning(f"Webhook request with invalid token: {auth_header}")
        return False
    
    return True

def validate_lead_payload(payload: Dict[str, Any]) -> tuple[bool, str]:
    """
    Validate incoming lead payload
    
    Args:
        payload: Dictionary containing lead data
        
    Returns:
        tuple: (is_valid, error_message)
    """
    required_fields = ['nama', 'no_hp']
    
    for field in required_fields:
        if field not in payload or not payload[field]:
            return False, f"Missing required field: {field}"
    
    # Validate phone number format (basic)
    phone = payload['no_hp']
    if not isinstance(phone, str) or len(phone) < 10:
        return False, "Invalid phone number format"
    
    return True, ""

@webhook_bp.route('/incoming-lead', methods=['POST'])
def incoming_lead():
    """
    Handle incoming lead webhook
    
    Expected payload:
    {
        "nama": "John Doe",
        "no_hp": "08123456789",
        "email": "john@example.com",
        "sumber": "Facebook Ads",
        "campaign": "Summer Promo 2024",
        "catatan": "Interested in 2BR unit"
    }
    """
    try:
        # Validate webhook security
        if not validate_webhook_request():
            logger.warning("Unauthorized webhook attempt")
            return jsonify({
                'success': False,
                'error': 'Unauthorized',
                'message': 'Invalid or missing security token'
            }), 401
        
        # Get JSON payload
        payload = request.get_json()
        
        if not payload:
            logger.warning("Webhook received empty payload")
            return jsonify({
                'success': False,
                'error': 'Bad Request',
                'message': 'Empty payload received'
            }), 400
        
        # Validate payload structure
        is_valid, error_message = validate_lead_payload(payload)
        if not is_valid:
            logger.warning(f"Invalid payload: {error_message}")
            return jsonify({
                'success': False,
                'error': 'Validation Error',
                'message': error_message
            }), 400
        
        # Log incoming lead
        logger.info(f"Processing incoming lead: {payload.get('nama', 'Unknown')} from {payload.get('sumber', 'Unknown')}")
        
        # Process lead through Predictive Scoring Engine
        scoring_engine = PredictiveScoringEngine()
        scoring_result = scoring_engine.calculate_final_score(payload)
        
        # Enhance payload with scoring results
        enhanced_lead = {
            **payload,
            'skor_akhir': scoring_result.get('skor_akhir', 0),
            'kategori': scoring_result.get('kategori', 'Cold'),
            'alasan_skor': scoring_result.get('alasan_skor', ''),
            'rekomendasi': scoring_result.get('rekomendasi', ''),
            'next_action': scoring_result.get('next_action', ''),
            'waktu_proses': datetime.now().isoformat(),
            'sumber_data': 'webhook_incoming',
            'status': 'new'
        }
        
        # Save to database
        db_manager = DatabaseManager()
        
        # Prepare data for database insertion
        lead_data = {
            'nama': enhanced_lead['nama'],
            'no_hp': enhanced_lead['no_hp'],
            'email': enhanced_lead.get('email', ''),
            'lokasi': enhanced_lead.get('lokasi', ''),
            'catatan': enhanced_lead.get('catatan', ''),
            'sumber': enhanced_lead.get('sumber', 'Webhook'),
            'skor_akhir': enhanced_lead['skor_akhir'],
            'kategori': enhanced_lead['kategori'],
            'alasan_skor': enhanced_lead['alasan_skor'],
            'rekomendasi': enhanced_lead['rekomendasi'],
            'next_action': enhanced_lead['next_action'],
            'waktu_proses': enhanced_lead['waktu_proses'],
            'sumber_data': enhanced_lead['sumber_data'],
            'status': enhanced_lead['status'],
            'campaign': enhanced_lead.get('campaign', ''),
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        # Insert lead into database
        lead_id = db_manager.insert_lead(lead_data)
        
        if not lead_id:
            logger.error("Failed to save lead to database")
            return jsonify({
                'success': False,
                'error': 'Database Error',
                'message': 'Failed to save lead to database'
            }), 500
        
        # Log successful processing
        logger.info(f"Successfully processed lead {lead_id}: {enhanced_lead['nama']} (Score: {enhanced_lead['skor_akhir']}, Category: {enhanced_lead['kategori']})")
        
        # Return success response
        return jsonify({
            'success': True,
            'message': 'Lead processed successfully',
            'data': {
                'lead_id': lead_id,
                'nama': enhanced_lead['nama'],
                'skor_akhir': enhanced_lead['skor_akhir'],
                'kategori': enhanced_lead['kategori'],
                'waktu_proses': enhanced_lead['waktu_proses']
            }
        }), 201
        
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal Server Error',
            'message': f'An error occurred while processing the webhook: {str(e)}'
        }), 500

@webhook_bp.route('/health', methods=['GET'])
def webhook_health():
    """
    Webhook health check endpoint
    
    Returns:
        JSON: Webhook system status
    """
    try:
        # Test PredictiveScoringEngine
        scoring_engine = PredictiveScoringEngine()
        scoring_status = scoring_engine.get_status()
        
        # Test DatabaseManager
        db_manager = DatabaseManager()
        db_status = db_manager.get_connection_status()
        
        return jsonify({
            'success': True,
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'components': {
                'scoring_engine': scoring_status,
                'database': db_status,
                'security': 'enabled'
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Webhook health check failed: {str(e)}")
        return jsonify({
            'success': False,
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@webhook_bp.route('/test', methods=['POST'])
def test_webhook():
    """
    Test webhook endpoint with sample data
    
    Returns:
        JSON: Test results
    """
    try:
        # Validate webhook security
        if not validate_webhook_request():
            return jsonify({
                'success': False,
                'error': 'Unauthorized',
                'message': 'Invalid or missing security token'
            }), 401
        
        # Sample test data
        test_payload = {
            'nama': 'Test User',
            'no_hp': '08123456789',
            'email': 'test@example.com',
            'sumber': 'Test Webhook',
            'campaign': 'Test Campaign',
            'catatan': 'This is a test lead'
        }
        
        # Process test lead
        scoring_engine = PredictiveScoringEngine()
        scoring_result = scoring_engine.calculate_final_score(test_payload)
        
        return jsonify({
            'success': True,
            'message': 'Webhook test successful',
            'test_data': test_payload,
            'scoring_result': scoring_result,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Webhook test failed: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Test Failed',
            'message': str(e)
        }), 500

# Error handlers
@webhook_bp.errorhandler(404)
def webhook_not_found(error):
    return jsonify({
        'success': False,
        'error': 'Not Found',
        'message': 'Webhook endpoint not found'
    }), 404

@webhook_bp.errorhandler(405)
def webhook_method_not_allowed(error):
    return jsonify({
        'success': False,
        'error': 'Method Not Allowed',
        'message': 'HTTP method not allowed for this endpoint'
    }), 405

@webhook_bp.errorhandler(500)
def webhook_internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal Server Error',
        'message': 'An internal server error occurred'
    }), 500

# Export blueprint
__all__ = ['webhook_bp']
