#!/usr/bin/env python3
"""
Partner Network Manager - Partner Agent
Comprehensive partner relationship and network management system
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

class PartnerStatus(Enum):
    """Partner status tracking"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    TERMINATED = "terminated"
    PENDING = "pending"

class PartnerType(Enum):
    """Types of partners"""
    INDIVIDUAL_AGENT = "individual_agent"
    PROPERTY_AGENCY = "property_agency"
    DEVELOPER = "developer"
    INFLUENCER = "influencer"
    CORPORATE_PARTNER = "corporate_partner"
    REFINERRAL_PARTNER = "referral_partner"

class PartnershipLevel(Enum):
    """Partnership levels"""
    BASIC = "basic"
    PREMIUM = "premium"
    ELITE = "elite"
    PLATINUM = "platinum"
    DIAMOND = "diamond"

@dataclass
class Partner:
    """Partner information structure"""
    partner_id: str
    name: str
    partner_type: PartnerType
    status: PartnerStatus
    partnership_level: PartnershipLevel
    contact_info: Dict
    business_info: Dict
    performance_metrics: Dict
    joined_date: datetime
    last_active: Optional[datetime] = None
    notes: str = ""

@dataclass
class PartnershipAgreement:
    """Partnership agreement details"""
    agreement_id: str
    partner_id: str
    agreement_type: str
    terms: Dict
    commission_rate: float
    benefits: List[str]
    obligations: List[str]
    start_date: datetime
    end_date: Optional[datetime]
    status: str = "active"
    created_at: datetime = datetime.now()

@dataclass
class PartnershipActivity:
    """Partnership activity tracking"""
    activity_id: str
    partner_id: str
    activity_type: str
    description: str
    outcome: str
    date: datetime
    value: float = 0.0
    notes: str = ""

class PartnerNetworkManager:
    """Comprehensive partner network management system"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Initialize database
        self.db_path = 'data/partner_network.db (SQLite - removed)
        self._init_database()
        
        # Partnership benefits by level
        self.level_benefits = {
            PartnershipLevel.BASIC: [
                "Standard commission rate",
                "Basic marketing materials",
                "Email support"
            ],
            PartnershipLevel.PREMIUM: [
                "Enhanced commission rate",
                "Premium marketing materials",
                "Priority support",
                "Monthly performance reports"
            ],
            PartnershipLevel.ELITE: [
                "Maximum commission rate",
                "Exclusive marketing materials",
                "Dedicated account manager",
                "Weekly performance reports",
                "Lead generation support"
            ],
            PartnershipLevel.PLATINUM: [
                "Maximum commission + bonus",
                "Custom marketing materials",
                "Dedicated account team",
                "Real-time performance dashboard",
                "Exclusive territories",
                "Co-marketing opportunities"
            ],
            PartnershipLevel.DIAMOND: [
                "Maximum commission + profit sharing",
                "Full marketing studio access",
                "Executive account team",
                "Custom analytics platform",
                "Exclusive territories + expansion rights",
                "Strategic partnership opportunities",
                "Board advisory role"
            ]
        }
        
        # Level qualification criteria
        self.level_criteria = {
            PartnershipLevel.BASIC: {'min_deals': 0, 'min_value': 0, 'min_months': 0},
            PartnershipLevel.PREMIUM: {'min_deals': 5, 'min_value': 500000000, 'min_months': 3},
            PartnershipLevel.ELITE: {'min_deals': 15, 'min_value': 1500000000, 'min_months': 6},
            PartnershipLevel.PLATINUM: {'min_deals': 30, 'min_value': 3000000000, 'min_months': 12},
            PartnershipLevel.DIAMOND: {'min_deals': 50, 'min_value': 5000000000, 'min_months': 24}
        }
        
        # Commission rates by level
        self.level_commission_rates = {
            PartnershipLevel.BASIC: 1.0,    # 1%
            PartnershipLevel.PREMIUM: 1.5,  # 1.5%
            PartnershipLevel.ELITE: 2.0,    # 2%
            PartnershipLevel.PLATINUM: 2.5, # 2.5%
            PartnershipLevel.DIAMOND: 3.0   # 3%
        }
    
    def _init_database(self):
        """Initialize partner network database"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # Create partners table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS partners (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    partner_id TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    partner_type TEXT NOT NULL,
                    status TEXT NOT NULL,
                    partnership_level TEXT NOT NULL,
                    contact_info TEXT NOT NULL,
                    business_info TEXT NOT NULL,
                    performance_metrics TEXT NOT NULL,
                    joined_date TEXT NOT NULL,
                    last_active TEXT,
                    notes TEXT DEFAULT '',
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create partnership agreements table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS partnership_agreements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    agreement_id TEXT UNIQUE NOT NULL,
                    partner_id TEXT NOT NULL,
                    agreement_type TEXT NOT NULL,
                    terms TEXT NOT NULL,
                    commission_rate REAL NOT NULL,
                    benefits TEXT NOT NULL,
                    obligations TEXT NOT NULL,
                    start_date TEXT NOT NULL,
                    end_date TEXT,
                    status TEXT DEFAULT 'active',
                    created_at TEXT NOT NULL
                )
            ''')
            
            # Create partnership activities table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS partnership_activities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    activity_id TEXT UNIQUE NOT NULL,
                    partner_id TEXT NOT NULL,
                    activity_type TEXT NOT NULL,
                    description TEXT NOT NULL,
                    outcome TEXT NOT NULL,
                    activity_date TEXT NOT NULL,
                    value REAL DEFAULT 0,
                    notes TEXT DEFAULT '',
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create partner network table (for connections)
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS partner_network (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    partner_id_1 TEXT NOT NULL,
                    partner_id_2 TEXT NOT NULL,
                    relationship_type TEXT NOT NULL,
                    strength REAL DEFAULT 1.0,
                    collaboration_count INTEGER DEFAULT 0,
                    total_value REAL DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(partner_id_1, partner_id_2)
                )
            ''')
            
            # Create partner performance table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS partner_performance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    partner_id TEXT NOT NULL,
                    period TEXT NOT NULL,
                    deals_closed INTEGER DEFAULT 0,
                    total_value REAL DEFAULT 0,
                    commission_earned REAL DEFAULT 0,
                    leads_generated INTEGER DEFAULT 0,
                    customer_satisfaction REAL DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create indexes
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_partners_partner_id ON partners(partner_id)')
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_partners_status ON partners(status)')
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_agreements_partner_id ON partnership_agreements(partner_id)')
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_activities_partner_id ON partnership_activities(partner_id)')
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_network_partner_1 ON partner_network(partner_id_1)')
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_performance_partner_id ON partner_performance(partner_id)')
            
            # conn.commit() removed
            # conn.close() removed
            
            self.logger.info("Partner network database initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Error initializing partner network database: {e}")
            raise
    
    def add_partner(self, partner_data: Dict) -> str:
        """Add new partner to the network"""
        try:
            partner_id = f"partner_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            partner = Partner(
                partner_id=partner_id,
                name=partner_data.get('name', ''),
                partner_type=PartnerType(partner_data.get('partner_type', 'individual_agent')),
                status=PartnerStatus.PENDING,
                partnership_level=PartnershipLevel.BASIC,
                contact_info=partner_data.get('contact_info', {}),
                business_info=partner_data.get('business_info', {}),
                performance_metrics={
                    'deals_closed': 0,
                    'total_value': 0,
                    'commission_earned': 0,
                    'leads_generated': 0,
                    'customer_satisfaction': 0
                },
                joined_date=datetime.now()
            )
            
            # Save partner
            self._save_partner(partner)
            
            # Create initial partnership agreement
            agreement_id = self.create_partnership_agreement(
                partner_id,
                "standard_partnership",
                self.level_commission_rates[PartnershipLevel.BASIC],
                self.level_benefits[PartnershipLevel.BASIC]
            )
            
            self.logger.info(f"Added partner {partner_id}: {partner.name}")
            return partner_id
            
        except Exception as e:
            self.logger.error(f"Error adding partner: {e}")
            return ""
    
    def _save_partner(self, partner: Partner):
        """Save partner to database"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # cursor.execute() removed'''
                INSERT OR REPLACE INTO partners 
                (partner_id, name, partner_type, status, partnership_level, 
                 contact_info, business_info, performance_metrics, joined_date, last_active, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                partner.partner_id,
                partner.name,
                partner.partner_type.value,
                partner.status.value,
                partner.partnership_level.value,
                json.dumps(partner.contact_info),
                json.dumps(partner.business_info),
                json.dumps(partner.performance_metrics),
                partner.joined_date.isoformat(),
                partner.last_active.isoformat() if partner.last_active else None,
                partner.notes
            ))
            
            # conn.commit() removed
            # conn.close() removed
            
        except Exception as e:
            self.logger.error(f"Error saving partner {partner.partner_id}: {e}")
            raise
    
    def create_partnership_agreement(self, partner_id: str, agreement_type: str, 
                                  commission_rate: float, benefits: List[str]) -> str:
        """Create partnership agreement"""
        try:
            agreement_id = f"agreement_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            agreement = PartnershipAgreement(
                agreement_id=agreement_id,
                partner_id=partner_id,
                agreement_type=agreement_type,
                terms={
                    'commission_rate': commission_rate,
                    'payment_terms': 'monthly',
                    'exclusivity': 'non-exclusive',
                    'territory': 'serang_area',
                    'duration': '12_months'
                },
                commission_rate=commission_rate,
                benefits=benefits,
                obligations=[
                    'Generate qualified leads',
                    'Maintain professional standards',
                    'Submit monthly reports',
                    'Follow ethical guidelines'
                ],
                start_date=datetime.now(),
                end_date=datetime.now() + timedelta(days=365)
            )
            
            # Save agreement
            self._save_agreement(agreement)
            
            self.logger.info(f"Created partnership agreement {agreement_id} for partner {partner_id}")
            return agreement_id
            
        except Exception as e:
            self.logger.error(f"Error creating partnership agreement: {e}")
            return ""
    
    def _save_agreement(self, agreement: PartnershipAgreement):
        """Save partnership agreement to database"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # cursor.execute() removed'''
                INSERT INTO partnership_agreements 
                (agreement_id, partner_id, agreement_type, terms, commission_rate, 
                 benefits, obligations, start_date, end_date, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                agreement.agreement_id,
                agreement.partner_id,
                agreement.agreement_type,
                json.dumps(agreement.terms),
                agreement.commission_rate,
                json.dumps(agreement.benefits),
                json.dumps(agreement.obligations),
                agreement.start_date.isoformat(),
                agreement.end_date.isoformat() if agreement.end_date else None,
                agreement.status,
                agreement.created_at.isoformat()
            ))
            
            # conn.commit() removed
            # conn.close() removed
            
        except Exception as e:
            self.logger.error(f"Error saving agreement {agreement.agreement_id}: {e}")
            raise
    
    def update_partner_level(self, partner_id: str, new_level: PartnershipLevel, 
                           reason: str = "") -> bool:
        """Update partner partnership level"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # Get current partner info
            # cursor.execute() removed'SELECT * FROM partners WHERE partner_id = ?', (partner_id,))
            result = cursor.fetchone()
            
            if not result:
                self.logger.error(f"Partner {partner_id} not found")
                return False
            
            columns = [desc[0] for desc in cursor.description]
            partner_data = dict(zip(columns, result))
            
            old_level = PartnershipLevel(partner_data['partnership_level'])
            
            # Update partner level
            # cursor.execute() removed'''
                UPDATE partners 
                SET partnership_level = ?, updated_at = ?
                WHERE partner_id = ?
            ''', (new_level.value, datetime.now().isoformat(), partner_id))
            
            # Create new agreement with new commission rate
            new_commission_rate = self.level_commission_rates[new_level]
            new_benefits = self.level_benefits[new_level]
            
            agreement_id = self.create_partnership_agreement(
                partner_id,
                f"level_upgrade_{new_level.value}",
                new_commission_rate,
                new_benefits
            )
            
            # Log activity
            self._log_activity(
                partner_id,
                "level_upgrade",
                f"Upgraded from {old_level.value} to {new_level.value}",
                "Partnership level enhanced",
                0,
                reason
            )
            
            # conn.commit() removed
            # conn.close() removed
            
            self.logger.info(f"Updated partner {partner_id} level to {new_level.value}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error updating partner {partner_id} level: {e}")
            return False
    
    def _log_activity(self, partner_id: str, activity_type: str, description: str, 
                     outcome: str, value: float = 0, notes: str = "") -> str:
        """Log partnership activity"""
        try:
            activity_id = f"activity_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            activity = PartnershipActivity(
                activity_id=activity_id,
                partner_id=partner_id,
                activity_type=activity_type,
                description=description,
                outcome=outcome,
                date=datetime.now(),
                value=value,
                notes=notes
            )
            
            # Save activity
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # cursor.execute() removed'''
                INSERT INTO partnership_activities 
                (activity_id, partner_id, activity_type, description, outcome, activity_date, value, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                activity.activity_id,
                activity.partner_id,
                activity.activity_type,
                activity.description,
                activity.outcome,
                activity.date.isoformat(),
                activity.value,
                activity.notes
            ))
            
            # conn.commit() removed
            # conn.close() removed
            
            return activity_id
            
        except Exception as e:
            self.logger.error(f"Error logging activity for partner {partner_id}: {e}")
            return ""
    
    def create_partner_connection(self, partner_id_1: str, partner_id_2: str, 
                               relationship_type: str) -> bool:
        """Create connection between partners"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # cursor.execute() removed'''
                INSERT OR REPLACE INTO partner_network 
                (partner_id_1, partner_id_2, relationship_type, created_at)
                VALUES (?, ?, ?, ?)
            ''', (partner_id_1, partner_id_2, relationship_type, datetime.now().isoformat()))
            
            # conn.commit() removed
            # conn.close() removed
            
            self.logger.info(f"Created connection between {partner_id_1} and {partner_id_2}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating partner connection: {e}")
            return False
    
    def update_partner_performance(self, partner_id: str, period: str, 
                                 metrics: Dict) -> bool:
        """Update partner performance metrics"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # cursor.execute() removed'''
                INSERT OR REPLACE INTO partner_performance 
                (partner_id, period, deals_closed, total_value, commission_earned, 
                 leads_generated, customer_satisfaction, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                partner_id,
                period,
                metrics.get('deals_closed', 0),
                metrics.get('total_value', 0),
                metrics.get('commission_earned', 0),
                metrics.get('leads_generated', 0),
                metrics.get('customer_satisfaction', 0),
                datetime.now().isoformat()
            ))
            
            # conn.commit() removed
            # conn.close() removed
            
            # Check for level upgrade
            self._check_performance_upgrade(partner_id)
            
            self.logger.info(f"Updated performance for partner {partner_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error updating partner performance: {e}")
            return False
    
    def _check_performance_upgrade(self, partner_id: str):
        """Check if partner qualifies for level upgrade"""
        try:
            # Get partner's performance history
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # cursor.execute() removed'''
                SELECT SUM(deals_closed), SUM(total_value), COUNT(DISTINCT period)
                FROM partner_performance 
                WHERE partner_id = ?
            ''', (partner_id,))
            
            total_deals, total_value, months_active = cursor.fetchone()
            
            # cursor.execute() removed'SELECT partnership_level FROM partners WHERE partner_id = ?', (partner_id,))
            current_level_result = cursor.fetchone()
            
            if not current_level_result:
                return
            
            current_level = PartnershipLevel(current_level_result[0])
            
            # conn.close() removed
            
            # Check each level from highest to current
            levels = [PartnershipLevel.DIAMOND, PartnershipLevel.PLATINUM, 
                     PartnershipLevel.ELITE, PartnershipLevel.PREMIUM]
            
            for level in levels:
                if level == current_level:
                    break
                
                criteria = self.level_criteria[level]
                if (total_deals >= criteria['min_deals'] and 
                    total_value >= criteria['min_value'] and 
                    months_active >= criteria['min_months']):
                    self.update_partner_level(
                        partner_id, 
                        level, 
                        f"Performance upgrade: {total_deals} deals, Rp {total_value:,.0f} value"
                    )
                    break
            
        except Exception as e:
            self.logger.error(f"Error checking performance upgrade for {partner_id}: {e}")
    
    def get_partner_network_analysis(self) -> Dict:
        """Analyze partner network structure and performance"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # Partner distribution by type
            # cursor.execute() removed'SELECT partner_type, COUNT(*) FROM partners GROUP BY partner_type')
            type_distribution = dict(cursor.fetchall())
            
            # Partner distribution by level
            # cursor.execute() removed'SELECT partnership_level, COUNT(*) FROM partners GROUP BY partnership_level')
            level_distribution = dict(cursor.fetchall())
            
            # Partner status distribution
            # cursor.execute() removed'SELECT status, COUNT(*) FROM partners GROUP BY status')
            status_distribution = dict(cursor.fetchall())
            
            # Network connections
            # cursor.execute() removed'SELECT COUNT(*) FROM partner_network')
            total_connections = cursor.fetchone()[0]
            
            # Performance metrics
            # cursor.execute() removed'''
                SELECT SUM(deals_closed), SUM(total_value), SUM(commission_earned)
                FROM partner_performance
            ''')
            total_deals, total_value, total_commissions = cursor.fetchone()
            
            # Top performing partners
            # cursor.execute() removed'''
                SELECT p.name, p.partner_id, SUM(pp.total_value) as total_value
                FROM partners p
                JOIN partner_performance pp ON p.partner_id = pp.partner_id
                GROUP BY p.partner_id
                ORDER BY total_value DESC
                LIMIT 5
            ''')
            
            top_partners = []
            for row in cursor.fetchall():
                top_partners.append({
                    'name': row[0],
                    'partner_id': row[1],
                    'total_value': row[2]
                })
            
            # conn.close() removed
            
            analysis = {
                'generated_at': datetime.now().isoformat(),
                'partner_statistics': {
                    'total_partners': sum(status_distribution.values()),
                    'type_distribution': type_distribution,
                    'level_distribution': level_distribution,
                    'status_distribution': status_distribution
                },
                'network_statistics': {
                    'total_connections': total_connections,
                    'average_connections_per_partner': total_connections / max(sum(status_distribution.values()), 1)
                },
                'performance_statistics': {
                    'total_deals_closed': total_deals or 0,
                    'total_deal_value': total_value or 0,
                    'total_commissions_earned': total_commissions or 0
                },
                'top_performers': top_partners
            }
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing partner network: {e}")
            return {}
    
    def create_sample_network(self) -> int:
        """Create sample partner network for testing"""
        try:
            sample_partners = [
                {
                    'name': 'PT. Properti Bersama',
                    'partner_type': 'property_agency',
                    'contact_info': {
                        'phone': '021-5551234',
                        'email': 'info@propertibersama.com',
                        'address': 'Jakarta Selatan'
                    },
                    'business_info': {
                        'established': '2015',
                        'employees': '15',
                        'specialization': 'residential',
                        'territory': 'jabodetabek'
                    }
                },
                {
                    'name': 'CV. Agen Rumahku',
                    'partner_type': 'individual_agent',
                    'contact_info': {
                        'phone': '0812-3456-7890',
                        'email': 'agenrumahku@gmail.com',
                        'address': 'Bandung'
                    },
                    'business_info': {
                        'experience': '5_years',
                        'specialization': 'first_home_buyers',
                        'territory': 'bandung_area'
                    }
                },
                {
                    'name': 'PT. Developer Maju',
                    'partner_type': 'developer',
                    'contact_info': {
                        'phone': '022-6677889',
                        'email': 'marketing@developermaju.com',
                        'address': 'Surabaya'
                    },
                    'business_info': {
                        'projects_completed': '10',
                        'ongoing_projects': '3',
                        'specialization': 'affordable_housing'
                    }
                },
                {
                    'name': 'Property Influencer ID',
                    'partner_type': 'influencer',
                    'contact_info': {
                        'phone': '0856-7890-1234',
                        'email': 'manager@influencer.id',
                        'social_media': '@propertyinfluencer'
                    },
                    'business_info': {
                        'followers': '50000',
                        'engagement_rate': '5%',
                        'specialization': 'property_reviews'
                    }
                }
            ]
            
            created_partners = []
            for partner_data in sample_partners:
                partner_id = self.add_partner(partner_data)
                if partner_id:
                    created_partners.append(partner_id)
            
            # Create some connections
            if len(created_partners) >= 2:
                self.create_partner_connection(created_partners[0], created_partners[1], "referral")
                self.create_partner_connection(created_partners[0], created_partners[2], "collaboration")
                self.create_partner_connection(created_partners[1], created_partners[3], "marketing")
            
            # Update some performance data
            for i, partner_id in enumerate(created_partners):
                performance = {
                    'deals_closed': i + 2,
                    'total_value': (i + 2) * 300000000,
                    'commission_earned': (i + 2) * 4500000,
                    'leads_generated': (i + 1) * 10,
                    'customer_satisfaction': 4.5 - (i * 0.2)
                }
                
                self.update_partner_performance(partner_id, "2026-05", performance)
            
            self.logger.info(f"Created sample network with {len(created_partners)} partners")
            return len(created_partners)
            
        except Exception as e:
            self.logger.error(f"Error creating sample network: {e}")
            return 0

def main():
    """Main function to demonstrate partner network manager"""
    print("=" * 60)
    print("🤝 PARTNER NETWORK MANAGER - PARTNER AGENT")
    print("=" * 60)
    
    # Initialize partner network manager
    pnm = PartnerNetworkManager()
    
    # Create sample network
    print("👥 Creating sample partner network...")
    created = pnm.create_sample_network()
    print(f"✅ Created {created} sample partners")
    
    # Get network analysis
    print("\n📊 Analyzing partner network...")
    analysis = pnm.get_partner_network_analysis()
    
    if analysis:
        print("📈 Network Statistics:")
        partner_stats = analysis.get('partner_statistics', {})
        print(f"  - Total Partners: {partner_stats.get('total_partners', 0)}")
        print(f"  - Type Distribution: {partner_stats.get('type_distribution', {})}")
        print(f"  - Level Distribution: {partner_stats.get('level_distribution', {})}")
        print(f"  - Status Distribution: {partner_stats.get('status_distribution', {})}")
        
        network_stats = analysis.get('network_statistics', {})
        print(f"  - Total Connections: {network_stats.get('total_connections', 0)}")
        print(f"  - Avg Connections/Partner: {network_stats.get('average_connections_per_partner', 0):.1f}")
        
        performance_stats = analysis.get('performance_statistics', {})
        print(f"  - Total Deals: {performance_stats.get('total_deals_closed', 0)}")
        print(f"  - Total Value: Rp {performance_stats.get('total_deal_value', 0):,.0f}")
        print(f"  - Total Commissions: Rp {performance_stats.get('total_commissions_earned', 0):,.0f}")
        
        top_performers = analysis.get('top_performers', [])
        if top_performers:
            print(f"\n🏆 Top Performers:")
            for i, partner in enumerate(top_performers):
                print(f"  {i+1}. {partner['name']} - Rp {partner['total_value']:,.0f}")
    
    # Save analysis
    analysis_file = 'partner_network_analysis.json'
    with open(analysis_file, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    
    print(f"\n📁 Analysis saved to: {analysis_file}")
    
    print("\n" + "=" * 60)
    print("✅ PARTNER NETWORK MANAGER SETUP COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()
