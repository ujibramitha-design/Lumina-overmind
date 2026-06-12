#!/usr/bin/env python3
"""
Test Script for Critical Files - Lumina OS
Test sheets_connector_mock.py and commission_tracker.py functions
"""

import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_sheets_connector_mock():
    """Test Google Sheets Sync Mock function"""
    print("🧪 Testing Google Sheets Sync Mock...")
    print("=" * 50)
    
    try:
        # Import the mock function
        from core_modules.dashboard_bridge.sheets_connector import sync_leads_to_sheets_mock
        
        # Test the function
        result = sync_leads_to_sheets_mock()
        
        if result:
            print("✅ Google Sheets Mock Sync: SUCCESS")
            return True
        else:
            print("❌ Google Sheets Mock Sync: FAILED")
            return False
            
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test Error: {e}")
        return False

def test_commission_calculator():
    """Test Commission Calculator functions"""
    print("\n💰 Testing Commission Calculator...")
    print("=" * 50)
    
    try:
        # Import commission functions
        from agents.partner_agent.commission_tracker import calculate_commission, log_commission
        
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
        
        if log_success:
            print("✅ Commission logging: SUCCESS")
        else:
            print("❌ Commission logging: FAILED")
        
        return calculation_success and log_success
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test Error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 LUMINA OS - CRITICAL FILES TEST")
    print("=" * 60)
    print("📅 Testing files created in response to audit gaps")
    print("=" * 60)
    
    # Test sheets connector mock
    sheets_result = test_sheets_connector_mock()
    
    # Test commission calculator
    commission_result = test_commission_calculator()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    if sheets_result:
        print("✅ Google Sheets Sync Mock: WORKING")
    else:
        print("❌ Google Sheets Sync Mock: NOT WORKING")
    
    if commission_result:
        print("✅ Commission Calculator: WORKING")
    else:
        print("❌ Commission Calculator: NOT WORKING")
    
    # Overall result
    if sheets_result and commission_result:
        print("\n🎉 ALL CRITICAL FILES: WORKING")
        print("🔐 Implementation successful!")
    else:
        print("\n⚠️ SOME CRITICAL FILES: NOT WORKING")
        print("🔧 Please check the implementation")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
