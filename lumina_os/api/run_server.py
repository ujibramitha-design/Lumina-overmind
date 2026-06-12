#!/usr/bin/env python3
"""
Lumina OS API Server Runner
Starts the Flask API server for Lumina OS

Author: HUNTER_AGENT_AI_MARKETING_DIGITAL
Version: 1.0.0
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.append(str(parent_dir))

# Import API app
from api import create_api_app

def main():
    """Main function to run the API server"""
    print("🚀 Starting Lumina OS API Server...")
    print("📍 Server will run on: http://localhost:5000")
    print("🔗 Webhook endpoint: http://localhost:5000/api/webhook/incoming-lead")
    print("🔗 Health check: http://localhost:5000/api/webhook/health")
    print("🔗 Leads API: http://localhost:5000/api/leads/")
    print("=" * 60)
    
    # Create Flask app
    app = create_api_app()
    
    # Set environment variables for webhook
    os.environ['LUMINA_WEBHOOK_TOKEN'] = 'DUMMY-TOKEN-123'
    
    # Run the app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=False  # Prevent issues with webhook processing
    )

if __name__ == "__main__":
    main()
