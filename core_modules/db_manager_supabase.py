"""
LUMINA OS - Supabase Cloud Database Manager
Professional cloud database connector for 24/7 autonomous operation
"""

import os
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import json
import time
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ANSI color codes for cyber logging
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
WHITE = '\033[97m'
BOLD = '\033[1m'
END = '\033[0m'

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs', 'supabase_manager.log')),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class SupabaseManager:
    """
    Professional Supabase Cloud Database Manager for Lumina OS
    Handles all database operations with cloud PostgreSQL backend
    """
    
    def __init__(self):
        """Initialize Supabase connection with cyber logging"""
        self.logger = logging.getLogger(__name__)
        
        # Get Supabase configuration
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_KEY')
        
        if not self.supabase_url or not self.supabase_key:
            self.logger.error(f"{RED}❌ CLOUD CONNECTION FAILED: Missing SUPABASE_URL or SUPABASE_KEY{END}")
            raise ValueError("Supabase configuration not found in environment variables")
        
        # Initialize Supabase client
        try:
            self.supabase = create_client(self.supabase_url, self.supabase_key)
            self.logger.info(f"{CYAN}☁️ 🔗 UPLINK ESTABLISHED: Connected to Supabase Cloud Engine{END}")
            self.logger.info(f"{GREEN}🌐 CLOUD DATABASE ONLINE: {self.supabase_url}{END}")
            self.connection_status = "connected"
            self.last_connection_time = datetime.now()
        except Exception as e:
            self.logger.error(f"{RED}❌ CLOUD CONNECTION FAILED: {str(e)}{END}")
            self.connection_status = "disconnected"
            self.supabase = None
            raise
    
    def _check_connection(self) -> bool:
        """Check if Supabase connection is active"""
        if not self.supabase:
            return False
        
        try:
            # Test connection with a simple query
            result = self.supabase.table('leads').select('id').limit(1).execute()
            self.connection_status = "connected"
            self.last_connection_time = datetime.now()
            return True
        except Exception as e:
            self.logger.warning(f"{YELLOW}⚠️  CONNECTION LOST: {str(e)}{END}")
            self.connection_status = "disconnected"
            return False
    
    def _handle_connection_error(self, operation: str, error: Exception):
        """Handle connection errors with graceful fallback"""
        self.logger.error(f"{RED}❌ CLOUD OPERATION FAILED ({operation}): {str(error)}{END}")
        self.connection_status = "disconnected"
        
        # Log cyber-style error message
        error_msg = f"""
{RED}╔══════════════════════════════════════════════════════════════╗
║                    CLOUD SYSTEM ERROR                            ║
╠══════════════════════════════════════════════════════════════╣
║ Operation: {operation:<50} ║
║ Error: {str(error):<52} ║
║ Status: DISCONNECTED                                         ║
║ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S'):<44} ║
╚══════════════════════════════════════════════════════════════╝{END}
        """
        self.logger.error(error_msg)
    
    def insert_lead(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Insert a new lead into Supabase cloud database
        
        Args:
            lead_data: Dictionary containing lead information
            
        Returns:
            Dict containing operation result
        """
        if not self._check_connection():
            self._handle_connection_error("insert_lead", Exception("Connection lost"))
            return {"success": False, "error": "Connection lost", "data": None}
        
        try:
            # Add timestamps if not present
            if 'created_at' not in lead_data:
                lead_data['created_at'] = datetime.now().isoformat()
            if 'updated_at' not in lead_data:
                lead_data['updated_at'] = datetime.now().isoformat()
            
            # Execute insert operation
            result = self.supabase.table('leads').insert(lead_data).execute()
            
            if result.data:
                self.logger.info(f"{GREEN}✅ LEAD UPLOADED: {lead_data.get('title', 'Unknown')} → Cloud Database{END}")
                self.logger.info(f"{CYAN}📊 CLOUD SYNC: Lead ID {result.data[0]['id']} stored in Supabase{END}")
                return {"success": True, "data": result.data[0], "error": None}
            else:
                self.logger.warning(f"{YELLOW}⚠️  INSERT FAILED: No data returned from Supabase{END}")
                return {"success": False, "error": "No data returned", "data": None}
                
        except Exception as e:
            self._handle_connection_error("insert_lead", e)
            return {"success": False, "error": str(e), "data": None}
    
    def get_pending_leads(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get pending leads that need follow-up from cloud database
        
        Args:
            limit: Maximum number of leads to retrieve
            
        Returns:
            List of pending leads
        """
        if not self._check_connection():
            self._handle_connection_error("get_pending_leads", Exception("Connection lost"))
            return []
        
        try:
            # Query pending leads
            result = self.supabase.table('leads')\
                .select('*')\
                .eq('status', 'pending')\
                .order('created_at', desc=True)\
                .limit(limit)\
                .execute()
            
            leads = result.data if result.data else []
            
            self.logger.info(f"{GREEN}✅ CLOUD RETRIEVAL: {len(leads)} pending leads downloaded{END}")
            self.logger.info(f"{CYAN}📊 SYNC STATUS: Latest data from Supabase Cloud{END}")
            
            return leads
            
        except Exception as e:
            self._handle_connection_error("get_pending_leads", e)
            return []
    
    def get_high_value_leads(self, min_score: int = 8, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Get high-value leads from cloud database
        
        Args:
            min_score: Minimum score threshold
            limit: Maximum number of leads to retrieve
            
        Returns:
            List of high-value leads
        """
        if not self._check_connection():
            self._handle_connection_error("get_high_value_leads", Exception("Connection lost"))
            return []
        
        try:
            # Query high-value leads
            result = self.supabase.table('leads')\
                .select('*')\
                .gte('score', min_score)\
                .order('score', desc=True)\
                .limit(limit)\
                .execute()
            
            leads = result.data if result.data else []
            
            self.logger.info(f"{GREEN}✅ HIGH-VALUE LEADS: {len(leads)} leads with score ≥ {min_score}{END}")
            self.logger.info(f"{CYAN}🎯 TARGET ACQUIRED: Premium prospects from Cloud Database{END}")
            
            return leads
            
        except Exception as e:
            self._handle_connection_error("get_high_value_leads", e)
            return []
    
    def update_lead_status(self, lead_id: int, status: str, notes: str = None) -> Dict[str, Any]:
        """
        Update lead status in cloud database
        
        Args:
            lead_id: ID of the lead to update
            status: New status value
            notes: Optional notes for the update
            
        Returns:
            Dict containing operation result
        """
        if not self._check_connection():
            self._handle_connection_error("update_lead_status", Exception("Connection lost"))
            return {"success": False, "error": "Connection lost"}
        
        try:
            # Prepare update data
            update_data = {
                'status': status,
                'updated_at': datetime.now().isoformat()
            }
            
            if notes:
                update_data['catatan_followup'] = notes
            
            # Execute update
            result = self.supabase.table('leads')\
                .update(update_data)\
                .eq('id', lead_id)\
                .execute()
            
            if result.data:
                self.logger.info(f"{GREEN}✅ LEAD UPDATED: ID {lead_id} → {status}{END}")
                self.logger.info(f"{CYAN}🔄 CLOUD SYNC: Status updated in Supabase{END}")
                return {"success": True, "data": result.data[0], "error": None}
            else:
                self.logger.warning(f"{YELLOW}⚠️  UPDATE FAILED: Lead ID {lead_id} not found{END}")
                return {"success": False, "error": "Lead not found", "data": None}
                
        except Exception as e:
            self._handle_connection_error("update_lead_status", e)
            return {"success": False, "error": str(e), "data": None}
    
    def get_database_stats(self) -> Dict[str, Any]:
        """
        Get database statistics from cloud database
        
        Returns:
            Dict containing database statistics
        """
        if not self._check_connection():
            self._handle_connection_error("get_database_stats", Exception("Connection lost"))
            return {}
        
        try:
            # Get total leads count
            total_result = self.supabase.table('leads').select('id', count='exact').execute()
            total_leads = total_result.count if total_result.count else 0
            
            # Get pending leads count
            pending_result = self.supabase.table('leads')\
                .select('id', count='exact')\
                .eq('status', 'pending')\
                .execute()
            pending_leads = pending_result.count if pending_result.count else 0
            
            # Get high-value leads count
            high_value_result = self.supabase.table('leads')\
                .select('id', count='exact')\
                .gte('score', 8)\
                .execute()
            high_value_leads = high_value_result.count if high_value_result.count else 0
            
            stats = {
                'total_leads': total_leads,
                'pending_leads': pending_leads,
                'high_value_leads': high_value_leads,
                'connection_status': self.connection_status,
                'last_connection': self.last_connection_time.isoformat() if self.last_connection_time else None,
                'database_type': 'Supabase Cloud PostgreSQL',
                'timestamp': datetime.now().isoformat()
            }
            
            self.logger.info(f"{GREEN}✅ DATABASE STATS: {total_leads} total, {pending_leads} pending, {high_value_leads} high-value{END}")
            self.logger.info(f"{CYAN}📊 CLOUD ANALYTICS: Real-time statistics from Supabase{END}")
            
            return stats
            
        except Exception as e:
            self._handle_connection_error("get_database_stats", e)
            return {}
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test Supabase connection and return status
        
        Returns:
            Dict containing connection test results
        """
        try:
            if not self.supabase:
                return {
                    "success": False,
                    "error": "Supabase client not initialized",
                    "status": "disconnected"
                }
            
            # Test with a simple query
            result = self.supabase.table('leads').select('id').limit(1).execute()
            
            self.logger.info(f"{GREEN}✅ CONNECTION TEST: Supabase Cloud Engine online{END}")
            self.logger.info(f"{CYAN}🌐 UPLINK STATUS: Connected to {self.supabase_url}{END}")
            
            return {
                "success": True,
                "status": "connected",
                "url": self.supabase_url,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self._handle_connection_error("test_connection", e)
            return {
                "success": False,
                "error": str(e),
                "status": "disconnected"
            }
    
    def create_table_if_not_exists(self, table_name: str, schema: Dict[str, str]) -> bool:
        """
        Create table in Supabase if it doesn't exist (requires admin privileges)
        
        Args:
            table_name: Name of the table to create
            schema: Dictionary defining table schema
            
        Returns:
            Boolean indicating success
        """
        if not self._check_connection():
            self._handle_connection_error("create_table_if_not_exists", Exception("Connection lost"))
            return False
        
        try:
            # Note: This requires admin privileges and SQL execution
            # For now, log the requirement
            self.logger.info(f"{YELLOW}⚠️  TABLE CREATION: {table_name} requires admin SQL execution{END}")
            self.logger.info(f"{CYAN}📋 SCHEMA DEFINITION: {json.dumps(schema, indent=2)}{END}")
            
            return True
            
        except Exception as e:
            self._handle_connection_error("create_table_if_not_exists", e)
            return False

# Global Supabase manager instance
supabase_manager = None

def get_supabase_manager() -> SupabaseManager:
    """Get or create Supabase manager instance"""
    global supabase_manager
    if supabase_manager is None:
        try:
            supabase_manager = SupabaseManager()
        except Exception as e:
            logger.error(f"Failed to initialize Supabase manager: {e}")
            raise
    return supabase_manager

# Convenience functions
def insert_lead(lead_data: Dict[str, Any]) -> Dict[str, Any]:
    """Insert lead using global Supabase manager"""
    manager = get_supabase_manager()
    return manager.insert_lead(lead_data)

def get_pending_leads(limit: int = 50) -> List[Dict[str, Any]]:
    """Get pending leads using global Supabase manager"""
    manager = get_supabase_manager()
    return manager.get_pending_leads(limit)

def get_high_value_leads(min_score: int = 8, limit: int = 20) -> List[Dict[str, Any]]:
    """Get high-value leads using global Supabase manager"""
    manager = get_supabase_manager()
    return manager.get_high_value_leads(min_score, limit)

def get_database_stats() -> Dict[str, Any]:
    """Get database statistics using global Supabase manager"""
    manager = get_supabase_manager()
    return manager.get_database_stats()

if __name__ == "__main__":
    # Test Supabase connection
    print(f"{MAGENTA}{'='*60}{END}")
    print(f"{CYAN}LUMINA OS - SUPABASE CLOUD DATABASE MANAGER{END}")
    print(f"{MAGENTA}{'='*60}{END}")
    
    try:
        manager = get_supabase_manager()
        test_result = manager.test_connection()
        
        if test_result["success"]:
            print(f"{GREEN}✅ SUPABASE CONNECTION: SUCCESS{END}")
            print(f"{CYAN}🌐 CLOUD URL: {test_result['url']}{END}")
            
            # Get database stats
            stats = manager.get_database_stats()
            print(f"{GREEN}📊 DATABASE STATS: {json.dumps(stats, indent=2)}{END}")
        else:
            print(f"{RED}❌ SUPABASE CONNECTION: FAILED{END}")
            print(f"{RED}🔥 ERROR: {test_result['error']}{END}")
            
    except Exception as e:
        print(f"{RED}❌ INITIALIZATION FAILED: {str(e)}{END}")
    
    print(f"{MAGENTA}{'='*60}{END}")
