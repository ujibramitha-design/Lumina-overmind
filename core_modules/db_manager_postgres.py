"""
PostgreSQL Database Manager - Enterprise Grade Database Operations
Professional PostgreSQL connection using Prisma Client for Lumina OS Enterprise
"""

import os
import json
import logging
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
from prisma import Prisma
from prisma.enums import LeadStatus, CampaignMode, Priority, UserRole, TaskType, TaskStatus, ApiService
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PostgresDatabaseManager:
    """Enterprise PostgreSQL Database Manager using Prisma Client"""
    
    def __init__(self):
        """Initialize PostgreSQL database manager"""
        self.logger = logging.getLogger(__name__)
        self.prisma = None
        self.cipher = None
        
        # Initialize database connection
        self._initialize_database()
        self._initialize_encryption()
    
    def _initialize_database(self):
        """Initialize Prisma client with PostgreSQL"""
        try:
            # Get database URL from environment
            database_url = os.getenv('DATABASE_URL')
            if not database_url:
                raise ValueError("DATABASE_URL environment variable is required")
            
            # Initialize Prisma client
            self.prisma = Prisma(
                datasource={
                    'url': database_url
                },
                log_queries=os.getenv('ENVIRONMENT') == 'development'
            )
            
            logger.info("✅ PostgreSQL connection initialized with Prisma")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize PostgreSQL: {e}")
            raise
    
    def _initialize_encryption(self):
        """Initialize Fernet encryption for AES-256 compliance"""
        try:
            encryption_key = os.getenv('ENCRYPTION_KEY')
            if not encryption_key:
                # Generate new encryption key
                encryption_key = Fernet.generate_key().decode()
                # Save to .env file
                env_file = '.env'
                with open(env_file, 'a') as f:
                    f.write(f'\nENCRYPTION_KEY={encryption_key}\n')
                logger.info(f"Generated new encryption key and saved to .env")
            
            self.cipher = Fernet(encryption_key.encode())
            logger.info("✅ AES-256 encryption initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize encryption: {e}")
            # Fallback: disable encryption
            self.cipher = None
    
    def _encrypt(self, text: str) -> str:
        """Encrypt sensitive data with AES-256"""
        if not self.cipher or not text:
            return text
        
        try:
            encrypted = self.cipher.encrypt(text.encode())
            return encrypted.decode()
        except Exception as e:
            logger.error(f"❌ Error encrypting data: {e}")
            return text  # Fallback to plain text
    
    def _decrypt(self, token: str) -> str:
        """Decrypt sensitive data with AES-256"""
        if not self.cipher or not token:
            return token
        
        try:
            decrypted = self.cipher.decrypt(token.encode())
            return decrypted.decode()
        except Exception as e:
            logger.error(f"❌ Error decrypting data: {e}")
            return token  # Fallback to plain text
    
    async def create_lead(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create new lead with AES-256 encryption
        """
        try:
            # Encrypt sensitive data
            encrypted_data = {
                'contact_info': json.dumps(lead_data.get('contact_info', {})),
                'phone': self._encrypt(lead_data.get('phone', '')),
                'email': self._encrypt(lead_data.get('email', '')),
                'personal_data': self._encrypt(json.dumps(lead_data.get('personal_data', {})))
            }
            
            # Create lead with Prisma
            lead = await self.prisma.lead.create(
                data={
                    'encryptedData': json.dumps(encrypted_data),
                    'status': LeadStatus.SCOUTED,
                    'campaignId': lead_data.get('campaign_id'),
                    'priority': Priority(lead_data.get('priority', 'MEDIUM')),
                    'intentCategory': lead_data.get('intent_category', 'Informational'),
                    'entityData': json.dumps(lead_data.get('entities', {})),
                    'isTrend': lead_data.get('is_trend', False),
                    'source': lead_data.get('source', 'system'),
                    'area': lead_data.get('area'),
                    'keywords': lead_data.get('keywords', [])
                }
            )
            
            logger.info(f"✅ Lead created: ID {lead.id}")
            return {
                'success': True,
                'lead_id': lead.id,
                'lead': lead
            }
            
        except Exception as e:
            logger.error(f"❌ Error creating lead: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def get_lead_by_id(self, lead_id: str) -> Optional[Dict[str, Any]]:
        """
        Get lead by ID with decrypted data
        """
        try:
            lead = await self.prisma.lead.find_unique(
                where={'id': lead_id}
            )
            
            if not lead:
                return None
            
            # Parse and decrypt encrypted data
            encrypted_data = json.loads(lead.encryptedData or '{}')
            decrypted_data = {
                'contact_info': json.loads(encrypted_data.get('contact_info', '{}')),
                'phone': self._decrypt(encrypted_data.get('phone', '')),
                'email': self._decrypt(encrypted_data.get('email', '')),
                'personal_data': json.loads(self._decrypt(encrypted_data.get('personal_data', '{}')))
            }
            
            # Parse entity data
            entity_data = json.loads(lead.entityData or '{}')
            
            # Combine data
            lead_dict = {
                'id': lead.id,
                'status': lead.status,
                'campaignId': lead.campaignId,
                'priority': lead.priority,
                'intentCategory': lead.intentCategory,
                'entityData': entity_data,
                'isTrend': lead.isTrend,
                'source': lead.source,
                'area': lead.area,
                'keywords': lead.keywords,
                'createdAt': lead.createdAt,
                'updatedAt': lead.updatedAt,
                **decrypted_data
            }
            
            return lead_dict
            
        except Exception as e:
            logger.error(f"❌ Error getting lead by ID: {e}")
            return None
    
    async def update_lead_status(self, lead_id: str, status: LeadStatus) -> bool:
        """
        Update lead status
        """
        try:
            lead = await self.prisma.lead.update(
                where={'id': lead_id},
                data={'status': status}
            )
            
            logger.info(f"✅ Lead {lead_id} status updated to: {status}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error updating lead status: {e}")
            return False
    
    async def get_leads_by_status(self, status: LeadStatus, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get leads by status
        """
        try:
            leads = await self.prisma.lead.find_many(
                where={'status': status},
                take=limit,
                order={'createdAt': 'desc'}
            )
            
            result = []
            for lead in leads:
                # Parse and decrypt data
                encrypted_data = json.loads(lead.encrypted_data or '{}')
                decrypted_data = {
                    'contact_info': json.loads(encrypted_data.get('contact_info', '{}')),
                    'phone': self._decrypt(encrypted_data.get('phone', '')),
                    'email': self._decrypt(encrypted_data.get('email', '')),
                    'personal_data': json.loads(self._decrypt(encrypted_data.get('personal_data', '{}')))
                }
                
                entity_data = json.loads(lead.entityData or '{}')
                
                lead_dict = {
                    'id': lead.id,
                    'status': lead.status,
                    'campaignId': lead.campaignId,
                    'priority': lead.priority,
                    'intentCategory': lead.intentCategory,
                    'entityData': entity_data,
                    'isTrend': lead.isTrend,
                    'source': lead.source,
                    'area': lead.area,
                    'keywords': lead.keywords,
                    'createdAt': lead.createdAt,
                    'updatedAt': lead.updatedAt,
                    **decrypted_data
                }
                
                result.append(lead_dict)
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Error getting leads by status: {e}")
            return []
    
    async def create_campaign(self, campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create new campaign
        """
        try:
            campaign = await self.prisma.campaign.create(
                data={
                    'name': campaign_data['name'],
                    'description': campaign_data.get('description', ''),
                    'mode': CampaignMode(campaign_data['mode']),
                    'config': campaign_data.get('config', {}),
                    'targetArea': campaign_data.get('target_area'),
                    'keywords': campaign_data.get('keywords', []),
                    'status': 'ACTIVE',
                    'isActive': True
                }
            )
            
            logger.info(f"✅ Campaign created: ID {campaign.id}")
            return {
                'success': True,
                'campaign_id': campaign.id,
                'campaign': campaign
            }
            
        except Exception as e:
            logger.error(f"❌ Error creating campaign: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def create_vr_sentinel_log(self, log_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create VR Sentinel log entry
        """
        try:
            vr_log = await self.prisma.vrsentinelLog.create(
                data={
                    'sessionId': log_data['session_id'],
                    'userId': log_data.get('user_id'),
                    'campaignId': log_data.get('campaign_id'),
                    'gazeData': log_data['gaze_data'],
                    'objectName': log_data.get('object_name'),
                    'focusDuration': log_data.get('focus_duration'),
                    'interactionType': log_data.get('interaction_type', 'VIEW'),
                    'position': log_data.get('position'),
                    'rotation': log_data.get('rotation'),
                    'viewport': log_data.get('viewport'),
                    'leadIntent': log_data.get('lead_intent'),
                    'confidence': log_data.get('confidence'),
                    'tags': log_data.get('tags', [])
                }
            )
            
            logger.info(f"✅ VR Sentinel log created: ID {vr_log.id}")
            return {
                'success': True,
                'log_id': vr_log.id,
                'vr_log': vr_log
            }
            
        except Exception as e:
            logger.error(f"❌ Error creating VR Sentinel log: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def get_system_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive system statistics
        """
        try:
            # Lead statistics
            total_leads = await self.prisma.lead.count()
            
            leads_by_status = {}
            for status in LeadStatus:
                count = await self.prisma.lead.count(where={'status': status})
                leads_by_status[status.value] = count
            
            # Campaign statistics
            total_campaigns = await self.prisma.campaign.count()
            
            campaigns_by_mode = {}
            for mode in CampaignMode:
                count = await self.prisma.campaign.count(where={'mode': mode})
                campaigns_by_mode[mode.value] = count
            
            # VR statistics
            total_vr_sessions = await self.prisma.vrsentinelLog.count()
            
            # Intent distribution
            intent_stats = {}
            for intent in ['Informational', 'Comparison', 'Pain-Point', 'Transactional']:
                count = await self.prisma.lead.count(where={'intentCategory': intent})
                intent_stats[intent] = count
            
            return {
                'leads': {
                    'total': total_leads,
                    'by_status': leads_by_status,
                    'by_intent': intent_stats
                },
                'campaigns': {
                    'total': total_campaigns,
                    'by_mode': campaigns_by_mode
                },
                'vr': {
                    'total_sessions': total_vr_sessions
                },
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting system statistics: {e}")
            return {}
    
    async def execute_query(self, query: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Execute raw SQL query (use with caution)
        """
        try:
            if params:
                result = await self.prisma.query_raw(query, params)
            else:
                result = await self.prisma.query_raw(query)
            
            # Convert result to list of dictionaries
            return [dict(row) for row in result]
            
        except Exception as e:
            logger.error(f"❌ Error executing query: {e}")
            return []
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Database health check
        """
        try:
            # Test basic connection
            await self.prisma.query_raw('SELECT 1')
            
            # Test table existence
            tables = await self.prisma.query_raw("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)
            
            return {
                'status': 'healthy',
                'database': 'postgresql',
                'tables': len([dict(row)['table_name'] for row in tables]),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Database health check failed: {e}")
            return {
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    async def cleanup_old_records(self, days: int = 90) -> Dict[str, int]:
        """
        Clean up old records
        """
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            # Delete old leads
            leads_deleted = await self.prisma.lead.delete_many(
                where={'createdAt': {'lt': cutoff_date}}
            )
            
            # Delete old VR logs
            vr_logs_deleted = await self.prisma.vrsentinelLog.delete_many(
                where={'timestamp': {'lt': cutoff_date}}
            )
            
            # Delete old campaigns
            campaigns_deleted = await self.prisma.campaign.delete_many(
                where={'createdAt': {'lt': cutoff_date}}
            )
            
            total_deleted = leads_deleted + vr_logs_deleted + campaigns_deleted
            
            logger.info(f"✅ Cleanup completed: {total_deleted} records deleted")
            return {
                'leads_deleted': leads_deleted,
                'vr_logs_deleted': vr_logs_deleted,
                'campaigns_deleted': campaigns_deleted,
                'total_deleted': total_deleted
            }
            
        except Exception as e:
            logger.error(f"❌ Error during cleanup: {e}")
            return {
                'leads_deleted': 0,
                'vr_logs_deleted': 0,
                'campaigns_deleted': 0,
                'total_deleted': 0,
                'error': str(e)
            }

# Global database manager instance
postgres_db_manager = PostgresDatabaseManager()

# Convenience functions
async def create_lead(lead_data: Dict[str, Any]) -> Dict[str, Any]:
    """Convenience function to create lead"""
    return await postgres_db_manager.create_lead(lead_data)

async def get_high_intent_leads(limit: int = 50) -> List[Dict[str, Any]]:
    """Convenience function to get high intent leads"""
    return await postgres_db_manager.get_leads_by_status(
        LeadStatus.HOT_RESPONDED, limit
    )

async def get_system_stats() -> Dict[str, Any]:
    """Convenience function to get system statistics"""
    return await postgres_db_manager.get_system_statistics()

if __name__ == "__main__":
    # Test the database manager
    import asyncio
    
    async def test_database():
        # Test health check
        health = await postgres_db_manager.health_check()
        print(f"Database health: {health}")
        
        # Test statistics
        stats = await postgres_db_manager.get_system_statistics()
        print(f"System statistics: {stats}")
    
    asyncio.run(test_database())
