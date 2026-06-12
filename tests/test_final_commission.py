#!/usr/bin/env python3
"""
Final Commission Test - Lumina OS
Working commission calculation and logging test
"""

import os
from datetime import datetime

def calculate_commission(deal_value: float, partner_tier: str) -> float:
    """
    Calculate commission based on deal value and partner tier
    
    Args:
        deal_value: Total value of the deal
        partner_tier: Partner tier (Gold, Silver, Bronze)
    
    Returns:
        Commission amount
    """
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
    
    print(f"💰 Commission Calculation:")
    print(f"   Deal Value: Rp {deal_value:,.0f}")
    print(f"   Partner Tier: {partner_tier.upper()}")
    print(f"   Commission Rate: {rate*100:.0f}%")
    print(f"   Commission Amount: Rp {commission:,.0f}")
    print(f"   Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return commission

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
    try:
        # Connect to analytics database
        db_path = 'data/analytics.db (SQLite - removed)
        
        # Ensure data directory exists
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
                created_at TEXT NOT NULL
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
            (commission_id, partner_id, deal_id, deal_value, partner_tier, commission_rate, commission_amount, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            commission_id,
            partner_id,
            deal_id,
            deal_value,
            partner_tier,
            commission_rate,
            commission_amount,
            'pending',
            datetime.now().isoformat()
        ))
        
        # conn.commit() removed
        # conn.close() removed
        
        print(f"🔐 Commission Logged to Database:")
        print(f"   Commission ID: {commission_id}")
        print(f"   Partner ID: {partner_id}")
        print(f"   Deal ID: {deal_id}")
        print(f"   Database: analytics.db (SQLite - removed))
        print(f"   Table: partner_commissions")
        print(f"   Status: SUCCESSFULLY LOGGED")
        print(f"   Analytics DB updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return True
        
    except sqlite3.Error as e:
        print(f"❌ DATABASE ERROR: {e}")
        return False
    except Exception as e:
        print(f"❌ LOGGING ERROR: {e}")
        return False

def main():
    """Main test function"""
    print("💰 COMMISSION TRACKER - FINAL TEST")
    print("=" * 50)
    print("🔐 Testing commission calculation and logging")
    print("=" * 50)
    
    # Test calculate_commission
    print("\n📊 Testing calculate_commission...")
    test_cases = [
        (500000000, 'gold', 15000000),    # 3% of 500M = 15M
        (300000000, 'silver', 6000000),    # 2% of 300M = 6M
        (200000000, 'bronze', 2000000),    # 1% of 200M = 2M
        (750000000, 'gold', 22500000),    # 3% of 750M = 22.5M
        (150000000, 'silver', 3000000),    # 2% of 150M = 3M
    ]
    
    calculation_success = True
    for deal_value, tier, expected in test_cases:
        result = calculate_commission(deal_value, tier)
        if result == expected:
            print(f"✅ {tier.upper()} - Rp {deal_value:,.0f} → Rp {result:,.0f}")
        else:
            print(f"❌ {tier.upper()} - Expected Rp {expected:,.0f}, Got Rp {result:,.0f}")
            calculation_success = False
    
    # Test log_commission
    print("\n📝 Testing log_commission...")
    log_success = log_commission(
        partner_id="TEST_PARTNER",
        deal_id="TEST_DEAL_001",
        deal_value=500000000,
        partner_tier="gold",
        commission_amount=15000000
    )
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    if calculation_success:
        print("✅ Commission Calculation: WORKING")
    else:
        print("❌ Commission Calculation: NOT WORKING")
    
    if log_success:
        print("✅ Commission Logging: WORKING")
    else:
        print("❌ Commission Logging: NOT WORKING")
    
    # Overall result
    if calculation_success and log_success:
        print("\n🎉 COMMISSION TRACKER: FULLY FUNCTIONAL")
        print("💰 All commission operations working correctly")
        print("🔐 Database integration successful")
        print("🚀 Ready for production use")
    else:
        print("\n⚠️ COMMISSION TRACKER: PARTIALLY FUNCTIONAL")
        print("🔧 Please check the implementation")
    print("=" * 50)

if __name__ == "__main__":
    main()
