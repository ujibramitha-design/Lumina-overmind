"""
API Endpoints Package Initialization

This module initializes the API endpoints package and exports all blueprints.

Author: HUNTER_AGENT_AI_MARKETING_DIGITAL
Version: 1.0.0
"""

# Import all endpoint blueprints
from .leads import leads_bp

# Export blueprints for registration
__all__ = ['leads_bp']
