#!/usr/bin/env python3
"""
Commission Tracker - Partner Agent
Commission calculation and tracking system for partner network
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

class CommissionStatus(Enum):
    """Commission payment status"""
    PENDING = "pending"
    APPROVED = "approved"
    PAID = "paid"
    DISPUTED = "disputed"
    CANCELLED = "cancelled"

class PartnerTier(Enum):
    """Partner tier levels"""
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"
    DIAMOND = "diamond"

class CommissionType(Enum):
    """Types of commissions"""
    REFERRAL = "referral"
    DIRECT_SALE = "direct_sale"
    RECURRING = "recurring"
    BONUS = "bonus"

@dataclass
class Partner:
    """Partner information"""
    partner_id: str
    name: str
    contact_info: Dict
    tier: PartnerTier
    commission_rate: float
    total_commissions: float
    active_deals: int
    joined_date: datetime
    status: str = "active"

@dataclass
class Commission:
    """Commission record"""
    commission_id: str
    partner_id: str
    deal_id: str
    commission_type: CommissionType
    deal_value: float
    commission_rate: float
    commission_amount: float
    status: CommissionStatus
    created_at: datetime
    approved_at: Optional[datetime] = None
    paid_at: Optional[datetime] = None
    notes: str = ""

class CommissionTracker:
    """Commission calculation and tracking system"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Initialize database
        self.db_path = 'data/commission_tracker.db (SQLite - removed)
        self._init_database()
        
        # Commission rates by tier
        self.tier_commission_rates = {
            PartnerTier.BRONZE: 1.0,    # 1%
            PartnerTier.SILVER: 1.5,    # 1.5%
            PartnerTier.GOLD: 2.0,      # 2%
            PartnerTier.PLATINUM: 2.5,  # 2.5%
            PartnerTier.DIAMOND: 3.0     # 3%
        }
        
        # Tier qualification criteria
        self.tier_criteria = {
            PartnerTier.BRONZE: {'min_deals': 0, 'min_value': 0},
            PartnerTier.SILVER: {'min_deals': 5, 'min_value': 500000000},
            PartnerTier.GOLD: {'min_deals': 15, 'min_value': 1500000000},
            PartnerTier.PLATINUM: {'min_deals': 30, 'min_value': 3000000000},
            PartnerTier.DIAMOND: {'min_deals': 50, 'min_value': 5000000000}
        }
        
        # Bonus commission rules
        self.bonus_rules = {
            'monthly_target': {
                'deals': 10,
                'value': 1000000000,
                'bonus_rate': 0.5  # 0.5% bonus
            },
            'quarterly_target': {
                'deals': 25,
                'value': 2500000000,
                'bonus_rate': 1.0  # 1% bonus
            },
            'referral_bonus': {
                'rate': 0.2,  # 0.2% of referred partner's commissions
                'months': 12   # For 12 months
            }
        }
    
    def _init_database(self):
        """Initialize commission tracker database"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # Create partners table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS partners (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    partner_id TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    contact_info TEXT NOT NULL,
                    tier TEXT NOT NULL,
                    commission_rate REAL NOT NULL,
                    total_commissions REAL DEFAULT 0,
                    active_deals INTEGER DEFAULT 0,
                    joined_date TEXT NOT NULL,
                    status TEXT DEFAULT 'active',
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create commissions table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS commissions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    commission_id TEXT UNIQUE NOT NULL,
                    partner_id TEXT NOT NULL,
                    deal_id TEXT NOT NULL,
                    commission_type TEXT NOT NULL,
                    deal_value REAL NOT NULL,
                    commission_rate REAL NOT NULL,
                    commission_amount REAL NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    approved_at TEXT,
                    paid_at TEXT,
                    notes TEXT DEFAULT '',
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create commission payments table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS commission_payments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    payment_id TEXT UNIQUE NOT NULL,
                    commission_ids TEXT NOT NULL,
                    partner_id TEXT NOT NULL,
                    total_amount REAL NOT NULL,
                    payment_date TEXT NOT NULL,
                    payment_method TEXT,
                    reference_number TEXT,
                    status TEXT DEFAULT 'pending',
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create tier history table
            # cursor.execute() removed'''
                CREATE TABLE IF NOT EXISTS tier_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    partner_id TEXT NOT NULL,
                    old_tier TEXT,
                    new_tier TEXT NOT NULL,
                    changed_at TEXT NOT NULL,
                    reason TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create indexes
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_partners_partner_id ON partners(partner_id)')
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_commissions_partner_id ON commissions(partner_id)')
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_commissions_status ON commissions(status)')
            # cursor.execute() removed'CREATE INDEX IF NOT EXISTS idx_payments_partner_id ON commission_payments(partner_id)')
            
            # conn.commit() removed
            # conn.close() removed
            
            self.logger.info("Commission tracker database initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Error initializing commission tracker database: {e}")
            raise
    
    def add_partner(self, partner_data: Dict) -> str:
        """Add new partner to the system"""
        try:
            partner_id = f"partner_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            partner = Partner(
                partner_id=partner_id,
                name=partner_data.get('name', ''),
                contact_info=partner_data.get('contact_info', {}),
                tier=PartnerTier.BRONZE,  # Start at bronze
                commission_rate=self.tier_commission_rates[PartnerTier.BRONZE],
                total_commissions=0,
                active_deals=0,
                joined_date=datetime.now()
            )
            
            # Save to database
            self._save_partner(partner)
            
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
                (partner_id, name, contact_info, tier, commission_rate, 
                 total_commissions, active_deals, joined_date, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                partner.partner_id,
                partner.name,
                json.dumps(partner.contact_info),
                partner.tier.value,
                partner.commission_rate,
                partner.total_commissions,
                partner.active_deals,
                partner.joined_date.isoformat(),
                partner.status
            ))
            
            # conn.commit() removed
            # conn.close() removed
            
        except Exception as e:
            self.logger.error(f"Error saving partner {partner.partner_id}: {e}")
            raise
    
    def create_commission(self, partner_id: str, deal_id: str, deal_value: float, 
                         commission_type: CommissionType = CommissionType.DIRECT_SALE) -> str:
        """Create commission record for a deal"""
        try:
            commission_id = f"comm_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Get partner info
            partner = self._get_partner(partner_id)
            if not partner:
                self.logger.error(f"Partner {partner_id} not found")
                return ""
            
            # Calculate commission amount
            commission_rate = partner.commission_rate
            commission_amount = deal_value * (commission_rate / 100)
            
            commission = Commission(
                commission_id=commission_id,
                partner_id=partner_id,
                deal_id=deal_id,
                commission_type=commission_type,
                deal_value=deal_value,
                commission_rate=commission_rate,
                commission_amount=commission_amount,
                status=CommissionStatus.PENDING,
                created_at=datetime.now()
            )
            
            # Save to database
            self._save_commission(commission)
            
            # Update partner stats
            self._update_partner_stats(partner_id)
            
            self.logger.info(f"Created commission {commission_id}: Rp {commission_amount:,.0f} for partner {partner_id}")
            return commission_id
            
        except Exception as e:
            self.logger.error(f"Error creating commission: {e}")
            return ""
    
    def _get_partner(self, partner_id: str) -> Optional[Partner]:
        """Get partner by ID"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # cursor.execute() removed'SELECT * FROM partners WHERE partner_id = ?', (partner_id,))
            result = cursor.fetchone()
            
            if not result:
                return None
            
            columns = [desc[0] for desc in cursor.description]
            partner_data = dict(zip(columns, result))
            
            partner = Partner(
                partner_id=partner_data['partner_id'],
                name=partner_data['name'],
                contact_info=json.loads(partner_data['contact_info']),
                tier=PartnerTier(partner_data['tier']),
                commission_rate=partner_data['commission_rate'],
                total_commissions=partner_data['total_commissions'],
                active_deals=partner_data['active_deals'],
                joined_date=datetime.fromisoformat(partner_data['joined_date']),
                status=partner_data['status']
            )
            
            # conn.close() removed
            return partner
            
        except Exception as e:
            self.logger.error(f"Error getting partner {partner_id}: {e}")
            return None
    
    def _save_commission(self, commission: Commission):
        """Save commission to database"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # cursor.execute() removed'''
                INSERT INTO commissions 
                (commission_id, partner_id, deal_id, commission_type, deal_value, 
                 commission_rate, commission_amount, status, created_at, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                commission.commission_id,
                commission.partner_id,
                commission.deal_id,
                commission.commission_type.value,
                commission.deal_value,
                commission.commission_rate,
                commission.commission_amount,
                commission.status.value,
                commission.created_at.isoformat(),
                commission.notes
            ))
            
            # conn.commit() removed
            # conn.close() removed
            
        except Exception as e:
            self.logger.error(f"Error saving commission {commission.commission_id}: {e}")
            raise
    
    def _update_partner_stats(self, partner_id: str):
        """Update partner statistics"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # Calculate total commissions
            # cursor.execute() removed'''
                SELECT SUM(commission_amount) 
                FROM commissions 
                WHERE partner_id = ? AND status = ?
            ''', (partner_id, CommissionStatus.PAID.value))
            
            total_commissions = cursor.fetchone()[0] or 0
            
            # Count active deals (this would come from deals database)
            active_deals = 5  # Placeholder - would integrate with deals system
            
            # Update partner
            # cursor.execute() removed'''
                UPDATE partners 
                SET total_commissions = ?, active_deals = ?, updated_at = ?
                WHERE partner_id = ?
            ''', (total_commissions, active_deals, datetime.now().isoformat(), partner_id))
            
            # conn.commit() removed
            # conn.close() removed
            
            # Check for tier upgrade
            self._check_tier_upgrade(partner_id)
            
        except Exception as e:
            self.logger.error(f"Error updating partner stats for {partner_id}: {e}")
    
    def _check_tier_upgrade(self, partner_id: str):
        """Check if partner qualifies for tier upgrade"""
        try:
            partner = self._get_partner(partner_id)
            if not partner:
                return
            
            current_tier = partner.tier
            new_tier = current_tier
            
            # Check each tier from highest to current
            tiers = [PartnerTier.DIAMOND, PartnerTier.PLATINUM, PartnerTier.GOLD, PartnerTier.SILVER]
            
            for tier in tiers:
                if tier == current_tier:
                    break
                
                criteria = self.tier_criteria[tier]
                if (partner.total_commissions >= criteria['min_value'] and 
                    partner.active_deals >= criteria['min_deals']):
                    new_tier = tier
                    break
            
            # Upgrade if needed
            if new_tier != current_tier:
                self._upgrade_partner_tier(partner_id, current_tier, new_tier)
            
        except Exception as e:
            self.logger.error(f"Error checking tier upgrade for {partner_id}: {e}")
    
    def _upgrade_partner_tier(self, partner_id: str, old_tier: PartnerTier, new_tier: PartnerTier):
        """Upgrade partner to new tier"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # Update partner tier and commission rate
            new_rate = self.tier_commission_rates[new_tier]
            
            # cursor.execute() removed'''
                UPDATE partners 
                SET tier = ?, commission_rate = ?, updated_at = ?
                WHERE partner_id = ?
            ''', (new_tier.value, new_rate, datetime.now().isoformat(), partner_id))
            
            # Record tier change
            # cursor.execute() removed'''
                INSERT INTO tier_history (partner_id, old_tier, new_tier, changed_at, reason)
                VALUES (?, ?, ?, ?, ?)
            ''', (partner_id, old_tier.value, new_tier.value, datetime.now().isoformat(), 
                  "Performance-based upgrade"))
            
            # conn.commit() removed
            # conn.close() removed
            
            self.logger.info(f"Upgraded partner {partner_id} from {old_tier.value} to {new_tier.value}")
            
        except Exception as e:
            self.logger.error(f"Error upgrading partner {partner_id}: {e}")
    
    def approve_commission(self, commission_id: str, notes: str = "") -> bool:
        """Approve commission for payment"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # cursor.execute() removed'''
                UPDATE commissions 
                SET status = ?, approved_at = ?, notes = ?, updated_at = ?
                WHERE commission_id = ?
            ''', (CommissionStatus.APPROVED.value, datetime.now().isoformat(), 
                  notes, datetime.now().isoformat(), commission_id))
            
            # conn.commit() removed
            # conn.close() removed
            
            self.logger.info(f"Approved commission {commission_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error approving commission {commission_id}: {e}")
            return False
    
    def pay_commission(self, commission_id: str, payment_method: str = "bank_transfer") -> bool:
        """Mark commission as paid"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # cursor.execute() removed'''
                UPDATE commissions 
                SET status = ?, paid_at = ?, updated_at = ?
                WHERE commission_id = ? AND status = ?
            ''', (CommissionStatus.PAID.value, datetime.now().isoformat(), 
                  datetime.now().isoformat(), commission_id, CommissionStatus.APPROVED.value))
            
            # conn.commit() removed
            # conn.close() removed
            
            # Update partner stats
            commission = self._get_commission(commission_id)
            if commission:
                self._update_partner_stats(commission.partner_id)
            
            self.logger.info(f"Paid commission {commission_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error paying commission {commission_id}: {e}")
            return False
    
    def _get_commission(self, commission_id: str) -> Optional[Commission]:
        """Get commission by ID"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # cursor.execute() removed'SELECT * FROM commissions WHERE commission_id = ?', (commission_id,))
            result = cursor.fetchone()
            
            if not result:
                return None
            
            columns = [desc[0] for desc in cursor.description]
            commission_data = dict(zip(columns, result))
            
            commission = Commission(
                commission_id=commission_data['commission_id'],
                partner_id=commission_data['partner_id'],
                deal_id=commission_data['deal_id'],
                commission_type=CommissionType(commission_data['commission_type']),
                deal_value=commission_data['deal_value'],
                commission_rate=commission_data['commission_rate'],
                commission_amount=commission_data['commission_amount'],
                status=CommissionStatus(commission_data['status']),
                created_at=datetime.fromisoformat(commission_data['created_at']),
                approved_at=datetime.fromisoformat(commission_data['approved_at']) if commission_data['approved_at'] else None,
                paid_at=datetime.fromisoformat(commission_data['paid_at']) if commission_data['paid_at'] else None,
                notes=commission_data['notes']
            )
            
            # conn.close() removed
            return commission
            
        except Exception as e:
            self.logger.error(f"Error getting commission {commission_id}: {e}")
            return None
    
    def calculate_monthly_bonus(self, partner_id: str, year: int, month: int) -> float:
        """Calculate monthly bonus for partner"""
        try:
            # Get commissions for the month
            start_date = datetime(year, month, 1)
            if month == 12:
                end_date = datetime(year + 1, 1, 1)
            else:
                end_date = datetime(year, month + 1, 1)
            
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            # cursor.execute() removed'''
                SELECT COUNT(*), SUM(deal_value)
                FROM commissions 
                WHERE partner_id = ? AND status = ? 
                AND created_at >= ? AND created_at < ?
            ''', (partner_id, CommissionStatus.PAID.value, start_date.isoformat(), end_date.isoformat()))
            
            deals_count, total_value = cursor.fetchone()
            
            # conn.close() removed
            
            # Check bonus criteria
            bonus_rule = self.bonus_rules['monthly_target']
            
            if (deals_count >= bonus_rule['deals'] and 
                total_value >= bonus_rule['value']):
                return total_value * (bonus_rule['bonus_rate'] / 100)
            
            return 0.0
            
        except Exception as e:
            self.logger.error(f"Error calculating monthly bonus for {partner_id}: {e}")
            return 0.0
    
    def generate_commission_report(self, partner_id: Optional[str] = None) -> Dict:
        """Generate commission report"""
        try:
            conn = # SQLite connection removed
            cursor = conn.cursor()
            
            if partner_id:
                # Report for specific partner
                # cursor.execute() removed'''
                    SELECT status, COUNT(*), SUM(commission_amount)
                    FROM commissions 
                    WHERE partner_id = ?
                    GROUP BY status
                ''', (partner_id,))
                
                status_stats = dict(cursor.fetchall())
                
                # cursor.execute() removed'''
                    SELECT SUM(commission_amount)
                    FROM commissions 
                    WHERE partner_id = ? AND status = ?
                ''', (partner_id, CommissionStatus.PAID.value))
                
                total_paid = cursor.fetchone()[0] or 0
                
                partner = self._get_partner(partner_id)
                
                report = {
                    'partner_id': partner_id,
                    'partner_name': partner.name if partner else 'Unknown',
                    'partner_tier': partner.tier.value if partner else 'Unknown',
                    'commission_statistics': status_stats,
                    'total_paid': total_paid,
                    'pending_commissions': status_stats.get(CommissionStatus.PENDING.value, 0),
                    'generated_at': datetime.now().isoformat()
                }
            else:
                # Overall report
                # cursor.execute() removed'SELECT status, COUNT(*), SUM(commission_amount) FROM commissions GROUP BY status')
                status_stats = dict(cursor.fetchall())
                
                # cursor.execute() removed'SELECT tier, COUNT(*) FROM partners GROUP BY tier')
                tier_dist = dict(cursor.fetchall())
                
                # cursor.execute() removed'SELECT SUM(total_commissions), COUNT(*) FROM partners')
                total_commissions, partner_count = cursor.fetchone()
                
                report = {
                    'overall_statistics': status_stats,
                    'partner_tier_distribution': tier_dist,
                    'total_partners': partner_count,
                    'total_commissions_paid': total_commissions or 0,
                    'generated_at': datetime.now().isoformat()
                }
            
            # conn.close() removed
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating commission report: {e}")
            return {}
    
    def create_sample_partners(self) -> int:
        """Create sample partners for testing"""
        try:
            sample_partners = [
                {
                    'name': 'PT. Properti Bersama',
                    'contact_info': {
                        'phone': '021-5551234',
                        'email': 'info@propertibersama.com',
                        'address': 'Jakarta Selatan'
                    }
                },
                {
                    'name': 'CV. Agen Rumahku',
                    'contact_info': {
                        'phone': '022-6677889',
                        'email': 'marketing@rumahku.com',
                        'address': 'Bandung'
                    }
                },
                {
                    'name': 'UD. Makmur Sejahtera',
                    'contact_info': {
                        'phone': '031-9988776',
                        'email': 'ud.makmur@gmail.com',
                        'address': 'Surabaya'
                    }
                }
            ]
            
            created_count = 0
            for partner_data in sample_partners:
                partner_id = self.add_partner(partner_data)
                if partner_id:
                    created_count += 1
                    
                    # Create some sample commissions
                    for i in range(3):
                        self.create_commission(
                            partner_id, 
                            f"deal_{partner_id}_{i+1}", 
                            350000000 + (i * 50000000)
                        )
            
            self.logger.info(f"Created {created_count} sample partners with commissions")
            return created_count
            
        except Exception as e:
            self.logger.error(f"Error creating sample partners: {e}")
            return 0

def calculate_commission(deal_value: float, partner_tier: str) -> float:
    """
    Calculate commission based on deal value and partner tier
    
    Args:
        deal_value: Total value of the deal
        partner_tier: Partner tier (Gold, Silver, Bronze)
    
    Returns:
        Commission amount
    """
    # ANSI Color Codes for hacker-style logging
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'
    
    try:
        # Commission rates by tier
        commission_rates = {
            'gold': 0.03,    # 3%
            'silver': 0.02,  # 2%
            'bronze': 0.01   # 1%
        }
        
        # Get commission rate
        rate = commission_rates.get(partner_tier.lower(), 0.01)  # Default 1%
        
        # Calculate commission
        commission = deal_value * rate
        
        # Hacker-style logging
        print(f"{GREEN}💰 COMMISSION CALCULATION INITIATED{END}")
        print(f"{CYAN}├── Deal Value: Rp {deal_value:,.0f}{END}")
        print(f"{CYAN}├── Partner Tier: {partner_tier.upper()}{END}")
        print(f"{CYAN}├── Commission Rate: {rate*100:.0f}%{END}")
        print(f"{GREEN}└── Commission Amount: Rp {commission:,.0f}{END}")
        print(f"{YELLOW}🔐 Transaction logged: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{END}")
        
        return commission
        
    except Exception as e:
        print(f"{RED}❌ COMMISSION CALCULATION ERROR: {e}{END}")
        return 0.0

def log_commission(partner_id: str, deal_id: str, deal_value: float, partner_tier: str, commission_amount: float) -> bool:
    """
    Log commission calculation to analytics database
    
    Args:
        partner_id: Unique partner identifier
        deal_id: Unique deal identifier
        deal_value: Total deal value
        partner_tier: Partner tier
        commission_amount: Calculated commission amount
    
    Returns:
        True if logged successfully, False otherwise
    """
    # ANSI Color Codes for hacker-style logging
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'
    
    try:
        # Connect to analytics database
        db_path = 'data/analytics.db (SQLite - removed)
        
        # Ensure data directory exists
        import os
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        conn = # SQLite connection removed
        cursor = conn.cursor()
        
        # Create partner_commissions table if not exists
        # cursor.execute() removed'''
            CREATE TABLE IF NOT EXISTS partner_commissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                commission_id TEXT UNIQUE NOT NULL,
                partner_id TEXT NOT NULL,
                deal_id TEXT NOT NULL,
                deal_value REAL NOT NULL,
                partner_tier TEXT NOT NULL,
                commission_rate REAL NOT NULL,
                commission_amount REAL NOT NULL,
                status TEXT DEFAULT 'pending',
                created_at TEXT NOT NULL,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Generate unique commission ID
        commission_id = f"COMM_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{partner_id}"
        
        # Get commission rate
        commission_rates = {
            'gold': 0.03,
            'silver': 0.02,
            'bronze': 0.01
        }
        commission_rate = commission_rates.get(partner_tier.lower(), 0.01)
        
        # Insert commission record
        # cursor.execute() removed'''
            INSERT INTO partner_commissions 
            (commission_id, partner_id, deal_id, deal_value, partner_tier, commission_rate, commission_amount, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            commission_id,
            partner_id,
            deal_id,
            deal_value,
            partner_tier,
            commission_rate,
            commission_amount,
            datetime.now().isoformat()
        ))
        
        # conn.commit() removed
        # conn.close() removed
        
        # Hacker-style success logging
        print(f"{GREEN}🔐 COMMISSION LOGGED TO DATABASE{END}")
        print(f"{CYAN}├── Commission ID: {commission_id}{END}")
        print(f"{CYAN}├── Partner ID: {partner_id}{END}")
        print(f"{CYAN}├── Deal ID: {deal_id}{END}")
        print(f"{CYAN}├── Database: analytics.db{END}")
        print(f"{CYAN}├── Table: partner_commissions{END}")
        print(f"{GREEN}└── Status: SUCCESSFULLY LOGGED{END}")
        print(f"{YELLOW}📊 Analytics DB updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{END}")
        
        return True
        
    except sqlite3.Error as e:
        print(f"{RED}❌ DATABASE ERROR: {e}{END}")
        return False
    except Exception as e:
        print(f"{RED}❌ LOGGING ERROR: {e}{END}")
        return False

def main():
    """Main function to demonstrate commission tracker"""
    print("=" * 60)
    print("💰 COMMISSION TRACKER - PARTNER AGENT")
    print("=" * 60)
    
    # Initialize commission tracker
    tracker = CommissionTracker()
    
    # Test commission calculation
    print("\n💰 Testing commission calculation...")
    test_deals = [
        (500000000, 'gold'),
        (300000000, 'silver'),
        (200000000, 'bronze'),
        (750000000, 'gold'),
        (150000000, 'silver')
    ]
    
    for deal_value, tier in test_deals:
        commission = calculate_commission(deal_value, tier)
        if commission > 0:
            # Log the commission
            log_success = log_commission(
                partner_id=f"PARTNER_{tier.upper()}",
                deal_id=f"DEAL_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                deal_value=deal_value,
                partner_tier=tier,
                commission_amount=commission
            )
            if log_success:
                print(f"✅ Commission logged successfully for {tier.upper()} partner")
            else:
                print(f"❌ Failed to log commission for {tier.upper()} partner")
    
    # Create sample partners
    print("\n👥 Creating sample partners...")
    created = tracker.create_sample_partners()
    print(f"✅ Created {created} partners with sample commissions")
    
    # Generate overall report
    print("\n📈 Generating commission report...")
    report = tracker.generate_commission_report()
    
    if report:
        print("📊 Commission Statistics:")
        print(f"  - Total Partners: {report.get('total_partners', 0)}")
        print(f"  - Partner Tiers: {report.get('partner_tier_distribution', {})}")
        print(f"  - Total Commissions Paid: Rp {report.get('total_commissions_paid', 0):,.0f}")
        print(f"  - Commission Status: {report.get('overall_statistics', {})}")
    
    # Get pending commissions
    print("\n💼 Processing pending commissions...")
    
    # Approve and pay some commissions
    conn = # SQLite connection removed
    cursor = conn.cursor()
    
    # cursor.execute() removed'SELECT commission_id FROM commissions WHERE status = ? LIMIT 3', (CommissionStatus.PENDING.value,))
    pending_commissions = cursor.fetchall()
    
    approved_count = 0
    for (commission_id,) in pending_commissions:
        if tracker.approve_commission(commission_id, "Approved for payment"):
            if tracker.pay_commission(commission_id):
                approved_count += 1
    
    # conn.close() removed
    
    print(f"✅ Approved and paid {approved_count} commissions")
    
    # Generate updated report
    print("\n📊 Updated Commission Report:")
    updated_report = tracker.generate_commission_report()
    
    if updated_report:
        print(f"  - Total Commissions Paid: Rp {updated_report.get('total_commissions_paid', 0):,.0f}")
    
    # Save report
    report_file = 'commission_report.json'
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(updated_report, f, indent=2, ensure_ascii=False)
    
    print(f"\n📁 Report saved to: {report_file}")
    
    print("\n" + "=" * 60)
    print("✅ COMMISSION TRACKER SETUP COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()
