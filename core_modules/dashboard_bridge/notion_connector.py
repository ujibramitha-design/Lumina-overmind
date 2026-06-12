#!/usr/bin/env python3
"""
Notion Connector - Dashboard Bridge
Notion database integration for real-time data synchronization
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import requests
from notion_client import Client as NotionClient
import pandas as pd
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NotionConnector:
    """Notion database integration for real-time data synchronization"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Notion API configuration
        self.api_key = os.getenv('NOTION_API_KEY')
        self.client = None
        
        # Database configurations
        self.database_config = {
            'leads': {
                'database_name': 'Leads Management',
                'properties': {
                    'ID': {'type': 'title', 'title': ['ID']},
                    'Name': {'type': 'rich_text', 'rich_text': []},
                    'Contact': {'type': 'phone', 'phone': ''},
                    'Email': {'type': 'email', 'email': ''},
                    'Property': {'type': 'select', 'select': {}},
                    'Status': {'type': 'status', 'status': {}},
                    'Value': {'type': 'number', 'number': 0},
                    'Source': {'type': 'multi_select', 'multi_select': []},
                    'Date': {'type': 'date', 'date': None},
                    'Notes': {'type': 'rich_text', 'rich_text': []}
                }
            },
            'analytics': {
                'database_name': 'Analytics Dashboard',
                'properties': {
                    'Date': {'type': 'date', 'date': None},
                    'Leads Generated': {'type': 'number', 'number': 0},
                    'Deals Closed': {'type': 'number', 'number': 0},
                    'Revenue': {'type': 'number', 'number': 0},
                    'Conversion Rate': {'type': 'percent', 'percent': 0},
                    'Active Users': {'type': 'number', 'number': 0}
                }
            },
            'properties': {
                'database_name': 'Property Database',
                'properties': {
                    'Title': {'type': 'title', 'title': ['Title']},
                    'Type': {'type': 'select', 'select': {}},
                    'Location': {'type': 'rich_text', 'rich_text': []},
                    'Price': {'type': 'number', 'number': 0},
                    'Status': {'type': 'status', 'status': {}},
                    'Features': {'type': 'rich_text', 'rich_text': []},
                    'Images': {'type': 'files', 'files': []},
                    'Created': {'type': 'created_time', 'created_time': None}
                }
            },
            'reports': {
                'database_name': 'Performance Reports',
                'properties': {
                    'Report Date': {'type': 'date', 'date': None},
                    'Period': {'type': 'select', 'select': {}},
                    'Metric': {'type': 'title', 'title': ['Metric']},
                    'Value': {'type': 'number', 'number': 0},
                    'Target': {'type': 'number', 'number': 0},
                    'Achievement': {'type': 'number', 'number': 0},
                    'Notes': {'type': 'rich_text', 'rich_text': []}
                }
            }
        }
        
        # Initialize connection
        self._initialize_connection()
    
    def _initialize_connection(self):
        """Initialize Notion connection"""
        try:
            if self.api_key:
                self.client = NotionClient(auth=self.api_key)
                self.logger.info("Notion connection initialized successfully")
            else:
                self.logger.warning("Notion API key not found in environment variables")
                self.client = None
                
        except Exception as e:
            self.logger.error(f"Error initializing Notion connection: {e}")
            self.client = None
    
    def authenticate(self) -> bool:
        """Test Notion API connection"""
        try:
            if not self.client:
                self.logger.error("No Notion client available for authentication")
                return False
            
            # Test connection by getting user info
            user_info = self.client.me.get()
            self.logger.info(f"Notion authentication successful. User: {user_info.get('name', 'Unknown')}")
            return True
            
        except Exception as e:
            self.logger.error(f"Notion authentication failed: {e}")
            return False
    
    def create_database(self, database_name: str, properties: Dict) -> Optional[str]:
        """Create Notion database"""
        try:
            if not self.client:
                self.logger.error("No Notion client available")
                return None
            
            # Create database
            database = self.client.databases.create(
                title=database_name,
                schema=[{
                    "name": property_name,
                    "type": property_type
                }
                for property_name, property_type in properties.items()
                ]
            )
            
            self.logger.info(f"Created Notion database: {database_name}")
            return database.id
            
        except Exception as e:
            self.logger.error(f"Error creating Notion database: {e}")
            return None
    
    def get_database_by_name(self, database_name: str) -> Optional[Any]:
        """Get database by name"""
        try:
            if not self.client:
                self.logger.error("No Notion client available")
                return None
            
            # Search for database
            databases = self.client.databases.query(filter={"property": "title", "value": database_name})
            
            if databases:
                database = databases[0]
                self.logger.info(f"Found Notion database: {database_name}")
                return database
            else:
                self.logger.warning(f"Database not found: {database_name}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error getting Notion database: {e}")
            return None
    
    def create_page(self, database_id: str, page_data: Dict) -> Optional[str]:
        """Create page in Notion database"""
        try:
            if not self.client:
                self.logger.error("No Notion client available")
                return None
            
            # Create page
            page = self.client.pages.create(
                parent={"database_id": database_id},
                properties=page_data
            )
            
            self.logger.info(f"Created page in Notion database")
            return page.id
            
        except Exception as e:
            self.logger.error(f"Error creating Notion page: {e}")
            return None
    
    def sync_leads_to_notion(self, leads_data: List[Dict]) -> bool:
        """Sync leads data to Notion database"""
        try:
            config = self.database_config['leads']
            
            # Get or create database
            database = self.get_database_by_name(config['database_name'])
            if not database:
                database_id = self.create_database(config['database_name'], config['properties'])
                if not database_id:
                    return False
            else:
                database_id = database.id
            
            # Create pages for each lead
            created_count = 0
            for lead in leads_data:
                page_data = {
                    'ID': {'title': [{'text': lead.get('id', '')}]},
                    'Name': {'rich_text': [{'text': lead.get('name', '')}]},
                    'Contact': {'phone': lead.get('contact', {}).get('phone', '')},
                    'Email': {'email': lead.get('contact', {}).get('email', '')},
                    'Property': {'select': {'name': lead.get('property', '')}},
                    'Status': {'status': {'name': lead.get('status', 'New')}},
                    'Value': {'number': lead.get('value', 0)},
                    'Source': {'multi_select': [{'name': source} for source in lead.get('source', '').split(',')]},
                    'Date': {'date': lead.get('date', None)},
                    'Notes': {'rich_text': [{'text': lead.get('notes', '')}]}
                }
                
                page_id = self.create_page(database_id, page_data)
                if page_id:
                    created_count += 1
            
            self.logger.info(f"Synced {created_count} leads to Notion")
            return True
            
        except Exception as e:
            self.logger.error(f"Error syncing leads to Notion: {e}")
            return False
    
    def sync_analytics_to_notion(self, analytics_data: Dict) -> bool:
        """Sync analytics data to Notion database"""
        try:
            config = self.database_config['analytics']
            
            # Get or create database
            database = self.get_database_by_name(config['database_name'])
            if not database:
                database_id = self.create_database(config['database_name'], config['properties'])
                if not database_id:
                    return False
            else:
                database_id = database.id
            
            # Create pages for each date
            created_count = 0
            for date, metrics in analytics_data.items():
                page_data = {
                    'Date': {'date': date},
                    'Leads Generated': {'number': metrics.get('leads_generated', 0)},
                    'Deals Closed': {'number': metrics.get('deals_closed', 0)},
                    'Revenue': {'number': metrics.get('revenue', 0)},
                    'Conversion Rate': {'percent': metrics.get('conversion_rate', 0)},
                    'Active Users': {'number': metrics.get('active_users', 0)}
                }
                
                page_id = self.create_page(database_id, page_data)
                if page_id:
                    created_count += 1
            
            self.logger.info(f"Synced {created_count} analytics records to Notion")
            return True
            
        except Exception as e:
            self.logger.error(f"Error syncing analytics to Notion: {e}")
            return False
    
    def sync_properties_to_notion(self, properties_data: List[Dict]) -> bool:
        """Sync properties data to Notion database"""
        try:
            config = self.database_config['properties']
            
            # Get or create database
            database = self.get_database_by_name(config['database_name'])
            if not database:
                database_id = self.create_database(config['database_name'], config['properties'])
                if not database_id:
                    return False
            else:
                database_id = database.id
            
            # Create pages for each property
            created_count = 0
            for prop in properties_data:
                page_data = {
                    'Title': {'title': [{'text': prop.get('title', '')}]},
                    'Type': {'select': {'name': prop.get('type', '')}},
                    'Location': {'rich_text': [{'text': prop.get('location', '')}]},
                    'Price': {'number': prop.get('price', 0)},
                    'Status': {'status': {'name': prop.get('status', 'Available')}},
                    'Features': {'rich_text': [{'text': prop.get('features', '')}]},
                    'Images': {'files': []},  # Would need to upload files separately
                    'Created': {'created_time': prop.get('created', datetime.now().isoformat())}
                }
                
                page_id = self.create_page(database_id, page_data)
                if page_id:
                    created_count += 1
            
            self.logger.info(f"Synced {created_count} properties to Notion")
            return True
            
        except Exception as e:
            self.logger.error(f"Error syncing properties to Notion: {e}")
            return False
    
    def get_database_pages(self, database_id: str) -> List[Dict]:
        """Get all pages from Notion database"""
        try:
            if not self.client:
                self.logger.error("No Notion client available")
                return []
            
            # Get pages
            pages = self.client.databases.query(database_id=database_id)
            
            page_data = []
            for page in pages:
                page_info = {
                    'id': page.id,
                    'created_time': page.created_time,
                    'last_edited_time': page.last_edited_time,
                    'properties': page.properties
                }
                page_data.append(page_info)
            
            self.logger.info(f"Retrieved {len(page_data)} pages from Notion database")
            return page_data
            
        except Exception as e:
            self.logger.error(f"Error getting pages from Notion database: {e}")
            return []
    
    def update_page(self, page_id: str, properties: Dict) -> bool:
        """Update page properties"""
        try:
            if not self.client:
                self.logger.error("No Notion client available")
                return False
            
            # Update page
            self.client.pages.update(page_id, properties=properties)
            
            self.logger.info(f"Updated page {page_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error updating page {page_id}: {e}")
            return False
    
    def create_dashboard_summary(self) -> Dict:
        """Create dashboard summary from Notion databases"""
        try:
            summary = {
                'databases': {},
                'last_sync': datetime.now().isoformat(),
                'status': 'connected' if self.client else 'disconnected'
            }
            
            if self.client:
                for db_type, config in self.database_config.items():
                    try:
                        database = self.get_database_by_name(config['database_name'])
                        if database:
                            pages = self.get_database_pages(database.id)
                            summary['databases'][db_type] = {
                                'database_name': config['database_name'],
                                'database_id': database.id,
                                'page_count': len(pages),
                                'last_updated': datetime.now().isoformat()
                            }
                        else:
                            summary['databases'][db_type] = {
                                'database_name': config['database_name'],
                                'status': 'not_found',
                                'page_count': 0
                            }
                    except Exception as e:
                        self.logger.error(f"Error getting {db_type} database info: {e}")
                        summary['databases'][db_type] = {
                            'error': str(e),
                            'page_count': 0
                        }
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Error creating dashboard summary: {e}")
            return {'error': str(e)}
    
    def export_to_csv(self, database_id: str, output_file: str) -> bool:
        """Export database pages to CSV file"""
        try:
            # Get pages from database
            pages = self.get_database_pages(database_id)
            
            if not pages:
                self.logger.error("No pages to export")
                return False
            
            # Convert to DataFrame
            data = []
            for page in pages:
                page_data = {
                    'ID': page['id'],
                    'Created': page['created_time'],
                    'Last Edited': page['last_edited_time']
                }
                
                # Add properties
                for prop_name, prop_value in page['properties'].items():
                    if hasattr(prop_value, 'title'):
                        page_data[prop_name] = prop_value.title[0]['text'] if prop_value.title else ''
                    elif hasattr(prop_value, 'rich_text'):
                        page_data[prop_name] = prop_value.rich_text[0]['text'] if prop_value.rich_text else ''
                    elif hasattr(prop_value, 'phone'):
                        page_data[prop_name] = prop_value.phone
                    elif hasattr(prop_value, 'email'):
                        page_data[prop_name] = prop_value.email
                    elif hasattr(prop_value, 'date'):
                        page_data[prop_name] = prop_value.date
                    elif hasattr(prop_value, 'number'):
                        page_data[prop_name] = prop_value.number
                    elif hasattr(prop_value, 'percent'):
                        page_data[prop_name] = prop_value.percent
                    else:
                        page_data[prop_name] = str(prop_value)
                
                data.append(page_data)
            
            # Save to CSV
            df = pd.DataFrame(data)
            df.to_csv(output_file, index=False)
            
            self.logger.info(f"Exported {len(data)} records to {output_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error exporting to CSV: {e}")
            return False
    
    def create_sample_data(self) -> bool:
        """Create sample data for testing"""
        try:
            # Sample leads data
            leads_data = [
                {
                    'id': 'LEAD001',
                    'name': 'Budi Santoso',
                    'contact': {'phone': '0812-3456-7890', 'email': 'budi@email.com'},
                    'property': 'Rumah Type 36 Serang',
                    'status': 'New',
                    'value': 350000000,
                    'source': 'Website, Instagram',
                    'date': '2026-05-28',
                    'notes': 'Interested in property near industrial area'
                },
                {
                    'id': 'LEAD002',
                    'name': 'Siti Nurhaliza',
                    'contact': {'phone': '0856-7890-1234', 'email': 'siti@email.com'},
                    'property': 'Rumah Type 45 Serang',
                    'status': 'Qualified',
                    'value': 450000000,
                    'source': 'Facebook, WhatsApp',
                    'date': '2026-05-28',
                    'notes': 'Looking for family home with good schools'
                }
            ]
            
            # Sample analytics data
            analytics_data = {
                '2026-05-28': {
                    'leads_generated': 15,
                    'deals_closed': 2,
                    'revenue': 800000000,
                    'conversion_rate': 13.3,
                    'active_users': 45
                }
            }
            
            # Sample properties data
            properties_data = [
                {
                    'id': 'PROP001',
                    'title': 'Rumah Modern di Cipocok Jaya',
                    'type': 'House',
                    'location': 'Serang, Banten',
                    'price': 350000000,
                    'status': 'Available',
                    'features': '3 bedrooms, 2 bathrooms, carport',
                    'created': '2026-05-28T10:00:00.000Z'
                },
                {
                    'id': 'PROP002',
                    'title': 'Apartemen Serang City Center',
                    'type': 'Apartment',
                    'location': 'Serang, Banten',
                    'price': 280000000,
                    'status': 'Available',
                    'features': '2 bedrooms, 1 bathroom, swimming pool',
                    'created': '2026-05-28T11:00:00.000Z'
                }
            ]
            
            # Sync all sample data
            success = True
            success &= self.sync_leads_to_notion(leads_data)
            success &= self.sync_analytics_to_notion(analytics_data)
            success &= self.sync_properties_to_notion(properties_data)
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error creating sample data: {e}")
            return False

def main():
    """Main function to test Notion connector"""
    print("=" * 60)
    print("🗃️ NOTION CONNECTOR - DASHBOARD BRIDGE")
    print("=" * 60)
    
    # Initialize connector
    connector = NotionConnector()
    
    # Test authentication
    print("\n🔐 Testing Notion API authentication...")
    auth_success = connector.authenticate()
    
    if auth_success:
        print("✅ Notion API authentication successful")
        
        # Create sample data
        print("\n📋 Creating sample data...")
        sample_success = connector.create_sample_data()
        
        if sample_success:
            print("✅ Sample data created successfully")
            
            # Create dashboard summary
            print("\n📊 Creating dashboard summary...")
            summary = connector.create_dashboard_summary()
            
            print("📈 Dashboard Summary:")
            for db_type, info in summary.get('databases', {}).items():
                if 'error' not in info:
                    print(f"  - {db_type.title()}: {info['page_count']} pages")
                else:
                    print(f"  - {db_type.title()}: Error - {info['error']}")
            
            print(f"  - Last Sync: {summary.get('last_sync', 'Unknown')}")
            print(f"  - Status: {summary.get('status', 'Unknown')}")
            
            # Export to CSV
            print("\n💾 Exporting sample data to CSV...")
            # Get database ID for leads
            leads_db = connector.get_database_by_name('Leads Management')
            if leads_db:
                export_success = connector.export_to_csv(leads_db.id, 'leads_export.csv')
                
                if export_success:
                    print("✅ Data exported to leads_export.csv")
            
        else:
            print("❌ Failed to create sample data")
    else:
        print("❌ Notion API authentication failed")
        print("📝 Please ensure NOTION_API_KEY is set in environment variables")
    
    print("\n" + "=" * 60)
    print("✅ NOTION CONNECTOR TEST COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()
