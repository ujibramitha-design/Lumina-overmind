"""
API Package Initialization

This module initializes the Flask API package and registers all blueprints.
It serves as the main entry point for all API endpoints in the application.

Author: HUNTER_AGENT_AI_MARKETING_DIGITAL
Version: 1.0.0
"""

from flask import Flask
import logging
import os

# Import blueprints
from .endpoints import leads_bp
from .endpoints.webhook import webhook_bp

def create_api_app():
    """
    Create and configure Flask API application
    
    Returns:
        Flask: Configured Flask application
    """
    app = Flask(__name__)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/api.log'),
            logging.StreamHandler()
        ]
    )
    
    # Register blueprints
    app.register_blueprint(leads_bp)
    app.register_blueprint(webhook_bp)
    
    # Configure app
    app.config['JSON_SORT_KEYS'] = False
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    
    # Add CORS headers if needed
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
    
    return app

# Export blueprint for easy import
__all__ = ['create_api_app', 'leads_bp', 'webhook_bp']
