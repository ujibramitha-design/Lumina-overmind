#!/usr/bin/env python3
"""
Deal Closer - Closer Agent
Advanced closing system for deal management and conversion tracking
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DealStage(Enum):
    """Deal pipeline stages"""
    LEAD = "lead"
    QUALIFIED = "qualified"
    PROPOSAL_SENT = "proposal_sent"
    NEGOTIATION = "negotiation"
    VERIFICATION = "verification"
    CLOSING = "closing"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"

class DealPriority(Enum):
    """Deal priority levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

@dataclass
class Deal:
    """Deal data structure"""
    deal_id: str
    lead_id: str
    property_info: Dict
    client_info: Dict
    stage: DealStage
    priority: DealPriority
    value: float
    probability: float
    created_at: datetime
    expected_close_date: Optional[datetime] = None
    actual_close_date: Optional[datetime] = None
    notes: str = ""
    next_action: str = ""

class DealCloser:
    """Advanced deal closing and management system"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Initialize database
        self.db_path = 'data/deals.db (SQLite - removed)
        self._init_database()
        
        # Deal stage transitions and probabilities
        self.stage_probabilities = {
            DealStage.LEAD: 10,
            DealStage.QUALIFIED: 25,
            DealStage.PROPOSAL_SENT: 40,
            DealStage.NEGOTIATION: 60,
            DealStage.VERIFICATION: 80,
            DealStage.CLOSING: 90,
            DealStage.CLOSED_WON: 100,
            DealStage.CLOSED_LOST: 0
        }
        
        # Next action templates by stage
        self.next_actions = {
            DealStage.LEAD: "Qualify lead and verify requirements",
            DealStage.QUALIFIED: "Prepare and send property proposal",
            DealStage.PROPOSAL_SENT: "Follow up on proposal and address questions",
            DealStage.NEGOTIATION: "Negotiate terms and conditions",
            DealStage.VERIFICATION: "Complete document verification",
            DealStage.CLOSING: "Prepare closing documents",
            DealStage.CLOSED_WON: "Handover and post-sale support",
            DealStage.CLOSED_LOST: "Analyze reasons and improve process"
        }
        
        # Closing checklists
        self.closing_checklist = {
            DealStage.VERIFICATION: [
                "Verify client identity documents",
                "Check financial capability",
                "Validate property ownership documents",
                "Confirm legal compliance"
            ],
            DealStage.CLOSING: [
                "Prepare sale agreement",
                "Arrange payment schedule",
                "Schedule property handover",
                "Prepare transfer documents"
            ]
        }
    
    def _init_database(self):
        """Initialize deals database"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # Create deals table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS deals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    deal_id TEXT UNIQUE NOT NULL,
                    lead_id TEXT NOT NULL,
                    property_info TEXT NOT NULL,
                    client_info TEXT NOT NULL,
                    stage TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    value REAL NOT NULL,
                    probability REAL NOT NULL,
                    created_at TEXT NOT NULL,
                    expected_close_date TEXT,
                    actual_close_date TEXT,
                    notes TEXT DEFAULT '',
                    next_action TEXT DEFAULT '',
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create deal activities table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS deal_activities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    deal_id TEXT NOT NULL,
                    activity_type TEXT NOT NULL,
                    activity_description TEXT NOT NULL,
                    activity_date TEXT NOT NULL,
                    user_id TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create deal pipeline metrics table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS pipeline_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    metric_date TEXT NOT NULL,
                    stage TEXT NOT NULL,
                    deal_count INTEGER NOT NULL,
                    total_value REAL NOT NULL,
                    avg_probability REAL NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create indexes
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_deals_deal_id ON deals(deal_id)')
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_deals_lead_id ON deals(lead_id)')
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_deals_stage ON deals(stage)')
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_activities_deal_id ON deal_activities(deal_id)')
            
            # conn.commit() removed
            # conn.close() removed
            
            self.logger.info("Deals database initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Error initializing deals database: {e}")
            raise
    
    def create_deal_from_lead(self, lead_data: Dict, property_info: Dict) -> str:
        """Create a new deal from lead data"""
        try:
            deal_id = f"deal_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            lead_id = lead_data.get('id', 'unknown')
            
            # Extract client information
            client_info = {
                'name': self._extract_name_from_lead(lead_data),
                'contact': lead_data.get('contact_info', {}),
                'source': lead_data.get('source', 'unknown'),
                'requirements': self._extract_requirements_from_lead(lead_data)
            }
            
            # Determine initial priority and value
            priority = self._determine_deal_priority(lead_data, property_info)
            value = self._estimate_deal_value(lead_data, property_info)
            
            # Create deal
            deal = Deal(
                deal_id=deal_id,
                lead_id=lead_id,
                property_info=property_info,
                client_info=client_info,
                stage=DealStage.LEAD,
                priority=priority,
                value=value,
                probability=self.stage_probabilities[DealStage.LEAD],
                created_at=datetime.now(),
                expected_close_date=self._estimate_close_date(priority),
                next_action=self.next_actions[DealStage.LEAD]
            )
            
            # Save to database
            self._save_deal(deal)
            
            # Log activity
            self._log_activity(deal_id, "deal_created", f"Deal created from lead {lead_id}")
            
            self.logger.info(f"Created deal {deal_id} for lead {lead_id} with value {value:,.0f}")
            return deal_id
            
        except Exception as e:
            self.logger.error(f"Error creating deal from lead {lead_data.get('id', 'unknown')}: {e}")
            return ""
    
    def _extract_name_from_lead(self, lead_data: Dict) -> str:
        """Extract client name from lead data"""
        # Try to extract from title or content
        title = lead_data.get('title', '')
        content = lead_data.get('content_snippet', '')
        
        # Simple name extraction (can be enhanced with NLP)
        import re
        
        # Look for common name patterns
        name_patterns = [
            r'(?:Halo|Hi|Hello)\s+([A-Z][a-z]+\s+[A-Z][a-z]+)',
            r'([A-Z][a-z]+\s+[A-Z][a-z]+)\s+(?:mencari|cari|butuh)',
            r'Contact\s*:\s*([A-Z][a-z]+\s+[A-Z][a-z]+)'
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, f"{title} {content}")
            if match:
                return match.group(1)
        
        # Fallback to generic name
        return f"Client {lead_data.get('id', 'Unknown')}"
    
    def _extract_requirements_from_lead(self, lead_data: Dict) -> Dict:
        """Extract client requirements from lead data"""
        content = lead_data.get('content_snippet', '').lower()
        title = lead_data.get('title', '').lower()
        full_text = f"{title} {content}"
        
        requirements = {
            'property_type': 'unknown',
            'location': 'Serang',
            'price_range': 'unknown',
            'bedrooms': 'unknown',
            'urgency': 'medium'
        }
        
        # Extract property type
        if 'rumah' in full_text:
            requirements['property_type'] = 'house'
        elif 'apartemen' in full_text or 'apartment' in full_text:
            requirements['property_type'] = 'apartment'
        elif 'tanah' in full_text:
            requirements['property_type'] = 'land'
        
        # Extract price range
        import re
        price_patterns = [
            r'(\d+)\s*juta',
            r'(\d+)\s*miliar',
            r'rp\s*(\d+(?:\.\d+)?)'
        ]
        
        for pattern in price_patterns:
            match = re.search(pattern, full_text)
            if match:
                price = float(match.group(1))
                if 'miliar' in full_text:
                    requirements['price_range'] = f"{price*1000}M"
                else:
                    requirements['price_range'] = f"{price}M"
                break
        
        # Extract bedrooms
        bedroom_patterns = [
            r'(\d+)\s*kamar',
            r'(\d+)\s*kt',
            r'type\s*(\d+)'
        ]
        
        for pattern in bedroom_patterns:
            match = re.search(pattern, full_text)
            if match:
                requirements['bedrooms'] = int(match.group(1))
                break
        
        # Extract urgency
        urgency_keywords = ['segera', 'urgent', 'butuh', 'cepat', 'sekarang']
        if any(keyword in full_text for keyword in urgency_keywords):
            requirements['urgency'] = 'high'
        
        return requirements
    
    def _determine_deal_priority(self, lead_data: Dict, property_info: Dict) -> DealPriority:
        """Determine deal priority based on lead and property data"""
        score = 0
        
        # Lead quality indicators
        if lead_data.get('contact_info', {}).get('phone'):
            score += 2
        if lead_data.get('contact_info', {}).get('email'):
            score += 1
        
        # Content analysis
        content = lead_data.get('content_snippet', '').lower()
        if any(keyword in content for keyword in ['segera', 'butuh', 'urgent']):
            score += 2
        if any(keyword in content for keyword in ['nego', 'bisa nego', 'negoisasi']):
            score += 1
        
        # Property value indicators
        if property_info.get('price', 0) > 0:
            if property_info['price'] < 500000000:  # < 500 juta
                score += 2
            elif property_info['price'] < 1000000000:  # < 1 miliar
                score += 1
        
        # Determine priority
        if score >= 5:
            return DealPriority.CRITICAL
        elif score >= 3:
            return DealPriority.HIGH
        elif score >= 2:
            return DealPriority.MEDIUM
        else:
            return DealPriority.LOW
    
    def _estimate_deal_value(self, lead_data: Dict, property_info: Dict) -> float:
        """Estimate deal value"""
        # Try to get price from property info
        if property_info.get('price'):
            return float(property_info['price'])
        
        # Try to extract from lead content
        content = lead_data.get('content_snippet', '')
        import re
        
        # Look for price patterns
        price_patterns = [
            r'(\d+(?:\.\d+)?)\s*juta',
            r'(\d+(?:\.\d+)?)\s*miliar',
            r'rp\s*(\d+(?:\.\d+)?)'
        ]
        
        for pattern in price_patterns:
            match = re.search(pattern, content.lower())
            if match:
                price = float(match.group(1))
                if 'miliar' in content.lower():
                    return price * 1000000000
                elif 'juta' in content.lower():
                    return price * 1000000
                else:
                    return price
        
        # Default estimation based on Serang market
        return 350000000  # 350 juta default
    
    def _estimate_close_date(self, priority: DealPriority) -> datetime:
        """Estimate expected close date based on priority"""
        if priority == DealPriority.CRITICAL:
            return datetime.now() + timedelta(days=14)
        elif priority == DealPriority.HIGH:
            return datetime.now() + timedelta(days=30)
        elif priority == DealPriority.MEDIUM:
            return datetime.now() + timedelta(days=60)
        else:
            return datetime.now() + timedelta(days=90)
    
    def _save_deal(self, deal: Deal):
        """Save deal to database"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # cursor.execute() removed'''
                INSERT OR REPLACE INTO deals 
                (deal_id, lead_id, property_info, client_info, stage, priority, 
                 value, probability, created_at, expected_close_date, 
                 actual_close_date, notes, next_action)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                deal.deal_id,
                deal.lead_id,
                json.dumps(deal.property_info),
                json.dumps(deal.client_info),
                deal.stage.value,
                deal.priority.value,
                deal.value,
                deal.probability,
                deal.created_at.isoformat(),
                deal.expected_close_date.isoformat() if deal.expected_close_date else None,
                deal.actual_close_date.isoformat() if deal.actual_close_date else None,
                deal.notes,
                deal.next_action
            ))
            
            # conn.commit() removed
            # conn.close() removed
            
        except Exception as e:
            self.logger.error(f"Error saving deal {deal.deal_id}: {e}")
            raise
    
    def _log_activity(self, deal_id: str, activity_type: str, description: str):
        """Log deal activity"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # cursor.execute() removed'''
                INSERT INTO deal_activities (deal_id, activity_type, activity_description, activity_date)
                VALUES (?, ?, ?, ?)
            ''', (deal_id, activity_type, description, datetime.now().isoformat()))
            
            # conn.commit() removed
            # conn.close() removed
            
        except Exception as e:
            self.logger.error(f"Error logging activity for deal {deal_id}: {e}")
    
    def advance_deal_stage(self, deal_id: str, new_stage: DealStage, notes: str = "") -> bool:
        """Advance deal to next stage"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # Get current deal
            # cursor.execute() removed'SELECT * FROM deals WHERE deal_id = ?', (deal_id,))
            result = cursor.fetchone()
            
            if not result:
                self.logger.error(f"Deal {deal_id} not found")
                return False
            
            columns = [desc[0] for desc in cursor.description]
            deal_data = dict(zip(columns, result))
            
            # Update deal
            new_probability = self.stage_probabilities[new_stage]
            new_next_action = self.next_actions[new_stage]
            
            if new_stage in [DealStage.CLOSED_WON, DealStage.CLOSED_LOST]:
                actual_close_date = datetime.now().isoformat()
            else:
                actual_close_date = None
            
            # cursor.execute() removed'''
                UPDATE deals 
                SET stage = ?, probability = ?, next_action = ?, 
                    actual_close_date = ?, notes = ?, updated_at = ?
                WHERE deal_id = ?
            ''', (
                new_stage.value,
                new_probability,
                new_next_action,
                actual_close_date,
                notes,
                datetime.now().isoformat(),
                deal_id
            ))
            
            # conn.commit() removed
            # conn.close() removed
            
            # Log activity
            self._log_activity(deal_id, "stage_advanced", f"Advanced to {new_stage.value}: {notes}")
            
            self.logger.info(f"Advanced deal {deal_id} to {new_stage.value}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error advancing deal {deal_id}: {e}")
            return False
    
    def get_deal_pipeline(self) -> Dict:
        """Get current deal pipeline by stages"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            pipeline = {}
            total_value = 0
            
            for stage in DealStage:
                # cursor.execute() removed'''
                    SELECT COUNT(*), SUM(value), AVG(probability)
                    FROM deals 
                    WHERE stage = ? AND actual_close_date IS NULL
                ''', (stage.value,))
                
                count, value, prob = cursor.fetchone()
                
                pipeline[stage.value] = {
                    'count': count or 0,
                    'total_value': value or 0,
                    'avg_probability': prob or 0,
                    'weighted_value': (value or 0) * ((prob or 0) / 100)
                }
                
                total_value += pipeline[stage.value]['weighted_value']
            
            # conn.close() removed
            
            pipeline['total_pipeline_value'] = total_value
            return pipeline
            
        except Exception as e:
            self.logger.error(f"Error getting deal pipeline: {e}")
            return {}
    
    def generate_closing_checklist(self, deal_id: str) -> Dict:
        """Generate closing checklist for a deal"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # cursor.execute() removed'SELECT stage FROM deals WHERE deal_id = ?', (deal_id,))
            result = cursor.fetchone()
            
            if not result:
                return {}
            
            stage = DealStage(result[0])
            checklist = self.closing_checklist.get(stage, [])
            
            # conn.close() removed
            
            return {
                'deal_id': deal_id,
                'stage': stage.value,
                'checklist': checklist,
                'completion_percentage': 0  # Can be enhanced with actual tracking
            }
            
        except Exception as e:
            self.logger.error(f"Error generating checklist for deal {deal_id}: {e}")
            return {}
    
    def get_deal_metrics(self) -> Dict:
        """Get comprehensive deal metrics"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # Basic statistics
            # cursor.execute() removed'SELECT COUNT(*) FROM deals')
            total_deals = cursor.fetchone()[0]
            
            # cursor.execute() removed'SELECT COUNT(*) FROM deals WHERE stage = ?', (DealStage.CLOSED_WON.value,))
            won_deals = cursor.fetchone()[0]
            
            # cursor.execute() removed'SELECT COUNT(*) FROM deals WHERE stage = ?', (DealStage.CLOSED_LOST.value,))
            lost_deals = cursor.fetchone()[0]
            
            # Value metrics
            # cursor.execute() removed'SELECT SUM(value) FROM deals WHERE stage = ?', (DealStage.CLOSED_WON.value,))
            won_value = cursor.fetchone()[0] or 0
            
            # cursor.execute() removed'SELECT AVG(value) FROM deals WHERE stage = ?', (DealStage.CLOSED_WON.value,))
            avg_deal_value = cursor.fetchone()[0] or 0
            
            # Conversion rates
            conversion_rate = (won_deals / max(total_deals, 1)) * 100
            
            # Average deal cycle
            # cursor.execute() removed'''
                SELECT AVG(JULIANDAY(actual_close_date) - JULIANDAY(created_at))
                FROM deals 
                WHERE stage = ? AND actual_close_date IS NOT NULL
            ''', (DealStage.CLOSED_WON.value,))
            
            avg_cycle_days = cursor.fetchone()[0] or 0
            
            # conn.close() removed
            
            metrics = {
                'total_deals': total_deals,
                'won_deals': won_deals,
                'lost_deals': lost_deals,
                'active_deals': total_deals - won_deals - lost_deals,
                'conversion_rate': conversion_rate,
                'won_value': won_value,
                'avg_deal_value': avg_deal_value,
                'avg_cycle_days': avg_cycle_days,
                'generated_at': datetime.now().isoformat()
            }
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Error getting deal metrics: {e}")
            return {}

def main():
    """Main function to demonstrate deal closer"""
    print("=" * 60)
    print("💼 DEAL CLOSER - CLOSER AGENT")
    print("=" * 60)
    
    # Initialize deal closer
    deal_closer = DealCloser()
    
    # Load test leads and create deals
    print("📥 Creating deals from search results...")
    
    try:
        with open('test_leads_results.json', 'r', encoding='utf-8') as f:
            leads_data = json.load(f)
        
        leads = leads_data.get('leads', [])
        deals_created = 0
        
        for lead in leads[:3]:  # Create deals for first 3 leads
            # Mock property info (would come from property database)
            property_info = {
                'title': lead.get('title', ''),
                'url': lead.get('url', ''),
                'price': deal_closer._estimate_deal_value(lead, {}),
                'location': 'Serang',
                'type': 'house'
            }
            
            deal_id = deal_closer.create_deal_from_lead(lead, property_info)
            if deal_id:
                deals_created += 1
                print(f"  ✅ Created deal: {deal_id}")
        
        print(f"📊 Created {deals_created} deals from {len(leads)} leads")
        
    except Exception as e:
        print(f"❌ Error loading leads: {e}")
    
    # Get deal pipeline
    print("\n📈 Current Deal Pipeline:")
    pipeline = deal_closer.get_deal_pipeline()
    
    for stage, data in pipeline.items():
        if stage != 'total_pipeline_value':
            print(f"  {stage}: {data['count']} deals, Rp {data['total_value']:,.0f} value")
    
    print(f"\n💰 Total Pipeline Value: Rp {pipeline.get('total_pipeline_value', 0):,.0f}")
    
    # Get deal metrics
    print("\n📊 Deal Metrics:")
    metrics = deal_closer.get_deal_metrics()
    
    if metrics:
        print(f"  - Total Deals: {metrics.get('total_deals', 0)}")
        print(f"  - Won Deals: {metrics.get('won_deals', 0)}")
        print(f"  - Conversion Rate: {metrics.get('conversion_rate', 0):.1f}%")
        print(f"  - Average Deal Value: Rp {metrics.get('avg_deal_value', 0):,.0f}")
        print(f"  - Average Cycle: {metrics.get('avg_cycle_days', 0):.0f} days")
    
    # Save metrics
    metrics_file = 'deal_metrics.json'
    with open(metrics_file, 'w', encoding='utf-8') as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)
    
    print(f"\n📁 Metrics saved to: {metrics_file}")
    
    print("\n" + "=" * 60)
    print("✅ DEAL CLOSER SETUP COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()
