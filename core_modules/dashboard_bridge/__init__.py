"""
Dashboard Bridge Module
Connects backend systems with frontend dashboard
"""

__version__ = "1.0.0"
__author__ = "HUNTER_AGENT_AI_MARKETING_DIGITAL"

from .api_connector import APIConnector
from .data_processor import DataProcessor
from .real_time_updater import RealTimeUpdater

__all__ = ['APIConnector', 'DataProcessor', 'RealTimeUpdater']
