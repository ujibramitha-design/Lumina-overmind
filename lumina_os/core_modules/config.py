"""
LUMINA OS Configuration Module
Enterprise Security & Professional Operations

Author: HUNTER_AGENT_AI_MARKETING_DIGITAL
Version: 1.0.0
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for LUMINA OS Enterprise"""
    
    # Dashboard Security
    DASHBOARD_PASSWORD = os.getenv('DASHBOARD_PASSWORD', 'LuminaOS2026')
    SESSION_TIMEOUT = int(os.getenv('SESSION_TIMEOUT', '3600'))  # 1 hour default
    
    # Social Media API Credentials (Blueprint for Deep Comment Analysis)
    SOCIAL_MEDIA_CREDENTIALS = {
        'facebook': {
            'access_token': os.getenv('FB_ACCESS_TOKEN', ''),
            'app_id': os.getenv('FB_APP_ID', ''),
            'app_secret': os.getenv('FB_APP_SECRET', ''),
            'webhook_secret': os.getenv('FB_WEBHOOK_SECRET', '')
        },
        'instagram': {
            'access_token': os.getenv('INSTAGRAM_ACCESS_TOKEN', ''),
            'business_account_id': os.getenv('INSTAGRAM_BUSINESS_ID', '')
        },
        'tiktok': {
            'api_key': os.getenv('TIKTOK_API_KEY', ''),
            'client_key': os.getenv('TIKTOK_CLIENT_KEY', ''),
            'client_secret': os.getenv('TIKTOK_CLIENT_SECRET', '')
        },
        'twitter': {
            'bearer_token': os.getenv('TWITTER_BEARER_TOKEN', ''),
            'consumer_key': os.getenv('TWITTER_CONSUMER_KEY', ''),
            'consumer_secret': os.getenv('TWITTER_CONSUMER_SECRET', ''),
            'access_token': os.getenv('TWITTER_ACCESS_TOKEN', ''),
            'access_token_secret': os.getenv('TWITTER_ACCESS_TOKEN_SECRET', '')
        },
        'youtube': {
            'api_key': os.getenv('YOUTUBE_API_KEY', ''),
            'client_id': os.getenv('YOUTUBE_CLIENT_ID', ''),
            'client_secret': os.getenv('YOUTUBE_CLIENT_SECRET', '')
        },
        'apify': {
            'token': os.getenv('APIFY_TOKEN', ''),
            'actor_id': os.getenv('APIFY_ACTOR_ID', '')
        },
        'reddit': {
            'client_id': os.getenv('REDDIT_CLIENT_ID', ''),
            'client_secret': os.getenv('REDDIT_CLIENT_SECRET', ''),
            'user_agent': os.getenv('REDDIT_USER_AGENT', 'HUNTER_AGENT_AI_MARKETING_DIGITAL/1.0')
        }
    }
    
    # AI Service Credentials
    AI_CREDENTIALS = {
        'gemini_api_key': os.getenv('GEMINI_API_KEY', ''),
        'openai_api_key': os.getenv('OPENAI_API_KEY', ''),
        'anthropic_api_key': os.getenv('ANTHROPIC_API_KEY', ''),
        'azure_openai_endpoint': os.getenv('AZURE_OPENAI_ENDPOINT', ''),
        'azure_openai_key': os.getenv('AZURE_OPENAI_KEY', '')
    }
    
    # Deep Comment Analysis Settings
    COMMENT_ANALYSIS_CONFIG = {
        'max_comments_per_post': int(os.getenv('MAX_COMMENTS_PER_POST', '200')),
        'intent_score_threshold': int(os.getenv('INTENT_SCORE_THRESHOLD', '75')),
        'enable_ai_profiling': os.getenv('ENABLE_AI_PROFILING', 'true').lower() == 'true',
        'profiling_confidence_threshold': int(os.getenv('PROFILING_CONFIDENCE_THRESHOLD', '70')),
        'comment_retention_days': int(os.getenv('COMMENT_RETENTION_DAYS', '30')),
        'enable_real_time_analysis': os.getenv('ENABLE_REAL_TIME_ANALYSIS', 'true').lower() == 'true',
        'batch_size': int(os.getenv('COMMENT_ANALYSIS_BATCH_SIZE', '50'))
    }
    
    # Rate Limiting & API Quotas
    RATE_LIMITING = {
        'facebook': {
            'requests_per_hour': int(os.getenv('FB_RATE_LIMIT', '200')),
            'comments_per_request': int(os.getenv('FB_COMMENTS_PER_REQUEST', '100'))
        },
        'instagram': {
            'requests_per_hour': int(os.getenv('IG_RATE_LIMIT', '200')),
            'comments_per_request': int(os.getenv('IG_COMMENTS_PER_REQUEST', '50'))
        },
        'tiktok': {
            'requests_per_hour': int(os.getenv('TT_RATE_LIMIT', '100')),
            'comments_per_request': int(os.getenv('TT_COMMENTS_PER_REQUEST', '20'))
        },
        'twitter': {
            'requests_per_hour': int(os.getenv('TW_RATE_LIMIT', '300')),
            'comments_per_request': int(os.getenv('TW_COMMENTS_PER_REQUEST', '100'))
        },
        'youtube': {
            'requests_per_hour': int(os.getenv('YT_RATE_LIMIT', '10000')),
            'comments_per_request': int(os.getenv('YT_COMMENTS_PER_REQUEST', '50'))
        }
    }
    
    # Database Configuration
    DATABASE_PATH = os.getenv('DATABASE_PATH', '../data/leads.db (SQLite - removed))
    BACKUP_FOLDER = os.getenv('BACKUP_FOLDER', '../backups')
    AUTO_BACKUP = os.getenv('AUTO_BACKUP_ENABLED', 'true').lower() == 'true'
    
    # Application Settings
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    SECRET_KEY = os.getenv('SECRET_KEY', 'lumina-os-enterprise-secret-key-2026')
    HOST = os.getenv('HOST', '127.0.0.1')
    PORT = int(os.getenv('PORT', '5000'))
    
    # Product Catalog Configuration
    PRODUCT_CATALOG = [
        {
            'id': 1,
            'name': 'Cluster Emerald Tipe 36',
            'type': 'Tipe 36',
            'price': 350000000,
            'size': '36/72',
            'features': [
                '2 Kamar Tidur',
                '1 Kamar Mandi',
                'Carport 1 Mobil',
                'Garden Mini',
                'Listrik 1300W'
            ],
            'advantages': [
                'Harga Terjangkau',
                'Lokasi Strategis',
                'Bebas Banjir',
                'Legalitas SHM'
            ],
            'target_budget': [300000000, 400000000]
        },
        {
            'id': 2,
            'name': 'Cluster Emerald Tipe 45',
            'type': 'Tipe 45',
            'price': 450000000,
            'size': '45/90',
            'features': [
                '2 Kamar Tidur',
                '1 Kamar Mandi',
                'Carport 1 Mobil',
                'Taman Depan',
                'Listrik 1300W'
            ],
            'advantages': [
                'Desain Modern',
                'Ruang Lebih Luas',
                'Investasi Potensial',
                'Developer Terpercaya'
            ],
            'target_budget': [400000000, 500000000]
        },
        {
            'id': 3,
            'name': 'Cluster Ruby Tipe 60',
            'type': 'Tipe 60',
            'price': 650000000,
            'size': '60/120',
            'features': [
                '3 Kamar Tidur',
                '2 Kamar Mandi',
                'Carport 2 Mobil',
                'Taman Depan & Belakang',
                'Listrik 2200W'
            ],
            'advantages': [
                'Premium Location',
                'Spacious Design',
                'Luxury Finishing',
                'High ROI Potential'
            ],
            'target_budget': [600000000, 700000000]
        },
        {
            'id': 4,
            'name': 'Cluster Diamond Tipe 70',
            'type': 'Tipe 70',
            'price': 850000000,
            'size': '70/140',
            'features': [
                '3 Kamar Tidur',
                '2 Kamar Mandi',
                'Carport 2 Mobil',
                'Taman Luas',
                'Listrik 2200W',
                'Private Pool (Optional)'
            ],
            'advantages': [
                'Exclusive Design',
                'Prime Location',
                'Investment Grade',
                'Premium Facilities'
            ],
            'target_budget': [800000000, 900000000]
        },
        {
            'id': 5,
            'name': 'Cluster Sapphire Tipe 90',
            'type': 'Tipe 90',
            'price': 1200000000,
            'size': '90/180',
            'features': [
                '4 Kamar Tidur',
                '3 Kamar Mandi',
                'Carport 3 Mobil',
                'Taman Luas',
                'Listrik 3500W',
                'Private Pool',
                'Smart Home System'
            ],
            'advantages': [
                'Luxury Living',
                'Best Location',
                'High-End Materials',
                'Smart Technology'
            ],
            'target_budget': [1100000000, 1300000000]
        }
    ]
    
    @classmethod
    def get_product_by_budget(cls, budget):
        """Get product recommendations based on budget"""
        recommendations = []
        
        for product in cls.PRODUCT_CATALOG:
            min_budget, max_budget = product['target_budget']
            
            if min_budget <= budget <= max_budget:
                recommendations.append(product)
            elif budget < min_budget and not recommendations:
                # If budget is lower than all, show closest lower option
                if budget >= min_budget * 0.8:  # Within 80% of min budget
                    recommendations.append(product)
            elif budget > max_budget and not recommendations:
                # If budget is higher than all, show closest higher option
                if budget <= max_budget * 1.2:  # Within 120% of max budget
                    recommendations.append(product)
        
        return recommendations if recommendations else [cls.PRODUCT_CATALOG[0]]  # Default to first product
    
    @classmethod
    def format_price(cls, price):
        """Format price in Indonesian Rupiah"""
        if price >= 1000000000:
            return f"Rp {price/1000000000:.1f}M"
        elif price >= 1000000:
            return f"Rp {price/1000000:.0f}JT"
        else:
            return f"Rp {price:,}"

# Global configuration instance
config = Config()
