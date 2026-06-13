#!/usr/bin/env python3
"""
Customer Success Manager - Closer Agent
Post-sale management and customer relationship system
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

class CustomerStatus(Enum):
    """Customer relationship status"""
    NEW_CUSTOMER = "new_customer"
    ONBOARDING = "onboarding"
    ACTIVE = "active"
    AT_RISK = "at_risk"
    CHURNED = "churned"
    REFERRAL_SOURCE = "referral_source"

class SatisfactionLevel(Enum):
    """Customer satisfaction levels"""
    VERY_DISSATISFIED = 1
    DISSATISFIED = 2
    NEUTRAL = 3
    SATISFIED = 4
    VERY_SATISFIED = 5

class InteractionType(Enum):
    """Types of customer interactions"""
    PHONE_CALL = "phone_call"
    EMAIL = "email"
    SITE_VISIT = "site_visit"
    DOCUMENTATION = "documentation"
    PAYMENT = "payment"
    COMPLAINT = "complaint"
    REQUEST = "request"
    FEEDBACK = "feedback"

@dataclass
class Customer:
    """Customer data structure"""
    customer_id: str
    deal_id: str
    personal_info: Dict
    property_info: Dict
    purchase_info: Dict
    status: CustomerStatus
    satisfaction_score: SatisfactionLevel
    created_at: datetime
    last_contact: Optional[datetime] = None
    next_follow_up: Optional[datetime] = None
    notes: str = ""
    referral_count: int = 0
    total_value: float = 0

@dataclass
class Interaction:
    """Customer interaction record"""
    interaction_id: str
    customer_id: str
    interaction_type: InteractionType
    description: str
    outcome: str
    satisfaction_rating: Optional[SatisfactionLevel]
    interaction_date: datetime
    follow_up_required: bool = False
    follow_up_date: Optional[datetime] = None
    notes: str = ""

class CustomerSuccessManager:
    """Customer success and relationship management system"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Initialize database
        self.db_path = 'data/customer_success.db (SQLite - removed)
        self._init_database()
        
        # Customer journey milestones
        self.journey_milestones = {
            CustomerStatus.NEW_CUSTOMER: [
                "Welcome package sent",
                "Initial contact established",
                "Documentation collection started"
            ],
            CustomerStatus.ONBOARDING: [
                "Property handover completed",
                "Documents processed",
                "Payment schedule confirmed",
                "Keys and access provided"
            ],
            CustomerStatus.ACTIVE: [
                "Settled in property",
                "First satisfaction check",
                "Community integration"
            ]
        }
        
        # Satisfaction improvement actions
        self.satisfaction_actions = {
            SatisfactionLevel.VERY_DISSATISFIED: [
                "Immediate manager intervention",
                "Problem resolution within 24 hours",
                "Compensation offer if applicable"
            ],
            SatisfactionLevel.DISSATISFIED: [
                "Personal follow-up call",
                "Issue investigation",
                "Resolution plan communication"
            ],
            SatisfactionLevel.NEUTRAL: [
                "Regular check-ins",
                "Value-added services offer",
                "Community engagement invitation"
            ],
            SatisfactionLevel.SATISFIED: [
                "Referral program invitation",
                "Testimonial request",
                "Exclusive offers"
            ],
            SatisfactionLevel.VERY_SATISFIED: [
                "VIP status benefits",
                "Referral multiplier program",
                "Case study opportunity"
            ]
        }
        
        # Follow-up schedules by status
        self.follow_up_schedules = {
            CustomerStatus.NEW_CUSTOMER: timedelta(days=3),
            CustomerStatus.ONBOARDING: timedelta(days=7),
            CustomerStatus.ACTIVE: timedelta(days=30),
            CustomerStatus.AT_RISK: timedelta(days=7),
            CustomerStatus.REFERRAL_SOURCE: timedelta(days=60)
        }
    
    def _init_database(self):
        """Initialize customer success database"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # Create customers table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_id TEXT UNIQUE NOT NULL,
                    deal_id TEXT NOT NULL,
                    personal_info TEXT NOT NULL,
                    property_info TEXT NOT NULL,
                    purchase_info TEXT NOT NULL,
                    status TEXT NOT NULL,
                    satisfaction_score INTEGER NOT NULL,
                    created_at TEXT NOT NULL,
                    last_contact TEXT,
                    next_follow_up TEXT,
                    notes TEXT DEFAULT '',
                    referral_count INTEGER DEFAULT 0,
                    total_value REAL DEFAULT 0,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create interactions table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS customer_interactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    interaction_id TEXT UNIQUE NOT NULL,
                    customer_id TEXT NOT NULL,
                    interaction_type TEXT NOT NULL,
                    description TEXT NOT NULL,
                    outcome TEXT NOT NULL,
                    satisfaction_rating INTEGER,
                    interaction_date TEXT NOT NULL,
                    follow_up_required BOOLEAN DEFAULT 0,
                    follow_up_date TEXT,
                    notes TEXT DEFAULT '',
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create satisfaction surveys table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS satisfaction_surveys (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_id TEXT NOT NULL,
                    survey_date TEXT NOT NULL,
                    overall_rating INTEGER NOT NULL,
                    property_quality INTEGER,
                    service_quality INTEGER,
                    communication_quality INTEGER,
                    value_for_money INTEGER,
                    comments TEXT,
                    follow_up_actions TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create referrals table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS referrals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    referrer_customer_id TEXT NOT NULL,
                    referred_customer_id TEXT,
                    referral_date TEXT NOT NULL,
                    status TEXT DEFAULT 'pending',
                    commission_amount REAL DEFAULT 0,
                    commission_paid BOOLEAN DEFAULT 0,
                    notes TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create indexes
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_customers_customer_id ON customers(customer_id)')
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_customers_status ON customers(status)')
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_interactions_customer_id ON customer_interactions(customer_id)')
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_surveys_customer_id ON satisfaction_surveys(customer_id)')
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_referrals_referrer_id ON referrals(referrer_customer_id)')
            
            # conn.commit() removed
            # conn.close() removed
            
            self.logger.info("Customer success database initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Error initializing customer success database: {e}")
            raise
    
    def create_customer_from_deal(self, deal_data: Dict) -> str:
        """Create customer record from closed deal"""
        try:
            customer_id = f"cust_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            deal_id = deal_data.get('deal_id', 'unknown')
            
            # Extract customer information
            personal_info = {
                'name': deal_data.get('client_info', {}).get('name', 'Unknown'),
                'contact': deal_data.get('client_info', {}).get('contact', {}),
                'source': deal_data.get('client_info', {}).get('source', 'direct')
            }
            
            property_info = deal_data.get('property_info', {})
            purchase_info = {
                'purchase_date': datetime.now().isoformat(),
                'purchase_price': deal_data.get('value', 0),
                'payment_method': 'cash',  # Default, should be updated
                'deal_stage': deal_data.get('stage', 'unknown')
            }
            
            # Create customer
            customer = Customer(
                customer_id=customer_id,
                deal_id=deal_id,
                personal_info=personal_info,
                property_info=property_info,
                purchase_info=purchase_info,
                status=CustomerStatus.NEW_CUSTOMER,
                satisfaction_score=SatisfactionLevel.NEUTRAL,
                created_at=datetime.now(),
                last_contact=datetime.now(),
                next_follow_up=datetime.now() + self.follow_up_schedules[CustomerStatus.NEW_CUSTOMER],
                total_value=deal_data.get('value', 0)
            )
            
            # Save to database
            self._save_customer(customer)
            
            # Log initial interaction
            self._create_interaction(
                customer_id,
                InteractionType.DOCUMENTATION,
                "Customer onboarded from closed deal",
                "Welcome process initiated",
                None
            )
            
            self.logger.info(f"Created customer {customer_id} from deal {deal_id}")
            return customer_id
            
        except Exception as e:
            self.logger.error(f"Error creating customer from deal {deal_data.get('deal_id', 'unknown')}: {e}")
            return ""
    
    def _save_customer(self, customer: Customer):
        """Save customer to database"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # cursor.execute() removed'''
                INSERT OR REPLACE INTO customers 
                (customer_id, deal_id, personal_info, property_info, purchase_info, 
                 status, satisfaction_score, created_at, last_contact, 
                 next_follow_up, notes, referral_count, total_value)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                customer.customer_id,
                customer.deal_id,
                json.dumps(customer.personal_info),
                json.dumps(customer.property_info),
                json.dumps(customer.purchase_info),
                customer.status.value,
                customer.satisfaction_score.value,
                customer.created_at.isoformat(),
                customer.last_contact.isoformat() if customer.last_contact else None,
                customer.next_follow_up.isoformat() if customer.next_follow_up else None,
                customer.notes,
                customer.referral_count,
                customer.total_value
            ))
            
            # conn.commit() removed
            # conn.close() removed
            
        except Exception as e:
            self.logger.error(f"Error saving customer {customer.customer_id}: {e}")
            raise
    
    def _create_interaction(self, customer_id: str, interaction_type: InteractionType, 
                          description: str, outcome: str, satisfaction_rating: Optional[SatisfactionLevel],
                          follow_up_required: bool = False, follow_up_date: Optional[datetime] = None,
                          notes: str = "") -> str:
        """Create customer interaction record"""
        try:
            interaction_id = f"int_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            interaction = Interaction(
                interaction_id=interaction_id,
                customer_id=customer_id,
                interaction_type=interaction_type,
                description=description,
                outcome=outcome,
                satisfaction_rating=satisfaction_rating,
                interaction_date=datetime.now(),
                follow_up_required=follow_up_required,
                follow_up_date=follow_up_date,
                notes=notes
            )
            
            # Save to database
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # cursor.execute() removed'''
                INSERT INTO customer_interactions 
                (interaction_id, customer_id, interaction_type, description, outcome, 
                 satisfaction_rating, interaction_date, follow_up_required, follow_up_date, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                interaction.interaction_id,
                interaction.customer_id,
                interaction.interaction_type.value,
                interaction.description,
                interaction.outcome,
                interaction.satisfaction_rating.value if interaction.satisfaction_rating else None,
                interaction.interaction_date.isoformat(),
                interaction.follow_up_required,
                interaction.follow_up_date.isoformat() if interaction.follow_up_date else None,
                interaction.notes
            ))
            
            # conn.commit() removed
            # conn.close() removed
            
            return interaction_id
            
        except Exception as e:
            self.logger.error(f"Error creating interaction for customer {customer_id}: {e}")
            return ""
    
    def update_customer_status(self, customer_id: str, new_status: CustomerStatus, 
                             notes: str = "") -> bool:
        """Update customer status and schedule follow-ups"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # Calculate next follow-up date
            next_follow_up = datetime.now() + self.follow_up_schedules[new_status]
            
            # cursor.execute() removed'''
                UPDATE customers 
                SET status = ?, next_follow_up = ?, notes = ?, updated_at = ?
                WHERE customer_id = ?
            ''', (
                new_status.value,
                next_follow_up.isoformat(),
                notes,
                datetime.now().isoformat(),
                customer_id
            ))
            
            # conn.commit() removed
            # conn.close() removed
            
            # Log status change interaction
            self._create_interaction(
                customer_id,
                InteractionType.PHONE_CALL,
                f"Status updated to {new_status.value}",
                "Customer status change processed",
                None,
                True,
                next_follow_up,
                notes
            )
            
            self.logger.info(f"Updated customer {customer_id} status to {new_status.value}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error updating customer {customer_id} status: {e}")
            return False
    
    def record_satisfaction_survey(self, customer_id: str, survey_data: Dict) -> str:
        """Record customer satisfaction survey"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # Calculate overall satisfaction
            ratings = [
                survey_data.get('overall_rating', 3),
                survey_data.get('property_quality', 3),
                survey_data.get('service_quality', 3),
                survey_data.get('communication_quality', 3),
                survey_data.get('value_for_money', 3)
            ]
            
            overall_rating = sum(ratings) / len(ratings)
            satisfaction_level = SatisfactionLevel(int(round(overall_rating)))
            
            # Update customer satisfaction score
            # cursor.execute() removed'''
                UPDATE customers 
                SET satisfaction_score = ?, updated_at = ?
                WHERE customer_id = ?
            ''', (satisfaction_level.value, datetime.now().isoformat(), customer_id))
            
            # Save survey
            # cursor.execute() removed'''
                INSERT INTO satisfaction_surveys 
                (customer_id, survey_date, overall_rating, property_quality, 
                 service_quality, communication_quality, value_for_money, comments, follow_up_actions)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                customer_id,
                datetime.now().isoformat(),
                survey_data.get('overall_rating', 3),
                survey_data.get('property_quality', 3),
                survey_data.get('service_quality', 3),
                survey_data.get('communication_quality', 3),
                survey_data.get('value_for_money', 3),
                survey_data.get('comments', ''),
                json.dumps(self.satisfaction_actions.get(satisfaction_level, []))
            ))
            
            # conn.commit() removed
            # conn.close() removed
            
            # Create interaction
            self._create_interaction(
                customer_id,
                InteractionType.FEEDBACK,
                "Satisfaction survey completed",
                f"Overall rating: {overall_rating:.1f}",
                satisfaction_level,
                overall_rating < 4,  # Follow up if not satisfied
                datetime.now() + timedelta(days=7) if overall_rating < 4 else None,
                f"Survey comments: {survey_data.get('comments', '')}"
            )
            
            self.logger.info(f"Recorded satisfaction survey for customer {customer_id}")
            return f"survey_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
        except Exception as e:
            self.logger.error(f"Error recording survey for customer {customer_id}: {e}")
            return ""
    
    def get_pending_follow_ups(self, days_ahead: int = 7) -> List[Dict]:
        """Get customers requiring follow-up"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            end_date = datetime.now() + timedelta(days=days_ahead)
            
            # cursor.execute() removed'''
                SELECT * FROM customers 
                WHERE next_follow_up <= ? 
                ORDER BY next_follow_up ASC
            ''', (end_date.isoformat(),))
            
            columns = [desc[0] for desc in cursor.description]
            customers = []
            
            for row in cursor.fetchall():
                customer = dict(zip(columns, row))
                customers.append(customer)
            
            # conn.close() removed
            
            self.logger.info(f"Found {len(customers)} customers requiring follow-up")
            return customers
            
        except Exception as e:
            self.logger.error(f"Error getting pending follow-ups: {e}")
            return []
    
    def generate_customer_report(self) -> Dict:
        """Generate comprehensive customer success report"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # Customer statistics
            # cursor.execute() removed'SELECT status, COUNT(*) FROM customers GROUP BY status')
            status_stats = dict(cursor.fetchall())
            
            # cursor.execute() removed'SELECT satisfaction_score, COUNT(*) FROM customers GROUP BY satisfaction_score')
            satisfaction_stats = dict(cursor.fetchall())
            
            # Value metrics
            # cursor.execute() removed'SELECT SUM(total_value), AVG(total_value) FROM customers')
            total_value, avg_value = cursor.fetchone()
            
            # Referral metrics
            # cursor.execute() removed'SELECT COUNT(*), SUM(commission_amount) FROM referrals WHERE commission_paid = 1')
            paid_referrals, total_commissions = cursor.fetchone()
            
            # Recent interactions
            # cursor.execute() removed'''
                SELECT COUNT(*) FROM customer_interactions 
                WHERE interaction_date >= ?
            ''', ((datetime.now() - timedelta(days=30)).isoformat(),))
            
            recent_interactions = cursor.fetchone()[0]
            
            # At-risk customers
            # cursor.execute() removed'SELECT COUNT(*) FROM customers WHERE status = ?', (CustomerStatus.AT_RISK.value,))
            at_risk_count = cursor.fetchone()[0]
            
            # conn.close() removed
            
            report = {
                'generated_at': datetime.now().isoformat(),
                'customer_statistics': status_stats,
                'satisfaction_distribution': satisfaction_stats,
                'value_metrics': {
                    'total_customer_value': total_value or 0,
                    'average_customer_value': avg_value or 0
                },
                'referral_metrics': {
                    'paid_referrals': paid_referrals or 0,
                    'total_commissions': total_commissions or 0
                },
                'engagement_metrics': {
                    'recent_interactions_30_days': recent_interactions,
                    'at_risk_customers': at_risk_count
                },
                'total_customers': sum(status_stats.values())
            }
            
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating customer report: {e}")
            return {}
    
    def import_customers_from_deals(self, deals_file: str) -> int:
        """Import customers from deals database"""
        try:
            # This would connect to deals database and import closed/won deals
            # For demo, we'll create some sample customers
            
            sample_customers = [
                {
                    'deal_id': 'deal_sample_1',
                    'client_info': {'name': 'Budi Santoso', 'contact': {'phone': '0812-3456-7890'}},
                    'property_info': {'title': 'Rumah di Serang', 'type': 'house'},
                    'value': 450000000,
                    'stage': 'closed_won'
                },
                {
                    'deal_id': 'deal_sample_2',
                    'client_info': {'name': 'Siti Nurhaliza', 'contact': {'phone': '0856-7890-1234'}},
                    'property_info': {'title': 'Perumahan Griya Serang', 'type': 'house'},
                    'value': 350000000,
                    'stage': 'closed_won'
                }
            ]
            
            imported_count = 0
            for deal in sample_customers:
                customer_id = self.create_customer_from_deal(deal)
                if customer_id:
                    imported_count += 1
            
            self.logger.info(f"Imported {imported_count} customers from deals")
            return imported_count
            
        except Exception as e:
            self.logger.error(f"Error importing customers: {e}")
            return 0

def main():
    """Main function to demonstrate customer success manager"""
    print("=" * 60)
    print("😊 CUSTOMER SUCCESS MANAGER - CLOSER AGENT")
    print("=" * 60)
    
    # Initialize customer success manager
    csm = CustomerSuccessManager()
    
    # Import sample customers
    print("👥 Importing sample customers...")
    imported = csm.import_customers_from_deals('deals.db (SQLite - removed))
    print(f"✅ Imported {imported} customers")
    
    # Get pending follow-ups
    print("\n📋 Getting pending follow-ups...")
    pending_follow_ups = csm.get_pending_follow_ups(7)
    
    if pending_follow_ups:
        print(f"📊 Found {len(pending_follow_ups)} customers requiring follow-up:")
        for i, customer in enumerate(pending_follow_ups[:3]):  # Show first 3
            print(f"  {i+1}. {customer['customer_id']} - {customer['status']}")
            print(f"     Next follow-up: {customer['next_follow_up']}")
            print("")
    else:
        print("📭 No pending follow-ups found")
    
    # Record sample satisfaction survey
    print("\n📝 Recording sample satisfaction survey...")
    survey_data = {
        'overall_rating': 4,
        'property_quality': 5,
        'service_quality': 4,
        'communication_quality': 4,
        'value_for_money': 3,
        'comments': 'Good property, excellent service, but price could be better'
    }
    
    if pending_follow_ups:
        survey_id = csm.record_satisfaction_survey(pending_follow_ups[0]['customer_id'], survey_data)
        print(f"✅ Recorded survey: {survey_id}")
    
    # Generate customer report
    print("\n📈 Generating customer success report...")
    report = csm.generate_customer_report()
    
    if report:
        print("📊 Customer Success Metrics:")
        print(f"  - Total Customers: {report.get('total_customers', 0)}")
        print(f"  - Customer Status: {report.get('customer_statistics', {})}")
        print(f"  - Satisfaction Distribution: {report.get('satisfaction_distribution', {})}")
        print(f"  - Total Customer Value: Rp {report.get('value_metrics', {}).get('total_customer_value', 0):,.0f}")
        print(f"  - Paid Referrals: {report.get('referral_metrics', {}).get('paid_referrals', 0)}")
        print(f"  - At-Risk Customers: {report.get('engagement_metrics', {}).get('at_risk_customers', 0)}")
    
    # Save report
    report_file = 'customer_success_report.json'
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n📁 Report saved to: {report_file}")
    
    print("\n" + "=" * 60)
    print("✅ CUSTOMER SUCCESS MANAGER SETUP COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()
