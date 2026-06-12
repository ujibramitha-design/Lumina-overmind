#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
💰 KPR ENGINE - Fin-Tech Pricing Calculator
==========================================

Advanced mortgage calculation system for personalized financing options.
Supports dynamic pricing based on prospect profile and market conditions.

Features:
- Personalized KPR calculations based on prospect age and profile
- Dynamic interest rate calculations (Fix + Floating)
- Amortization schedule generation
- Multiple financing scenarios comparison
- Bank-specific rate calculations
- Down payment optimization recommendations
"""

import os
import json
import logging
import math
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BankType(Enum):
    """Bank types for KPR calculations"""
    BNI = "BNI"
    BCA = "BCA"
    BRI = "BRI"
    MANDIRI = "Mandiri"
    BTN = "BTN"
    CIMB = "CIMB"
    DANAMON = "Danamon"
    PANIN = "Panin"

class ProspectType(Enum):
    """Prospect types for personalized calculations"""
    FIRST_TIME_BUYER = "first_time_buyer"
    UPGRADER = "upgrader"
    INVESTOR = "investor"
    ELDERLY = "elderly"
    YOUNG_PROFESSIONAL = "young_professional"

@dataclass
class KPRParameters:
    """KPR calculation parameters"""
    property_price: float
    down_payment_percentage: float
    loan_amount: float
    interest_rate_fix: float
    interest_rate_floating: float
    loan_term_years: int
    fix_period_years: int
    
@dataclass
class AmortizationRow:
    """Single amortization schedule row"""
    month: int
    payment: float
    principal: float
    interest: float
    balance: float
    cumulative_interest: float

@dataclass
class ProspectProfile:
    """Prospect profile for personalized calculations"""
    age: int
    monthly_income: float
    employment_type: str  # permanent, contract, business
    credit_score: int
    existing_loans: float
    family_size: int
    prospect_type: ProspectType

class KPREngine:
    """Advanced KPR calculation engine"""
    
    def __init__(self):
        # Bank-specific interest rates (annual percentages)
        self.bank_rates = {
            BankType.BNI: {
                'fix_5_year': 6.75,
                'fix_10_year': 7.25,
                'fix_15_year': 8.00,
                'floating_base': 9.50,
                'max_dpr': 15,
                'max_loan_term': 25,
                'admin_fee': 550000
            },
            BankType.BCA: {
                'fix_5_year': 6.50,
                'fix_10_year': 7.00,
                'fix_15_year': 7.75,
                'floating_base': 9.25,
                'max_dpr': 15,
                'max_loan_term': 25,
                'admin_fee': 500000
            },
            BankType.BRI: {
                'fix_5_year': 6.25,
                'fix_10_year': 6.75,
                'fix_15_year': 7.50,
                'floating_base': 9.00,
                'max_dpr': 20,
                'max_loan_term': 30,
                'admin_fee': 450000
            },
            BankType.MANDIRI: {
                'fix_5_year': 6.75,
                'fix_10_year': 7.25,
                'fix_15_year': 8.00,
                'floating_base': 9.50,
                'max_dpr': 15,
                'max_loan_term': 25,
                'admin_fee': 550000
            },
            BankType.BTN: {
                'fix_5_year': 6.00,
                'fix_10_year': 6.50,
                'fix_15_year': 7.25,
                'floating_base': 8.75,
                'max_dpr': 25,
                'max_loan_term': 30,
                'admin_fee': 400000
            },
            BankType.CIMB: {
                'fix_5_year': 6.50,
                'fix_10_year': 7.00,
                'fix_15_year': 7.75,
                'floating_base': 9.25,
                'max_dpr': 15,
                'max_loan_term': 25,
                'admin_fee': 500000
            }
        }
        
        # Risk adjustments based on prospect profile
        self.risk_adjustments = {
            ProspectType.FIRST_TIME_BUYER: {
                'rate_adjustment': 0.25,  # +0.25% for first-time buyers
                'dpr_reduction': 5,       # 5% lower DP requirement
                'max_loan_multiplier': 4.0
            },
            ProspectType.UPGRADER: {
                'rate_adjustment': -0.15,  # -0.15% for upgraders
                'dpr_reduction': 2,
                'max_loan_multiplier': 5.0
            },
            ProspectType.INVESTOR: {
                'rate_adjustment': 0.50,   # +0.50% for investors
                'dpr_reduction': 0,
                'max_loan_multiplier': 3.5
            },
            ProspectType.ELDERLY: {
                'rate_adjustment': -0.25,  # -0.25% for elderly (better rates)
                'dpr_reduction': 10,
                'max_loan_multiplier': 3.0,
                'max_term_reduction': 10   # Shorter loan term for elderly
            },
            ProspectType.YOUNG_PROFESSIONAL: {
                'rate_adjustment': 0.10,   # +0.10% for young professionals
                'dpr_reduction': 3,
                'max_loan_multiplier': 4.5
            }
        }
        
        # Employment type adjustments
        self.employment_adjustments = {
            'permanent': {'rate_adjustment': -0.25, 'loan_multiplier': 1.0},
            'contract': {'rate_adjustment': 0.25, 'loan_multiplier': 0.8},
            'business': {'rate_adjustment': 0.50, 'loan_multiplier': 0.9}
        }
        
        # Credit score adjustments
        self.credit_score_adjustments = {
            (800, 850): {'rate_adjustment': -0.50, 'dpr_reduction': 5},
            (750, 799): {'rate_adjustment': -0.25, 'dpr_reduction': 3},
            (700, 749): {'rate_adjustment': 0.0, 'dpr_reduction': 0},
            (650, 699): {'rate_adjustment': 0.25, 'dpr_reduction': -2},
            (600, 649): {'rate_adjustment': 0.50, 'dpr_reduction': -5},
            (0, 599): {'rate_adjustment': 1.00, 'dpr_reduction': -10}
        }
    
    def generate_personalized_pricelist(
        self,
        property_price: float,
        prospect_profile: ProspectProfile,
        preferred_banks: Optional[List[BankType]] = None
    ) -> Dict[str, Any]:
        """
        Generate personalized KPR pricing list
        
        Args:
            property_price: Property price in IDR
            prospect_profile: Prospect profile information
            preferred_banks: List of preferred banks (optional)
        
        Returns:
            Dictionary with personalized KPR options and recommendations
        """
        try:
            logger.info(f"💰 Generating personalized KPR for property: Rp {property_price:,.0f}")
            
            # Determine eligible banks
            if preferred_banks:
                eligible_banks = preferred_banks
            else:
                eligible_banks = list(self.bank_rates.keys())
            
            # Calculate personalized parameters
            personalized_options = []
            
            for bank in eligible_banks:
                try:
                    bank_option = self._calculate_bank_option(bank, property_price, prospect_profile)
                    if bank_option:
                        personalized_options.append(bank_option)
                except Exception as e:
                    logger.warning(f"⚠️ Failed to calculate option for {bank}: {e}")
            
            # Sort by total payment amount
            personalized_options.sort(key=lambda x: x['total_payment'])
            
            # Generate recommendations
            recommendations = self._generate_recommendations(personalized_options, prospect_profile)
            
            # Create summary
            result = {
                'property_price': property_price,
                'prospect_profile': {
                    'age': prospect_profile.age,
                    'monthly_income': prospect_profile.monthly_income,
                    'prospect_type': prospect_profile.prospect_type.value,
                    'credit_score': prospect_profile.credit_score
                },
                'options': personalized_options,
                'recommendations': recommendations,
                'generated_at': datetime.now().isoformat()
            }
            
            logger.info(f"✅ Generated {len(personalized_options)} KPR options")
            return result
            
        except Exception as e:
            logger.error(f"❌ KPR calculation failed: {e}")
            raise
    
    def _calculate_bank_option(
        self,
        bank: BankType,
        property_price: float,
        prospect_profile: ProspectProfile
    ) -> Optional[Dict[str, Any]]:
        """Calculate KPR option for specific bank"""
        try:
            bank_config = self.bank_rates[bank]
            
            # Calculate adjustments
            rate_adjustment = self._calculate_rate_adjustment(prospect_profile)
            dpr_adjustment = self._calculate_dpr_adjustment(prospect_profile)
            max_term = self._calculate_max_term(bank_config, prospect_profile)
            
            # Calculate loan parameters
            max_dpr = bank_config['max_dpr'] - dpr_adjustment
            max_dpr = max(5, min(30, max_dpr))  # Ensure reasonable bounds
            
            # Calculate optimal DP (start with minimum, then optimize)
            optimal_dp_percentage = self._optimize_down_payment(
                property_price, prospect_profile, max_dpr, bank_config
            )
            
            down_payment = property_price * (optimal_dp_percentage / 100)
            loan_amount = property_price - down_payment
            
            # Validate loan affordability
            max_loan_amount = prospect_profile.monthly_income * self._calculate_loan_multiplier(
                prospect_profile, bank_config
            )
            
            if loan_amount > max_loan_amount:
                # Adjust loan to affordable amount
                loan_amount = max_loan_amount
                down_payment = property_price - loan_amount
                optimal_dp_percentage = (down_payment / property_price) * 100
            
            # Calculate interest rates with adjustments
            fix_rates = {
                5: bank_config['fix_5_year'] + rate_adjustment,
                10: bank_config['fix_10_year'] + rate_adjustment,
                15: bank_config['fix_15_year'] + rate_adjustment
            }
            floating_rate = bank_config['floating_base'] + rate_adjustment
            
            # Calculate options for different fix periods
            options = []
            for fix_years in [5, 10, 15]:
                if fix_years <= max_term:
                    option = self._calculate_fix_option(
                        loan_amount, fix_rates[fix_years], floating_rate,
                        fix_years, max_term, bank_config['admin_fee']
                    )
                    options.append({
                        'fix_years': fix_years,
                        'fix_rate': fix_rates[fix_years],
                        'floating_rate': floating_rate,
                        'monthly_payment': option['monthly_payment'],
                        'total_payment': option['total_payment'],
                        'total_interest': option['total_interest'],
                        'amortization': option['amortization'][:12]  # First year only
                    })
            
            # Select best option (lowest monthly payment)
            best_option = min(options, key=lambda x: x['monthly_payment']) if options else options[0]
            
            return {
                'bank': bank.value,
                'down_payment_percentage': optimal_dp_percentage,
                'down_payment_amount': down_payment,
                'loan_amount': loan_amount,
                'loan_term_years': max_term,
                'admin_fee': bank_config['admin_fee'],
                'best_option': best_option,
                'all_options': options,
                'affordability_score': self._calculate_affordability_score(
                    best_option['monthly_payment'], prospect_profile.monthly_income
                )
            }
            
        except Exception as e:
            logger.error(f"❌ Bank option calculation failed for {bank}: {e}")
            return None
    
    def _calculate_rate_adjustment(self, prospect_profile: ProspectProfile) -> float:
        """Calculate interest rate adjustment based on profile"""
        adjustment = 0.0
        
        # Prospect type adjustment
        prospect_adj = self.risk_adjustments.get(prospect_profile.prospect_type, {})
        adjustment += prospect_adj.get('rate_adjustment', 0.0)
        
        # Employment type adjustment
        emp_adj = self.employment_adjustments.get(prospect_profile.employment_type, {})
        adjustment += emp_adj.get('rate_adjustment', 0.0)
        
        # Credit score adjustment
        credit_score = prospect_profile.credit_score
        for (min_score, max_score), score_adj in self.credit_score_adjustments.items():
            if min_score <= credit_score <= max_score:
                adjustment += score_adj.get('rate_adjustment', 0.0)
                break
        
        return adjustment
    
    def _calculate_dpr_adjustment(self, prospect_profile: ProspectProfile) -> float:
        """Calculate down payment adjustment based on profile"""
        adjustment = 0.0
        
        # Prospect type adjustment
        prospect_adj = self.risk_adjustments.get(prospect_profile.prospect_type, {})
        adjustment += prospect_adj.get('dpr_reduction', 0.0)
        
        # Credit score adjustment
        credit_score = prospect_profile.credit_score
        for (min_score, max_score), score_adj in self.credit_score_adjustments.items():
            if min_score <= credit_score <= max_score:
                adjustment += score_adj.get('dpr_reduction', 0.0)
                break
        
        return adjustment
    
    def _calculate_max_term(self, bank_config: Dict[str, Any], prospect_profile: ProspectProfile) -> int:
        """Calculate maximum loan term based on profile"""
        max_term = bank_config['max_loan_term']
        
        # Age-based reduction for elderly
        if prospect_profile.prospect_type == ProspectType.ELDERLY:
            term_reduction = self.risk_adjustments[ProspectType.ELDERLY].get('max_term_reduction', 0)
            max_term = max(10, max_term - term_reduction)
        
        # Age-based maximum term (retirement consideration)
        retirement_age = 60
        remaining_years = retirement_age - prospect_profile.age
        if remaining_years < max_term:
            max_term = max(5, remaining_years)
        
        return max_term
    
    def _optimize_down_payment(
        self,
        property_price: float,
        prospect_profile: ProspectProfile,
        max_dpr: float,
        bank_config: Dict[str, Any]
    ) -> float:
        """Optimize down payment percentage for affordability"""
        try:
            # Start with minimum DP
            min_dpr = 5.0
            optimal_dpr = min_dpr
            
            # Calculate monthly income capacity (30% rule)
            max_monthly_payment = prospect_profile.monthly_income * 0.3
            
            # Try different DP percentages
            for dpr in range(int(min_dpr), int(max_dpr) + 1, 1):
                loan_amount = property_price * (1 - dpr / 100)
                
                # Estimate monthly payment (simplified)
                estimated_rate = bank_config['fix_10_year'] / 100 / 12
                estimated_term = bank_config['max_loan_term'] * 12
                
                if estimated_rate > 0:
                    monthly_payment = loan_amount * (estimated_rate * (1 + estimated_rate) ** estimated_term) / ((1 + estimated_rate) ** estimated_term - 1)
                else:
                    monthly_payment = loan_amount / estimated_term
                
                # Check affordability
                if monthly_payment <= max_monthly_payment:
                    optimal_dpr = dpr
                else:
                    break
            
            return optimal_dpr
            
        except Exception as e:
            logger.warning(f"⚠️ DP optimization failed: {e}")
            return max(5.0, min_dpr)
    
    def _calculate_loan_multiplier(self, prospect_profile: ProspectProfile, bank_config: Dict[str, Any]) -> float:
        """Calculate loan multiplier based on profile"""
        multiplier = 4.0  # Base multiplier
        
        # Prospect type adjustment
        prospect_adj = self.risk_adjustments.get(prospect_profile.prospect_type, {})
        multiplier *= prospect_adj.get('max_loan_multiplier', 4.0) / 4.0
        
        # Employment type adjustment
        emp_adj = self.employment_adjustments.get(prospect_profile.employment_type, {})
        multiplier *= emp_adj.get('loan_multiplier', 1.0)
        
        return multiplier
    
    def _calculate_fix_option(
        self,
        loan_amount: float,
        fix_rate: float,
        floating_rate: float,
        fix_years: int,
        total_years: int,
        admin_fee: float
    ) -> Dict[str, Any]:
        """Calculate KPR option with fix period"""
        try:
            # Convert to monthly rates
            monthly_fix_rate = fix_rate / 100 / 12
            monthly_floating_rate = floating_rate / 100 / 12
            
            # Calculate fix period payments
            fix_months = fix_years * 12
            total_months = total_years * 12
            
            # Monthly payment during fix period
            if monthly_fix_rate > 0:
                fix_payment = loan_amount * (monthly_fix_rate * (1 + monthly_fix_rate) ** fix_months) / ((1 + monthly_fix_rate) ** fix_months - 1)
            else:
                fix_payment = loan_amount / fix_months
            
            # Generate amortization schedule
            amortization = []
            balance = loan_amount
            cumulative_interest = 0.0
            
            for month in range(1, total_months + 1):
                if month <= fix_months:
                    # Fix period
                    interest_payment = balance * monthly_fix_rate
                    principal_payment = fix_payment - interest_payment
                else:
                    # Floating period
                    interest_payment = balance * monthly_floating_rate
                    remaining_months = total_months - month + 1
                    if monthly_floating_rate > 0 and remaining_months > 0:
                        floating_payment = balance * (monthly_floating_rate * (1 + monthly_floating_rate) ** remaining_months) / ((1 + monthly_floating_rate) ** remaining_months - 1)
                        principal_payment = floating_payment - interest_payment
                    else:
                        principal_payment = balance
                        interest_payment = 0
                
                principal_payment = min(principal_payment, balance)
                balance -= principal_payment
                cumulative_interest += interest_payment
                
                amortization.append(AmortizationRow(
                    month=month,
                    payment=principal_payment + interest_payment,
                    principal=principal_payment,
                    interest=interest_payment,
                    balance=max(0, balance),
                    cumulative_interest=cumulative_interest
                ))
                
                if balance <= 0:
                    break
            
            # Calculate totals
            total_payment = sum(row.payment for row in amortization) + admin_fee
            total_interest = sum(row.interest for row in amortization)
            monthly_payment = amortization[0].payment if amortization else 0
            
            return {
                'monthly_payment': monthly_payment,
                'total_payment': total_payment,
                'total_interest': total_interest,
                'amortization': amortization
            }
            
        except Exception as e:
            logger.error(f"❌ Fix option calculation failed: {e}")
            raise
    
    def _calculate_affordability_score(self, monthly_payment: float, monthly_income: float) -> float:
        """Calculate affordability score (0-100)"""
        try:
            # Calculate debt-to-income ratio
            dti_ratio = (monthly_payment / monthly_income) * 100 if monthly_income > 0 else 100
            
            # Score based on DTI ratio
            if dti_ratio <= 20:
                return 100
            elif dti_ratio <= 25:
                return 90
            elif dti_ratio <= 30:
                return 80
            elif dti_ratio <= 35:
                return 70
            elif dti_ratio <= 40:
                return 60
            elif dti_ratio <= 45:
                return 50
            else:
                return max(0, 50 - (dti_ratio - 45))
                
        except Exception as e:
            logger.warning(f"⚠️ Affordability score calculation failed: {e}")
            return 50
    
    def _generate_recommendations(
        self,
        options: List[Dict[str, Any]],
        prospect_profile: ProspectProfile
    ) -> Dict[str, Any]:
        """Generate personalized recommendations"""
        try:
            if not options:
                return {"message": "No suitable KPR options found"}
            
            # Best overall option
            best_option = min(options, key=lambda x: x['total_payment'])
            
            # Most affordable option
            most_affordable = max(options, key=lambda x: x['affordability_score'])
            
            # Recommendations based on prospect type
            recommendations = {
                "best_overall": {
                    "bank": best_option['bank'],
                    "monthly_payment": best_option['best_option']['monthly_payment'],
                    "total_payment": best_option['total_payment'],
                    "down_payment": best_option['down_payment_amount'],
                    "reason": "Lowest total payment over loan term"
                },
                "most_affordable": {
                    "bank": most_affordable['bank'],
                    "monthly_payment": most_affordable['best_option']['monthly_payment'],
                    "affordability_score": most_affordable['affordability_score'],
                    "reason": "Best fits your monthly income capacity"
                }
            }
            
            # Prospect-specific recommendations
            if prospect_profile.prospect_type == ProspectType.FIRST_TIME_BUYER:
                recommendations["first_time_buyer_tips"] = [
                    "Consider government subsidies for first-time buyers",
                    "Look for banks offering special first-time buyer rates",
                    "Save additional funds for unexpected costs"
                ]
            elif prospect_profile.prospect_type == ProspectType.ELDERLY:
                recommendations["elderly_tips"] = [
                    "Consider shorter loan terms for peace of mind",
                    "Look for banks with elderly-friendly policies",
                    "Ensure monthly payments fit retirement income"
                ]
            elif prospect_profile.prospect_type == ProspectType.INVESTOR:
                recommendations["investor_tips"] = [
                    "Consider interest-only loans for cash flow",
                    "Look for flexible repayment options",
                    "Factor in rental income when calculating affordability"
                ]
            
            return recommendations
            
        except Exception as e:
            logger.error(f"❌ Recommendation generation failed: {e}")
            return {"error": "Failed to generate recommendations"}
    
    def create_comparison_table(self, options: List[Dict[str, Any]]) -> str:
        """Create readable comparison table for brochure"""
        try:
            if not options:
                return "No KPR options available"
            
            table_lines = []
            table_lines.append("💰 PERBANDINGAN OPSI KPR PERSONAL")
            table_lines.append("=" * 80)
            table_lines.append(f"{'Bank':<10} {'DP %':<6} {'Cicilan/Bln':<12} {'Total':<15} {'Skor':<5}")
            table_lines.append("-" * 80)
            
            for option in options[:5]:  # Top 5 options
                bank = option['bank']
                dp_pct = f"{option['down_payment_percentage']:.1f}%"
                monthly = f"Rp {option['best_option']['monthly_payment']:,.0f}"
                total = f"Rp {option['total_payment']:,.0f}"
                score = f"{option['affordability_score']:.0f}"
                
                table_lines.append(f"{bank:<10} {dp_pct:<6} {monthly:<12} {total:<15} {score:<5}")
            
            table_lines.append("=" * 80)
            
            return "\n".join(table_lines)
            
        except Exception as e:
            logger.error(f"❌ Comparison table creation failed: {e}")
            return "Failed to create comparison table"

# Convenience function for easy usage
def generate_personalized_pricelist(
    property_price: float,
    prospect_profile: ProspectProfile,
    preferred_banks: Optional[List[BankType]] = None
) -> Dict[str, Any]:
    """
    Generate personalized KPR pricing list
    
    Args:
        property_price: Property price in IDR
        prospect_profile: Prospect profile information
        preferred_banks: List of preferred banks (optional)
    
    Returns:
        Dictionary with personalized KPR options and recommendations
    """
    engine = KPREngine()
    return engine.generate_personalized_pricelist(property_price, prospect_profile, preferred_banks)

# Example usage and testing
if __name__ == "__main__":
    def test_kpr_engine():
        """Test KPR Engine functionality"""
        
        # Create sample prospect profile
        prospect = ProspectProfile(
            age=35,
            monthly_income=15000000,  # Rp 15 juta
            employment_type="permanent",
            credit_score=750,
            existing_loans=2000000,   # Rp 2 juta
            family_size=4,
            prospect_type=ProspectType.UPGRADER
        )
        
        property_price = 800000000  # Rp 800 juta
        
        try:
            # Test KPR calculation
            kpr_options = generate_personalized_pricelist(property_price, prospect)
            
            print(f"✅ Generated {len(kpr_options['options'])} KPR options")
            print(f"🏠 Property Price: Rp {property_price:,}")
            print(f"👤 Prospect Age: {prospect.age}")
            print(f"💰 Monthly Income: Rp {prospect.monthly_income:,}")
            
            # Display best option
            if kpr_options['options']:
                best = kpr_options['options'][0]
                print(f"\n🏆 Best Option: {best['bank']}")
                print(f"💳 Down Payment: Rp {best['down_payment_amount']:,.0f} ({best['down_payment_percentage']:.1f}%)")
                print(f"📅 Monthly Payment: Rp {best['best_option']['monthly_payment']:,.0f}")
                print(f"💵 Total Payment: Rp {best['total_payment']:,.0f}")
                print(f"⭐ Affordability Score: {best['affordability_score']:.0f}/100")
            
            # Test comparison table
            engine = KPREngine()
            comparison = engine.create_comparison_table(kpr_options['options'])
            print(f"\n{comparison}")
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
    
    # Run test
    test_kpr_engine()
