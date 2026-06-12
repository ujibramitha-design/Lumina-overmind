"""
Leads API Endpoints

This module provides RESTful API endpoints for lead management operations.
It serves as the bridge between the SQLite database and the web frontend,
offering CRUD operations with proper validation, pagination, and error handling.

Author: HUNTER_AGENT_AI_MARKETING_DIGITAL
Version: 1.0.0
"""

from flask import Blueprint, request, jsonify
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime

# Import database manager
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from core_modules.db_manager import DatabaseManager

# Create Blueprint
leads_bp = Blueprint('leads', __name__, url_prefix='/api/leads')

# Configure logging
logger = logging.getLogger(__name__)

# Initialize database manager
db_manager = DatabaseManager()

# Standard response format
def create_response(status: str, data: Any = None, message: str = None, code: int = 200):
    """
    Create standardized JSON response
    
    Args:
        status: 'success' or 'error'
        data: Response data (optional)
        message: Response message (optional)
        code: HTTP status code
    
    Returns:
        Flask JSON response
    """
    response = {'status': status}
    
    if data is not None:
        response['data'] = data
    if message is not None:
        response['message'] = message
    
    return jsonify(response), code

def validate_lead_data(data: Dict) -> tuple:
    """
    Validate lead data for POST/PUT operations
    
    Args:
        data: Dictionary containing lead data
    
    Returns:
        tuple: (is_valid, error_message)
    """
    required_fields = ['nama', 'no_hp']
    
    for field in required_fields:
        if field not in data or not data[field] or not data[field].strip():
            return False, f"Field '{field}' is required and cannot be empty"
    
    # Validate phone number format (basic Indonesian format)
    phone = data['no_hp'].strip()
    if not phone.startswith(('+62', '08')):
        return False, "Phone number must start with '+62' or '08'"
    
    if len(phone) < 10 or len(phone) > 15:
        return False, "Phone number must be between 10-15 digits"
    
    return True, None

@leads_bp.route('/', methods=['GET'])
def get_leads():
    """
    Get all leads with pagination and filtering support
    
    Query Parameters:
        limit: Number of leads to return (default: 50, max: 100)
        offset: Number of leads to skip (default: 0)
        status: Filter by lead status (optional)
        source: Filter by lead source (optional)
        search: Search in nama, no_hp, or lokasi fields (optional)
        sort_by: Field to sort by (default: created_at)
        sort_order: Sort order 'asc' or 'desc' (default: desc)
    
    Returns:
        JSON response with leads list and pagination info
    """
    try:
        # Get query parameters
        limit = min(int(request.args.get('limit', 50)), 100)  # Max 100
        offset = max(int(request.args.get('offset', 0)), 0)
        status_filter = request.args.get('status', '').strip()
        source_filter = request.args.get('source', '').strip()
        search_query = request.args.get('search', '').strip()
        sort_by = request.args.get('sort_by', 'created_at').strip()
        sort_order = request.args.get('sort_order', 'desc').strip().lower()
        
        # Validate sort order
        if sort_order not in ['asc', 'desc']:
            sort_order = 'desc'
        
        # Validate sort field (prevent SQL injection)
        valid_sort_fields = ['created_at', 'nama', 'skor_ai', 'status', 'sumber', 'lokasi']
        if sort_by not in valid_sort_fields:
            sort_by = 'created_at'
        
        # Connect to database
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        # Build base query
        base_query = "SELECT * FROM leads WHERE 1=1"
        params = []
        
        # Add filters
        if status_filter:
            base_query += " AND status = ?"
            params.append(status_filter)
        
        if source_filter:
            base_query += " AND sumber = ?"
            params.append(source_filter)
        
        if search_query:
            base_query += " AND (nama LIKE ? OR no_hp LIKE ? OR lokasi LIKE ?)"
            search_param = f"%{search_query}%"
            params.extend([search_param, search_param, search_param])
        
        # Add sorting and pagination
        base_query += f" ORDER BY {sort_by} {sort_order.upper()}"
        base_query += " LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
        # Execute query
        # cursor.execute() removedbase_query, params)
        leads = cursor.fetchall()
        
        # Get column names
        columns = [description[0] for description in cursor.description]
        
        # Convert to list of dictionaries
        leads_list = []
        for lead in leads:
            lead_dict = dict(zip(columns, lead))
            # Convert timestamp to string if needed
            if 'created_at' in lead_dict and lead_dict['created_at']:
                lead_dict['created_at'] = str(lead_dict['created_at'])
            leads_list.append(lead_dict)
        
        # Get total count for pagination
        count_query = "SELECT COUNT(*) FROM leads WHERE 1=1"
        count_params = []
        
        if status_filter:
            count_query += " AND status = ?"
            count_params.append(status_filter)
        
        if source_filter:
            count_query += " AND sumber = ?"
            count_params.append(source_filter)
        
        if search_query:
            count_query += " AND (nama LIKE ? OR no_hp LIKE ? OR lokasi LIKE ?)"
            search_param = f"%{search_query}%"
            count_params.extend([search_param, search_param, search_param])
        
        # cursor.execute() removedcount_query, count_params)
        total_count = cursor.fetchone()[0]
        
        # conn.close() removed
        
        # Prepare response data
        response_data = {
            'leads': leads_list,
            'pagination': {
                'total': total_count,
                'limit': limit,
                'offset': offset,
                'has_next': offset + limit < total_count,
                'has_prev': offset > 0
            },
            'filters_applied': {
                'status': status_filter if status_filter else None,
                'source': source_filter if source_filter else None,
                'search': search_query if search_query else None
            }
        }
        
        logger.info(f"Retrieved {len(leads_list)} leads (total: {total_count})")
        return create_response('success', response_data, f"Successfully retrieved {len(leads_list)} leads")
        
    except sqlite3.Error as e:
        logger.error(f"Database error in get_leads: {e}")
        return create_response('error', message="Database error occurred", code=500)
    
    except Exception as e:
        logger.error(f"Unexpected error in get_leads: {e}")
        return create_response('error', message="Internal server error", code=500)

@leads_bp.route('/<int:lead_id>', methods=['GET'])
def get_lead(lead_id: int):
    """
    Get specific lead by ID
    
    Args:
        lead_id: ID of the lead to retrieve
    
    Returns:
        JSON response with lead details or error message
    """
    try:
        if lead_id <= 0:
            return create_response('error', message="Invalid lead ID", code=400)
        
        # Connect to database
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        # Execute query
        # cursor.execute() removed"SELECT * FROM leads WHERE id = ?", (lead_id,))
        lead = cursor.fetchone()
        
        # conn.close() removed
        
        if not lead:
            return create_response('error', message=f"Lead with ID {lead_id} not found", code=404)
        
        # Convert to dictionary
        columns = [description[0] for description in cursor.description]
        lead_dict = dict(zip(columns, lead))
        
        # Convert timestamp to string if needed
        if 'created_at' in lead_dict and lead_dict['created_at']:
            lead_dict['created_at'] = str(lead_dict['created_at'])
        
        logger.info(f"Retrieved lead ID: {lead_id}")
        return create_response('success', lead_dict, f"Successfully retrieved lead {lead_id}")
        
    except sqlite3.Error as e:
        logger.error(f"Database error in get_lead: {e}")
        return create_response('error', message="Database error occurred", code=500)
    
    except Exception as e:
        logger.error(f"Unexpected error in get_lead: {e}")
        return create_response('error', message="Internal server error", code=500)

@leads_bp.route('/', methods=['POST'])
def create_lead():
    """
    Create a new lead
    
    Expected JSON payload:
        {
            "nama": "John Doe",
            "no_hp": "+62812345678",
            "email": "john@example.com",
            "lokasi": "Jakarta",
            "sumber": "Website",
            "catatan": "Interested in property",
            "skor_ai": 8
        }
    
    Returns:
        JSON response with created lead details or error message
    """
    try:
        # Get JSON data
        data = request.get_json()
        
        if not data:
            return create_response('error', message="No JSON data provided", code=400)
        
        # Validate required fields
        is_valid, error_message = validate_lead_data(data)
        if not is_valid:
            return create_response('error', message=error_message, code=400)
        
        # Prepare lead data
        lead_data = {
            'nama': data['nama'].strip(),
            'no_hp': data['no_hp'].strip(),
            'email': data.get('email', '').strip(),
            'lokasi': data.get('lokasi', '').strip(),
            'sumber': data.get('sumber', 'API').strip(),
            'catatan': data.get('catatan', '').strip(),
            'skor_ai': int(data.get('skor_ai', 0)),
            'status': data.get('status', 'New').strip(),
            'validation_status': data.get('validation_status', 'pending').strip()
        }
        
        # Validate score range
        if lead_data['skor_ai'] < 0 or lead_data['skor_ai'] > 10:
            return create_response('error', message="AI score must be between 0 and 10", code=400)
        
        # Insert lead
        lead_id = db_manager.insert_lead(lead_data)
        
        if not lead_id:
            return create_response('error', message="Failed to create lead", code=500)
        
        # Get the created lead
        created_lead = db_manager.get_lead_by_id(lead_id)
        
        if created_lead:
            # Convert timestamp to string
            if 'created_at' in created_lead and created_lead['created_at']:
                created_lead['created_at'] = str(created_lead['created_at'])
            
            logger.info(f"Created new lead with ID: {lead_id}")
            return create_response('success', created_lead, f"Successfully created lead {lead_id}", 201)
        else:
            return create_response('error', message="Lead created but failed to retrieve details", code=500)
        
    except ValueError as e:
        logger.error(f"Value error in create_lead: {e}")
        return create_response('error', message="Invalid data format", code=400)
    
    except sqlite3.Error as e:
        logger.error(f"Database error in create_lead: {e}")
        return create_response('error', message="Database error occurred", code=500)
    
    except Exception as e:
        logger.error(f"Unexpected error in create_lead: {e}")
        return create_response('error', message="Internal server error", code=500)

@leads_bp.route('/<int:lead_id>', methods=['PUT'])
def update_lead(lead_id: int):
    """
    Update an existing lead
    
    Args:
        lead_id: ID of the lead to update
    
    Expected JSON payload (partial update supported):
        {
            "status": "Follow Up",
            "catatan": "Updated notes",
            "skor_ai": 9,
            "validation_status": "qualified"
        }
    
    Returns:
        JSON response with updated lead details or error message
    """
    try:
        if lead_id <= 0:
            return create_response('error', message="Invalid lead ID", code=400)
        
        # Get JSON data
        data = request.get_json()
        
        if not data:
            return create_response('error', message="No JSON data provided", code=400)
        
        # Check if lead exists
        existing_lead = db_manager.get_lead_by_id(lead_id)
        if not existing_lead:
            return create_response('error', message=f"Lead with ID {lead_id} not found", code=404)
        
        # Prepare update data (only include provided fields)
        update_data = {}
        
        # Allowed fields for update
        updatable_fields = ['nama', 'no_hp', 'email', 'lokasi', 'sumber', 'catatan', 'skor_ai', 'status', 'validation_status']
        
        for field in updatable_fields:
            if field in data:
                if field in ['nama', 'no_hp', 'email', 'lokasi', 'sumber', 'catatan', 'status', 'validation_status']:
                    update_data[field] = str(data[field]).strip()
                elif field == 'skor_ai':
                    score = int(data[field])
                    if score < 0 or score > 10:
                        return create_response('error', message="AI score must be between 0 and 10", code=400)
                    update_data[field] = score
        
        if not update_data:
            return create_response('error', message="No valid fields provided for update", code=400)
        
        # Validate phone if being updated
        if 'no_hp' in update_data:
            phone = update_data['no_hp']
            if not phone.startswith(('+62', '08')):
                return create_response('error', message="Phone number must start with '+62' or '08'", code=400)
            if len(phone) < 10 or len(phone) > 15:
                return create_response('error', message="Phone number must be between 10-15 digits", code=400)
        
        # Update lead
        success = db_manager.update_lead(lead_id, update_data)
        
        if not success:
            return create_response('error', message="Failed to update lead", code=500)
        
        # Get updated lead
        updated_lead = db_manager.get_lead_by_id(lead_id)
        
        if updated_lead:
            # Convert timestamp to string
            if 'created_at' in updated_lead and updated_lead['created_at']:
                updated_lead['created_at'] = str(updated_lead['created_at'])
            if 'updated_at' in updated_lead and updated_lead['updated_at']:
                updated_lead['updated_at'] = str(updated_lead['updated_at'])
            
            logger.info(f"Updated lead ID: {lead_id}")
            return create_response('success', updated_lead, f"Successfully updated lead {lead_id}")
        else:
            return create_response('error', message="Lead updated but failed to retrieve details", code=500)
        
    except ValueError as e:
        logger.error(f"Value error in update_lead: {e}")
        return create_response('error', message="Invalid data format", code=400)
    
    except sqlite3.Error as e:
        logger.error(f"Database error in update_lead: {e}")
        return create_response('error', message="Database error occurred", code=500)
    
    except Exception as e:
        logger.error(f"Unexpected error in update_lead: {e}")
        return create_response('error', message="Internal server error", code=500)

@leads_bp.route('/<int:lead_id>', methods=['DELETE'])
def delete_lead(lead_id: int):
    """
    Delete a lead (soft delete by marking as deleted)
    
    Args:
        lead_id: ID of the lead to delete
    
    Returns:
        JSON response confirming deletion or error message
    """
    try:
        if lead_id <= 0:
            return create_response('error', message="Invalid lead ID", code=400)
        
        # Check if lead exists
        existing_lead = db_manager.get_lead_by_id(lead_id)
        if not existing_lead:
            return create_response('error', message=f"Lead with ID {lead_id} not found", code=404)
        
        # Soft delete by updating status
        success = db_manager.update_lead(lead_id, {'status': 'Deleted'})
        
        if not success:
            return create_response('error', message="Failed to delete lead", code=500)
        
        logger.info(f"Deleted lead ID: {lead_id}")
        return create_response('success', {'deleted_id': lead_id}, f"Successfully deleted lead {lead_id}")
        
    except sqlite3.Error as e:
        logger.error(f"Database error in delete_lead: {e}")
        return create_response('error', message="Database error occurred", code=500)
    
    except Exception as e:
        logger.error(f"Unexpected error in delete_lead: {e}")
        return create_response('error', message="Internal server error", code=500)

@leads_bp.route('/stats', methods=['GET'])
def get_leads_stats():
    """
    Get leads statistics and analytics
    
    Returns:
        JSON response with leads statistics
    """
    try:
        # Connect to database
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        # Get total leads
        # cursor.execute() removed"SELECT COUNT(*) FROM leads WHERE status != 'Deleted'")
        total_leads = cursor.fetchone()[0]
        
        # Get leads by status
        # cursor.execute() removed"""
            SELECT status, COUNT(*) as count 
            FROM leads 
            WHERE status != 'Deleted'
            GROUP BY status
            ORDER BY count DESC
        """)
        status_stats = dict(cursor.fetchall())
        
        # Get leads by source
        # cursor.execute() removed"""
            SELECT sumber, COUNT(*) as count 
            FROM leads 
            WHERE status != 'Deleted'
            GROUP BY sumber
            ORDER BY count DESC
            LIMIT 10
        """)
        source_stats = dict(cursor.fetchall())
        
        # Get average AI score
        # cursor.execute() removed"""
            SELECT AVG(skor_ai) as avg_score 
            FROM leads 
            WHERE status != 'Deleted' AND skor_ai > 0
        """)
        avg_score_result = cursor.fetchone()
        avg_score = round(float(avg_score_result[0]), 2) if avg_score_result[0] else 0
        
        # Get recent leads (last 7 days)
        # cursor.execute() removed"""
            SELECT COUNT(*) 
            FROM leads 
            WHERE created_at >= date('now', '-7 days') AND status != 'Deleted'
        """)
        recent_leads = cursor.fetchone()[0]
        
        # Get high value leads (score >= 8)
        # cursor.execute() removed"""
            SELECT COUNT(*) 
            FROM leads 
            WHERE skor_ai >= 8 AND status != 'Deleted'
        """)
        high_value_leads = cursor.fetchone()[0]
        
        # conn.close() removed
        
        # Prepare response
        stats_data = {
            'total_leads': total_leads,
            'status_distribution': status_stats,
            'source_distribution': source_stats,
            'average_ai_score': avg_score,
            'recent_leads_7_days': recent_leads,
            'high_value_leads': high_value_leads,
            'high_value_percentage': round((high_value_leads / total_leads * 100), 2) if total_leads > 0 else 0
        }
        
        logger.info("Retrieved leads statistics")
        return create_response('success', stats_data, "Successfully retrieved leads statistics")
        
    except sqlite3.Error as e:
        logger.error(f"Database error in get_leads_stats: {e}")
        return create_response('error', message="Database error occurred", code=500)
    
    except Exception as e:
        logger.error(f"Unexpected error in get_leads_stats: {e}")
        return create_response('error', message="Internal server error", code=500)

# Error handlers
@leads_bp.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return create_response('error', message="Resource not found", code=404)

@leads_bp.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return create_response('error', message="Method not allowed", code=405)

@leads_bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return create_response('error', message="Internal server error", code=500)

# Health check endpoint
@leads_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for the leads API
    
    Returns:
        JSON response with API status
    """
    try:
        # Test database connection
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        # cursor.execute() removed"SELECT 1")
        cursor.fetchone()
        # conn.close() removed
        
        health_data = {
            'status': 'healthy',
            'database': 'connected',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0'
        }
        
        return create_response('success', health_data, "Leads API is healthy")
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return create_response('error', message="Service unavailable", code=503)

# Register error handlers
@leads_bp.app_errorhandler(Exception)
def handle_exception(e):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {e}")
    return create_response('error', message="An unexpected error occurred", code=500)
