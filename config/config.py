"""
Configuration Settings for HUNTER_AGENT_AI_MARKETING_DIGITAL
"""

import os
from datetime import timedelta

# Base Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
KNOWLEDGE_BASE_DIR = os.path.join(BASE_DIR, 'knowledge_base')

# API Configuration
REQUEST_TIMEOUT = 30
MAX_RETRIES = 3
RETRY_DELAY = 1

# Lead Hunting Configuration
MIN_BUDGET_THRESHOLD = 500000000  # 500M IDR
MIN_LAND_SIZE = 200  # sqm
PREFERRED_LOCATIONS = ['Jakarta', 'Tangerang', 'Bekasi', 'Depok', 'Bogor']
PROJECT_TYPES = ['residential', 'commercial', 'mixed_use']

# Market Intelligence Configuration
MAX_LISTINGS_PER_SEARCH = 50
MARKET_TREND_ANALYSIS_PERIOD = 30  # days
COMPETITOR_MONITORING_INTERVAL = 24  # hours

# Scoring Configuration
HOT_LEAD_THRESHOLD = 80
WARM_LEAD_THRESHOLD = 60
COLD_LEAD_THRESHOLD = 0

# Logging Configuration
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE = os.path.join(LOGS_DIR, 'hunter_agent.log')

# Report Configuration
REPORT_RETENTION_DAYS = 30
AUTO_SAVE_REPORTS = True

# Search Configuration
SEARCH_ENGINES = {
    'duckduckgo': {
        'enabled': True,
        'max_results': 20
    },
    'google': {
        'enabled': False,
        'api_key': None,
        'max_results': 20
    }
}

# Social Media Monitoring
SOCIAL_MEDIA_PLATFORMS = {
    'linkedin': {'enabled': True},
    'facebook': {'enabled': True},
    'twitter': {'enabled': False},
    'instagram': {'enabled': False}
}

# Email Configuration (for future notifications)
SMTP_CONFIG = {
    'server': 'smtp.gmail.com',
    'port': 587,
    'username': None,
    'password': None,
    'use_tls': True
}

# Database Configuration (for future use)
DATABASE_CONFIG = {
    'type': 'sqlite',
    'path': os.path.join(BASE_DIR, 'data', 'hunter_agent.db (SQLite - removed))
}

# Performance Configuration
MAX_CONCURRENT_REQUESTS = 5
RATE_LIMIT_DELAY = 1  # seconds between requests

# Development/Testing
DEBUG_MODE = False
MOCK_DATA = True  # Use mock data for development
