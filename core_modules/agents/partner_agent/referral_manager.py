#!/usr/bin/env python3
"""
Referral Manager - Partner Agent
Advanced referral program management and tracking system
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ReferralStatus(Enum):
    """Referral status tracking"""
    PENDING = "pending"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    CONVERTED = "converted"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"
    EXPIRED = "expired"

class ReferralType(Enum):
    """Types of referrals"""
    CUSTOMER_REFERRAL = "customer_referral"
    PARTNER_REFERRAL = "partner_referral"
    EMPLOYEE_REFERRAL = "employee_referral"
    INFLUENCER_REFERRAL = "influencer_referral"
    SELF_REFERRAL = "self_referral"

class ReferralTier(Enum):
    """Referral reward tiers"""
    BASIC = "basic"
    PREMIUM = "premium"
    ELITE = "elite"
    PLATINUM = "platinum"

@dataclass
class Referral:
    """Referral information structure"""
    referral_id: str
    referrer_id: str
    referred_person: Dict
    referral_type: ReferralType
    status: ReferralStatus
    referral_code: str
    created_at: datetime
    contacted_at: Optional[datetime] = None
    qualified_at: Optional[datetime] = None
    converted_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    deal_value: float = 0.0
    commission_earned: float = 0.0
    notes: str = ""

@dataclass
class ReferralProgram:
    """Referral program configuration"""
    program_id: str
    program_name: str
    program_type: ReferralType
    reward_structure: Dict
    eligibility_criteria: Dict
    duration: timedelta
    status: str = "active"
    created_at: datetime = datetime.now()

@dataclass
class ReferralReward:
    """Referral reward structure"""
    reward_id: str
    referral_id: str
    reward_type: str
    reward_amount: float
    reward_tier: ReferralTier
    status: str = "pending"
    paid_at: Optional[datetime] = None
    notes: str = ""

class ReferralManager:
    """Advanced referral program management system"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Initialize database
        self.db_path = 'data/referral_manager.db (SQLite - removed)
        self._init_database()
        
        # Default referral programs
        self.default_programs = {
            ReferralType.CUSTOMER_REFERRAL: {
                'name': 'Customer Referral Program',
                'reward_structure': {
                    ReferralTier.BASIC: {'amount': 2500000, 'condition': 'lead_generated'},
                    ReferralTier.PREMIUM: {'amount': 5000000, 'condition': 'deal_closed'},
                    ReferralTier.ELITE: {'amount': 10000000, 'condition': 'high_value_deal'},
                    ReferralTier.PLATINUM: {'amount': 15000000, 'condition': 'premium_deal'}
                },
                'eligibility': {
                    'min_deals': 1,
                    'customer_status': 'active',
                    'referral_limit': 10
                }
            },
            ReferralType.PARTNER_REFERRAL: {
                'name': 'Partner Referral Program',
                'reward_structure': {
                    ReferralTier.BASIC: {'amount': 5000000, 'condition': 'partner_onboarded'},
                    ReferralTier.PREMIUM: {'amount': 10000000, 'condition': 'first_deal'},
                    ReferralTier.ELITE: {'amount': 20000000, 'condition': 'volume_target'},
                    ReferralTier.PLATINUM: {'amount': 30000000, 'condition': 'strategic_partner'}
                },
                'eligibility': {
                    'partner_status': 'active',
                    'partnership_level': 'basic',
                    'referral_limit': 20
                }
            }
        }
        
        # Referral code generation
        self.code_prefixes = {
            ReferralType.CUSTOMER_REFERRAL: 'CUST',
            ReferralType.PARTNER_REFERRAL: 'PART',
            ReferralType.EMPLOYEE_REFERRAL: 'EMP',
            ReferralType.INFLUENCER_REFERRAL: 'INF',
            ReferralType.SELF_REFERRAL: 'SELF'
        }
    
    def _init_database(self):
        """Initialize referral manager database"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # Create referrals table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS referrals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    referral_id TEXT UNIQUE NOT NULL,
                    referrer_id TEXT NOT NULL,
                    referred_person TEXT NOT NULL,
                    referral_type TEXT NOT NULL,
                    status TEXT NOT NULL,
                    referral_code TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    contacted_at TEXT,
                    qualified_at TEXT,
                    converted_at TEXT,
                    closed_at TEXT,
                    deal_value REAL DEFAULT 0,
                    commission_earned REAL DEFAULT 0,
                    notes TEXT DEFAULT '',
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create referral programs table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS referral_programs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    program_id TEXT UNIQUE NOT NULL,
                    program_name TEXT NOT NULL,
                    program_type TEXT NOT NULL,
                    reward_structure TEXT NOT NULL,
                    eligibility_criteria TEXT NOT NULL,
                    duration_days INTEGER NOT NULL,
                    status TEXT DEFAULT 'active',
                    created_at TEXT NOT NULL
                )
            ''')
            
            # Create referral rewards table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS referral_rewards (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    reward_id TEXT UNIQUE NOT NULL,
                    referral_id TEXT NOT NULL,
                    reward_type TEXT NOT NULL,
                    reward_amount REAL NOT NULL,
                    reward_tier TEXT NOT NULL,
                    status TEXT DEFAULT 'pending',
                    paid_at TEXT,
                    notes TEXT DEFAULT '',
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create referral analytics table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS referral_analytics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    referrer_id TEXT NOT NULL,
                    period TEXT NOT NULL,
                    referrals_generated INTEGER DEFAULT 0,
                    referrals_converted INTEGER DEFAULT 0,
                    total_value REAL DEFAULT 0,
                    total_rewards REAL DEFAULT 0,
                    conversion_rate REAL DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create referral tracking table (for clicks, shares, etc.)
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS referral_tracking (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tracking_id TEXT UNIQUE NOT NULL,
                    referral_id TEXT NOT NULL,
                    tracking_type TEXT NOT NULL,
                    tracking_data TEXT,
                    tracked_at TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create indexes
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_referrals_referrer_id ON referrals(referrer_id)')
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_referrals_status ON referrals(status)')
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_referrals_code ON referrals(referral_code)')
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_rewards_referral_id ON referral_rewards(referral_id)')
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_analytics_referrer_id ON referral_analytics(referrer_id)')
            
            # conn.commit() removed
            # conn.close() removed
            
            self.logger.info("Referral manager database initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Error initializing referral manager database: {e}")
            raise
    
    def create_referral(self, referrer_id: str, referred_person: Dict, 
                       referral_type: ReferralType) -> str:
        """Create new referral"""
        try:
            referral_id = f"ref_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Generate referral code
            referral_code = self._generate_referral_code(referral_type)
            
            referral = Referral(
                referral_id=referral_id,
                referrer_id=referrer_id,
                referred_person=referred_person,
                referral_type=referral_type,
                status=ReferralStatus.PENDING,
                referral_code=referral_code,
                created_at=datetime.now()
            )
            
            # Save referral
            self._save_referral(referral)
            
            # Log tracking event
            self._track_referral_event(referral_id, "created", {
                'referrer_id': referrer_id,
                'referral_type': referral_type.value,
                'referral_code': referral_code
            })
            
            self.logger.info(f"Created referral {referral_id} with code {referral_code}")
            return referral_id
            
        except Exception as e:
            self.logger.error(f"Error creating referral: {e}")
            return ""
    
    def _generate_referral_code(self, referral_type: ReferralType) -> str:
        """Generate unique referral code"""
        prefix = self.code_prefixes.get(referral_type, 'REF')
        timestamp = datetime.now().strftime('%Y%m%d')
        random_suffix = str(uuid.uuid4())[:8].upper()
        return f"{prefix}{timestamp}{random_suffix}"
    
    def _save_referral(self, referral: Referral):
        """Save referral to database"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # cursor.execute() removed'''
                INSERT INTO referrals 
                (referral_id, referrer_id, referred_person, referral_type, status, 
                 referral_code, created_at, contacted_at, qualified_at, converted_at, 
                 closed_at, deal_value, commission_earned, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                referral.referral_id,
                referral.referrer_id,
                json.dumps(referral.referred_person),
                referral.referral_type.value,
                referral.status.value,
                referral.referral_code,
                referral.created_at.isoformat(),
                referral.contacted_at.isoformat() if referral.contacted_at else None,
                referral.qualified_at.isoformat() if referral.qualified_at else None,
                referral.converted_at.isoformat() if referral.converted_at else None,
                referral.closed_at.isoformat() if referral.closed_at else None,
                referral.deal_value,
                referral.commission_earned,
                referral.notes
            ))
            
            # conn.commit() removed
            # conn.close() removed
            
        except Exception as e:
            self.logger.error(f"Error saving referral {referral.referral_id}: {e}")
            raise
    
    def _track_referral_event(self, referral_id: str, tracking_type: str, tracking_data: Dict):
        """Track referral events"""
        try:
            tracking_id = f"track_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # cursor.execute() removed'''
                INSERT INTO referral_tracking 
                (tracking_id, referral_id, tracking_type, tracking_data, tracked_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                tracking_id,
                referral_id,
                tracking_type,
                json.dumps(tracking_data),
                datetime.now().isoformat()
            ))
            
            # conn.commit() removed
            # conn.close() removed
            
        except Exception as e:
            self.logger.error(f"Error tracking referral event: {e}")
    
    def update_referral_status(self, referral_id: str, new_status: ReferralStatus, 
                             notes: str = "", deal_value: float = 0.0) -> bool:
        """Update referral status and calculate rewards"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # Get current referral
            # cursor.execute() removed'SELECT * FROM referrals WHERE referral_id = ?', (referral_id,))
            result = cursor.fetchone()
            
            if not result:
                self.logger.error(f"Referral {referral_id} not found")
                return False
            
            columns = [desc[0] for desc in cursor.description]
            referral_data = dict(zip(columns, result))
            
            # Update status and timestamps
            update_fields = ['status = ?', 'updated_at = ?']
            update_values = [new_status.value, datetime.now().isoformat()]
            
            if new_status == ReferralStatus.CONTACTED:
                update_fields.append('contacted_at = ?')
                update_values.append(datetime.now().isoformat())
            elif new_status == ReferralStatus.QUALIFIED:
                update_fields.append('qualified_at = ?')
                update_values.append(datetime.now().isoformat())
            elif new_status == ReferralStatus.CONVERTED:
                update_fields.append('converted_at = ?')
                update_values.append(datetime.now().isoformat())
            elif new_status in [ReferralStatus.CLOSED_WON, ReferralStatus.CLOSED_LOST]:
                update_fields.append('closed_at = ?')
                update_values.append(datetime.now().isoformat())
                update_fields.append('deal_value = ?')
                update_values.append(deal_value)
            
            update_values.append(referral_id)
            
            # cursor.execute() removedf'''
                UPDATE referrals 
                SET {', '.join(update_fields)}, notes = ?
                WHERE referral_id = ?
            ''', update_values + [notes, referral_id])
            
            # conn.commit() removed
            # conn.close() removed
            
            # Calculate and create rewards if applicable
            if new_status in [ReferralStatus.CONVERTED, ReferralStatus.CLOSED_WON]:
                self._calculate_referral_reward(referral_id, deal_value)
            
            # Log tracking event
            self._track_referral_event(referral_id, "status_updated", {
                'old_status': referral_data['status'],
                'new_status': new_status.value,
                'deal_value': deal_value,
                'notes': notes
            })
            
            self.logger.info(f"Updated referral {referral_id} status to {new_status.value}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error updating referral {referral_id} status: {e}")
            return False
    
    def _calculate_referral_reward(self, referral_id: str, deal_value: float):
        """Calculate and create referral reward"""
        try:
            # Get referral details
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # cursor.execute() removed'SELECT * FROM referrals WHERE referral_id = ?', (referral_id,))
            result = cursor.fetchone()
            
            if not result:
                return
            
            columns = [desc[0] for desc in cursor.description]
            referral_data = dict(zip(columns, result))
            
            referral_type = ReferralType(referral_data['referral_type'])
            
            # Get reward structure
            program_config = self.default_programs.get(referral_type)
            if not program_config:
                return
            
            reward_structure = program_config['reward_structure']
            
            # Determine reward tier based on deal value
            reward_tier = self._determine_reward_tier(deal_value)
            
            if reward_tier not in reward_structure:
                return
            
            reward_config = reward_structure[reward_tier]
            reward_amount = reward_config['amount']
            
            # Create reward record
            reward_id = f"reward_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # cursor.execute() removed'''
                INSERT INTO referral_rewards 
                (reward_id, referral_id, reward_type, reward_amount, reward_tier, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                reward_id,
                referral_id,
                reward_config['condition'],
                reward_amount,
                reward_tier.value,
                f"Reward for {reward_config['condition']} - Deal value: Rp {deal_value:,.0f}"
            ))
            
            # conn.commit() removed
            # conn.close() removed
            
            self.logger.info(f"Created reward {reward_id}: Rp {reward_amount:,.0f} for referral {referral_id}")
            
        except Exception as e:
            self.logger.error(f"Error calculating referral reward: {e}")
    
    def _determine_reward_tier(self, deal_value: float) -> ReferralTier:
        """Determine reward tier based on deal value"""
        if deal_value >= 1000000000:  # >= 1 miliar
            return ReferralTier.PLATINUM
        elif deal_value >= 750000000:  # >= 750 juta
            return ReferralTier.ELITE
        elif deal_value >= 500000000:  # >= 500 juta
            return ReferralTier.PREMIUM
        else:
            return ReferralTier.BASIC
    
    def get_referral_analytics(self, referrer_id: Optional[str] = None) -> Dict:
        """Get referral analytics and performance metrics"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            if referrer_id:
                # Analytics for specific referrer
                # cursor.execute() removed'''
                    SELECT status, COUNT(*) 
                    FROM referrals 
                    WHERE referrer_id = ?
                    GROUP BY status
                ''', (referrer_id,))
                
                status_stats = dict(cursor.fetchall())
                
                # cursor.execute() removed'''
                    SELECT COUNT(*), SUM(deal_value), SUM(commission_earned)
                    FROM referrals 
                    WHERE referrer_id = ? AND status IN (?, ?)
                ''', (referrer_id, ReferralStatus.CLOSED_WON.value, ReferralStatus.CONVERTED.value))
                
                converted_count, total_value, total_commission = cursor.fetchone()
                
                # Get rewards
                # cursor.execute() removed'''
                    SELECT COUNT(*), SUM(reward_amount)
                    FROM referral_rewards 
                    WHERE referral_id IN (
                        SELECT referral_id FROM referrals WHERE referrer_id = ?
                    )
                ''', (referrer_id,))
                
                rewards_count, total_rewards = cursor.fetchone()
                
                analytics = {
                    'referrer_id': referrer_id,
                    'referral_statistics': status_stats,
                    'conversion_metrics': {
                        'total_converted': converted_count or 0,
                        'total_deal_value': total_value or 0,
                        'total_commission': total_commission or 0,
                        'conversion_rate': (converted_count or 0) / max(sum(status_stats.values()), 1) * 100
                    },
                    'reward_metrics': {
                        'total_rewards': rewards_count or 0,
                        'total_reward_amount': total_rewards or 0
                    }
                }
            else:
                # Overall analytics
                # cursor.execute() removed'SELECT status, COUNT(*) FROM referrals GROUP BY status')
                status_stats = dict(cursor.fetchall())
                
                # cursor.execute() removed'SELECT COUNT(*), SUM(deal_value) FROM referrals WHERE status = ?', (ReferralStatus.CLOSED_WON.value,))
                closed_count, closed_value = cursor.fetchone()
                
                # cursor.execute() removed'SELECT COUNT(*), SUM(reward_amount) FROM referral_rewards WHERE status = ?', ('paid',))
                paid_rewards, paid_amount = cursor.fetchone()
                
                analytics = {
                    'overall_statistics': status_stats,
                    'performance_metrics': {
                        'total_closed_deals': closed_count or 0,
                        'total_closed_value': closed_value or 0,
                        'total_paid_rewards': paid_rewards or 0,
                        'total_reward_amount': paid_amount or 0
                    }
                }
            
            # conn.close() removed
            return analytics
            
        except Exception as e:
            self.logger.error(f"Error getting referral analytics: {e}")
            return {}
    
    def get_referral_leaderboard(self, limit: int = 10) -> List[Dict]:
        """Get referral leaderboard"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # cursor.execute() removed'''
                SELECT 
                    r.referrer_id,
                    COUNT(*) as total_referrals,
                    SUM(CASE WHEN r.status IN (?, ?) THEN 1 ELSE 0 END) as converted_referrals,
                    SUM(r.deal_value) as total_deal_value,
                    SUM(r.commission_earned) as total_commission
                FROM referrals r
                GROUP BY r.referrer_id
                ORDER BY converted_referrals DESC, total_deal_value DESC
                LIMIT ?
            ''', (ReferralStatus.CLOSED_WON.value, ReferralStatus.CONVERTED.value, limit))
            
            leaderboard = []
            for row in cursor.fetchall():
                leaderboard.append({
                    'referrer_id': row[0],
                    'total_referrals': row[1],
                    'converted_referrals': row[2],
                    'total_deal_value': row[3] or 0,
                    'total_commission': row[4] or 0,
                    'conversion_rate': (row[2] / row[1] * 100) if row[1] > 0 else 0
                })
            
            # conn.close() removed
            return leaderboard
            
        except Exception as e:
            self.logger.error(f"Error getting referral leaderboard: {e}")
            return []
    
    def create_sample_referrals(self) -> int:
        """Create sample referrals for testing"""
        try:
            sample_referrers = [
                {'id': 'partner_001', 'name': 'PT. Properti Bersama'},
                {'id': 'customer_001', 'name': 'Budi Santoso'},
                {'id': 'influencer_001', 'name': 'Property Influencer ID'},
                {'id': 'employee_001', 'name': 'Sales Agent A'}
            ]
            
            sample_referred = [
                {'name': 'Ahmad Wijaya', 'phone': '0812-1111-2222', 'email': 'ahmad@email.com'},
                {'name': 'Siti Nurhaliza', 'phone': '0856-3333-4444', 'email': 'siti@email.com'},
                {'name': 'Rudi Hermawan', 'phone': '0878-5555-6666', 'email': 'rudi@email.com'},
                {'name': 'Dewi Lestari', 'phone': '0899-7777-8888', 'email': 'dewi@email.com'}
            ]
            
            created_count = 0
            
            for i, referrer in enumerate(sample_referrers):
                for j, referred in enumerate(sample_referred):
                    if i + j < 6:  # Create 6 sample referrals
                        referral_type = ReferralType.PARTNER_REFERRAL if i == 0 else ReferralType.CUSTOMER_REFERRAL
                        
                        referral_id = self.create_referral(
                            referrer['id'],
                            referred,
                            referral_type
                        )
                        
                        if referral_id:
                            created_count += 1
                            
                            # Simulate different statuses
                            if (i + j) % 3 == 0:
                                self.update_referral_status(
                                    referral_id, 
                                    ReferralStatus.CONTACTED,
                                    "Initial contact made"
                                )
                            elif (i + j) % 3 == 1:
                                self.update_referral_status(
                                    referral_id,
                                    ReferralStatus.CONVERTED,
                                    "Deal converted successfully",
                                    350000000 + (i * 50000000)
                                )
                            elif (i + j) % 3 == 2:
                                self.update_referral_status(
                                    referral_id,
                                    ReferralStatus.CLOSED_WON,
                                    "Deal closed successfully",
                                    450000000 + (i * 75000000)
                                )
            
            self.logger.info(f"Created {created_count} sample referrals")
            return created_count
            
        except Exception as e:
            self.logger.error(f"Error creating sample referrals: {e}")
            return 0

def main():
    """Main function to demonstrate referral manager"""
    print("=" * 60)
    print("🎯 REFERRAL MANAGER - PARTNER AGENT")
    print("=" * 60)
    
    # Initialize referral manager
    rm = ReferralManager()
    
    # Create sample referrals
    print("👥 Creating sample referrals...")
    created = rm.create_sample_referrals()
    print(f"✅ Created {created} sample referrals")
    
    # Get referral analytics
    print("\n📊 Getting referral analytics...")
    analytics = rm.get_referral_analytics()
    
    if analytics:
        print("📈 Overall Analytics:")
        overall_stats = analytics.get('overall_statistics', {})
        print(f"  - Referral Status: {overall_stats}")
        
        performance = analytics.get('performance_metrics', {})
        print(f"  - Closed Deals: {performance.get('total_closed_deals', 0)}")
        print(f"  - Closed Value: Rp {performance.get('total_closed_value', 0):,.0f}")
        print(f"  - Paid Rewards: {performance.get('total_paid_rewards', 0)}")
        print(f"  - Reward Amount: Rp {performance.get('total_reward_amount', 0):,.0f}")
    
    # Get leaderboard
    print("\n🏆 Referral Leaderboard:")
    leaderboard = rm.get_referral_leaderboard(5)
    
    for i, entry in enumerate(leaderboard):
        print(f"  {i+1}. {entry['referrer_id']}")
        print(f"     Referrals: {entry['total_referrals']} | Converted: {entry['converted_referrals']}")
        print(f"     Value: Rp {entry['total_deal_value']:,.0f} | Rate: {entry['conversion_rate']:.1f}%")
    
    # Get specific referrer analytics
    if leaderboard:
        top_referrer = leaderboard[0]['referrer_id']
        print(f"\n📊 Detailed Analytics for {top_referrer}:")
        detailed_analytics = rm.get_referral_analytics(top_referrer)
        
        if detailed_analytics:
            ref_stats = detailed_analytics.get('referral_statistics', {})
            conv_metrics = detailed_analytics.get('conversion_metrics', {})
            reward_metrics = detailed_analytics.get('reward_metrics', {})
            
            print(f"  - Status Distribution: {ref_stats}")
            print(f"  - Conversion Rate: {conv_metrics.get('conversion_rate', 0):.1f}%")
            print(f"  - Total Deal Value: Rp {conv_metrics.get('total_deal_value', 0):,.0f}")
            print(f"  - Total Rewards: Rp {reward_metrics.get('total_reward_amount', 0):,.0f}")
    
    # Save analytics
    analytics_file = 'referral_analytics.json'
    with open(analytics_file, 'w', encoding='utf-8') as f:
        json.dump(analytics, f, indent=2, ensure_ascii=False)
    
    print(f"\n📁 Analytics saved to: {analytics_file}")
    
    print("\n" + "=" * 60)
    print("✅ REFERRAL MANAGER SETUP COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()
